# About
A library of file readers for permafrost-related dataloggers.

# Installation
To install LoggerReader, follow these instructions:

```bash
git clone https://github.com/nicholas512/LoggerRead
cd LoggerRead
python setup.py develop
```

# Using

## GeoPrecision
Geoprecision logger format differs between the FG2 and GP5W variants
### FG2
### GP5W
## HOBO
Because of the variability of HOBOWare CSV exports, the HOBO reader relies on specifying the configuration

## The HOBOProperties configuration object

```python
from LoggerReader.readers import HOBOProperties
from pathlib import Path

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

# initialize a HOBO reader with a HOBOProperties object
classic_file = resource_filename("LoggerReader", "sample_files/hobo_1_AB_classic.csv")
classic_properties = HOBOProperties.classic()
hobo = HOBO(classic_properties)
data = hobo.read(classic_file)
```

# Format
Reads data into a pandas dataframe. Column titles are of the format:

\<*index*\>_\<*standard name*\>_\<*depth in mm*\> e.g. 1_soil_temperature_500

The date/time column is named *time* and is the first column

