""" Unit tests for readers"""
import pkg_resources
import unittest
from LoggerReader import readers

pkg = "LoggerReader"


class TestHoboProperties(unittest.TestCase):

    def setUp(self):
        self.P = readers.HOBOProperties

    def test_date_regex(self):
        self.assertTrue("%I" in self.P(time_format_24hr=False).time_pattern())
        self.assertTrue("%H" in self.P(time_format_24hr=True).time_pattern())


class TestHOBOPropertiesDetectionElements(unittest.TestCase):

    def setUp(self):
        self.P = readers.HOBOProperties
        MAXLINES = 400

        f_classic = pkg_resources.resource_filename(pkg, "sample_files/hobo_1_AB_classic.csv")
        with open(f_classic, encoding="UTF-8") as f:
            lines = f.readlines()
            self.classic_lines = lines[:MAXLINES] + lines[MAXLINES::1000]

        f_default = pkg_resources.resource_filename(pkg, "sample_files/hobo_1_AB_defaults.csv")
        with open(f_default, encoding="UTF-8") as f:
            lines = f.readlines()
            self.default_lines = lines[:MAXLINES] + lines[MAXLINES::1000]

        f_min = pkg_resources.resource_filename(pkg, "sample_files/hobo_1_AB_minimal.txt")
        with open(f_min, encoding="UTF-8") as f:
            lines = f.readlines()
            self.minimal_lines = lines[:MAXLINES] + lines[MAXLINES::1000]

        f_var1 = pkg_resources.resource_filename(pkg, "sample_files/hobo_1_AB.csv")
        with open(f_var1, encoding="UTF-8") as f:
            lines = f.readlines()
            self.var1_lines = lines[:MAXLINES] + lines[MAXLINES::1000]

        f_var2 = pkg_resources.resource_filename(pkg, "sample_files/hobo_1_AB_var2.csv")
        with open(f_var2, encoding="UTF-8") as f:
            lines = f.readlines()
            self.var2_lines = lines[:MAXLINES] + lines[MAXLINES::1000]

        f_pos1 = pkg_resources.resource_filename(pkg, "sample_files/hobo-positive-number-1.txt")
        with open(f_pos1, encoding="UTF-8") as f:
            lines = f.readlines()
            self.f_pos1 = lines[:MAXLINES] + lines[MAXLINES::1000]

        f_pos2 = pkg_resources.resource_filename(pkg, "sample_files/hobo-positive-number-2.csv")
        with open(f_pos2, encoding="UTF-8") as f:
            lines = f.readlines()
            self.f_pos2 = lines[:MAXLINES] + lines[MAXLINES::1000]

        f_pos3 = pkg_resources.resource_filename(pkg, "sample_files/hobo-positive-number-3.csv")
        with open(f_pos3, encoding="UTF-8") as f:
            lines = f.readlines()
            self.f_pos3 = lines[:MAXLINES] + lines[MAXLINES::1000]

        f_pos4 = pkg_resources.resource_filename(pkg, "sample_files/hobo-positive-number-4.csv")
        with open(f_pos4, encoding="UTF-8") as f:
            lines = f.readlines()
            self.f_pos4 = lines[:MAXLINES] + lines[MAXLINES::1000]

        f_neg2 = pkg_resources.resource_filename(pkg, "sample_files/hobo-negative-2.txt")
        with open(f_neg2, encoding="UTF-8") as f:
            lines = f.readlines()
            self.f_neg2 = lines[:MAXLINES] + lines[MAXLINES::1000]

        f_neg3 = pkg_resources.resource_filename(pkg, "sample_files/hobo-negative-3.txt")
        with open(f_neg3, encoding="UTF-8") as f:
            lines = f.readlines()
            self.f_neg3 = lines[:MAXLINES] + lines[MAXLINES::1000]

    def test_separator(self):
        self.assertEqual(readers.HOBOProperties.detect_separator(self.classic_lines), "\t")
        self.assertEqual(readers.HOBOProperties.detect_separator(self.default_lines), ",")
        self.assertEqual(readers.HOBOProperties.detect_separator(self.minimal_lines), ";")

    def test_date_separator(self):
        self.assertEqual(readers.HOBOProperties.detect_date_separator(self.classic_lines), "/")
        self.assertEqual(readers.HOBOProperties.detect_date_separator(self.default_lines), "/")
        self.assertEqual(readers.HOBOProperties.detect_date_separator(self.minimal_lines), "-")

    def test_detect_date_format(self):
        self.assertEqual(readers.HOBOProperties.detect_date_format(self.classic_lines), "MDY")
        self.assertEqual(readers.HOBOProperties.detect_date_format(self.default_lines), "MDY")
        self.assertEqual(readers.HOBOProperties.detect_date_format(self.minimal_lines), "DMY")
        self.assertEqual(readers.HOBOProperties.detect_date_format(self.var2_lines), "YMD")

    def test_plot_details(self):
        self.assertTrue(readers.HOBOProperties.detect_include_plot_details(self.classic_lines))
        self.assertFalse(readers.HOBOProperties.detect_include_plot_details(self.default_lines))
        self.assertFalse(readers.HOBOProperties.detect_include_plot_details(self.minimal_lines))

    def test_24hr(self):
        self.assertTrue(readers.HOBOProperties.detect_time_format_24hr(self.classic_lines))
        self.assertFalse(readers.HOBOProperties.detect_time_format_24hr(self.default_lines))
        self.assertTrue(readers.HOBOProperties.detect_time_format_24hr(self.minimal_lines))

    def test_detect_separate_date_and_time(self):
        self.assertFalse(readers.HOBOProperties.detect_separate_date_time(self.classic_lines))
        self.assertFalse(readers.HOBOProperties.detect_separate_date_time(self.default_lines))
        self.assertFalse(readers.HOBOProperties.detect_separate_date_time(self.minimal_lines))
        self.assertTrue(readers.HOBOProperties.detect_separate_date_time(self.var1_lines))

    def test_detect_always_show_fractional_seconds(self):
        self.assertTrue(readers.HOBOProperties.detect_always_show_fractional_seconds(self.classic_lines))
        self.assertFalse(readers.HOBOProperties.detect_always_show_fractional_seconds(self.default_lines))
        self.assertFalse(readers.HOBOProperties.detect_always_show_fractional_seconds(self.minimal_lines))

    def test_detect_line_numbers(self):
        self.assertFalse(readers.HOBOProperties.detect_line_number(self.classic_lines))
        self.assertTrue(readers.HOBOProperties.detect_line_number(self.default_lines))
        self.assertFalse(readers.HOBOProperties.detect_line_number(self.minimal_lines))

    def test_quotes_commas(self):
        self.assertTrue(readers.HOBOProperties.detect_no_quotes_or_commas(self.classic_lines))
        self.assertFalse(readers.HOBOProperties.detect_no_quotes_or_commas(self.default_lines))
        self.assertFalse(readers.HOBOProperties.detect_no_quotes_or_commas(self.minimal_lines))
        self.assertFalse(readers.HOBOProperties.detect_no_quotes_or_commas(self.var1_lines))
        self.assertTrue(readers.HOBOProperties.detect_no_quotes_or_commas(self.var2_lines))

    def test_detect_positive_number_format(self):
        self.assertEqual(readers.HOBOProperties.parse_number_format(self.f_pos1), (None, ".", ";", None, None))
        self.assertEqual(readers.HOBOProperties.parse_number_format(self.f_pos2), (None, ",", "\t", None, None))
        self.assertEqual(readers.HOBOProperties.parse_number_format(self.f_pos3), (None, ",", ";", None, None))
        self.assertEqual(readers.HOBOProperties.parse_number_format(self.f_pos4), (None, " ", ",", None, None))
        self.assertEqual(readers.HOBOProperties.parse_number_format(self.f_neg2), (None, ",", "\t", None, "-"))
        self.assertEqual(readers.HOBOProperties.parse_number_format(self.f_neg3), (None, " ", "\t", "(", ")"))
        self.assertEqual(readers.HOBOProperties.parse_number_format(self.classic_lines), (None, ".", "\t", "-", None))
        self.assertEqual(readers.HOBOProperties.parse_number_format(self.default_lines), (None, ".", ",", "-", None))
        self.assertEqual(readers.HOBOProperties.parse_number_format(self.minimal_lines), (None, ",", ";", None, None))


class TestHOBOPropertiesFullDetection(unittest.TestCase):

    def setUp(self):
        pass

    def test_classic(self):
        f_classic = pkg_resources.resource_filename(pkg, "sample_files/hobo_1_AB_classic.csv")
        detected_properties = readers.HOBOProperties.autodetect(f_classic, 400).get_properties()
        true_properties = readers.HOBOProperties.CLASSIC

        self.assertEqual(true_properties["include_line_number"], detected_properties["include_line_number"])
        self.assertEqual(true_properties["always_show_fractional_seconds"], detected_properties["always_show_fractional_seconds"])
        self.assertEqual(true_properties["separate_date_time"], detected_properties["separate_date_time"])
        self.assertEqual(true_properties["no_quotes_or_commas"], detected_properties["no_quotes_or_commas"])

    def test_defaults(self):
        f_classic = pkg_resources.resource_filename(pkg, "sample_files/hobo_1_AB_defaults.csv")
        detected_properties = readers.HOBOProperties.autodetect(f_classic, 400).get_properties()
        true_properties = readers.HOBOProperties.DEFAULTS

        self.assertEqual(true_properties["include_line_number"], detected_properties["include_line_number"])
        self.assertEqual(true_properties["always_show_fractional_seconds"], detected_properties["always_show_fractional_seconds"])
        self.assertEqual(true_properties["separate_date_time"], detected_properties["separate_date_time"])
        self.assertEqual(true_properties["no_quotes_or_commas"], detected_properties["no_quotes_or_commas"])


class TestHOBOFileRead(unittest.TestCase):

    def setUp(self):
        f_classic = pkg_resources.resource_filename(pkg, "sample_files/hobo_1_AB_classic.csv")
        self.h_classic = readers.HOBO()
        self.h_classic.read(f_classic)
        
        f_default = pkg_resources.resource_filename(pkg, "sample_files/hobo_1_AB_defaults.csv")
        self.h_default = readers.HOBO()
        self.h_default.read(f_default)

        f_min = pkg_resources.resource_filename(pkg, "sample_files/hobo_1_AB_minimal.txt")
        self.h_min = readers.HOBO()
        self.h_min.read(f_min)

        f_var1 = pkg_resources.resource_filename(pkg, "sample_files/hobo_1_AB.csv")
        self.h_var1 = readers.HOBO()
        self.h_var1.read(f_var1)

        self.f_var2 = pkg_resources.resource_filename(pkg, "sample_files/hobo_1_AB_var2.csv")
        self.h_var2 = readers.HOBO()

    def test_time_zone_detection(self):
        self.assertEqual(self.h_classic.META['tz_offset'], "-0700")
        self.assertEqual(self.h_default.META['tz_offset'], "-0700")
        self.assertEqual(self.h_min.META['tz_offset'], "-0700")
        self.assertEqual(self.h_var1.META['tz_offset'], "-0700")

    @unittest.expectedFailure
    def failing_time_zone_detection(self):
        h_var2 = self.h_var2.read(self.f_var2)
        self.assertEqual(h_var2.META['tz_offset'], "-0700")

    def test_values(self):
        pass


if __name__ == '__main__':
    unittest.main()
