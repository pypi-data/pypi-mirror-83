# OGC LD API Test Client
A test client (command line program) for implementations of the "OGC LD API" which is a variant of the standardised [OGC API: Features](http://www.opengis.net/doc/IS/ogcapi-features-1/1.0) that delivers OGC API data and also Linked Data.

1. [Installation](#installation)
2. [Use](#use)
3. [License](#license)
4. [Citation](#citation)
5. [Contacts](#contacts)


This test client performs tests against a target API instance and reports test passing, failure and failure messages.

It has no Python Package Index dependencies (Standard Library modules only)  so should run directly with only a basic Python installation.


## Installation
This program runs as a Python 3, command line utility and has only been tested on Unix/Linux systems but should run just fine on Windows too.


## Use
_work in progress_

The program can be run as a Python script on the command line or via the `tc.sh` shell script in the `bin/` folder.

The command line arguments (Python & shell) are:

**Flag** | **Input values** | **Requirement** | **Notes**  
--- | --- | --- | ---
`api_home`<br />_positional arg_ | URI of an API instance to test | Required | 
`-r` / `--requirements` | Perform the OGC APIs Requirements tests | Optional |
`-as` / `--abstracttests` | Perform the OGC APIs Abstract Tests tests | Optional |
`-a` / `--alltests` | Perform all tests | Optional |
`-l` / `--log` | How to log: screen, file, both | Optional | Default: screen


## License  
This code is licensed using the GPL v3 licence. See the [LICENSE file](LICENSE) for the deed. 

Note [Citation](#citation) below for attribution.


## Citation
To cite this software, please use the following BibTex:

```
@software{10.5281/zenodo.xxxxx,
  author = {{Nicholas J. Car}},
  title = {OGC LD API Test Client},
  version = {0.5},
  date = {2020},
  publisher = "SURROUND Australia Pty. Ltd.",
  doi = {10.5281/zenodo.xxxxx},
  url = {https://doi.org/10.5281/zenodo.xxxxx}
}
```

Or the following RDF:

```
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix sdo: <https://schema.org/> .
@prefix wiki: <https://www.wikidata.org/wiki/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<https://doi.org/10.5281/zenodo.xxxxx>
    a sdo:SoftwareSourceCode , owl:NamedIndividual ;
    sdo:codeRepository <https://github.com/surroundaustralia/ogcapild-testclient> ;
    dcterms:type wiki:Q7397 ; # "software"
    dcterms:creator "Nicholas J. Car" ;
    dcterms:date "2020"^^xsd:gYear ;
    dcterms:title "OGC LD API Test Client" ;
    sdo:version "0.5" ;
    dcterms:publisher [
        a sdo:Organization ;
        sdo:name "SURROUND Pty Ltd" ;
        sdo:url <https://surroundaustralia.com> ;
    ]
.
```


## Contacts

*publisher:*  
![](style/SURROUND-logo-100.png)  
**SURROUND Australia Pty. Ltd.**  
<https://surroundaustralia.com>  

*creator:*  
**Dr Nicholas J. Car**  
*Data Systems Architect*  
SURROUND Australia Pty. Ltd.  
<nicholas.car@surroudaustralia.com>  