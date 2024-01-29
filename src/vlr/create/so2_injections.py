"""Create a time series representing SO2 injections."""

import datetime
import pathlib
import subprocess

import numpy as np
import numpy.typing as npt
import volcano_base
import volcano_cooking
import volcano_cooking.modules.create as vc_create


class GenerateFromHistoricalData(vc_create.Generate):
    """Generate SO2 emissions from historical data."""

    def gen_dates_totalemission_vei(self) -> None:
        """Generate dates, total emission and VEI."""
        out = generate_exponential_waiting_times_historical_amplitudes()
        yoes, moes, does = _convert_datetime_to_date_array(out[0])
        nonzero_values = np.argwhere(out[1] != 0)
        self.tes = out[1][nonzero_values].flatten().astype(np.float32)
        self.yoes = yoes[nonzero_values].flatten().astype(np.int16) + 1
        self.moes = moes[nonzero_values].flatten().astype(np.int8)
        self.does = does[nonzero_values].flatten().astype(np.int8)
        # Add one item to the beginning of the arrays
        self.tes = np.insert(self.tes, 0, 1)
        self.yoes = np.insert(self.yoes, 0, 1849)
        self.moes = np.insert(self.moes, 0, 1)
        self.does = np.insert(self.does, 0, 1)
        self.veis = volcano_cooking.modules.convert.totalemission_to_vei(self.tes)


def _draw_amplitudes_from_historic() -> npt.NDArray[np.float32]:
    """Draw amplitudes from historic eruptions."""
    # Grab the historic eruptions
    dates, values = volcano_base.load.get_so2_ob16_peak_timeseries()
    # dates, values = vlr.load_historic_data.get_so2_ob16_peak_timeseries()
    # Filter out the zeros
    peak_idx = np.argwhere(values > 0)
    peaks = values[peak_idx].flatten()
    peaks *= 257.9 / peaks.max()  # Otto-Bliesner (2016) largest value
    # Randomise, then rotate so the largest is the first one (works in-place)
    np.random.default_rng().shuffle(peaks)
    if max_idx := np.argmax(peaks):
        peaks = np.roll(peaks, -max_idx)
    return peaks.astype(np.float32)


def _draw_exponential_waiting_times(
    size: int,
) -> tuple[npt.NDArray[np.int16], npt.NDArray[np.int8], npt.NDArray[np.int8]]:
    init_year = 1851
    years = 2 * size  # We want on average 50 eruptions per century
    rg = np.random.default_rng()
    yoes = rg.integers(0, years, size=size)
    yoes += init_year
    yoes = yoes.astype(np.int16)
    moes = rg.integers(1, 13, size=size).astype(np.int8)
    does = rg.integers(1, 29, size=size).astype(np.int8)
    # Force the first date to be 1851-01-01
    yoes[0] = 1851
    moes[0] = 1
    does[0] = 1
    # Create a structured array
    dates = np.zeros(len(yoes), dtype=[("year", int), ("month", int), ("day", int)])
    dates["year"] = yoes
    dates["month"] = moes
    dates["day"] = does
    # Make sure that they are unique
    if (days := (12 * 28 * years)) < size:
        raise ValueError(
            f"The number of eruptions are larger than the number of days ({days = }, {size = })"
        )
    else:
        print(
            f"The number of eruptions are {size/days*100:.2f} % of the total number of days"
        )
    counter = 0
    while len(dates) != len(np.unique(dates)):
        counter += 1
        print(f"I've tried re-setting dates {counter} times", end="\r")
        unique_dates, indices, counts = np.unique(
            dates, return_index=True, return_counts=True
        )
        # Re-set dates that were not unique
        for idx in indices[counts > 1]:
            # We want to make sure the first eruption is 1851-01-01
            y = rg.integers(1, years) + init_year
            m = rg.integers(1, 13)
            d = rg.integers(1, 29)
            dates[idx] = (y, m, d)
    if counter:
        print("")
    assert len(dates) == len(np.unique(dates))
    # Sort the array
    sorted_dates = np.sort(dates, order=["year", "month", "day"])
    assert [1851, 1, 1] == list(sorted_dates[0])
    # Extract the sorted arrays
    sorted_years = sorted_dates["year"]
    sorted_months = sorted_dates["month"]
    sorted_days = sorted_dates["day"]
    return sorted_years, sorted_months, sorted_days


def _from_individual_date_arrays_to_datetime(
    y: np.ndarray, m: np.ndarray, d: np.ndarray
) -> list[datetime.datetime]:
    return [datetime.datetime(y_, m_, d_) for y_, m_, d_ in zip(y, m, d, strict=True)]


def generate_exponential_waiting_times_historical_amplitudes() -> (
    tuple[np.ndarray, np.ndarray]
):
    """Generate a time series of SO2 injections.

    Returns
    -------
    dates_extended, forcing_extended : tuple[np.ndarray, np.ndarray]
        Array of length 'size' with the dates of the eruptions
    """
    iso = _draw_amplitudes_from_historic()
    ymd = _draw_exponential_waiting_times(len(iso))
    dates = _from_individual_date_arrays_to_datetime(*ymd)
    # Determine the range for the daily time axis
    start_date = min(dates)
    end_date = max(dates)
    num_days = (end_date - start_date).days + 1

    # Create a daily time axis
    # daily_dates = [start_date + datetime.timedelta(days=x) for x in range(num_days)]

    # Initialize the forcing array
    forcing = np.zeros(num_days)
    # Fill it up with amplitudes
    for i, date in enumerate(dates):
        # Find the index in the daily_dates array
        index = (date - start_date).days
        # Replace the zero with a white noise value
        forcing[index] = iso[i]
    # Add a year of zeros before the first eruption
    start_date_extended = start_date - datetime.timedelta(days=365)
    num_days_extended = (end_date - start_date_extended).days + 1
    forcing_extended = np.zeros(num_days_extended)
    forcing_extended[365 : 365 + num_days] = forcing
    dates_extended = [
        start_date_extended + datetime.timedelta(days=x)
        for x in range(num_days_extended)
    ]
    return np.asarray(dates_extended), forcing_extended


def _convert_datetime_to_date_array(
    dates: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Convert a datetime array to a year, month, day array."""
    years = np.asarray([date.year for date in dates])
    months = np.asarray([date.month for date in dates])
    days = np.asarray([date.day for date in dates])
    return years, months, days


def _package_last(volcano_cooking_path: pathlib.Path) -> None:
    shell_file = volcano_cooking_path / "package_last.sh"
    if not shell_file.exists():
        raise FileNotFoundError(f"Could not find {shell_file}")
    subprocess.call(["sh", shell_file])


def _run_ncl(volcano_cooking_path: pathlib.Path) -> None:
    # Get directory of the volcano_cooking package
    shell_file = volcano_cooking_path / "create_cesm_frc.sh"
    if not shell_file.exists():
        raise FileNotFoundError(f"Could not find {shell_file}")
    subprocess.call(["sh", shell_file, volcano_cooking_path])


def main() -> None:
    """Run the main function."""
    out = generate_exponential_waiting_times_historical_amplitudes()
    g = GenerateFromHistoricalData(len(out[1]), 1849)
    g.generate()
    frc_cls = vc_create.Data(*g.get_arrays())
    frc_cls.make_dataset()
    frc_cls.save_to_file()

    # Get directory of the volcano_cooking package
    volcano_cooking_path = pathlib.Path(volcano_cooking.__file__).parent.resolve()
    # Run ncl script
    _run_ncl(volcano_cooking_path)
    # Run package-last
    _package_last(volcano_cooking_path)


if __name__ == "__main__":
    main()
