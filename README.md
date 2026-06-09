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
User can generate choropleth 


##Building Area Categories

| Category   | Area Range   |
| ---------- | ------------ |
| Small      | 0 - 50 m²    |
| Medium     | 50 - 150 m²  |
| Large      | 150 - 300 m² |
| Very Large | 300+ m²      |

## How to Run

```bash
git clone https://github.com/SkOrPiOnX007/open-building-visualization.git

cd open-building-visualization

python3 -m venv .venv

source .venv/bin/activate

pip install fastapi uvicorn earthengine-api geopandas shapely pyproj momepy

earthengine authenticate

uvicorn main:app --reload
```

After the server starts:

1. Open `index.html`
2. Enter Latitude and Longitude
3. Click **Show Location**
4. Click **Generate Area Visualization**
5. Click any building to view:
   - Area
   - Perimeter
   - Length
   - Width
6. Download the visualization if required
   
Future Improvements
 -Add viewport-based loading for large areas
 -Improve export quality
 -Add density heatmap visualization
 -Add GeoJSON/CSV export
 -Add user-defined area size
 -Add better building accuracy validation

Author
Arya Goyal

