import os
import sys
import datetime
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.dates



def main(csv_path: str):
    """Generates a plot with the data of the last two days and saves it as png file.

    Args:
        csv_path (str): full path of the csv input file

    Csv input file format must be like this:
    ```
    Epoch,Time,Humidity %RH,Temperature C
    1749823801.0,2025-06-13 16:10,25.1,22.6
    ```
    """
    start_time = datetime.datetime.now() - datetime.timedelta(days=2)

    csv_data = pd.read_csv(csv_path, header=0, parse_dates=[1], date_format="%Y-%m-%d %H:%M")
    data_lasttwodays = csv_data.loc[csv_data['Time'] >= start_time.strftime("%Y-%m-%d %H:%M")]

    fig, (axes_hum, axes_temp) = plt.subplots(2, 1, sharex=True, figsize=(16,9),
            gridspec_kw={ 'hspace': 0.05, 'left': 0.07, 'right':0.95, 'top':0.95, 'bottom':0.09})


    axes_hum.plot(data_lasttwodays["Time"],data_lasttwodays["Humidity %RH"])
    axes_hum.set_ylabel("% Rel. Hum.")
    axes_hum.grid(which='both', linestyle='--')

    axes_temp.plot(data_lasttwodays["Time"],data_lasttwodays["Temperature C"],  color='green')
    axes_temp.set_ylabel("Degree Celsius")
    axes_temp.set_xlabel("Time")
    axes_temp.grid(which='both', linestyle='--')
    axes_temp.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%d.%m.%y %H:%M"))

    png_filename = "env_data.png"
    png_path = os.path.join(os.path.dirname(csv_path), png_filename)
    #print(png_path)
    fig.savefig(png_path)


if __name__ == "__main__":
    csv_filename = sys.argv[1] if len(sys.argv) > 1 else ""
    if not csv_filename:
        print("No csv file specified.")
        sys.exit()

    csv_fullpath = os.path.abspath(csv_filename)

    main(csv_fullpath)
