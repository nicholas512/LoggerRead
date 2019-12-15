# Pyrmafrost
Generic file reader for permafrost-related dataloggers

# Format
Reads data into a pandas dataframe. Column titles are of the format:

\<*index*\>_\<*standard name*\>_\<*depth in mm*\> e.g. 1_soil_temperature_500

The date/time column is named *time* and is the first column

