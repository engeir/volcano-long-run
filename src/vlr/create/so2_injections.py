"""Create a time series representing SO2 injections."""


import volcano_cooking as vc


def main() -> None:
    """Run the main function."""
    help(vc.synthetic_volcanoes.create)
    vc.modules.create.GenerateFromFile(200, 1850, "./src/vlr/data/eruptions.json")
