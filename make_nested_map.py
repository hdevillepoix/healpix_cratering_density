import os
import argparse

import healpy as hp
import numpy as np

from astropy.table import Table


def main(ifile, order):
        
    ofile = os.split('.')[0] + f'_nested_hpx{order}_map.fits'
    if False or not os.path.isfile(ofile):
        print(f'creating map from scratch...')
        create_map_from_scratch(ifile, order, ofile)
    else:
        print(f'output file {ofile} already exists')


def create_map_from_scratch(ifile, order, ofile):
    
    nside = hp.order2nside(order)
    npix = hp.nside2npix(nside)
    
    # load data
    tab = Table.read(ifile)

    # each crater counts as 1, but that could be different
    fs = np.ones_like(tab['Var2_1'], dtype=np.uint8)

    # Go from HEALPix coordinates to indices
    indices = hp.ang2pix(nside, tab['Var2_1'], tab['Var2_2'], nest=True, lonlat=True)

    hpxmap = np.zeros(npix, dtype=np.uint16)

    # add up to pixels
    np.add.at(hpxmap, indices, fs)
    
    print(f'saving to {ofile} ...')
    hp.write_map(ofile, hpxmap, nest=True)
    
    return hpxmap
    

if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser(description='Create nested healpix map from data')
    parser.add_argument("-i", "--input", type=str, required=True, help="Table data file location")
    parser.add_argument("-o", "--order", type=str, required=True, help="Healpix map order")
    
    args = parser.parse_args()
    
    order = int(args.order)
    
    main(args.input, order)

