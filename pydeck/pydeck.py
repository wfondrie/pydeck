import logging
import argparse
import pydeck

def main():
    # setup logging
    logging.basicConfig(format="{asctime} [{levelname}/{processName}] "
                               "{module}.{funcName} : {message}",
                        style="{", level=logging.DEBUG)

    # Parse cmd line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("md_file", help="The markdown input file.")
    args = parser.parse_args()

    # build the slide deck

if __name__ == "__main__":
    main()
