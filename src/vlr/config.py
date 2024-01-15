"""Configuration file for `volcano-long-run`."""

import pathlib
import tomllib


def create_config() -> pathlib.Path:
    """Create the file where the configuration will be saved."""
    HERE = pathlib.Path(__file__)
    for i, parents in enumerate(HERE.parents):
        if parents.name == "src":
            project_root = HERE.parents[i + 1]
            break
    if not project_root.exists():
        project_root.mkdir(parents=True)
    return project_root


_root = create_config()
(_data := _root / "downloaded_files").mkdir(exist_ok=True)
(_save := _root / "generated_files").mkdir(exist_ok=True)
_cfg = _root / "vlr.toml"
if not _cfg.exists():
    with open(_cfg, mode="w") as cfg:
        cfg.write("[vlr]\n")
        cfg.write("# Location of the repository\n")
        cfg.write(f'project_root = "{_root}"\n')
        cfg.write("# Location of the data used in analysis scripts\n")
        cfg.write(f'data_path = "{_data}"\n')
        cfg.write("# Location of the saved figures\n")
        cfg.write(f'save_path = "{_save}"')

HOME = pathlib.Path().home()
# https://github.com/python/mypy/issues/16423
with _cfg.open(mode="rb") as cfg:  # type: ignore
    out = tomllib.load(cfg)  # type: ignore
    PROJECT_ROOT = pathlib.Path(out["vlr"]["project_root"])
    DATA_PATH = pathlib.Path(out["vlr"]["data_path"])
    SAVE_PATH = pathlib.Path(out["vlr"]["save_path"])
    # data_path = "/media/een023/LaCie/een023/cesm/model-runs"

DATA_ATTRS = {
    "AODVISstdn": ["Stratospheric aerosol optical depth 550 nm day night", "1"],
    "FSNTOA": ["Net solar flux at top of atmosphere", "W/m2"],
    "TREFHT": ["Reference height temperature", "K"],
    "so4_a1": ["so4_a1 concentration", "kg/kg"],
    "so4_a2": ["so4_a2 concentration", "kg/kg"],
    "so4_a3": ["so4_a3 concentration", "kg/kg"],
    "TROP_P": ["Tropopause Pressure", "Pa"],
    "TMSO2": ["SO2 burden", "Tg"],
    "FLUT": ["Upwelling longwave flux at top of model", "W/m2"],
    "FLNT": ["Net longwave flux at top of model", "W/m2"],
    "FSNT": ["Net solar flux at top of model", "W/m2"],
    "FLNS": ["Net longwave flux at surface", "W/m2"],
    "SO2": ["SO2 concentration", "mol/mol"],
    "SST": ["sea surface temperature", "K"],
    "T": ["Temperature", "K"],
    "U": ["Zonal wind", "m/s"],
}
