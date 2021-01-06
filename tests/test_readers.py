""" Unit tests for readers"""
import pkg_resources
import unittest
from LoggerReader import readers

pkg = "LoggerReader"


class TestFG2_399(unittest.TestCase):

    def setUp(self):
        dat_fg2_399 = pkg_resources.resource_filename(pkg, "sample_files/FG2_399.csv")
        self.reader = readers.FG2()
        self.reader.read(dat_fg2_399)

    def test_array_shape(self):
        self.assertEqual(self.reader.get_data().shape[0], 9869)
        self.assertEqual(self.reader.get_data().shape[1], 8)

    def test_date_order(self):
        self.assertLess(self.reader.get_data().iloc[1,0], self.reader.get_data().iloc[10,0])
        self.assertGreater(self.reader.get_data().iloc[100,0], self.reader.get_data().iloc[10,0])


class TestGP5W_270(unittest.TestCase):

    def setUp(self):
        dat_gp5w_270 = pkg_resources.resource_filename(pkg, "sample_files/GP5W_270.csv")
        self.reader = readers.GP5W()
        self.reader.read(dat_gp5w_270)

    def test_array_shape(self):
        self.assertEqual(self.reader.get_data().shape[0], 2206)
        self.assertEqual(self.reader.get_data().shape[1], 8)

    def test_date_order(self):
        self.assertLess(self.reader.get_data().iloc[1,0], self.reader.get_data().iloc[10,0])
        self.assertGreater(self.reader.get_data().iloc[100,0], self.reader.get_data().iloc[10,0])


class TestGP5W_260(unittest.TestCase):

    def setUp(self):
        dat_gp5w_260 = pkg_resources.resource_filename(pkg, "sample_files/GP5W_260.csv")
        self.reader = readers.GP5W()
        self.reader.read(dat_gp5w_260)

    def test_array_shape(self):
        self.assertEqual(self.reader.get_data().shape[0], 1882)
        self.assertEqual(self.reader.get_data().shape[1], 4)

    def test_date_order(self):
        self.assertLess(self.reader.get_data().iloc[1,0], self.reader.get_data().iloc[10,0])
        self.assertGreater(self.reader.get_data().iloc[100,0], self.reader.get_data().iloc[10,0])


class TestHoboProperties(unittest.TestCase):

    def setUp(self):
        self.P = readers.HOBOProperties

    def test_date_regex(self):
        self.assertTrue("%I" in self.P(time_format_24hr=False).time_pattern())
        self.assertTrue("%H" in self.P(time_format_24hr=True).time_pattern())


class TestHOBOPropertiesDetection(unittest.TestCase):

    def setUp(self):
        self.P = readers.HOBOProperties
        MAXLINES = 500

        f_classic = pkg_resources.resource_filename(pkg, "sample_files/hobo_1_AB_classic.csv")
        with open(f_classic, encoding="UTF-8") as f:
            self.classic_lines = f.readlines()[:MAXLINES]

        f_default = pkg_resources.resource_filename(pkg, "sample_files/hobo_1_AB_defaults.csv")
        with open(f_default, encoding="UTF-8") as f:
            self.default_lines = f.readlines()[:MAXLINES]

        f_min = pkg_resources.resource_filename(pkg, "sample_files/hobo_1_AB_minimal.txt")
        with open(f_min, encoding="UTF-8") as f:
            self.minimal_lines = f.readlines()[:MAXLINES]

        f_var1 = pkg_resources.resource_filename(pkg, "sample_files/hobo_1_AB.csv")
        with open(f_var1, encoding="UTF-8") as f:
            self.var1_lines = f.readlines()[:MAXLINES]

        f_var2 = pkg_resources.resource_filename(pkg, "sample_files/hobo_1_AB_var2.csv")
        with open(f_var2, encoding="UTF-8") as f:
            self.var2_lines = f.readlines()[:MAXLINES]

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
        self.assertFalse(readers.HOBOProperties.detect_separate_date_and_time(self.classic_lines))
        self.assertFalse(readers.HOBOProperties.detect_separate_date_and_time(self.default_lines))
        self.assertFalse(readers.HOBOProperties.detect_separate_date_and_time(self.minimal_lines))
        self.assertTrue(readers.HOBOProperties.detect_separate_date_and_time(self.var1_lines))

    def test_detect_always_show_fractional_seconds(self):
        self.assertTrue(readers.HOBOProperties.detect_fractional_seconds(self.classic_lines))
        self.assertFalse(readers.HOBOProperties.detect_fractional_seconds(self.default_lines))
        self.assertFalse(readers.HOBOProperties.detect_fractional_seconds(self.minimal_lines))

    def test_detect_line_numbers(self):
        self.assertFalse(readers.HOBOProperties.detect_line_number(self.classic_lines))
        self.assertTrue(readers.HOBOProperties.detect_line_number(self.default_lines))
        self.assertFalse(readers.HOBOProperties.detect_line_number(self.minimal_lines))

        
if __name__ == '__main__':
    unittest.main()
