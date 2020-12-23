import argparse
from LoggerReader import readers

fmtdict = {
    "GP5W": readers.GP5W,
    "FG2": readers.FG2
}


def main(args):
    Reader = fmtdict[args.format]
    reader = Reader()

    print(f"Reading {args.input}")
    reader.read(args.input)

    if args.csv_file:
        print(f"Writing data to {args.csv_file}")
        reader.DATA.to_csv(args.csv_file, index=False)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Read datalogger file")

    parser.add_argument("input", help="path to logger file. ")
    parser.add_argument("-f", "--format", dest='format',
                        help=f"The type of input file you are using. Chosen from {list(fmtdict.keys())}")
    parser.add_argument("-C", "--csv", default=None, dest='csv_file',
                        help="Path to csv file to write to")

    args = parser.parse_args()

    main(args)
