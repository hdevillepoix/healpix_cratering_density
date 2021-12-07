# Optimal resolution cratering density using healpix

## problem

Get the cratering density of a planetary surface, at optimal resolution.

Optimal resolution means high resolution where there is enough data, lower when number of craters are sparse.


## idea

Healpix is designated for this job, except the Healpix primer doesn't allow multiple map orders to be mixed.

There is a number of descriptions for doing this:

https://emfollow.docs.ligo.org/userguide/tutorial/multiorder_skymaps.html

https://github.com/healpy/healpy/issues/642


And one usefull implementation for creating these multi-order healpix maps: https://mhealpy.readthedocs.io/en/latest/

## how-to


### requirements

```pip install numpy healpy mhealpy astropy```


### start by making a normal NESTED map from your data


Import thing is to choose the healpix order here:
 - Choose a number that is at least good to represent the maximum resolution you want (12 is good for 1e8 craters on Mars).
 - Doesn't matter if it is too high: it will automatically get reduced at the next step, but it is more ressource intensive to do so.


see options usign the help menu
```python make_nested_map.py -h```



### then convert your map to multi-resolution

Here you need to choose the minimum count a healpix needs to have.
Counting errors on the density should in general drive this choice.

√N/N = % std error

So for a 10% maximum error on the map -> N=100.
 - 20% -> N=25
 - 1σ -> N=10


see options usign the help menu
```python create_MOC_map.py -h```


This will create two outputs: one MOC `density` map, and one MOC `count` map.
These maps are usually 10-100x smaller than the corresponding NESTED map.


## visualisation

Only software that I could find that does a decent job is Aladin:

download Aladin >11: https://aladin.u-strasbg.fr/java/nph-aladin.pl?frame=downloading

Plots can also be made programatically with matplotlib (see examples in mhealpy doc), but it's bloody slow.
