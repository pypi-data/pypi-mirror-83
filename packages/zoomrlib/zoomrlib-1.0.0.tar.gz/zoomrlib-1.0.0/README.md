[![pipeline status](https://gitlab.com/remytms/zoomrlib/badges/master/pipeline.svg)](https://gitlab.com/remytms/zoomrlib/pipelines)
[![coverage report](https://gitlab.com/remytms/zoomrlib/badges/master/coverage.svg)](https://gitlab.com/remytms/zoomrlib/pipelines)

zoomrlib
========

zoomrlib is a library that let you read and write a Zoom R16 project
file and export it into a JSON file. It provide also a little cli to
show content of a Zoom R16 project as text.


Installation
------------

Python >= 3.6 is needed (older python version may work, but it's not
tested).

```shell
pip install zoomrlib
```


Usage
-----

Most important information form a project file can be read and write:

For the hole **project**:
- name
- header
- bitlength
- protected
- insert_effect_on
- tracks
- master

For a **track**:
- file
- status
- stereo_on
- invert_on
- pan
- fader
- chorus_on
- chorus_gain
- reverb_on
- reverb_gain
- eqhigh_on
- eqhigh_freq
- eqhigh_gain
- eqmid_on
- eqmid_freq
- eqmid_qfactor
- eqmid_gain
- eqlow_on
- eqlow_freq
- eqlow_gain

For the **master track**:
- file
- fader

In a python program, use it like this:

```python
import zoomrlib

with zoomrlib.open("PRJDATA.ZDT", "r") as file:
    prjdata = zoomrlib.load(file)

print(prjdata.name)
for track in prjdata.tracks:
    print(track.file)
print(prjdata.master.file)
```

The package brings a small binary that let you export ZDT file to json:

```sh
zoomrlib PRJDATA.ZDT > prjdata.json
```

Or directly from the library:
```sh
python -m zoomrlib PRJDATA.ZDT > prjdata.json
```


Thanks
------

This library can't exist without the huge work and help of
Leonhard Schneider (http://www.audiolooper.de/zoom/home_english.shtml).
Thanks for his help. If you are looking to a GUI to manage your Zoom R16
take a look at his project.
