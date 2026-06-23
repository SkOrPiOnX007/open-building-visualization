import os
import json
import ee
import math
import geopandas as gpd
import momepy
from shapely.geometry import Polygon

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
if os.environ.get("GOOGLE_CREDENTIALS_JSON"):
    credentials = ee.ServiceAccountCredentials(
        json.loads(os.environ["GOOGLE_CREDENTIALS_JSON"])["client_email"],
        key_data=os.environ["GOOGLE_CREDENTIALS_JSON"]
    )

    ee.Initialize(credentials, project="ee-goyalarya2005")

else:
    ee.Initialize(project="ee-goyalarya2005")

    
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
def get_buildings(
    lat: float,
    lon: float,
    radius: int = 1000,
    limit: int = 200
):

    point = ee.Geometry.Point([lon, lat])

    area = point.buffer(radius).bounds()

    buildings = ee.FeatureCollection(
        "GOOGLE/Research/open-buildings/v3/polygons"
    ).filterBounds(area).limit(limit)

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

        gdf["area"] = momepy.Area(gdf).series
        gdf["perimeter"] = momepy.Perimeter(gdf).series
        gdf["elongation"] = momepy.Elongation(gdf).series
        gdf["compactness"] = momepy.CircularCompactness(gdf).series
        gdf["orientation"] = momepy.Orientation(gdf).series
        gdf["eri"] = momepy.EquivalentRectangularIndex(gdf).series
        gdf["squareness"] = momepy.Squareness(gdf).series

        area_m2 = gdf["area"].iloc[0]
        perimeter_m = gdf["perimeter"].iloc[0]

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

        feature["properties"]["area_m2"] = round(float(gdf["area"].iloc[0]), 2)
        feature["properties"]["perimeter_m"] = round(float(gdf["perimeter"].iloc[0]), 2)
        feature["properties"]["length_m"] = round(building_length, 2)
        feature["properties"]["width_m"] = round(building_width, 2)
        feature["properties"]["elongation"] = round(float(gdf["elongation"].iloc[0]), 2)
        feature["properties"]["compactness"] = round(float(gdf["compactness"].iloc[0]), 2)
        feature["properties"]["orientation"] = round(float(gdf["orientation"].iloc[0]), 2)
        feature["properties"]["equivalent_rectangular_index"] = round(float(gdf["eri"].iloc[0]), 2)
        feature["properties"]["squareness"] = round(float(gdf["squareness"].iloc[0]), 2)
    return geojson

@app.get("/grids")
def get_grids(
    lat: float,
    lon: float,
    radius: int = 1000,
    grid_size: int = 250
):
    point = ee.Geometry.Point([lon, lat])
    area = point.buffer(radius).bounds()

    coords = area.getInfo()["coordinates"][0]

    min_lon = min(coord[0] for coord in coords)
    max_lon = max(coord[0] for coord in coords)
    min_lat = min(coord[1] for coord in coords)
    max_lat = max(coord[1] for coord in coords)

    bbox = Polygon([
        (min_lon, min_lat),
        (max_lon, min_lat),
        (max_lon, max_lat),
        (min_lon, max_lat)
    ])

    gdf = gpd.GeoDataFrame(
        geometry=[bbox],
        crs="EPSG:4326"
    )

    gdf = gdf.to_crs("EPSG:3857")

    minx, miny, maxx, maxy = gdf.total_bounds

    grid_polygons = []

    x = minx
    grid_id = 1

    while x < maxx:
        y = miny

        while y < maxy:
            cell_maxx = min(x + grid_size, maxx)
            cell_maxy = min(y + grid_size, maxy)

            cell = Polygon([
                (x, y),
                (cell_maxx, y),
                (cell_maxx, cell_maxy),
                (x, cell_maxy)
            ])

            grid_polygons.append({
                "grid_id": grid_id,
                "geometry": cell
            })

            grid_id += 1
            y += grid_size

        x += grid_size

    grid_gdf = gpd.GeoDataFrame(
        grid_polygons,
        crs="EPSG:3857"
    )

    grid_gdf = grid_gdf.to_crs("EPSG:4326")

    return json.loads(grid_gdf.to_json())