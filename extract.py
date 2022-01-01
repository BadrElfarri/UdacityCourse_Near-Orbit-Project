"""Extract data from CSV and JSON files.

Data extreaced from on near-Earth objects and close approaches
The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the
command line, and uses the resulting collections to build an `NEODatabase`.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth
        objects.
    :return: A collection of `NearEarthObject`s.
    """
    with open(neo_csv_path, 'r') as infile:
        reader = csv.reader(infile)

        fields = next(reader)  # get the header.
        # `designation`, `name`, `diameter`, and `hazardous`
        fieldsOfInterest = ['pdes', 'name', 'pha', 'diameter']
        fieldsOfInterestIndex = {fieldOfInterest: fields.index(fieldOfInterest)
                                 for fieldOfInterest in fieldsOfInterest}
        NearEarthObjects = []
        for row in reader:
            NearEarthObjects.append(NearEarthObject(
                designation=row[fieldsOfInterestIndex['pdes']],
                name=row[fieldsOfInterestIndex['name']],
                diameter=row[fieldsOfInterestIndex['diameter']],
                hazardous=row[fieldsOfInterestIndex['pha']]))

    return NearEarthObjects


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close
        approaches.
    :return: A collection of `CloseApproach`es.
    """
    with open(cad_json_path) as f:
        jsonData = json.load(f)

    fields = jsonData['fields']
    # des = designation, cd = time, dist = distance, v_rel = velocity
    fieldsOfInterest = ['des', 'cd', 'dist', 'v_rel']
    # get index of the data array that we are interrested in
    itemsIndexInData = {fieldOfInterest: fields.index(fieldOfInterest)
                        for fieldOfInterest in fieldsOfInterest}

    data = jsonData['data']
    closeApproaches = [CloseApproach(
            designation=item[itemsIndexInData['des']],
            time=item[itemsIndexInData['cd']],
            distance=item[itemsIndexInData['dist']],
            velocity=item[itemsIndexInData['v_rel']]) for item in data]

    # data is an array of CloseApproach Dictionary
    return closeApproaches


if __name__ == '__main__':
    load_approaches('data/cad.json')
