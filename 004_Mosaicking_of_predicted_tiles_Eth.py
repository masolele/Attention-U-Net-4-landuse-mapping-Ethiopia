# Robert Masolele
# Mosaicking
# Date: 30-06-2020
"""
This script creates a mosaic of all the predicted planet-NICFI tiles for Ethiopia.

Environment:
- Sepal.io (Jupyetr notebook)

Package version:
 - gdal: 2.2.3

"""
import numpy as np
import matplotlib.pyplot as plt
import subprocess, glob
from osgeo import gdal                 
#https://gdal.org/programs/gdalwarp.html

def mosaicing(year):
  year = str(year)
  start2 = datetime.now() 
  predgeoref = "~/users/rmasolele/planet"+year+"/pred"+year+"/ETH*georef.tif"
  # gather all classified and georeferenced tiles
  files_to_mosaic = glob.glob(predgeoref)
  #mosaic them together
  g = gdal.Warp("~/users/rmasolele/mosaic/ETHmosaic_"+year+".tif", files_to_mosaic, format="GTiff",
              options=["COMPRESS=LZW", "TILED=YES"]) 
  g = None    
  stop2 = datetime.now()
#Execution time of the model 
  execution_time_mosaic = stop2-start2
  print("execution time mosaic is: ", execution_time_mosaic)

years= [2016, 2017, 2018, 2019, 2020, 2021]


# mosaicing for all years
for i in years:
  mosaicing(i)
