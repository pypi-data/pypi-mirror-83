import json
import sys

def coords_to_json_bb(x_min, y_min, x_max, y_max):
    return json.dumps({"type": "Polygon", "coordinates": [
        [
            [x_min, y_min],
            [x_min, y_max],
            [x_max, y_max],
            [x_max, y_min],
            [x_min, y_min],
        ]
    ]})

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as r:
        geojson = json.loads(r.read())

    x_min_all = None
    y_min_all = None
    x_max_all = None
    y_max_all = None

    if geojson.get('features'):
        features = geojson['features']
    else:
        features = [{'geometry': geojson}]
    for i, feature in enumerate(features):

        coordinates = feature.get('geometry', {}).get('coordinates')

        if not coordinates:
            print('No coordinates found in geometry provided')
            continue

        if isinstance(coordinates[0], list):
            coordinates = coordinates.pop()

        if isinstance(coordinates[0][0], list):
            coordinates = coordinates.pop()

        x_min_feature = None
        y_min_feature = None
        x_max_feature = None
        y_max_feature = None

        for coord_pair in coordinates:
            if x_min_feature is None or coord_pair[0] < x_min_feature:
                x_min_feature = coord_pair[0]

            if y_min_feature is None or coord_pair[1] < y_min_feature:
                y_min_feature = coord_pair[1]

            if x_max_feature is None or coord_pair[0] > x_max_feature:
                x_max_feature = coord_pair[0]

            if y_max_feature is None or coord_pair[1] > y_max_feature:
                y_max_feature = coord_pair[1]

        print('Feature {} bounding box:\n{}\n\n'.format(i+1, coords_to_json_bb(x_min_feature, y_min_feature,
                                                                             x_max_feature, y_max_feature)))

        if x_min_all is None or x_min_feature < x_min_all:
            x_min_all = x_min_feature

        if y_min_all is None or y_min_feature < y_min_all:
            y_min_all = y_min_feature

        if x_max_all is None or x_max_feature > x_max_all:
            x_max_all = x_max_feature

        if y_max_all is None or y_max_feature > y_max_all:
            y_max_all = y_max_feature


    print('Total bounding box:\n{}\n\n'.format(coords_to_json_bb(x_min_all, y_min_all,
                                                                             x_max_all, y_max_all)))
