import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

selected_driver_id = 4
# Load the datasets and drop unnecessary columns
races = pd.read_csv('F1_datasets/races.csv').drop(columns=['year','round','circuitId','time','url','fp1_date','fp1_time','fp2_date','fp2_time','fp3_date','fp3_time','quali_date','quali_time','sprint_date','sprint_time'])
results = pd.read_csv('F1_datasets/results.csv').drop(columns=['number','grid','positionText','positionOrder','points','laps','time','milliseconds','fastestLap','rank','fastestLapTime','fastestLapSpeed'])

# Merge the datasets on 'raceId' and sort
results = results.join(races.set_index('raceId'), on='raceId', how='left').sort_values(by=['date','position'])

# Get list of 
selected_driver_raceId_list = results[results['driverId'] == selected_driver_id]['raceId'].unique()
results = results[results['raceId'].isin(selected_driver_raceId_list)]
results['position'] = pd.to_numeric(results['position'], errors='coerce')
selected_driver_team_by_race = results[results['driverId'] == selected_driver_id][['raceId', 'constructorId']]

teammate_results = results.merge(selected_driver_team_by_race, on=['raceId','constructorId'])
teammate_results = teammate_results[teammate_results['driverId'] != selected_driver_id]

# Plot the results of the selected driver
plt.figure(figsize=(12, 6))
plt.plot(pd.to_datetime(results[results['driverId'] == selected_driver_id]['date']),results[results['driverId'] == selected_driver_id]['position'], marker='o', linestyle='', color='b', label='Position')
plt.plot(pd.to_datetime(results[results['driverId'] == selected_driver_id]['date']),teammate_results['position'], marker='o', linestyle='', color='r', label='Position')
plt.title("Driver")
plt.xlabel("Date")
plt.ylabel("Position")
plt.xticks(rotation=45)
plt.yticks(np.arange(1, 21))  # Assuming max 22 positions
plt.gca().invert_yaxis()  # Invert y-axis to show 1st position at the top
plt.grid()
plt.legend()
plt.tight_layout()
plt.show()