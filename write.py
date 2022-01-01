"""This module exports two functions.

`write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.
"""

import csv
import json
from os import close
from helpers import datetime_to_str


def write_to_csv(results, filename):
    """Write results to a csv file.

    The precise output specification is in `README.md`. Roughly, each output
    row corresponds to the information in a single close approach from the
    `results` stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be
        saved.
    """
    fieldnames = (
        'datetime_utc', 'distance_au', 'velocity_km_s',
        'designation', 'name', 'diameter_km', 'potentially_hazardous')

    with open(filename, 'w') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(fieldnames)  # write header
        for closeApproach in results:  # write each row of closeApproach
            writer.writerow([closeApproach.time,
                            closeApproach.distance,
                            closeApproach.velocity,
                            closeApproach.neo.designation,
                            closeApproach.neo.name,
                            closeApproach.neo.diameter,
                            closeApproach.neo.hazardous])


def write_to_json(results, filename):
    """Write results to a JSON file.
    
    The precise output specification is in `README.md`. Roughly, the output
    is a list containing dictionaries, each mapping `CloseApproach`
    attributes to their values and the 'neo' key mapping to a dictionary of
    the associated NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be
        saved.
    """
    with open(filename, 'w') as outfile:
        Approachs = []

        for closeApproach in results:
            neo_dict = {
                'designation': str(closeApproach.neo.designation),
                'name': closeApproach.neo.name,
                'diameter_km': closeApproach.neo.diameter,
                'potentially_hazardous': closeApproach.neo.hazardous}
            ApproachDict = {
                'datetime_utc': datetime_to_str(closeApproach.time),
                'distance_au': closeApproach.distance,
                'velocity_km_s': closeApproach.velocity,
                'neo': neo_dict}
            Approachs.append(ApproachDict)

        json.dump(Approachs, outfile, indent=2)
