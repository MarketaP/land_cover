import rasterio
import geopandas as gpd


class_names = {0: 'No Data', 
10: 'Cropland, rainfed', 
20: 'Cropland, irrigated or post-flooding',
30: 'Mosaic cropland (>50%)/natural vegetation (<50%)',
40: 'Mosaic natural vegetation( >50%)/cropland (<50%)', 
50: 'Tree cover, broadleaved, evergreen, closed to open (>15%)',
60: 'Tree cover, broadleaved, deciduous, closed to open (>15%)',
70: 'Tree cover, needleleaved, evergreen, closed to open (>15%)',
80: 'Tree cover, needleleaved, deciduous, closed to open (>15%)',
90: 'Tree cover, mixed leaf type',
100: 'Mosaic tree and shrub (>50%)/herbaceous cover (<50%)',
110: 'Mosaic herbaceous cover (>50%)/tree and shrub (<50%)',
120: 'Shrubland',
130: 'Grassland',
140: 'Lichens and mosses',
150: 'Sparse vegetation',
160: 'Tree cover, flooded, fresh or brackish water',
170: 'Tree cover, flooded, saline water',
180: 'Shrub or herbaceous cover, flooded',
190: 'Urban areas',
200: 'Bare areas',
210: 'Water bodies',
220: 'Permanent snow and ice'
}

def get_values_from_points(year):
    # Read points from shapefile
    pts = gpd.read_file(f'../../../mendelu/Marketa/land_cover/Top_1000_{year}.shp')
    src = rasterio.open(f'../../../mendelu/Marketa/land_cover/ESA_LC_classes{year}.tif')
    points = pts['geometry']
    entry = 1
    values = []
    names = []

    # Get values form raster to points
    for point in points:
        x = point.xy[0][0]
        y = point.xy[1][0]
        row, col = src.index(x, y)
        print("Point correspond to row, col: %d, %d"%(row,col))
        value = src.read(1)[row,col]
        print(value)
        values.append(value)
        name = class_names.get(value)
        print(name)
        names.append(name)
        print(f'Row {entry} done')
        entry = entry + 1

    pts['Land_Cover'] = values
    pts['Land_Cover_Name'] = names

    pts.to_csv(f'../../../mendelu/Marketa/land_cover/Top_1000_{year}_LC.csv', index = False)

years = range(2000, 2020)

for year in years:
    print(f'Working on year {year}')
    get_values_from_points(year)
