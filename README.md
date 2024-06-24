# Optimal resolution crater studies using Multi-Order HEALPix Maps

## Problem

Get the cratering density of a planetary surface, at optimal resolution.

Optimal resolution means high resolution where there is enough data, lower when number of craters are sparse.


## Idea

Healpix is designated for this job, except that originally the Healpix primer doesn't allow multiple map orders to be mixed.

For the needs of astronomical transients localisation on the sky, Healpix has now been extended to allow mixing different orders in same map Healpix.
This allows varying the resolution of the global map (sky or planet surface) depending on the need or data available.

Refs: 
 - [Greco+ 22](https://arxiv.org/abs/2201.05191)
 - [Multi-Order Coverage map IVOA Recommendation 2022-07-27](https://www.ivoa.net/documents/MOC/20220727/REC-moc-2.0-20220727.pdf)




## How-to

The scripts in this repo facilitate creating such maps in a planetary surface context.
Their purpose is to make a multi-resoluytion healpix maps from a catalogue of features (e.g. impact craters),
where each pixel contains at least N (user-defined) features.

### requirements

```pip install numpy healpy mhealpy astropy```


### making a normal NESTED map from a catalogue

Import thing is to choose the healpix order here:
 - Choose a number that is at least good to represent the maximum resolution you want (13 is good for 1e8 craters on Mars).
 - Doesn't matter if it is too high: it will automatically get reduced at the next step, but it is more ressource intensive to do so.

see options using the help menu
```python make_nested_map.py -h```


### convert the neste map to multi-resolution (uniq)

Here you need to choose the minimum count N each healpix needs to have.

Example: assuming errors are dominated by the counting process, in order to get a density map with maximum ε relative error.
We need: √N/N < ε
E.g. for a 10% maximum error on the map -> N=100.

see options using the help menu
```python create_MOC_map.py -h```


### convert a count map to a density one

Trivial in the Healpix framework, but need to know the radius of the planet.

see options using the help menu
```python count_to_density.py -h```


## visualisation

- [Aladin >11](https://aladin.u-strasbg.fr/java/nph-aladin.pl?frame=downloading)
- [Mhealpy](https://mhealpy.readthedocs.io/en/latest/tutorials/Intro.html#Plotting)
