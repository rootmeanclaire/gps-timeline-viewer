#!/usr/bin/env python3
from sys import argv, stderr
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def parse_args():
	if len(argv) < 2:
		print("Expected an input CSV file as an argument", file=stderr)
		exit(1)
	return load_csv(argv[1])

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
	return df


def make_animation(df: pd.DataFrame):
	# Initialize canvas
	fig, ax = plt.subplots()
	# Bounds
	xmin = min(df["Latitude"])
	xmax = max(df["Latitude"])
	xrange = xmax - xmin
	ymin = min(df["Longitude"])
	ymax = max(df["Longitude"])
	yrange = ymax - ymin
	ax.set(
		xlim=[
			xmin - xrange*0.1,
			xmax + xrange*0.1
		],
		ylim=[
			ymin - yrange*0.1,
			ymax + yrange*0.1
		],
		xlabel="Latitude",
		ylabel="Longitude"
	)
	# Animation objects
	title = ax.set_title(df["Time"][0])
	path = ax.plot(df["Latitude"][0], df["Longitude"][0])[0]
	# Animation procedure
	def frame(idx):
		title.set_text(df["Time"][idx])
		path.set_xdata(df["Latitude"][:idx])
		path.set_ydata(df["Longitude"][:idx])
		return path
	return FuncAnimation(fig, frame, frames=len(df), interval=20)


def main():
	df = parse_args()
	print(df)
	anim = make_animation(df)
	print("Displaying animation...")
	plt.show()
	print("Done!")


if __name__ == "__main__":
	main()
