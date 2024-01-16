"""Create a time series representing SO2 injections."""

import datetime

import matplotlib.pyplot as plt
import numpy as np
import volcano_cooking
import volcano_cooking.helper_scripts.view_generated_forcing as view_frc
import volcano_cooking.modules.create as vc_create

import vlr


class GenerateRegularIntervals2(vc_create.Generate):
    def gen_dates_totalemission_vei(self) -> None:
        self.yoes, self.moes, self.does, self.tes = white_noise_dates()
        self.veis = volcano_cooking.modules.convert.totalemission_to_vei(self.tes)


def _draw_amplitudes_from_historic() -> np.ndarray[np.float32]:
    """Draw amplitudes from historic eruptions."""
    # Grab the historic eruptions
    dates, values = vlr.load_historic_data.get_so2_ob16_peak_timeseries()
    # Filter out the zeros
    peak_idx = np.argwhere(values > 0)
    peaks = values[peak_idx].flatten()
    peaks *= 257.9 / peaks.max()  # Otto-Bliesner (2016) largest value
    # Randomise, then rotate so the largest is the first one
    peaks = np.random.shuffle(peaks)
    max_idx = np.argmax(peaks)
    if not max_idx:
        peaks = np.roll(peaks, -max_idx)
    return peaks.astype(np.int16)


def _draw_exponential_waiting_times(
    size: int,
) -> tuple[np.ndarray[np.int16], np.ndarray[np.int8], np.ndarray[np.int8]]:
    init_year = 1851
    years = 2 * size  # We want on average 50 eruptions per century
    yoes = np.random.default_rng().integers(0, years, size=size)
    yoes += init_year
    yoes = yoes.astype(np.int16)
    moes = np.random.default_rng().integers(1, 13, size=size).astype(np.int8)
    does = np.random.default_rng().integers(1, 29, size=size).astype(np.int8)
    # Force the first date to be 1851-01-01
    yoes[0] = 1851
    moes[0] = 1
    does[0] = 1
    # Create a structured array
    dates = np.zeros(len(yoes), dtype=[("year", int), ("month", int), ("day", int)])
    # Check that they are unique
    unique_dates = list(set(dates))
    assert len(dates) == len(unique_dates)
    dates["year"] = yoes
    dates["month"] = moes
    dates["day"] = does
    # Sort the array
    sorted_dates = np.sort(dates, order=["year", "month", "day"])
    # Extract the sorted arrays
    sorted_years = sorted_dates["year"]
    sorted_months = sorted_dates["month"]
    sorted_days = sorted_dates["day"]
    return sorted_years, sorted_months, sorted_days


def white_noise_dates():
    """Create random dates as white noise.

    Returns
    -------
    yoes: np.ndarray
        Array of length 'size' with the year of a date
    moes: np.ndarray
        Array of length 'size' with the month of a date
    does: np.ndarray
        Array of length 'size' with the day of a date
    veis: np.ndarray
        Array of length 'size' with the VEI
    """
    init_year = 1851
    size = 200
    # years = 1500
    # 32
    # Very hand wavy atm., but it is ratio * cumsum = length in years. Would expect
    # size/pareto_param = 80/2.5=32 to be correct?
    ratio = 25
    # yoes = np.random.uniform(0, years, size=size).astype(np.int16)
    # yoes = np.random.default_rng().gamma(shape=1, scale=100, size=size).astype(np.int16)
    yoes = np.cumsum(np.random.default_rng().pareto(2.5, size=size)) * ratio
    # print(years / yoes[-1])
    # yoes *= years / yoes[-1]
    yoes += init_year
    yoes = yoes.astype(np.int16)
    moes = np.random.uniform(1, 12, size=size).astype(np.int8)
    does = np.random.uniform(1, 28, size=size).astype(np.int8)
    # Force the first date to be 1851-01-01
    yoes[0] = 1851
    moes[0] = 1
    does[0] = 1
    # Create a structured array
    dates = np.zeros(len(yoes), dtype=[("year", int), ("month", int), ("day", int)])
    dates["year"] = yoes
    dates["month"] = moes
    dates["day"] = does
    # Sort the array
    sorted_dates = np.sort(dates, order=["year", "month", "day"])
    # Extract the sorted arrays
    sorted_years = sorted_dates["year"]
    sorted_months = sorted_dates["month"]
    sorted_days = sorted_dates["day"]
    # Total emitted SO2
    # tes = np.abs(np.random.normal(1, 200, size=size).astype(np.float32))
    # tes = np.random.default_rng().exponential(scale=3, size=size).astype(np.float32)
    # tes *= 90 / tes.max()
    # tes[0] = 257.9
    tes = np.random.default_rng().pareto(2.5, size=size).astype(np.float32)
    tes *= 257.9 / tes.max()
    return sorted_years, sorted_months, sorted_days, tes


def generate_exponential_waiting_times_historical_amplitudes() -> (
    tuple[np.ndarray, np.ndarray]
):
    iso = _draw_amplitudes_from_historic()
    dates = _draw_exponential_waiting_times(len(iso))
    # Determine the range for the daily time axis
    start_date = min(dates)
    end_date = max(dates)
    num_days = (end_date - start_date).days + 1

    # Create a daily time axis
    # daily_dates = [start_date + datetime.timedelta(days=x) for x in range(num_days)]

    # Initialize a white noise series with zeros
    daily_white_noise = np.zeros(num_days)

    # Generate white noise for the unique dates in sorted_dates
    unique_dates = list(set(dates))
    for i, date in enumerate(unique_dates):
        # Find the index in the daily_dates array
        index = (date - start_date).days
        # Replace the zero with a white noise value
        daily_white_noise[index] = iso[i]
    max_idx = np.argmax(daily_white_noise)
    if max_idx != 0:
        daily_white_noise = np.roll(daily_white_noise, -max_idx)
    start_date_extended = start_date - datetime.timedelta(days=365)
    num_days_extended = (end_date - start_date_extended).days + 1
    extended_white_noise = np.zeros(num_days_extended)
    # extended_white_noise[365] = Max_ids  # Place Max value after the year of zeros
    extended_white_noise[365 : 365 + num_days] = daily_white_noise
    daily_dates_extended = [
        start_date_extended + datetime.timedelta(days=x)
        for x in range(num_days_extended)
    ]
    return np.asarray(daily_dates_extended), extended_white_noise


def return_time_value_tuple() -> tuple[np.ndarray, np.ndarray]:
    y, m, d, t = white_noise_dates()
    datetimes = [
        datetime.datetime(y_, m_, d_) for y_, m_, d_ in zip(y, m, d, strict=True)
    ]
    return datetimes, t


def view() -> None:
    fig = view_frc.view_forcing(ext="nc", style="connected", save=False)
    plt.show()


def main() -> None:
    """Run the main function."""
    g = vc_create.create.GenerateRandomNormal(200, 1850)
    # g = vc_create.create.GenerateFromFile(
    #     200, 1850, vlr.config.PROJECT_ROOT / "src" / "vlr" / "data" / "eruptions.json"
    # )
    g.generate()
    frc_cls = vc_create.Data(*g.get_arrays())
    frc_cls.make_dataset()
    frc_cls.save_to_file()


if __name__ == "__main__":
    # view()
    # main()
    y, m, d, t = white_noise_dates()
    print(y)
    print(m)
    print(d)
    print(t)
    datetimes = [
        datetime.datetime(y_, m_, d_) for y_, m_, d_ in zip(y, m, d, strict=True)
    ]
    plt.plot(datetimes, t)
    plt.show()
