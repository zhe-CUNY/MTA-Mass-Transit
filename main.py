import os
from pathlib import Path
import zipfile

from mta_gtfs_data_getter import download_gtfs_data
from mta_gtfs_shapefiles_maker import (
    make_bus_routes_shapefiles,
    make_bus_stops_shapefiles,
    make_rail_routes_shapefiles,
    make_rail_stops_shapefiles,
    make_subway_entrances_shapefiles,
)

from datetime import datetime

path_name = os.getcwd()
# folder = "July2019"
folder = datetime.today().strftime("%b%Y")

rails = ["LIRR", "metro_north", "nyc_subway"]

download_gtfs_data(folder)
for rail in rails:
    make_rail_routes_shapefiles(path=path_name, folder=folder, rail=rail)
    make_rail_stops_shapefiles(path=path_name, folder=folder, rail=rail)
    
make_bus_routes_shapefiles(path=path_name, folder=folder)
make_bus_stops_shapefiles(path=path_name, folder=folder)
make_subway_entrances_shapefiles(path=path_name, folder=folder)

# Zip up individual shapefiles
shapes_folder = Path(folder) / 'shapes'
shp_files = shapes_folder.glob('*.shp')

for shp_file in sorted(shp_files):
    base_name = shp_file.stem
    
    related_files = list(shapes_folder.glob(f'{base_name}.*'))
    related_files = [f for f in related_files if f.suffix != '.zip']
    
    if related_files:
        zip_path = Path(shapes_folder / f"{base_name}.zip")
        
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file in related_files:
                zipf.write(file, arcname=file.name)
        
        # Delete original files
        for file in related_files:
            file.unlink()