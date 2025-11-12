import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


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
