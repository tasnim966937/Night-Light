#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import ee
import geemap
from geemap import cartoee


# In[36]:


import matplotlib.pyplot as plt


# In[ ]:


import matplotlib.pyplot as plt


# In[2]:


Map = geemap.Map()
Map


# In[29]:


lon = 91
lat = 22.942
start_year = 1992
end_year = 2014


# In[8]:


point = ee.Geometry.Point(lon, lat)
years = ee.List.sequence(start_year, end_year)


def get_best_image(year):

    start_date = ee.Date.fromYMD(year, 1, 1)
    end_date = ee.Date.fromYMD(year, 12, 31)
    image = (
        ee.ImageCollection("NOAA/DMSP-OLS/NIGHTTIME_LIGHTS")
        .filterBounds(point)
        .filterDate(start_date, end_date)
        .sort("CLOUD_COVER")
        .first()
    )
    return ee.Image(image)
collection = ee.ImageCollection(years.map(get_best_image))


# In[9]:


vis_params = {
    "bands": ['stable_lights'],
    "min": 0,
    "max": 63,
    "palette": ['black', 'goldenrod', 'yellow', 'orange']
}


# In[51]:


image = ee.Image(collection.first())
Map.addLayer(image, vis_params, 'First image')
Map.setCenter(lon, lat, 0.1)
Map

w = 3
h = 3

region = [lon + 2, lat - 2, lon - 4, lat + h]

fig = plt.figure(figsize=(16, 12))


# In[52]:


# use cartoee to get a map
ax = cartoee.get_map(image, region=region, vis_params=vis_params)


# In[53]:


# add north arrow
north_arrow_dict = {
    "text": "N",
    "xy": (0.1, 0.3),
    "arrow_length": 0.15,
    "text_color": "white",
    "arrow_color": "white",
    "fontsize": 20,
    "width": 5,
    "headwidth": 15,
    "ha": "center",
    "va": "center",
}
cartoee.add_north_arrow(ax, **north_arrow_dict)


# In[55]:


# add scale bar
scale_bar_dict = {
    "length": 10,
    "xy": (0.1, 0.05),
    "linewidth": 3,
    "fontsize": 20,
    "color": "white",
    "unit": "km",
    "ha": "center",
    "va": "bottom",
}
cartoee.add_scale_bar_lite(ax, **scale_bar_dict)

plt.show()


# In[58]:


cartoee.get_image_collection_gif(
    ee_ic=collection,
    out_dir = os.path.expanduser("C:\\Users\\alamm\\Desktop\\Night_life"),
    out_gif="animation2.gif",
    vis_params=vis_params,
    region=region,
    fps=2,
    mp4=True,
    grid_interval=(0.6, 0.6),
    plot_title="Night Light of Bangladesh",
    date_format='YYYY-MM-dd',
    fig_size=(10, 8),
    dpi_plot=1200,
    file_format="png",
    north_arrow_dict=north_arrow_dict,
    scale_bar_dict=scale_bar_dict,
    verbose=True,
)


# In[ ]:




