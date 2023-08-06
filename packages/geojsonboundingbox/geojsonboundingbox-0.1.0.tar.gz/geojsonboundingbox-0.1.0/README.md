# GeoJSON to bounding box utility

This utility will find the minimum and maximum coordinates in a given GeoJSON file and format them as a GeoJSON bounding box.

It is more of a proof-of-concept and it will sometimes fail. Please contact the author with feedback. 

## Usage
```shell script
python -m geojsonboundingbox "/path/to/myfile.geojson"
```

For anything more advanced, please look into the `shapely` Python library.