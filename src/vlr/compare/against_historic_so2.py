"""Compare synthetic SO2 against historic SO2."""


import numpy as np
import xarray as xr

import vlr

# We need both the OB16 SO2 input and a synthetically generated SO2 time series. Let us
# first verify that the OB16 SO2 input exists.


def _get_so2_ob16_full_timeseries() -> tuple[np.ndarray, np.ndarray]:
    """Load the npz file with volcanic injection.

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        Arrays containing time and value of SO2 peaks
    """
    file = "IVI2LoadingLatHeight501-2000_L18_c20100518.nc"
    if not (fn := vlr.config.DATA_PATH / "cesm-lme" / file).exists():
        print(f"Cannot find {fn.resolve()}")
        vlr.download.historic_so2.save_historical_so2(fn)
    ds = xr.open_dataset(fn)
    year = ds.time.data
    avgs_list = vlr.utils.time_series.mean_flatten([ds.colmass], dims=["lat"])
    avgs = avgs_list[0].data
    # Scale so that the unit is now in Tg (Otto-Bliesner et al. (2016)).
    avgs = avgs / avgs.max() * 257.9
    return year, avgs


if __name__ == "__main__":
    _ = _get_so2_ob16_full_timeseries()
