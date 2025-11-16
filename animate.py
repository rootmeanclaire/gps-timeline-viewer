from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.animation import FuncAnimation
from PIL import Image


X_KEY = "Longitude"
Y_KEY = "Latitude"
ZOOM_START = datetime.strptime("0:55:26", "%H:%M:%S")
ZOOM_END = datetime.strptime("01:08:43", "%H:%M:%S")
SPEED_MULTIPLIER = 10
LINE_COLOR = "red"


def set_bounds(ax, x, y, xslack=0.1, yslack=0.1):
	xmin = min(x)
	xmax = max(x)
	xrange = xmax - xmin
	ymin = min(y)
	ymax = max(y)
	yrange = ymax - ymin

	left = xmin - xrange*xslack
	right = xmax + xrange*xslack
	bottom = ymin - yrange*yslack
	top = ymax + yrange*yslack

	ax.set(
		xlim=[left, right], ylim=[bottom, top],
		xlabel=X_KEY, ylabel=Y_KEY
	)
	print(f"X-axis bound set to {left}, {right}")
	print(f"Y-axis bound set to {bottom}, {top}")

	return [left, right, bottom, top]


def make_animation(df: pd.DataFrame):
	# Initialize canvas
	fig = plt.figure(figsize=(9, 16), dpi=96)
	gs = gridspec.GridSpec(2, 1, height_ratios=[1, 2])
	ax1 = plt.subplot(gs[0])
	ax2 = plt.subplot(gs[1])
	ax1.ticklabel_format(style="plain", useOffset=False)
	ax2.ticklabel_format(style="plain", useOffset=False)
	zoom_idx = (df["Time"] >= ZOOM_START) & (df["Time"] <= ZOOM_END) & (df["Walking"])
	# Full Bounds
	ex1 = set_bounds(ax1, df[X_KEY], df[Y_KEY])
	ex2 = set_bounds(ax2, df[X_KEY][zoom_idx], df[Y_KEY][zoom_idx], xslack=5, yslack=3)
	bg1 = Image.open("bg1.png")
	bg2 = Image.open("bg2v2.png")
	ax1.imshow(bg1, extent=ex1)
	ax2.imshow(bg2, extent=[-117.858987 - ((-117.858987) - (-117.860776)) * (1234/781), -117.858987, 33.641766, 33.645278])
	# Animation objects
	title1 = ax1.set_title(df["Time"][0])
	title2 = ax2.set_title(df["Time"][0])
	path1 = ax1.plot(
		df[X_KEY][0], df[Y_KEY][0],
		linewidth=2, color=LINE_COLOR
	)[0]
	path2 = ax2.plot(
		df[X_KEY][0], df[Y_KEY][0],
		linewidth=1, color=LINE_COLOR
	)[0]
	# Animation procedure
	def frame(idx):
		title1.set_text(df["Time"][idx])
		title2.set_text(df["Time"][idx])
		path1.set_xdata(df[X_KEY][:idx])
		path1.set_ydata(df[Y_KEY][:idx])
		path2.set_xdata(df[X_KEY][:idx])
		path2.set_ydata(df[Y_KEY][:idx])
		return (path1, path2)
	return FuncAnimation(fig, frame, frames=len(df), interval=1000/SPEED_MULTIPLIER)
