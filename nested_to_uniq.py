import os
import argparse

# load up multi-order healpix library
from mhealpy import HealpixMap


def main(nested_map, N):

    if not os.path.isfile(nested_map):
        print(f'File {nested_map} NOT FOUND')
        exit(1)
    print(f'loading {nested_map} ...')

    m = HealpixMap.read_map(nested_map, density = False)

    # order = m.order
    # nside = hp.order2nside(order)
    #npix = hp.nside2npix(nside)
    
    err_percent = 1./(N)**0.5*100
    err_percent_str = f'_{err_percent:.0f}pc-error'
    
    uniq_map_count = nested_map.replace('nested','uniq').replace('map','count_map' + err_percent_str)
    # uniq_map_dens = nested_map.replace('nested','uniq').replace('map','nativedensity_map' + err_percent_str)


    def split_fun(start, stop):
        
        # Start and stop specify the current pixel as a range of 
        # the underlaying single-res map
        
        # Each pixel can be split in 4
        child_npix = int((stop-start)/4)
        
        # Check for the sum of contents on each potential child pixel
        # If they will all contain >N counts, return True
        return all([sum(m[start + child_npix*i: start + child_npix*(i+1)]) >= N for i in range(4)])
    
    print('recursively combining count map')
    # Create the appropiate grid
    m_multi = HealpixMap.adaptive_moc_mesh(m.nside, split_fun)

    # Fill the map
    rangesets = m_multi.pix_rangesets(m.nside)

    for pix,(start,stop) in enumerate(rangesets):
        
        m_multi[pix] = sum(m[start:stop])
        
        
    print(f'writing MOC map {uniq_map_count} to disk...')
    m_multi.write_map(uniq_map_count)

    # I don't know what the built-in density function actually does
    # hence this should be calculated manually at a later step
    # print('converting to density map')
    # m_multi.density(True)
    # print(f'writing MOC density map {uniq_map_dens} to disk...')
    # m_multi.write_map(uniq_map_dens)




if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser(description='Create multi-resolution healpix map from nested map')
    parser.add_argument("-i", "--input", type=str, required=True, help="Nested map file location")
    parser.add_argument("-n", "--mincount", type=str, required=True, help="Minimum count per healpixel")
    
    args = parser.parse_args()
    
    N = int(args.mincount)
    
    main(args.input, N)

