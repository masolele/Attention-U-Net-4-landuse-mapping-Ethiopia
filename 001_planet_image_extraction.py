# Robert Masolele
# Data extraction with GEE API & GEEMAP
# Date: 30-06-2020
"""
 This script extracts and saves PlanetScope data from Google Earth Engine for all years in the
 form of tiles by using the package GEEMAP. The composite are first
 created via GEE python API before being extracted.
 They are then saved in google drive to be used for classification."

Environment:
- Sepal.io (Jupyetr notebook)

Package version:
 - geopandas: 0.10.2
 - Geemap: 0.013.5
 - EE: 0.1.309
"""

# import libraries 
import os
os.chdir("~/users/rmasolele")
from datetime import datetime 
import ee
import geemap

# GEE API  needs to be initialized piror to be used. This opens a webpage in which we need to accept the terms of use of GEE.
ee.Authenticate()
ee.Initialize()


## Create composite from ee API

# import snnpr polygon to clip the image to the SNNPR boundaries
ETH = ee.FeatureCollection("projects/ee-masolele/assets/ETH")

# import the hansen dataset for forest cover loss 
hansen = ee.Image("UMD/hansen/global_forest_change_2020_v1_8")

# create snnpr polygon
ETH = ETH.geometry()


# select the year 2014 of the hansen dataset to be added to each and every one of the created composite. This will be used to highlight the FLU of the year 2014.
gfc2020 = ee.Image('UMD/hansen/global_forest_change_2020_v1_8').clip(snnpr)
treeLoss = gfc2020.select(['loss'])
lossyear2014 = gfc2020.select(['lossyear']).eq(14)
lossyear2014 = lossyear2014.mask(lossyear2014)

## Here, we create a yearly median composite of the bi-annual images (from 2016 to 2020) and the monthly images (2020-2021)

# Select the bi-annual or monthly image, clip it to the SNNPR polygon, and create composite 
# composite 2016
ImageCollection_2016_1 = ee.Image('projects/planet-nicfi/assets/basemaps/africa/planet_medres_normalized_analytic_2015-12_2016-05_mosaic').clip(snnpr)
ImageCollection_2016_2 = ee.Image('projects/planet-nicfi/assets/basemaps/africa/planet_medres_normalized_analytic_2016-06_2016-11_mosaic').clip(snnpr)
collection_planet_2016 = ee.ImageCollection([ImageCollection_2016_1, ImageCollection_2016_2])
composite2016 = collection_planet_2016.median().uint16()
#composite 2017
ImageCollection_2017_1 = ee.Image('projects/planet-nicfi/assets/basemaps/africa/planet_medres_normalized_analytic_2016-12_2017-05_mosaic').clip(snnpr)
ImageCollection_2017_2 = ee.Image('projects/planet-nicfi/assets/basemaps/africa/planet_medres_normalized_analytic_2017-06_2017-11_mosaic').clip(snnpr)
collection_planet_2017 = ee.ImageCollection([ImageCollection_2017_1, ImageCollection_2017_2])
composite2017 = collection_planet_2017.median().uint16()
#Composite 2018
ImageCollection_2018_1 = ee.Image('projects/planet-nicfi/assets/basemaps/africa/planet_medres_normalized_analytic_2017-12_2018-05_mosaic').clip(snnpr)
ImageCollection_2018_2 = ee.Image('projects/planet-nicfi/assets/basemaps/africa/planet_medres_normalized_analytic_2018-06_2018-11_mosaic').clip(snnpr)
collection_planet_2018 = ee.ImageCollection([ImageCollection_2018_1, ImageCollection_2018_2])
composite2018 = collection_planet_2018.median().uint16()
#Composite 2019
ImageCollection_2019_1 = ee.Image('projects/planet-nicfi/assets/basemaps/africa/planet_medres_normalized_analytic_2018-12_2019-05_mosaic').clip(snnpr)
ImageCollection_2019_2 = ee.Image('projects/planet-nicfi/assets/basemaps/africa/planet_medres_normalized_analytic_2019-06_2019-11_mosaic').clip(snnpr)
collection_planet_2019 = ee.ImageCollection([ImageCollection_2019_1, ImageCollection_2019_2])
composite2019 = collection_planet_2019.median().uint16()
#Composite 2020
ImageCollection_2020_1 = ee.Image('projects/planet-nicfi/assets/basemaps/africa/planet_medres_normalized_analytic_2019-12_2020-05_mosaic').clip(snnpr)
ImageCollection_2020_2 = ee.Image('projects/planet-nicfi/assets/basemaps/africa/planet_medres_normalized_analytic_2020-06_2020-08_mosaic').clip(snnpr)
ImageCollection_2020_3 = ee.Image('projects/planet-nicfi/assets/basemaps/africa/planet_medres_normalized_analytic_2020-09_mosaic').clip(snnpr)
ImageCollection_2020_4 = ee.Image('projects/planet-nicfi/assets/basemaps/africa/planet_medres_normalized_analytic_2020-10_mosaic').clip(snnpr)
ImageCollection_2020_5 = ee.Image('projects/planet-nicfi/assets/basemaps/africa/planet_medres_normalized_analytic_2020-11_mosaic').clip(snnpr)
collection_planet_2020 = ee.ImageCollection([ImageCollection_2020_1, ImageCollection_2020_2,
                                             ImageCollection_2020_3, ImageCollection_2020_4, ImageCollection_2020_5])
composite2020 = collection_planet_2020.median().uint16()
# Composite 2021
ImageCollection_2021_1 = ee.Image('projects/planet-nicfi/assets/basemaps/africa/planet_medres_normalized_analytic_2020-12_mosaic').clip(snnpr)
ImageCollection_2021_2 = ee.Image('projects/planet-nicfi/assets/basemaps/africa/planet_medres_normalized_analytic_2021-01_mosaic').clip(snnpr)
ImageCollection_2021_3 = ee.Image('projects/planet-nicfi/assets/basemaps/africa/planet_medres_normalized_analytic_2021-02_mosaic').clip(snnpr)
ImageCollection_2021_4 = ee.Image('projects/planet-nicfi/assets/basemaps/africa/planet_medres_normalized_analytic_2021-03_mosaic').clip(snnpr)
ImageCollection_2021_5 = ee.Image('projects/planet-nicfi/assets/basemaps/africa/planet_medres_normalized_analytic_2021-04_mosaic').clip(snnpr)
ImageCollection_2021_6 = ee.Image('projects/planet-nicfi/assets/basemaps/africa/planet_medres_normalized_analytic_2021-05_mosaic').clip(snnpr)
ImageCollection_2021_7 = ee.Image('projects/planet-nicfi/assets/basemaps/africa/planet_medres_normalized_analytic_2021-06_mosaic').clip(snnpr)
ImageCollection_2021_8 = ee.Image('projects/planet-nicfi/assets/basemaps/africa/planet_medres_normalized_analytic_2021-07_mosaic').clip(snnpr)
ImageCollection_2021_9 = ee.Image('projects/planet-nicfi/assets/basemaps/africa/planet_medres_normalized_analytic_2021-08_mosaic').clip(snnpr)
ImageCollection_2021_10 = ee.Image('projects/planet-nicfi/assets/basemaps/africa/planet_medres_normalized_analytic_2021-09_mosaic').clip(snnpr)
ImageCollection_2021_11 = ee.Image('projects/planet-nicfi/assets/basemaps/africa/planet_medres_normalized_analytic_2021-10_mosaic').clip(snnpr)
ImageCollection_2021_12 = ee.Image('projects/planet-nicfi/assets/basemaps/africa/planet_medres_normalized_analytic_2021-11_mosaic').clip(snnpr)
collection_planet_2021 = ee.ImageCollection([ImageCollection_2021_1, ImageCollection_2021_2, ImageCollection_2021_3, ImageCollection_2021_4, ImageCollection_2021_5, 
                                             ImageCollection_2021_6, ImageCollection_2021_7, ImageCollection_2021_8, 
                                             ImageCollection_2021_9, ImageCollection_2021_10, ImageCollection_2021_11, ImageCollection_2021_12])
composite2021 = collection_planet_2021.median().uint16()

#1st semester composite to match the bi -annual image (2016-2020)
composite2021_1st_semester = ee.ImageCollection([ImageCollection_2021_1, ImageCollection_2021_2, ImageCollection_2021_3, ImageCollection_2021_4, ImageCollection_2021_5, ImageCollection_2021_6])
composite2021_1st_semester = composite2021_1st_semester.median().uint16()



#Here we add the 2014 forest cover loss to highlight the FLU after classification
#For the yearly composite
FinalIMG2016 = composite2016.addBands(lossyear2014).uint16()
FinalIMG2017 = composite2017.addBands(lossyear2014).uint16()
FinalIMG2018 = composite2018.addBands(lossyear2014).uint16()
FinalIMG2019 = composite2019.addBands(lossyear2014).uint16()
FinalIMG2020 = composite2020.addBands(lossyear2014).uint16()
FinalIMG2021 = composite2021.addBands(lossyear2014).uint16()
#for the 1st semester composite
img2016_01 = ImageCollection_2016_1.addBands(lossyear2014).uint16();
img2017_01 =ImageCollection_2017_1.addBands(lossyear2014).uint16();
img2018_01 =ImageCollection_2018_1.addBands(lossyear2014).uint16();
img2019_01 =ImageCollection_2019_1.addBands(lossyear2014).uint16();
img2020_01 =ImageCollection_2020_1.addBands(lossyear2014).uint16();
img2021_01 =composite2021_1st_semester.addBands(lossyear2014).uint16();



##### Data extraction per tiles over Ethiopia area


import geopandas as gpd


#sample tiles corresponding to forest loss locations . Used to extract image grom GEE
roi_samples = '~/users/rmasolele/equal_area_eth/forest_loss_tiles_samples_locations.shp'

#convert shapefile to earthengine feature
roi = geemap.shp_to_ee(roi_samples) #to change if you want to use sample tiles or all tiles

#Max bytes to export per tile/patch  must be less than or equal to 33 554 432 bytes.  


start2 = datetime.now()


# function to extract each tiles coordinates 
featlist = roi.getInfo()['features']
print(len(featlist))
def unpack(thelist):
    unpacked = []
    for i in thelist:
        unpacked.append(i[0])
        unpacked.append(i[1])
    return unpacked

# extract the image of each tile by using GEEMAP package
def tile(image, featlist, year=0, filename1=0):
  filee='~/users/rmasolele/planet_'+str(year)
  if os.path.exists(filee):
    print(filee + " already created")
  else:
    os.mkdir(filee)
  for f in featlist:
    geomlist = None
    geomlist = unpack(f["geometry"]["coordinates"][0])
    year = str(year)
    feat = ee.Geometry.Polygon(geomlist)
    disS = f["properties"]["POLY_ID"]
    filename1='~/users/rmasolele/planet_'+year+'/ETH'+str(disS)+'.tif'
    if os.path.exists(filename1):
        print(filename1 + ' already downloaded')
    else:
        print('downloading '+ str(disS))
        geemap.ee_export_image(image,
                           filename= filename1,
                           scale=5,
                           region=feat.bounds(),
                           file_per_band=False)

#Yearly composite image extraction
#2016
tile(FinalIMG2016, featlist=featlist, year=2016)
#2017
tile(FinalIMG2017, featlist=featlist, year=2017)
#2018
tile(FinalIMG2018, featlist=featlist, year=2018)
#2019
tile(FinalIMG2019, featlist=featlist, year=2019)
#2020
tile(FinalIMG2020, featlist=featlist, year=2020)
#2021
tile(FinalIMG2021, featlist=featlist, year=2021)

# Six month image extaraction
#2016
tile(img2016_01, featlist=featlist, year=2016)
#2017
tile(img2017_01, featlist=featlist, year=2017)
#2018
tile(img2018_01, featlist=featlist, year=2018)
#2019
tile(img2019_01, featlist=featlist, year=2019)
#2020
tile(img2020_01, featlist=featlist, year=2020)
#2021
tile(img2021_01, featlist=featlist, year=2021)

stop2 = datetime.now()
#Execution time 
execution_time_download = stop2-start2
print("data download execution time is: ", execution_time_download)

