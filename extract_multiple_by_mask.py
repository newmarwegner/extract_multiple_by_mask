import os
import pandas as pd
import geopandas as gpd
import glob
import rasterio
from rasterstats import zonal_stats


# function to open a vector layers with geopandas
## vector need to be inside a folder (called vector) inside of folder of ipython notebook
def open_shp():

    return gpd.read_file(glob.glob(os.path.join(os.getcwd(),'vector/')+"*.shp")[0],encoding='utf-8')

## function to return a list of class inside of column attribute in vector ordered and without duplicates
def get_class(shp,attr):

    return sorted(list(set([v[attr] for k,v in shp.iterrows()])))

## function to return a list of tiffs files ordered. Need a folder called tiffs inside of folder of ipython notebook
def tiffs():

    return sorted(glob.glob(os.path.join(os.getcwd(),'tiffs/')+"*.tif"))

## function to make a loop in list for each vector feature and each raster to extract mean values
def extract_mean(codename,shp,raster_list,classes):
    extract_by_mask=[]

    for feature in classes:
        polygon=shp.loc[(shp[str(codename)] ==feature)]
        polygon_bbox = polygon.total_bounds

        for raster in raster_list:
            data= raster[-8:-4] ## the name of the raster it's the year, with tha
            tiff_rec=rasterio.open(raster)
            window = tiff_rec.window(*polygon_bbox)
            tiff_rec_np = tiff_rec.read(1, window=window)
            transform = tiff_rec.window_transform(window)
            stats=zonal_stats(polygon, tiff_rec_np,affine=transform)

            for i in stats:
                media=i['mean']
                lista=[feature,data,media]
                extract_by_mask.append(lista)

    return extract_by_mask

## function to export a pd.DataFrame to csv
def dataframe_to_csv(dataframe):

    return dataframe.to_csv('mean.csv',sep=';',encoding='utf8')

## function to start process, needs declare the attribute field with limites to be extract
def run(codename):
    shp = open_shp()
    classes = get_class(shp,codename)
    rasters_list = tiffs()
    estatistics=extract_mean(codename,shp,rasters_list,classes)
    dataframe_to_csv(pd.DataFrame(estatistics))

    return


## to called the function run it's necessary give the name of atribute that's will select features on shapefile to make the statistics
run('nome')
