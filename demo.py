import ee
import folium
import geehydro
import geemap
import os

ee.Authenticate()
ee.Initialize()

# Create a map centered at (lat, lon).
Map = geemap.Map(center=[40, -100], zoom=4)

# This function gets NDVI from Landsat 5 imagery.


def getNDVI(image):
    return image.normalizedDifference(['B4', 'B3'])


# Load two Landsat 5 images, 200 years apart.
image1 = ee.Image('LANDSAT/LT05/C01/T1_TOA/LT05_044034_19900604')
image2 = ee.Image('LANDSAT/LT05/C01/T1_TOA/LT05_044034_20100611')

# Compute NDVI from the scenes.
ndvi1 = getNDVI(image1)
ndvi2 = getNDVI(image2)

# Compute the difference in NDVI.
ndviDifference = ndvi2.subtract(ndvi1)
# Load the land mask from the SRTM DEM.
landMask = ee.Image('CGIAR/SRTM90_V4').mask()

# Update the NDVI difference mask with the land mask.
maskedDifference = ndviDifference.updateMask(landMask)

# Display the masked result.
vizParams = {'min': -0.5, 'max': 0.5,
             'palette': ['FF0000', 'FFFFFF', '0000FF']}
Map.setCenter(-122.2531, 37.6295, 9)
Map.addLayer(maskedDifference, vizParams, 'NDVI difference')

# Display the map.
Map

geemap.ee_search()

# Link: https://developers.google.com/earth-engine/tutorial_global_surface_water_02

import ee 
import geemap

# Create a map centered at (lat, lon).
Map = geemap.Map(center=[40, -100], zoom=4)

###############################
# Asset List
###############################

gsw = ee.Image('JRC/GSW1_1/GlobalSurfaceWater')
occurrence = gsw.select('occurrence')

###############################
# Constants
###############################

VIS_OCCURRENCE = {
  'min':0,
  'max':100,
  'palette': ['red', 'blue']
}
VIS_WATER_MASK = {
  'palette': ['white', 'black']
}

###############################
# Calculations
###############################

# Create a water mask layer, and set the image mask so that non-water areas
# are opaque.
water_mask = occurrence.gt(90).selfMask()

###############################
# Initialize Map Location
###############################

# Uncomment one of the following statements to center the map.
# Map.setCenter(-90.162, 29.8597, 10)   # New Orleans, USA
# Map.setCenter(-114.9774, 31.9254, 10) # Mouth of the Colorado River, Mexico
# Map.setCenter(-111.1871, 37.0963, 11) # Lake Powell, USA
# Map.setCenter(149.412, -35.0789, 11)  # Lake George, Australia
# Map.setCenter(105.26, 11.2134, 9)     # Mekong River Basin, SouthEast Asia
# Map.setCenter(90.6743, 22.7382, 10)   # Meghna River, Bangladesh
# Map.setCenter(81.2714, 16.5079, 11)   # Godavari River Basin Irrigation Project, India
# Map.setCenter(14.7035, 52.0985, 12)   # River Oder, Germany & Poland
# Map.setCenter(-59.1696, -33.8111, 9)  # Buenos Aires, Argentina
Map.setCenter(-74.4557, -8.4289, 11)  # Ucayali River, Peru

###############################
# Map Layers
###############################

Map.addLayer(occurrence.updateMask(occurrence.divide(100)), VIS_OCCURRENCE, "Water Occurrence (1984-2018)")
Map.addLayer(water_mask, VIS_WATER_MASK, '90% occurrence water mask', False)



# Display the map.
Map

