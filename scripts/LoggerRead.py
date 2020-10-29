import argparse
from pathlib import Path
from LoggerRead.libraries import readers

fmtdict = {
    "GP5W": readers.GP5W
    "FG2": readers.FG2
}

def main(args):
    Reader = fmtdict[args.format]
    reader = Reader()

    print(f"Reading {args.input}")
    loggerdata = reader.read(args.input)

    if args.csv_file:
        print(f"Reading {args.csv}")
        loggerdata.DATA.to_csv(args.csv)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Read datalogger file")

    parser.add_argument("input", help="path to logger file. ")
    parser.add_argument("-f", "--format", dest='format',
                        help="Whether or not to build directories automatically from a control file")
    parser.add_argument("-C", "--csv", , default=None, dest='csv_file',
                        help="Path to csv file to write to")
    
    args = parser.parse_args()

    main(args)