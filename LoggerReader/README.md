# About
Dataloggers for environmental science data can be configured to output text files in any number of flavours. Differences in date format, separator, and metadata can make it hard to easily open datalogger files for further processing. A script that one scientist uses to read their files can fail when trying to open files that were configured differently, even when the data are from a sensor of the same make and model. This makes it harder for scientists to share data and use a common set of tools for quality control and analysis of observational data.

LoggerRead is a library of text-file readers for permafrost-related dataloggers meant to open files effortly as pandas dataframes. Instead of trying to make a single csv-reader that can handle any format, LoggerRead treats each datalogger separately; this makes it possible to open files automatically with greater confidence that they're being read properly. LoggerRead can be used as a standalone library for interactive data analysis and exploration, or can be integrated into other programs. Currently, data from the following sensors are supported:

* GeoPrecision (GP5W)
* GeoPrecision (FG2)
* Onset HOBO (HOBOware)

# Installation
To install LoggerReader, the simplest way is to use `pip`:
```bash
pip install LoggerReader
```

If you would prefer to install the lastest version from the source code, 
```bash
git clone https://github.com/nicholas512/LoggerRead
cd LoggerRead
python setup.py develop
```
Consider using a virtual environment, because some dependencies are installed.

# Using LoggerReader
The class used to read logger data must be selected depending on what kind of instrument the data comes from. However, each reader behaves the same way. They all have the `.read()` method that takes the file name as an argument. You can create a reader first and then call the `.read()` method, or just run everything on one line. For Geoprecision FG for instance:

```python
FG2().read(file)
```
**OR**
```python
reader = FG2()
data = reader.read(file)
```
Some datalogger types may require other information in order to read the file correctly.

## GeoPrecision
Geoprecision logger format differs between the FG2 and GP5W variants. To read a GeoPrecision file, use either the FG2 or GP5W object
### FG2
FG2 is the newer software for GeoPrecision instruments:

```python
from LoggerReader.readers import FG2
from pkg_resources import resource_filename
fg2_file = resource_filename("LoggerReader", "sample_files/FG2_399.csv")

# Read an FG2 file
FG2().read(fg2_file)
```

### GP5W
GP5W is the older software for GeoPrecision instruments:

```python
from LoggerReader.readers import GP5W
from pkg_resources import resource_filename
gp5w_file = resource_filename("LoggerReader", "sample_files/GP5W_260.csv")

# To read a file, you might first create a reader object 
reader = GP5W()
reader.read(gp5w_file)

# Or instead, read the data in one line
data = GP5W().read(gp5w_file)
```
## HOBO
Because of the variability of HOBOWare CSV exports, the HOBO reader relies on on a HOBOProperties configuration object. This can be configured manually (most reliable) or autodetected from a file.

## The HOBOProperties configuration object

```python
from LoggerReader.readers import HOBOProperties
from pkg_resources import resource_filename
from pathlib import Path

# Autodetect file structure
hobo_file = resource_filename("LoggerReader", "sample_files/hobo_1_AB_classic.csv")
P = HOBOProperties.autodetect(hobo_file)
print(P)

# HOBOWare 'default' format
print(HOBOProperties.defaults())

# HOBOWare 'classic' format
print(HOBOProperties.classic())

# Custom format (unspecified properties are defaults)
P = HOBOProperties(date_separator=",",
                   date_format="YMD",
                   include_line_number=True,
                   include_plot_details=False,
                   no_quotes_or_commas=False,
                   separate_date_time=False)
print(P)
savepath = Path(Path.home(), "custom_hobo_properties.json")
P.write(savepath)  # Save to file

# Read from a saved file
Q = HOBOProperties.from_file(savepath)  # Read from a file
print(Q)
```

## Reading HOBO files with the HOBO object

```python
from LoggerReader.readers import HOBO, HOBOProperties
from pathlib import Path
from pkg_resources import resource_filename

classic_file = resource_filename("LoggerReader", "sample_files/hobo_1_AB_classic.csv")
defaults_file = resource_filename("LoggerReader", "sample_files/hobo_1_AB_defaults.csv")

# To autodetect HOBOWare Properties:
data = HOBO().read(defaults_file)

# To manually specify a the HOBOWare configuration, initialize the HOBO reader with a HOBOProperties object
classic_file = resource_filename("LoggerReader", "sample_files/hobo_1_AB_classic.csv")
classic_properties = HOBOProperties.classic()
hobo = HOBO(classic_properties)
data = hobo.read(classic_file)
```

# Format
Reader objects save csv data in a pandas dataframe stored as the `DATA` attribute.  Column titles are left unchanged with the exception of the datetime column which is renamed to `TIME`. It is always the first column in the dataframe.

Where possible, any metadata that is found in the file is stored in a `META` attribute.

