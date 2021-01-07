# About
A library of file readers for permafrost-related dataloggers. Instead of trying to make a single csv-reader that can handle any format, this treats each datalogger separately.

# Installation
To install LoggerReader, follow these instructions:

```bash
git clone https://github.com/nicholas512/LoggerRead
cd LoggerRead
python setup.py develop
```
Consider using a virtual environment, because some dependencies are installed.

# Using LoggerReader
The object that is used to read the logger data will differ depending on what kind of instrument the data comes from. However, each reader follows the same behaviour. They all have the `.read()` method that takes the file name as an argument. You can create the reader object first and then call the `.read()` method, or just run everything on one line.

```python
Reader().read(file)

""" or """
reader = Reader()
data = reader.read(file)
```

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
                   date_format="Y M D",
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

