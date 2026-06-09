from shapely.geometry import Polygon
import geopandas as gpd

# Simple rectangular building
poly = Polygon([
    (0, 0),
    (20, 0),
    (20, 10),
    (0, 10)
])

gdf = gpd.GeoDataFrame(
    {"geometry": [poly]},
    crs="EPSG:3857"
)

print("Area:", gdf.area.iloc[0], "m²")
print("Perimeter:", gdf.length.iloc[0], "m")