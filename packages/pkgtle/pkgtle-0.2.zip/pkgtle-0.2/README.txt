------------------- ogr2ogr -------------------

from pkgtle.ogr2ogr import ogr2console
ogr2_console( src, dst, driver )

example
src = input path
dst = output path
driver = type of vector input file

ogr2console('/content/test.geojson', '/content/BuengChawak.kml', 'GeoJSON' )

