"""Main script to print info about the package."""
import vlr


def main():
    """Run the main function for the vdd package."""
    print(f"Hello, this is {__package__} at version v{vlr.__version__}!")
