"""Compare synthetic SO2 against historic SO2."""

import datetime

import matplotlib.pyplot as plt
import numpy as np

import vlr

# We need both the OB16 SO2 input and a synthetically generated SO2 time series. Let us
# first verify that the OB16 SO2 input exists.


def _get_synthetic_so2() -> tuple[np.ndarray, np.ndarray]:
    dates, iso = vlr.create.so2_injections.return_time_value_tuple()
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


def print_stats_from_peak_arrays(dates: np.ndarray, values: np.ndarray) -> None:
    """Print statistics from peak arrays."""
    nonzero_values = np.argwhere(values != 0)
    peaks = values[nonzero_values]
    print(f"Number of peaks: {len(peaks)}")
    print(f"Minimum peak value: {peaks.min():.3f}")
    print(f"Maximum peak value: {peaks.max():.3f}")
    print(f"Mean peak value: {peaks.mean():.3f}")


def plot_amplitude_distribution(
    dates: np.ndarray, values: np.ndarray, **kwargs
) -> None:
    nonzero_values = np.argwhere(values != 0)
    peaks = values[nonzero_values]
    # out = fppanalysis.distribution(peaks, 10, kernel=False)
    # plt.figure()
    # plt.plot(out[2], out[0])
    plt.figure()
    # plt.plot(out[2], out[1])
    # plt.figure()
    plt.hist(peaks, bins=20)


def plot_waiting_times(dates: np.ndarray, values: np.ndarray, **kwargs) -> None:
    dates, values = dates.flatten(), values.flatten()
    nonzero_values = np.argwhere(values != 0)
    peak_dates = dates[nonzero_values].flatten()
    if isinstance(peak_dates[0], float):
        diff = np.diff(peak_dates)
    elif isinstance(peak_dates[0], datetime.datetime):
        diff = np.diff(
            [
                eval(datetime.datetime.strftime(i, "%Y+%-m/12+%-d/365"))
                for i in peak_dates
            ]
        )
    sorted = np.sort(diff.flatten())[::-1]
    plt.figure()
    plt.plot(sorted, **kwargs)


def plot_amplitudes(dates: np.ndarray, values: np.ndarray, **kwargs) -> None:
    nonzero_values = np.argwhere(values != 0)
    out = values[nonzero_values].flatten()
    peaks = np.sort(out)[::-1]
    plt.figure()
    plt.plot(peaks, **kwargs)


def plot_time_series(dates: np.ndarray, values: np.ndarray, **kwargs) -> None:
    """Plot both time series."""
    plt.figure()
    plt.plot(dates, values, **kwargs)


if __name__ == "__main__":
    historic = vlr.load_historic_data.get_so2_ob16_peak_timeseries()
    synthetic = _get_synthetic_so2()
    plot_time_series(*historic, c="r")
    plot_time_series(*synthetic)
    print_stats_from_peak_arrays(*historic)
    print_stats_from_peak_arrays(*synthetic)
    # # plot_amplitude_distribution(*historic)
    # # plot_amplitude_distribution(*synthetic)
    plot_amplitudes(*historic, c="r")
    plot_amplitudes(*synthetic)
    plot_waiting_times(*historic, c="r")
    plot_waiting_times(*synthetic)
    plt.show()
