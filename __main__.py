#!/usr/bin/env python3
from sys import argv, stderr
import matplotlib.pyplot as plt
# Local modules
from parse import load_csv
from animate import make_animation


def parse_args():
	if len(argv) < 2:
		print("Expected an input CSV file as an argument", file=stderr)
		exit(1)
	return load_csv(argv[1])


def main():
	df = parse_args()
	print(df)
	anim = make_animation(df)
	print("Displaying animation...")
	plt.show()
	print("Done!")
	print("Saving animation to file...")
	anim.save("output.mp4")
	print("Done!")


if __name__ == "__main__":
	main()
