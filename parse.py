from sys import stderr
import pandas as pd


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
