The `getPeople.py` script populates the "People" page of the website. In order to run it, you'll need the python wget module. To install, run `pip install wget`. 

This script will add new items/overwrite things in the `content/all_people` directory, and remake the `people/index.md` file. None of these should be manually edited given this fact. 

To run, just execute `python getPeople.py` from within the `scripts` directory.
