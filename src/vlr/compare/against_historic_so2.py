"""Compare synthetic SO2 against historic SO2."""

import datetime

import matplotlib.pyplot as plt
import numpy as np
import volcano_base

import vlr


def print_stats_from_peak_arrays(dates: np.ndarray, values: np.ndarray) -> None:
    """Print statistics from peak arrays."""
    nonzero_values = np.argwhere(values != 0)
    peaks = values[nonzero_values]
    print(f"Number of peaks: {len(peaks)}")
    print(f"Number of eruptions per century: {len(peaks)/len(dates)*36500:.3f}")
    print(f"Minimum peak value: {peaks.min():.3f}")
    print(f"Maximum peak value: {peaks.max():.3f}")
    print(f"Mean peak value: {peaks.mean():.3f}")


def plot_waiting_times(dates: np.ndarray, values: np.ndarray, **kwargs) -> None:
    """Plot the waiting times."""
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
    sorted_arr = np.sort(diff.flatten())[::-1]
    plt.figure()
    plt.plot(sorted_arr, **kwargs)


def plot_amplitudes(dates: np.ndarray, values: np.ndarray, **kwargs) -> None:
    """Plot the amplitudes."""
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
    historic = volcano_base.load.get_so2_ob16_peak_timeseries()
    synthetic = vlr.create.so2_injections.generate_exponential_waiting_times_historical_amplitudes()
    plot_time_series(*historic, c="r")
    plot_time_series(*synthetic)
    print_stats_from_peak_arrays(*historic)
    print_stats_from_peak_arrays(*synthetic)
    plot_amplitudes(*historic, c="r")
    plot_amplitudes(*synthetic)
    plot_waiting_times(*historic, c="r")
    plot_waiting_times(*synthetic)
    plt.show()
