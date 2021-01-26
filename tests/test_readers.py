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


class TestHOBOPropertiesDetectionElements(unittest.TestCase):

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

        f_var2 = pkg_resources.resource_filename(pkg, "sample_files/hobo_1_AB_var2.csv")
        self.h_var2 = readers.HOBO()
        self.h_var2.read(f_var2)

    def test_time_zone_detection(self):
        self.assertEqual(self.h_classic.META['tz_offset'], "-0700")
        self.assertEqual(self.h_default.META['tz_offset'], "-0700")
        self.assertEqual(self.h_min.META['tz_offset'], "-0700")
        self.assertEqual(self.h_var1.META['tz_offset'], "-0700")
        self.assertEqual(self.h_var2.META['tz_offset'], "-0700")



if __name__ == '__main__':
    unittest.main()
