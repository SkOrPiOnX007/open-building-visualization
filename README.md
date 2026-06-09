# Open Buildings Visualization

A web-based GIS application that allows users to enter latitude and longitude, fetch building footprints from Google Open Buildings using Google Earth Engine, visualize them on a Leaflet map, calculate building dimensions, and generate a building-area choropleth visualization.

## Features

- Search buildings using latitude and longitude
- Display a 2km × 2km area on map
- Fetch building footprints from Google Open Buildings dataset
- Visualize buildings on satellite map using Leaflet.js
- Show building information on click:
  - Area
  - Perimeter
  - Length
  - Width
- Generate choropleth visualization based on building area
- Add color legend for building size categories
- Download visualization as image

## Tech Stack

- HTML
- CSS
- JavaScript
- Leaflet.js
- FastAPI
- Python
- Google Earth Engine
- GeoPandas
- Shapely
- Momepy

## Project Flow

```text
User enters latitude and longitude
        ↓
Frontend sends request to FastAPI
        ↓
FastAPI queries Google Earth Engine
        ↓
Open Buildings data is fetched
        ↓
Building dimensions are calculated
        ↓
GeoJSON is sent back to frontend
        ↓
Leaflet displays buildings on map
        ↓
User can generate choropleth visualization
