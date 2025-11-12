#!/usr/bin/env python3
from sys import argv, stderr
import pandas as pd


def parse_args():
	err = False
	if len(argv) < 2:
		print("Expected an input CSV file as an argument", file=stderr)
		exit(1)
	# Load file
	print("Loading CSV file...")
	df = pd.read_csv(argv[1], parse_dates=[0], date_format="%H:%M:%S")
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


def main():
	print(parse_args())


if __name__ == "__main__":
	main()
