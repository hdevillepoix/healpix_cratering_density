from copy import deepcopy

import astropy.units as u
from astropy.constants import R_earth

# load up multi-order healpix library
from mhealpy import HealpixMap

# Planet characteristics
# future improvement: take flatenning into account
PLANETS = {'earth':{'radius': R_earth},
            'mars':{'radius': 3389.5 * u.km},
            'venus':{'radius': 6051.8 * u.km},
            'moon':{'radius': 1737.4 * u.km}}


def main(uniq_map_file_count, planet, ofile=None):
    # first check that we have this planet on file
    planet = planet.lower()
    if planet not in PLANETS:
        raise KeyError('planet ' + planet + ' not supported, need to choose from ' + list(PLANETS.keys()))

    if ofile is None:
        uniq_map_file_density = uniq_map_file_count.replace('_count_','_density_')
        if uniq_map_file_density == uniq_map_file_count:
            raise KeyError('Cannot determine a good output file name, please specify one')
    else:
        uniq_map_file_density = ofile
    
    uniq_map = HealpixMap.read_map(uniq_map_file_count)
    # consitency check: make sure the total area of the pixels equal to the entire surface area of the planet
    # all_pixels_sum = np.sum(uniq_map.pixarea()*PLANETS[planet]['radius']**2 /u.sr)
    # planet_area = 4*np.pi * PLANETS[planet]['radius']**2
    # should be ~ machine precision
    #print(f'relative area error: {abs(planet_area-all_pixels_sum)/all_pixels_sum:.2e}')

    # make a density map in craters/km2
    uniq_density_map = deepcopy(uniq_map)
    uniq_density_map = uniq_map / (uniq_map.pixarea()*PLANETS[planet]['radius']**2 /u.sr)
    print(f'writing density map to {uniq_map_file_density}')
    uniq_density_map.write_map(uniq_map_file_density, overwrite=True)

    

if __name__ == "__main__":
    import argparse
    # parse arguments
    parser = argparse.ArgumentParser(description='Convert a multi-resolution healpix count map into a density one (unit = km^-2)')
    parser.add_argument("-i", "--input", type=str, required=True, help="Count map file location")
    parser.add_argument("-p", "--planet", type=str, required=True, help="which planet are we on?")
    parser.add_argument("-o", "--ofile", type=str, help="output file name")
    
    args = parser.parse_args()
    
    main(args.input, args.planet, args.ofile)

