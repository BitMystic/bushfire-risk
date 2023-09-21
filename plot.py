import matplotlib.animation as animation
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeat

from datetime import datetime
import pandas as pd
import glob
import os

dir = os.getcwd() + "/data/download/*"
paths = glob.glob(dir)

#collecting datasets when looping over your files
list_da = []

for path in paths:
    da = xr.open_dataset(path)

    list_da.append(da)

#stack dataarrays in list
ds = xr.combine_by_coords(list_da).to_array()

def make_figure():
    fig = plt.figure(figsize=(8, 3))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

    # generate a basemap with country borders, oceans and coastlines
    ax.add_feature(cfeat.LAND)
    ax.add_feature(cfeat.OCEAN)
    ax.add_feature(cfeat.COASTLINE)
    ax.add_feature(cfeat.BORDERS, linestyle='dotted')
    return fig, ax



fig, ax = make_figure()

frames = ds.time.size        # Number of frames
min_value = ds.min(skipna=True)  # Lowest value
max_value = ds.max(skipna=True)  # Highest value
print(min_value, max_value)
def draw(frame, add_colorbar):
    grid = ds.isel(time=frame)
    contour = grid.plot(ax=ax, transform=ccrs.PlateCarree(), add_colorbar=add_colorbar, vmin=min_value, vmax=max_value)
    title = f'some title {frame}' 
    ax.set_title(title)
    return contour


def init():
    return draw(0, add_colorbar=True)


def animate(frame):
    return draw(frame, add_colorbar=False)


ani = animation.FuncAnimation(fig, animate, frames, interval=0.1, blit=False,
                              init_func=init, repeat=False)
ani.save('images/temp.mp4', writer=animation.FFMpegWriter(fps=2))
plt.close(fig)
