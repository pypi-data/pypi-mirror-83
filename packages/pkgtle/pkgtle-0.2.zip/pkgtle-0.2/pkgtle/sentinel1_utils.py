import os
import ogr2ogr
import zipfile

import rasterio as rio
from rasterio import plot, mask

import numpy as np
import geopandas as gpd
from shapely.geometry import Polygon


def get_path(dam_id):
    dam_path = os.getcwd() + '/' + dam_id
    try:
        os.makedirs(dam_path)
        print('Create folder "/{}/" ...done.'.format(dam_id))
    except:
        print('Folder "/{}/" already ...create '.format(dam_id))

    print('Path : {} '.format(dam_path))
    print('\n')

    try:
        files_path = dam_path + '/files'
        os.makedirs(files_path)
        print('Create folder "files" ...done.')
    except:
        print('Folder /{}/files/ already create'.format(dam_id))
    print('Path : {} '.format(files_path))
    print('\n')

    return dam_path, files_path


def kml2geojsoN(dam_id, dam_path, files_path):
    default_path = os.getcwd()
    os.chdir( files_path )
    try:
        print('Process Path : {}'.format( os.getcwd() ) )
        ogr2ogr.main([ " ", "-f", "GeoJSON",  dam_id + ".geojson", dam_id + ".kml"  ])
        print('\n')
        print('Convert "{}.kml" to "{}.GeoJSON" ...done'.format(dam_id, dam_id))
    except:
        print('Error : Cannot convert KML to GeoJSON')

    os.chdir( default_path )
    print('\n')
    print('Set Path to {}'.format( os.getcwd() ))



def print_odata(info):
        print('Title           : ', info['title'])
        print('Polarisation    : ', info['Polarisation'])
        print('Pass direction  : ', info['Pass direction'])
        print('Product level   : ', info['Product level'])
        print('Sensing start   : ', info['Sensing start'])
        print('Sensing stop    : ', info['Sensing stop'])
        print('Size            : ', info['Size'])
        print('Online          : ', info['Online'])
        print('\n')

def get_product( api, footprint, date_interval ):
        products = api.query(footprint,
                     date=date_interval,
                     producttype='GRD')

        products_df = api.to_dataframe( products )

        for uuid in products_df['uuid']:
                info = api.get_product_odata( uuid , full=True )
                print('Product ID      : ', uuid)
                print_odata(info)

        return products_df


def dowload_product( api, uuid, dam_path) :
        default_path = os.getcwd()
        os.chdir( dam_path )
        info = api.get_product_odata( uuid , full=True )
        print('Product ID      : ', uuid)
        print_odata(info)

        if info['Online']:
                print('Product {} is online. Starting download.'.format( uuid ))
                api.download( uuid )
        else:
                print( 'Product {} is not online.'.format( uuid ) )
        os.chdir( default_path )

def extract_zip( SAFE_path, dam_path ):
        default_path = os.getcwd()
        os.chdir( dam_path )
        zipSAFE_path = SAFE_path[:-6] + ".zip"
        with zipfile.ZipFile(zipSAFE_path, "r") as zip_ref :
                zip_ref.extractall()
                print('Extract zip file ...done')
                print('Path: {}'.format(zipSAFE_path))
                print('\n')
        os.remove(zipSAFE_path)
        print( 'Delete zip file  ...done' )
        print( 'Path: {}'.format(zipSAFE_path))

        os.chdir( default_path )


def get_BBox(dam_id, files_path):
        dam_geojson_path = files_path + '/' + dam_id + '.geojson'
        bbox_geojson_path = files_path + '/' + 'bbox.geojson'
        polygon = gpd.read_file(  dam_geojson_path )

        inflate_bbox = 0

        minx, miny, maxx, maxy = polygon.bounds[['minx', 'miny', 'maxx', 'maxy']].loc[0]
        delx = maxx - minx
        dely = maxy - miny

        minx = minx - delx * inflate_bbox
        maxx = maxx + delx * inflate_bbox
        miny = miny - dely * inflate_bbox
        maxy = maxy + dely * inflate_bbox

        bbox_geo = Polygon( [[minx, miny], [minx, maxy], [maxx,maxy], [maxx,miny]] )

        gpd.GeoDataFrame(crs = {'init':'epsg:4326'}, geometry = [bbox_geo]).to_file(bbox_geojson_path, driver='GeoJSON')

        bbox = gpd.read_file( bbox_geojson_path )
        dam_shape = gpd.read_file( dam_geojson_path )

        return bbox, dam_shape

            
            


