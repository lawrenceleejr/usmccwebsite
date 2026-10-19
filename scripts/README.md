The `getPeople.py` script populates the "People" page of the website from the
collaboration membership database (https://db.muoncollider.us). The database's
public export only includes active members who consented to being listed on
the public website (and only their public photos), so opt-outs are enforced at
the source — never hand-edit the generated files to add someone.

Dependencies: `pip install -r requirements.txt`.

This script will add new items/overwrite things in the `content/all_people`
directory, and remake the `people/index.md` file. None of these should be
manually edited given this fact.

Photos come from the database. For a member without a database photo, a file
in `saved_photos/` named after them (e.g. `JaneDoe.jpg`) is used instead, and
failing that the default `featured.png`.

To run, just execute `python getPeople.py` from within the `scripts`
directory. Set `USMCCDB_API` to point the script at a different database
instance (e.g. a local dev one).

```stl
solid cube_corner
  facet normal 0.0 -1.0 0.0
    outer loop
      vertex 0.0 0.0 0.0
      vertex 1.0 0.0 0.0
      vertex 0.0 0.0 1.0
    endloop
  endfacet
  facet normal 0.0 0.0 -1.0
    outer loop
      vertex 0.0 0.0 0.0
      vertex 0.0 1.0 0.0
      vertex 1.0 0.0 0.0
    endloop
  endfacet
  facet normal -1.0 0.0 0.0
    outer loop
      vertex 0.0 0.0 0.0
      vertex 0.0 0.0 1.0
      vertex 0.0 1.0 0.0
    endloop
  endfacet
  facet normal 0.577 0.577 0.577
    outer loop
      vertex 1.0 0.0 0.0
      vertex 0.0 1.0 0.0
      vertex 0.0 0.0 1.0
    endloop
  endfacet
endsolid
```
