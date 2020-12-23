import pandas as pd
import re
import json
import pprint

from .AbstractReader import AbstractReader


DATA_HEADERS = [  # Taken from HOBOware help manual. Not Complete.
    "x accel", "y accel", "z accel",
    "watt-hours", "kilowatt-hours",
    "watts",
    "rh", "temp", "wind speed", "wind dir", "soil moisture", "amps", "volts"
]


class HOBO(AbstractReader):
    TZ_REGEX = re.compile(r"GMT\s?[-+]\d\d:\d\d")
    MAX_LINES = 200  # How many lines to check for header, date, etc.

    def __init__(self, properties):
        super().__init__()
        self.properties = properties

    def read(self, file):
        """ Open a file """
        with open(file, encoding="UTF-8") as f:  # Get header info
            lines = f.readlines()
        self.extract_header_from_lines(lines)

        # Read remaining data as pd DataFrame
        self.raw_table = pd.read_csv(file, delimiter=self.properties.separator,
                                     skiprows=self.headerline, index_col=False)

        time_col = self.create_datetime_column(self.raw_table)
        data_col = self.extract_data_columns(self.raw_table)

        self.DATA = pd.concat([time_col, data_col], axis=1)

        return self.DATA

    def extract_header_from_lines(self, lines):
        """ Get the text and row index for the header row """
        for i, line in enumerate(lines):
            if self.is_header(line):
                self.headerline = line
                self.detect_time_zone_from_header_line(line)  # TODO: If "include_plot_details" and no_quotes_or_commas - get time zone elsewhere
                self.headerline = i
                break

            if i > self.MAX_LINES:
                raise Exception

    def is_header(self, line):
        """ Determine whether a line is a header row """
        pattern = self.properties.header_regex()
        match = pattern.search(line)
        return bool(match)

    def detect_time_zone_from_header_line(self, line):
        """ Extract time zone from header line """
        tz_match = self.TZ_REGEX.search(line)
        self.tz = tz_match.group()[-6:].replace(":", "") if tz_match else ""

    def is_data_header(self, text):
        """ Determine whether a string represents a column name with data """
        if self.properties.no_quotes_or_commas:
            pattern = re.compile(rf"({'|'.join(DATA_HEADERS)}) \(.{{1,5}}\)",  re.IGNORECASE)
        else:
            pattern = re.compile(f"({'|'.join(DATA_HEADERS)}), ", re.IGNORECASE)

        return pattern.findall(text)

    def is_datetime_header(self, text):
        """ Determine whether a string represents a column name for date or time """
        return bool(re.search("(Date Time|Date|Time)$", text))

    def extract_data_columns(self, df):
        """ Return a subset of a dataframe containing only data columns """
        keep = list()
        for col in df.columns:
            if self.is_data_header(col):
                keep.append(col)
        return df[keep]

    def create_datetime_column(self, df):
        """ Create a pandas datetime Series from a HOBO dataframe """
        tzfmt = "%z" if self.tz else ""

        if self.properties.separate_date_time:
            full_date = df["Date"] + df["Time"] + self.tz

            date_fmt = self.properties.date_pattern() + self.properties.time_pattern() + tzfmt
            TIME = pd.to_datetime(full_date, format=date_fmt)

        else:
            full_date = df["Date Time"] + self.tz
            date_fmt = self.properties.date_pattern() + tzfmt
            TIME = pd.to_datetime(full_date, format=date_fmt)

        TIME.columns = ['Time']

        return TIME


class HOBOProperties:
    DATE_FORMATS = ["M D Y", "Y M D", "D M Y"]
    POS_N_FMT = [""]
    NEG_N_FMT = [""]

    DEFAULTS = {"separator": ",",
                "include_line_number": True,
                "include_plot_title_in_header": True,
                "always_show_fractional_seconds": False,
                "separate_date_time": False,
                "no_quotes_or_commas": False,
                "include_logger_serial": True,
                "include_sensor_serial": True,
                "date_format": "M D Y",
                "date_separator": "/",
                "time_format_24hr": False,
                "positive_number_format": 1,
                "negative_number_format": 1,
                "include_plot_details": False
                }

    CLASSIC = {"separator": "\t",
               "include_line_number": False,
               "include_plot_title_in_header": False,
               "always_show_fractional_seconds": True,
               "separate_date_time": False,
               "no_quotes_or_commas": True,
               "include_logger_serial": False,
               "include_sensor_serial": True,
               "date_format": "M D Y",
               "date_separator": "/",
               "time_format_24hr": True,
               "positive_number_format": 1,
               "negative_number_format": 1,
               "include_plot_details": False
               }

    def __str__(self):
        return pprint.pformat(self.get_properties())

    def __init__(self, separator=",",
                 include_line_number=True,
                 include_plot_title_in_header=True,
                 always_show_fractional_seconds=False,
                 separate_date_time=False,
                 no_quotes_or_commas=False,
                 include_logger_serial=True,
                 include_sensor_serial=True,
                 date_format="M D Y",
                 date_separator="/",
                 time_format_24hr=False,
                 positive_number_format=1,
                 negative_number_format=1,
                 include_plot_details=False):

        self.separator = separator
        self.include_line_number = include_line_number
        self.include_plot_title_in_header = include_plot_title_in_header
        self.always_show_fractional_seconds = always_show_fractional_seconds
        self.separate_date_time = separate_date_time
        self.no_quotes_or_commas = no_quotes_or_commas
        self.include_logger_serial = include_logger_serial
        self.include_sensor_serial = include_sensor_serial
        self.date_format = date_format
        self.date_separator = date_separator
        self.time_format_24hr = time_format_24hr
        self.positive_number_format = positive_number_format
        self.negative_number_format = negative_number_format
        self.include_plot_details = include_plot_details

    @classmethod
    def defaults(cls):
        """ Create a HOBO Properties object using HOBOWare defaults """
        hobo_properties = cls(**cls.DEFAULTS)
        return hobo_properties

    @classmethod
    def classic(cls):
        """ Create a HOBO Properties object using HOBOWare 'classic' settings """
        hobo_properties = cls(**cls.CLASSIC)
        return hobo_properties

    @classmethod
    def from_file(cls, file):
        """ Create a HOBO Properties object from a text file """
        data = cls.read(file)
        hobo_properties = cls(**data)

        return hobo_properties

    def date_pattern(self):
        """ Return the appropriate strptime string to read dates from a HOBO file."""
        if self.date_format not in self.DATE_FORMATS:
            raise ValueError(f"Incorrect date pattern. Choose from {self.DATE_FORMATS}")

        if self.date_format == "Y M D":
            pattern = "%y{0}%m{0}%d".format(self.date_separator)

        elif self.date_format == "M D Y":
            pattern = "%m{0}%d{0}%y".format(self.date_separator)

        elif self.date_format == "D M Y":
            pattern = "%d{0}%m{0}%y".format(self.date_separator)

        if not self.separate_date_time:
            pattern += f" {self.time_pattern()}"

        return pattern

    def time_pattern(self):
        """ Return the appropriate strptime string to read time from a HOBO file."""

        if self.time_format_24hr:
            fmt = "%H:%M:%S"
        else:
            fmt = "%I:%M:%S %p"

        if self.always_show_fractional_seconds:
            fmt = fmt.replace("S", "S.%f")

        return fmt

    def header_regex(self):
        """ Return the regular expression to match a header row. """
        if self.separate_date_time:
            return re.compile(f"Date{self.separator}Time")
        else:
            return re.compile("Date Time")

    @staticmethod
    def read(file):
        """ Read HOBO file properties from a text file."""
        with open(file) as json_file:
            data = json.load(json_file)
        return data

    def write(self, file):
        """ Write HOBO properties to a text file."""
        with open(file, 'w') as json_file:
            json.dump(self.get_properties(), json_file)

    def get_properties(self):
        """ """
        return {x: getattr(self, x) for x in self.DEFAULTS.keys()}

    def detect_date_separator(self, lines):
        """ Detect the 'date_separator' property from a file."""
        pass

    def detect_separator(self, lines):
        """ Detect the 'separator' property from a file."""
        pass