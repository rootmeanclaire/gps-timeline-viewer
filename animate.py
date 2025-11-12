from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


ZOOM_START = datetime.strptime("0:55:26", "%H:%M:%S")
ZOOM_END = datetime.strptime("01:08:43", "%H:%M:%S")


def set_bounds(ax, x, y):
	xmin = min(x)
	xmax = max(x)
	xrange = xmax - xmin
	ymin = min(y)
	ymax = max(y)
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


def make_animation(df: pd.DataFrame):
	# Initialize canvas
	fig = plt.figure(figsize=(12, 5))
	ax1 = plt.subplot(1, 2, 1)
	ax2 = plt.subplot(1, 2, 2)
	zoom_idx = (df["Time"] >= ZOOM_START) & (df["Time"] <= ZOOM_END) & (df["Walking"])
	print(ZOOM_START)
	print(ZOOM_END)
	print(zoom_idx)
	# Full Bounds
	set_bounds(ax1, df["Latitude"], df["Longitude"])
	set_bounds(ax2,
		df["Latitude"][zoom_idx],
		df["Longitude"][zoom_idx]
	)
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
	return FuncAnimation(fig, frame, frames=len(df), interval=20)
