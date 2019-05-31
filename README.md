# An Alfred Workflow to search SAO/NASA ADS

With the deprecation of the classic SAO/NASA Astrophysics Data System (ADS) search interface,
I wanted to improve my workflow for searching for papers in the astronomy literature. I find
that I generally just want to do author based searches with possible year constraints so I made
this Workflow that can be used by [Alfred](https://www.alfredapp.com) (tested in versions 3
and 4) to make this fast and easy.

![Workflow Screenshot](https://github.com/dfm/adsabs.alfredworkflow/raw/master/screenshot.png)

## Installation

First you'll need to get [Alfred](https://www.alfredapp.com) and buy the
[Powerpack](https://www.alfredapp.com/powerpack/). Then you can download the `adsabs.workflow`
file from the [Releases](https://github.com/dfm/adsabs.alfredworkflow/releases) page. Double
click to import that into Alfred.

You can also install the development version of the workflow by cloning this repository into
the `~/Library/Application Support/Alfred/Alfred.alfredpreferences/workflows` directory.

## Usage

To get started you can just open Alfred and type `ads ` to start searching. This will let you
perform queries using the ADS website. If you want to perform queries within Alfred as well,
you'll need to install [Andy Casey's ads library](https://github.com/andycasey/ads) and save
your ADS API key in the `~/.ads/dev_key` file (the environment variable version won't work).
By default Alfred uses the system Python, but you can change that by putting the path to your
favorite Python executable in the file `~/.ads/python`.

## Example queries

This workflow is designed to search authors and years only. For example, if you want to search
for papers by an author named "Spergel" in 2015, you can execute:

```
ads spergel 2015
```

If you only want to search for the first author, use:

```
ads ^spergel 2015
```

You can list multiple authors, if you want:

```
ads ^mandel agol 2002
```

Or year ranges:

```
ads ^mandel agol 2000 2004
```

And you can include first names, initials, etc. using quotes:

```
ads "^mandel, k" "agol, e" 2000 2004
```
