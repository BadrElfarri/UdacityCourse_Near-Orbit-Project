"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.
"""
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional),
    diameter in kilometers (optional - sometimes unknown), and whether it's
    marked as potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments supplied to the
            constructor.
        """
        self.designation = ('' if not info['designation']
                            else info['designation'])
        self.name = (None if not info['name'] or info['name'] == ''
                     else info['name'])
        self.diameter = (float('nan') if not info['diameter']
                         or info['diameter'] == ''
                         else float(info['diameter']))
        self.hazardous = True if info['hazardous'] == 'Y' else False
        self.approaches = []

    @property
    def fullname(self):
        """Return the fullname accessed as a property."""
        return f"{self.designation} ({self.name})"

    def __str__(self):
        """Return then following string.
        
        NEO 433 (Eros) has a diameter of 16.840 km and is not
        potentially hazardous.
        """
        return f"NEO {self.fullname} has a diameter of {self.diameter} " + \
               f"km and is{' ' if self.hazardous else ' not '}" + \
               "potentially hazardous"

    def __repr__(self):
        """Return a machine 'representation'."""
        return "NearEarthObject(designation=" + \
               f"{self.designation!r}, name={self.name!r}, " + \
               f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach
    to Earth, such as the date and time (in UTC) of closest approach, the
    nominal approach distance in astronomical units, and the relative
    approach velocity in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied to the
            constructor.
        """
        self._designation = ('' if not info['designation']
                             else info['designation'])
        self.time = (None if not info['time']
                     else cd_to_datetime(info['time']))
        self.distance = (0.0 if not info['distance']
                         else float(info['distance']))
        self.velocity = (0.0 if not info['velocity']
                         else float(info['velocity']))
        self.neo = None

    @property
    def time_str(self):
        """Return a formatted representation of `CloseApproach`'s time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default
        representation includes seconds - significant figures that don't exist
        in our input data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return datetime_to_str(self.time)

    def __str__(self):
        """Return string representation."""
        return f"At {self.time_str}, " + \
               f"'{self.neo.fullname if self.neo else 'no Neo '}' " + \
               f"Connecion approaches Earth at a distance of " + \
               f"{self.distance:.2f} au and a velocity of " + \
               f"{self.velocity:.2f} km/s."

    def __repr__(self):
        """Return Machine representation."""
        return f"CloseApproach(time={self.time_str!r}, " + \
               f"distance={self.distance:.2f}, " + \
               f"velocity={self.velocity:.2f}, neo={self.neo!r})"


if __name__ == '__main__':  # Test code.
    print('Start')
    print(NearEarthObject(
            designation='1',
            name='2',
            diameter=20.0,
            hazardous=True))
