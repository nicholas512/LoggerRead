from datetime import datetime, timedelta, tzinfo
import pandas as pd
import re
import json

from AbstractReader import AbstractReader  


DATA_HEADERS = [  # Taken from HOBOware help manual. Not Complete.
    "x accel", "y accel", "z accel",
    "watt-hours", "kilowatt-hours",
    "watts",
    "rh", "temp", "wind speed", "wind dir", "soil moisture", "amps", "volts"
]


class HOBO(AbstractReader):
    TZ_REGEX = re.compile("GMT\s?[-+]\d\d:\d\d")

    def __init__(self, properties):
        super().__init__()
        self.properties = properties

    def read(self, file):
        with open(file, encoding="UTF-8") as f:  # Get header info
            L = 0
            for line in f:

                if self.is_header(line):
                    self.headerline = line
                    break
                
                elif self.is_meta(line):
                    self.META.append(line)

                else:
                    print(f"Skipping Line {line}")
                
                L += 1
                if L > 10:
                    raise Exception
        
        # Read remaining data as pd DataFrame
        self.raw_table = pd.read_csv(file, delimiter=self.properties.separator,
                                     skiprows=L, index_col=False)

        return self.raw_table

        self.convert_dates(self.raw_table)
        
        return self.raw_table

    def is_header(self, line):
        pattern = self.properties.header_regex()
        match = pattern.search(line)
        return bool(match)

    def count_delimiters(self, line):
        return line.count(self.properties.separator)

    def detect_time_zone(self, line):
        tz_match = self.TZ_REGEX.search(line)
        self.tz = tz_match.group()[-6:] if tz_match else None

    def is_data_column(self, text):
        if self.properties.no_quotes_or_commas:
            pattern = re.compile(f"({'|'.join(DATA_HEADERS)}) \(.{1,5}\)", "i")
        else:
            pattern = re.compile(f"({'|'.join(DATA_HEADERS)}), ", re.IGNORECASE)
        
        return pattern.findall(text)

    # def is_data(self, line):
       
    def convert_dates(self, df):
        if self.properties.separate_date_time:
            df
        else:
            fmt = self.properties.date_pattern
            df

    def is_meta(self, line):
        pass

class HOBOProperties:
    DATE_FORMATS = ["M D Y", "Y M D", "D M Y"]
    POS_N_FMT = [""]
    NEG_N_FMT = [""]
    
    DEFAULTS = {
                "separator": ",",
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
                "negative_number_format": 1
                
    }
    CLASSIC = {
                "separator": "\t",
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
                "negative_number_format": 1
    }
    
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
                negative_number_format=1):
 
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

    @classmethod
    def defaults(cls):
        hobo_properties = cls(**cls.DEFAULTS)
        return hobo_properties

    @classmethod
    def classic(cls):
        hobo_properties = cls(**cls.CLASSIC)
        return hobo_properties

    @classmethod
    def from_file(cls, file):
        data = cls.read(file)
        hobo_properties = cls(**data)

        return hobo_properties

    def date_pattern(self):
        if self.date_format not in self.DATE_FORMATS:
            raise ValueError(f"Incorrect date pattern. Choose from {self.DATE_FORMATS}")
        
        if self.date_format == "Y M D":
            pattern = "%Y{0}%m{0}%d".format(self.date_separator)
        
        elif self.date_format == "M D Y":
            pattern = "%m{0}%d{0}%Y".format(self.date_separator)
        
        elif self.date_format == "D M Y":
            pattern = "%d{0}%m{0}%Y".format(self.date_separator)
        
        if not self.separate_date_time:
            pattern += f" {self.time_pattern()}"
        
        return pattern

    def time_pattern(self):
        if self.time_format_24hr:
            return "%H:%M:%S"
        else:
            return "%I:%M:%S %p"

    def header_regex(self):
        if self.separate_date_time:
            return re.compile(f"Date{self.separator}Time")
        else:
            return re.compile("Date Time")

    @staticmethod
    def read(file):
        with open(file) as json_file:
            data = json.load(json_file)
        return data

    def write(self, file):
        """ Write HOBO properties to a text file """
        json.dump(self.get_properties(), file)
        
    def get_properties(self):
        return {x: getattr(self, x) for x in self.DEFAULTS.keys()}

    def detect_date_separator(self, raw):
        pass

    def detect_separator(self, raw):
        pass


