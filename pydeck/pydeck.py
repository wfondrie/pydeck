import logging
import argparse
import pydeck

def main():
    # setup logging
    logging.basicConfig(format="{asctime} [{levelname}] "
                               "{module}.{funcName} : {message}",
                        style="{", level=logging.DEBUG)

    # Parse cmd line arguments
    desc = "Create a remark slide deck from a markdown file."
    epi = ("The input, md_file, may contain a YAML header to customize "
           "the style of the resulting slide deck. See the documentation"
           " for more details.")


    parser = argparse.ArgumentParser(description=desc, epilog=epi)
    parser.add_argument("md_file", help="The markdown input file.")
    args = parser.parse_args()

    logging.info("Processing %s", args.md_file)
    deck = pydeck.SlideDeck(args.md_file)
    deck.build()
    logging.info("Wrote %s", deck.params["html_out"])

if __name__ == "__main__":
    main()
