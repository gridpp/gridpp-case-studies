The GridPP New User Engagement Programme: Selected Case Studies
===============================================================
This document presents a selection of case studies from the
GridPP New User Engagement Programme.

## Getting the images
The images used in the document are not stored in this repository.
You can get them using the script in `assets/images`:

```bash
$ cd assets/images
$ source get_images.sh
```

## Generating the case studies
The case studies themselves are not written in `.tex` format;
rather, the information has been put into a JSON file
that is then read into a Python wrapper class.

To generate the TeX for the case studies document, please use
the `make_casestudies.py` script provided.

```bash
$ python make_casestudies.py data/casestudies.json ./.
```

## Testing
To run the tests on the code, use:

```bash
$ nosetests --exe --nologcapture
```

## Licenses
<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons Licence" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a>
<br />
All documentation in this repository is covered by a
<a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.

All software in this repository is covered by the MIT license (see `LICENSE`)
apart from the TeX *.sty, *.srt, *.clo and *.cls files - please refer to the
relevant files themselves for more information regarding these.

## ToDo

* Implement full unit testing for the wrapper classes.
* Implement the HTML case study generation.

## Acknowledgements
This work was supported by the UK
[Science and Technology Facilities Council](http://www.stfc.ac.uk)
(STFC) via the [GridPP Collaboration](http://www.gridpp.ac.uk)
and grant ST/N00101X/1 as part of work with the CERN@school research
programme.


## Useful links

* [The GridPP Homepage](http://www.gridpp.ac.uk);
* [The GridPP Case Studies](http://www.gridpp.ac.uk/users/case-studies).
