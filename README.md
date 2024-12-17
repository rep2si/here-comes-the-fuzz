# here-comes-the-fuzz
Code to generate searchable database to find IDs.

This assumes you have a CSV file with the following variables:
- IndivID
- firstname
- caste
- gender
- age
- location
- fathersname
- mothersname
- spousesname

To generate the HTML version: 

run in Terminal (when located in the folder where the file is): 

`chmod +x here-come-the-fuzz.py`

and then:

`./here-come-the-fuzz.py path/to/the/CSV/with/data/indiv.csv path/to/where/you/want/html/to/output/what-the-fuzz.html`

This draws on [fuse.js](https://www.fusejs.io/) for the fuzzy search (included here in the raw form, so can run offline).

Many thanks to Janey Tietz for initial work in drafting this. 
