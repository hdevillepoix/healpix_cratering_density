import os
import argparse

import healpy as hp
import numpy as np

from astropy.table import Table


def main(ifile, **kwargs):
    
    order = kwargs['order']
        
    ofile = ifile.split('.')[0] + f'_nested_hpx{order}_map.fits'
    if False or not os.path.isfile(ofile):
        print(f'creating map from scratch...')
        create_map_from_scratch(ifile, ofile, **kwargs)
    else:
        print(f'output file {ofile} already exists')


def create_map_from_scratch(ifile, ofile, **kwargs):
    
    order = kwargs['order']
    lat_key = kwargs['lat_key']
    lon_key = kwargs['lon_key']
    
    nside = hp.order2nside(order)
    npix = hp.nside2npix(nside)
    
    # load data
    tab = Table.read(ifile)

    # each crater counts as 1, but that could be different
    fs = np.ones_like(tab[lon_key], dtype=np.int16)

    # Go from HEALPix coordinates to indices
    print(f'converting lat/long to healpix indices...')
    indices = hp.ang2pix(nside, tab[lon_key]%360, tab[lat_key], nest=True, lonlat=True)
    
    tab['hpx_index'] = indices
    catalogues_ofile = ifile.split('.')[0] + f'_catalogue_hpx{order}.fits'
    print(f'saving catalogue with healpix assignment to {catalogues_ofile} ...')
    tab.write(catalogues_ofile, overwrite=True)

    hpxmap = np.zeros(npix, dtype=np.int16)

    # add up to pixels
    print(f'filling up the map...')
    np.add.at(hpxmap, indices, fs)
    
    print(f'saving to {ofile} ...')
    hp.write_map(ofile, hpxmap, nest=True)
    
    return hpxmap
    

if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser(description='Create nested healpix map from data')
    parser.add_argument("-i", "--input", type=str, required=True, help="Table data file location")
    parser.add_argument("-o", "--order", type=str, required=True, help="Healpix map order")
    parser.add_argument("-latkey", "--latkey", type=str, default='latitude', help="name of the latitude column")
    parser.add_argument("-lonkey", "--lonkey", type=str, default='longitude', help="name of the longitude column")
    
    args = parser.parse_args()
    
    order = int(args.order)
    
    
    main(args.input,
         order=order,
         lat_key=args.latkey,
         lon_key=args.lonkey)

