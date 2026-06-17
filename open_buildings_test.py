import ee

ee.Initialize()

lat = 30.3165
lon = 78.0322

point = ee.Geometry.Point([lon, lat])

area = point.buffer(1000).bounds()

buildings = ee.FeatureCollection(
    "GOOGLE/Research/open-buildings/v3/polygons"
).filterBounds(area)

count = buildings.size().getInfo()

print("Number of buildings found:", count)
