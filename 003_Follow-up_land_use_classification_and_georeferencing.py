# Robert MASOLELE
# Direct driver prediction & georeferecning
# script written by R.N. Masolele
# Date: 30-06-2020

"""
This script classify, histogram match, and georeference the extracted data from 001 with the deep learning model developped by R.N. Masolele. 

Environment:
- Sepal.io (Jupyetr notebook)

Package version:
 - rasterio: 1.2.10
 - keras: 2.8.0
 - cv2: 4.1.2
 - numpy: 1.21.6
 - skimage: 0.18.3
 - matplotlib: 3.2.2
 - tqdm: 4.64.0
 - PIL: 7.1.2
 - sklearn: 1.0.2
"""


#PREDICTION FOR EACH tile
import rasterio
import os
from keras.models import load_model
import cv2
import numpy as np
from skimage import io
from matplotlib import pyplot as plt
from tqdm import tqdm_notebook, tnrange
from PIL import Image
from tensorflow.keras.utils import normalize
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime
scaler = MinMaxScaler()
from 002_Smooth_tiled_predictions import predict_img_with_smooth_windowing

from keras.models import load_model

os.chdir("~/users/rmasolele")

#prepare data to  be classified
def preprocess_planet(x_img):
  # compile
  x_img = x_img[:,:,[0,1,2,3]] 
  SIZE_X = (x_img.shape[0])
  SIZE_Y = (x_img.shape[1])
  nir = x_img[:,:,3]
  red = x_img[:,:,2]
  green = x_img[:,:,1]
  blue = x_img[:,:,0]
  ndvi = np.where((nir+red)==0., 0, (nir-red)/(nir+red))
  savi = np.where((nir+red)==0., 0, (nir-red)/(nir+red+0.5))*(1.5)
  ndwi = np.where((nir+red)==0., 0, (green-nir)/(green+nir))
  ndvi = np.reshape(ndvi, (SIZE_X,SIZE_Y,1))
  savi = np.reshape(savi, (SIZE_X,SIZE_Y,1))
  ndwi = np.reshape(ndwi, (SIZE_X,SIZE_Y,1))
  image = np.concatenate((x_img, ndvi, savi, ndwi), axis=2)
  image = normalize(image, axis=1)
  return image

#histogram match of the input tile to the ref tile. Make sure to have downloaded the reference tile beforehand
def hist_matching_preprocess(reference, target):
  import matplotlib.pyplot as plt
  import cv2
  from skimage import data
  from skimage import exposure
  from skimage.exposure import match_histograms
  reference = preprocess_planet(reference)
  target = preprocess_planet(target)
  print(reference.shape)
  print(target.shape)
  #Take only the seven bands to exclude forest cover loss data
  x_img11 = reference[:,:,:7]
  x_img22 = target[:,:,:7]
  #Match the image to ref
  x_img12M = match_histograms(x_img22, x_img11, multichannel = True)
  return x_img12M

def pred(root_directory, path_to_ref, year):
  year=str(year)
  img_dir=root_directory+"planet"+year+"/"
  ETHPRED = img_dir+"pred"+year+"/"
  if os.path.exists(img_dir):
    print(img_dir+ " already created")
  else:
   os.mkdir(img_dir)
  if os.path.exists(ETHPRED):
    print(ETHPRED+ " already created")
  else:
    os.mkdir(ETHPRED)
  scaler = MinMaxScaler()
  #load model
  att_unet_model = load_model("~/users/rmasolele/model/Att_unet_2Dplanet_model_Ethiopia.hdf5", compile=False)
  # size of patches
  patch_size = 128
  # Number of classes 
  n_classes = 11
  start2 = datetime.now() 

  for path, subdirs, files in os.walk(img_dir):
  #    print(path)  
      dirname = path.split(os.path.sep)[-1]
  #    print(dirname)
      images = os.listdir(path)  #List of all image names in this subdirectory

      for i, image_name in tqdm_notebook(enumerate(images), total=len(images)):
        filename1=ETHPRED+image_name[:-4]+'_georef.tif'  
        if os.path.exists(filename1) or image_name.endswith("_georef.tif"):
            print(filename1 + ' already predicted')
        else:
            if image_name.endswith(".tif"):
              image_name2=image_name[:-4]
              print(image_name2)
              path_to_ref1 = path_to_ref+image_name
              print(image_name)
              print(path_to_ref1)
              x_img = io.imread(path+"/"+image_name) #Read each image
              x_img_reference = io.imread(path_to_ref1) #read target reference image for histogram matching
              #extract hansen forest loss band 5
              Loss = x_img[:,:,4] 
              x_img = preprocess_planet(x_img)
              ########## preprocessing
              # x_img = hist_matching_preprocess(x_img_reference, x_img)
              ########
              #Extract image for prediction band 1 to 4
  #            print(x_img.shape)

              #print(x_img.shape)
              ############################################################################32 patch size ###############################################################################
              # Use the algorithm. The `pred_func` is passed and will process all the image 8-fold by tiling small patches with overlap, called once with all those image as a batch outer dimension.
              # Note that model.predict(...) accepts a 4D tensor of shape (batch, x, y, nb_channels), such as a Keras model.
              # predict using smooth blending
              predictions_smooth = predict_img_with_smooth_windowing(
                  x_img,
                  window_size=patch_size,
                  subdivisions=2,  # Minimal amount of overlap for windowing. Must be an even number.
                  nb_classes=n_classes,
                  pred_func=(
                      lambda img_batch_subdiv: att_unet_model.predict((img_batch_subdiv))
                  )
              )

              final_prediction = np.argmax(predictions_smooth, axis=2)
              
              final_prediction = np.where(final_prediction==10, 11, final_prediction)
              final_prediction = np.where(final_prediction==9, 10, final_prediction)
              final_prediction = np.where(final_prediction==8, 9, final_prediction)
              final_prediction = np.where(final_prediction==7, 8, final_prediction)
              final_prediction = np.where(final_prediction==6, 7, final_prediction)
              final_prediction = np.where(final_prediction==5, 6, final_prediction)
              final_prediction = np.where(final_prediction==4, 5, final_prediction)
              final_prediction = np.where(final_prediction==3, 4, final_prediction)
              final_prediction = np.where(final_prediction==2, 3, final_prediction)
              final_prediction = np.where(final_prediction==1, 2, final_prediction)
              final_prediction = np.where(final_prediction==0, 1, final_prediction)
                      

              #Mask predicted non forest loss areas
              final_prediction = np.where(Loss==0, np.nan, final_prediction)
              # data_type = final_prediction.dtype
              # print(data_type)
              # final_prediction = final_prediction.astype('uint16')
              # data_type = final_prediction.dtype
              # print(data_type)



              #georeferencing
              path_to_img_pred = ETHPRED+image_name2+".tif"
              cv2.imwrite(path_to_img_pred, final_prediction)
              # raster = gdal.Open(path+image_name)
              # array2raster(image_name2+'PRED_GEOREF.tif', raster, final_prediction, "uint16")
              a = rasterio.open(path_to_img_pred, dtype='uint8')
              print(a.profile)
              predimg = a.read(1, out_dtype='uint8') # read the entire array
              with rasterio.open(path+image_name, count=1, dtype='uint8') as src:
                profile = src.profile.copy()
                print(src)
                print(src.profile)

                aff = src.transform
                profile.update({
                        'dtype': 'uint8',
                        'height': predimg.shape[0],
                        'width': predimg.shape[1],
                        'count': 1,
                        'transform': aff})  
              print('georeferencing now')
              with rasterio.open(ETHPRED+
                      image_name2+"_georef.tif", 'w', **profile) as dst:
                      print('brooooooooo its good')
                      dst.write_band(1, predimg)
              os.remove(ETHPRED+image_name2+'.tif')      
            else: 
              print('prediction done')




  stop2 = datetime.now()
#Execution time of the model 
  execution_time_prediction = stop2-start2
  print("data prediction execution time is: ", execution_time_prediction)


root_directory = "~/users/rmasolele/images/"
path_to_ref2016 = root_directory+'planet_2016/'




# ######### execute classification
pred(root_directory, path_to_ref2016, 2016)
pred(root_directory, path_to_ref2016, 2017)
pred(root_directory, path_to_ref2016, 2018)
pred(root_directory, path_to_ref2016, 2019)
pred(root_directory, path_to_ref2016, 2020)
pred(root_directory, path_to_ref2016, 2021)



