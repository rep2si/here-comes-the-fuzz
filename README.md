# Here comes the fuzz

## Goal

A python script to generate a self-contained html page allowing for offline fuzzy-searching of a database.

The user should be able to provide a csv with arbitrary variable names, and a configuration file specifying which of these variables are targeted in an arbitrary number of search fields.

## Current status

This small project was born out of specific needs we met while working on the [rep<sup>2</sup>si project](https://rep2si.github.io/) project: offline fuzzy-searching (i.e., with tolerance for misspelling) across village census data stored in a csv file. The script currently transforms the csv data into json and relies on [Fuse.js](https://github.com/krisk/Fuse) to implement fuzzy searching across specific fields. It generates a single, self-contained html page that can be opened in any browser.

The script currently assumes that the csv follows a specific structure, and there is no possibility for the user to configure which variables are targeted by the search fields in the generated html file. We are working on a more general version of the script that meets the goal outlined above. PRs are welcome.

The scrips currently assumes that the following variables are present in the csv file.
- IndivID
- firstname
- caste
- gender
- age
- location
- fathersname
- mothersname
- spousesname

To generate the HTML file, first ensure that the script is executable: 

`chmod +x here-come-the-fuzz.py`

Then call it with the csv and desired output file as arguments:

`./here-come-the-fuzz.py path/to/the/CSV/with/data/indiv.csv path/to/where/you/want/html/to/output/what-the-fuzz.html`

The generated html file will include [fuse.js](https://www.fusejs.io/) in raw form. The entire script has to be included in the file itself as modern browsers' cross-scripting protection prevents loading this from a separate local file.

Many thanks to [Janey Tietz](https://github.com/janeytietz/) for initial work in drafting this. 
