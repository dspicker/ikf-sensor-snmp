import os
import datetime
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.dates


matplotlib.use('tkagg')
degree_sign = '\N{DEGREE SIGN}'

csv_filename = "env_data.csv"
csv_path = os.getcwd() + "/" + csv_filename
csv_data = pd.read_csv(csv_path, header=0, parse_dates=[1], date_format="%Y-%m-%d %H:%M")

#csv_data['Datetime'] = pd.to_datetime(csv_data['Epoch'], unit='s', utc=True)
#csv_data['Datetime'] = csv_data['Datetime'].dt.tz_convert('Europe/Berlin')
#print(csv_data)

start_time = datetime.datetime.now() - datetime.timedelta(days=2)
data_lasttwodays = csv_data.loc[csv_data['Time'] >= start_time.strftime("%Y-%m-%d %H:%M")]
#data_lasttwodays = csv_data
mean_hum = data_lasttwodays['Humidity %RH'].mean()
mean_temp = data_lasttwodays['Temperature C'].mean()
print(f"Plotting data from {start_time.strftime('%a %d.%m.%y %H:%M')} until now.")
print(f"Mean humidity    {mean_hum:.2f} %RH")
print(f"Mean temperature {mean_temp:.2f} {degree_sign}C")
#print(data_lasttwodays)
#print(data_lasttwodays.index)

fig, (axes_hum, axes_temp) = plt.subplots(2, 1, sharex=True, figsize=(16,9),
    gridspec_kw={ 'hspace': 0.05, 'left': 0.07, 'right':0.95, 'top':0.95, 'bottom':0.09})

#fig_hum = plt.figure(0)
#axes_hum: matplotlib.axes = data_lasttwodays.plot(1,2)
axes_hum.plot(data_lasttwodays["Time"],data_lasttwodays["Humidity %RH"])
axes_hum.set_ylabel("% Rel. Hum.")
axes_hum.grid(which='both', linestyle='--')


#fig_temp = plt.figure(1)
#axes_temp: matplotlib.axes = data_lasttwodays.plot(1,3, color='green')
axes_temp.plot(data_lasttwodays["Time"],data_lasttwodays["Temperature C"],  color='green')
axes_temp.set_ylabel("Degree Celsius")
axes_temp.set_xlabel("Time")
axes_temp.grid(which='both', linestyle='--')
axes_temp.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%d.%m.%y %H:%M"))

plt.show()
