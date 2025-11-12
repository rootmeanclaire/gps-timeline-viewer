from sys import stderr
import numpy as np
import pandas as pd
from pymap3d import geodetic2enu


def load_csv(filename):
	err = False
	print("Loading CSV file...")
	df = pd.read_csv(filename, parse_dates=[0], date_format="%H:%M:%S")
	# Check input file format
	# Check number of columns
	if len(df.columns) < 3:
		print(f"Expected at least 3 columns in CSV file, got {len(df.columns)}", file=stderr)
		err = True
	# Check names of columns
	columns = ["Time", "Latitude", "Longitude"]
	for i, colname in enumerate(columns):
		if df.columns[0] != "Time":
			print(f"Expected column {i+1} to be \"{colname}\", got \"{df.columns[i]}\"", file=stderr)
			err = True
	if err:
		exit(1)
	print("Done!")
	# Normalize for speed calculation
	ref_lat = np.median(df["Latitude"])
	ref_lon = np.median(df["Longitude"])
	east = np.zeros_like(df["Latitude"])
	north = np.zeros_like(df["Latitude"])
	speed = np.zeros_like(df["Latitude"])
	for i in range(len(df)):
		east[i], north[i], _ = geodetic2enu(
			df["Latitude"][i], df["Longitude"][i], 0,
			ref_lat, ref_lon, 0
		)
		if i > 0:
			dt = df["Time"][i] - df["Time"][i-1]
			speed[i] = np.sqrt(
				((east[i] - east[i-1]) ** 2) +
				((north[i] - north[i-1]) ** 2)
			) / dt.total_seconds()
	df.insert(3, "East", east)
	df.insert(4, "North", north)
	df.insert(5, "Speed (m/s)", speed)
	df.insert(6, "Walking", speed < 3)
	return df
