Licenses
========

This directory holds license and credit information for the pycraf package,
works the pycraf package is derived from, and/or datasets.


`pycraf` itself is published under `GPL v3 <https://www.github.com/bwinkel/pycraf/blob/master/COPYING>`_, an open-source license. The package is based on the `Astropy-affiliated package template <https://github.com/astropy/package-template>`_, which is under BSD 3-clause license.

For some of the functionality provided in pycraf, data files provided by the
ITU are necessary. For example, the atmospheric model in the pycraf.atm
subpackage implements the algorithm described in `ITU-R Recommendation P.676 <https://www.itu.int/rec/R-REC-P.676-10-201309-S/en>`_.
Annex 1 of this Recommendation makes use of spectroscopic information of the
oxygen and water vapour lines given in Tables 1 and 2 of P.676.

ITU kindly gave us permission to include data files into pycraf that are
distributed with the Recommendations on the ITU servers. This makes it possible
to just use pycraf without the need to manually download necessary data files.
However, these data files are not free for commercial use. For details, please
see the `LICENSE.ITU <https://www.github.com/bwinkel/pycraf/blob/master/LICENSE.ITU>`_ file.

We are very grateful for the kind support from ITU study groups and ITU's
legal department.

Some of the examples/images in the pycraf documentation and tutorial notebooks
make use of `Copernicus <https://www.copernicus.eu/en>`_ data. For these, the
conditions in `COPERNICUS.EU <https://www.github.com/bwinkel/pycraf/blob/master/COPERNICUS.EU>`_ apply.
