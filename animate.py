from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from PIL import Image


ZOOM_START = datetime.strptime("0:55:26", "%H:%M:%S")
ZOOM_END = datetime.strptime("01:08:43", "%H:%M:%S")
SPEED_MULTIPLIER = 10


def set_bounds(ax, x, y):
	xmin = min(x)
	xmax = max(x)
	xrange = xmax - xmin
	ymin = min(y)
	ymax = max(y)
	yrange = ymax - ymin

	left = xmin - xrange*0.1
	right = xmax + xrange*0.1
	bottom = ymin - yrange*0.1
	top = ymax + yrange*0.1

	ax.set(
		xlim=[left, right], ylim=[bottom, top],
		xlabel="Latitude", ylabel="Longitude"
	)
	print(f"X-axis bound set to {left}, {right}")
	print(f"Y-axis bound set to {bottom}, {top}")

	return [left, right, bottom, top]


def make_animation(df: pd.DataFrame):
	# Initialize canvas
	fig = plt.figure(figsize=(12, 6), dpi=96)
	ax1 = plt.subplot(1, 2, 1)
	ax2 = plt.subplot(1, 2, 2)
	ax1.ticklabel_format(style="plain", useOffset=False)
	ax2.ticklabel_format(style="plain", useOffset=False)
	zoom_idx = (df["Time"] >= ZOOM_START) & (df["Time"] <= ZOOM_END) & (df["Walking"])
	# Full Bounds
	ex1 = set_bounds(ax1, df["Latitude"], df["Longitude"])
	ex2 = set_bounds(ax2,
		df["Latitude"][zoom_idx],
		df["Longitude"][zoom_idx]
	)
	bg1 = Image.open("bg1.png")
	bg2 = Image.open("bg2.png")
	ax1.imshow(bg1, extent=ex1, aspect="equal")
	ax2.imshow(bg2, extent=ex2, aspect="equal")
	ax1.set_aspect(bg1.size[1]/bg1.size[0])
	ax2.set_aspect(bg2.size[1]/bg2.size[0])
	# Animation objects
	title1 = ax1.set_title(df["Time"][0])
	title2 = ax2.set_title(df["Time"][0])
	path1 = ax1.plot(df["Latitude"][0], df["Longitude"][0])[0]
	path2 = ax2.plot(df["Latitude"][0], df["Longitude"][0])[0]
	# Animation procedure
	def frame(idx):
		title1.set_text(df["Time"][idx])
		title2.set_text(df["Time"][idx])
		path1.set_xdata(df["Latitude"][:idx])
		path1.set_ydata(df["Longitude"][:idx])
		path2.set_xdata(df["Latitude"][:idx])
		path2.set_ydata(df["Longitude"][:idx])
		return (path1, path2)
	return FuncAnimation(fig, frame, frames=len(df), interval=1000/SPEED_MULTIPLIER)
