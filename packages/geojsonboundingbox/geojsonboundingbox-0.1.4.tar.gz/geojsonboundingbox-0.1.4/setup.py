# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geojsonboundingbox']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'geojsonboundingbox',
    'version': '0.1.4',
    'description': 'Prints out the bounding box of a geojson input file',
    'long_description': '# GeoJSON to bounding box utility\n\nThis utility will find the minimum and maximum coordinates in a given GeoJSON file and format them as a GeoJSON bounding box.\n\nIt is more of a proof-of-concept and it will sometimes fail. Please contact the author with feedback. \n\n## Usage\n```shell script\npython -m geojsonboundingbox "/path/to/myfile.geojson"\n```\n\nFor anything more advanced, please look into the `shapely` Python library.',
    'author': 'Eric McCowan',
    'author_email': 'eric.mccowan@servian.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ericmccowan/geojsonboundingbox',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.0,<4.0',
}


setup(**setup_kwargs)
