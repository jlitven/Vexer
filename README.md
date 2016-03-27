# vexer
Vexer (Vocabulary Expander) creates stylish, multiple-choice English vocabulary flash cards for the popular SRS software anki (http://ankisrs.net/) using mac osx`s built-in dictionary.

## Version
0.2-alpha

## Prerequisites
* Python 2
* Mac OS X 10.5 or higher
* Anki
* `pip` (Python Install Packager)

## Install
`vexer` can be installed using `pip`:
```
sudo pip install vexer
```

## Usage
To create vocabulary cards in Anki, simply call `vexer` with a list of words in the command line or from within a text file:
```
vexer goofy funky silly
```
or
```
vexer my_words.txt
```

Upon running for the first time, `vexer` will ask you for your anki collection path and the name of the deck the words will be added to. These will be stored in a `config.ini` file in the local package directory which you can edit if these parameters change.

You can also include the number of choices in a card using the -n_c paramater as well as the number of definitions for each part of speech using the -n_d parameter:
```
vexer goofy funky silly -n_c 3 -n_d 2
```

`vexer` also stores these parameters in the `config.ini` file.

For information about all parameters run:
```
vexer --help
```

_Note: Vexer adds the tag `vocbulary` to the anki cards. Do not edit these tags as vexer uses this tag information._

## Uninstall
`vexer` can be uninstalled using `pip`:
```
sudo pip uninstall vexer
```
