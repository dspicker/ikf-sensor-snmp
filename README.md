# Sensor reading via snmp

Receives temperature and relative-humidity values via snmp and visualizes them with pyplot.

## Snmp get script

The script `snmp_get.py` reads the sensor values and stores them in a csv-file.
It can be automatically executed by a crontab to get a permanent monitoring of 
the sensor values.

E.g. to execute it every 10 minutes:
```
*/10 * * * * /path/to/python /path/to/this_repo/snmp_get.py >> /path/to/optional_logfile/snmp_get.log
```

## Plotting

The files `plot.py`and `àutoplot.py` create a plot of the last 48 hours.