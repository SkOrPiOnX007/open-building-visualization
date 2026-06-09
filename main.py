import ee
import math
import geopandas as gpd
from shapely.geometry import Polygon

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
ee.Initialize()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Backend is running"}

@app.get("/buildings")
def get_buildings(lat: float, lon: float):

    point = ee.Geometry.Point([lon, lat])
    area = point.buffer(1000).bounds()

    buildings = ee.FeatureCollection(
        "GOOGLE/Research/open-buildings/v3/polygons"
    ).filterBounds(area).limit(3000)

    geojson = buildings.getInfo()

    for feature in geojson["features"]:
        coords = feature["geometry"]["coordinates"][0]

        polygon = Polygon(coords)

        gdf = gpd.GeoDataFrame(
            {"geometry": [polygon]},
            crs="EPSG:4326"
        )

        gdf = gdf.to_crs(epsg=3857)

        geom = gdf.geometry.iloc[0]

        area_m2 = geom.area
        perimeter_m = geom.length

        min_rect = geom.minimum_rotated_rectangle
        rect_coords = list(min_rect.exterior.coords)

        side_lengths = []

        for i in range(4):
            x1, y1 = rect_coords[i]
            x2, y2 = rect_coords[i + 1]

            length = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            side_lengths.append(length)

        building_length = max(side_lengths)
        building_width = min(side_lengths)

        feature["properties"]["area_m2"] = round(area_m2, 2)
        feature["properties"]["perimeter_m"] = round(perimeter_m, 2)
        feature["properties"]["length_m"] = round(building_length, 2)
        feature["properties"]["width_m"] = round(building_width, 2)

    return geojson