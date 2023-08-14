import fastf1 as ff1
import numpy as np
import matplotlib as mpl

from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection

import os

schedule = ff1.get_event_schedule(2022)

for round in range(1,schedule.shape[0]):
	print(schedule.iloc[round][:])
	session = ff1.get_event(schedule['EventDate'][round].year,schedule['OfficialEventName'][round])

	session = ff1.get_session(schedule['EventDate'][round].year,session['EventName'],"Q")
	weekend = round
	session.load()
	ses = 'Q'
	year=schedule['EventDate'][0].year
	path = f'Speed/{year}/{weekend}/{ses}/'
	
	if not os.path.exists(path):
		os.makedirs(path)
		print("Folder %s created!" % path)
	else:
		print("Folder %s already exists" % path)

	
	lap_fast = session.laps.pick_fastest()
	driver_fast = lap_fast.Driver


	# Get telemetry data
	x = lap_fast.telemetry['X']              # values for x-axis
	y = lap_fast.telemetry['Y']              # values for y-axis
	color_fast = lap_fast.telemetry['Speed']      # value to base color gradient on
	points = np.array([x, y]).T.reshape(-1, 1, 2)
	segments = np.concatenate([points[:-1], points[1:]], axis=1)
	las = session.drivers
	las.remove(lap_fast.DriverNumber)

	colormap = mpl.colormaps['Reds']

	for i,driver in enumerate(las):
		try:
			fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(12, 6.75))

			lap = session.laps.pick_driver(las[i])

			driver = session.get_driver(las[i])['Abbreviation']
		
			color = np.subtract(color_fast,lap.pick_fastest().telemetry["Speed"])

			fig.suptitle(f'{session.event.OfficialEventName} \n {driver_fast} vs {driver}', size=24, y=0.97)

			# Adjust margins and turn of axis
			plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)
			ax.axis('off')


			# After this, we plot the data itself.
			# Create background track line
			ax.plot(lap_fast.telemetry['X'], lap_fast.telemetry['Y'], color='black', linestyle='-', linewidth=16, zorder=0)

			# Create a continuous norm to map from data points to colors
			norm = plt.Normalize(color.min(), color.max())
			lc = LineCollection(segments, cmap=colormap, norm=norm, linestyle='-', linewidth=5)

			# Set the values used for colormapping
			lc.set_array(color)

			# Merge all line segments together
			line = ax.add_collection(lc)


			# Finally, we create a color bar as a legend.
			cbaxes = fig.add_axes([0.25, 0.05, 0.5, 0.05])
			normlegend = mpl.colors.Normalize(vmin=color.min(), vmax=color.max())
			legend = mpl.colorbar.ColorbarBase(cbaxes, norm=normlegend, cmap=colormap, orientation="horizontal")

			plt.savefig(f'{path}/{driver_fast} vs {driver}.png')
			print(f'{path}/{driver_fast} vs {driver}.png')
			# Show the plot
			#plt.show()
		except:
			print(f'{path}/{driver_fast} vs {driver}.png - > Not Usefull')
