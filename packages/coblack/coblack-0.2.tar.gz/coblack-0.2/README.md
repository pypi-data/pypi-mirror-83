# CoBlack

_CoBlack_ is a <em><a href="https://black.readthedocs.io">Black</a></em>-compliant formatter/rewrapper for Python comments.


#### Example code

Before:
```python
def care_for(self, favorite_plant):
    self.sing_a_lullaby_to(favorite_plant)  # This should help them grow. Note that this comment is too long to fit on one line, given the recommended line length.
    favorite_plant.water(100 * mL)  # Prevent dehydration.
```

After:
```python
def care_for(self, favorite_plant):
    self.sing_a_lullaby_to(favorite_plant)  # This should help them grow. Note that this
    #                                       # comment is too long to fit on one line,
    #                                       # given the recommended line length.
    favorite_plant.water(100 * mL)  # Prevent dehydration.
```
The extra `#`'s at the beginning of each line are necessary to be Black-compliant:\
If they were not there, Black would pull the comments to the start of the line, 
destroying the alignment, and making the code look messier.
(Compare to how the [naive way](#naive-way-of-wrapping-comments) of wrapping comments looks).


<br>


## Installation

```
$ pip install coblack
```

This will get you the [![latest release on PyPI](https://img.shields.io/pypi/v/coblack.svg?label=latest%20release%20on%20PyPI:)](https://pypi.python.org/pypi/coblack/)

(Upgrade an existing installation of _CoBlack_ by adding the `--upgrade`/`-U` flag).


<br>


## Usage

In your terminal:
```
$ coblack my_file.py
```
This wraps & fills out multiline comments, and passes the result through `black`.\
The file is edited in-place.

Get info on additional options (such as eg `-l` to set the line length) 
with `coblack -h`.


<br>


## IDE integration

For PyCharm, create a new [_External Tool_](https://www.jetbrains.com/help/pycharm/configuring-third-party-tools.html),
as follows:

<img alt='Screenshot of External Tool UI in PyCharm. Gist: `coblack "$FilePath$"`'
     src='doc/IDE_integration_PyCharm.png'
     width=600>

Then assign a keyboard shortcut to this tool.\
This enables you to format your files quickly and often during coding sessions.

In VS Code, you'd create a new [_Task_](https://code.visualstudio.com/docs/editor/tasks), in a similar fashion.


<br>


## Python API

```python
import coblack

coblack.format_file("path/to/my_file.py")  # You can also pass a `pathlib.Path`.
```


<br>


## Appendix

#### Naive way of wrapping comments

```python
def care_for(self, favorite_plant):
    self.sing_a_lullaby_to(favorite_plant)  # This should help them grow. Note that this
    # comment is too long to fit on one line, given the recommended line length.
    favorite_plant.water(100 * mL)  # Prevent dehydration.
```
([👆 back to top of ReadMe](#coblack)).


<br>

#### Other comment styles

On own line, before code:
```python
def care_for(self, favorite_plant):
    
    # This should help them grow. Note that this comment is too long to fit on one line,
    # given the recommended line length.
    self.sing_a_lullaby_to(favorite_plant)

    # Prevent dehydration.
    favorite_plant.water(100 * mL)
```

On own line, after code:
```python
def care_for(self, favorite_plant):
    
    self.sing_a_lullaby_to(favorite_plant)
    # This should help them grow. Note that this comment is too long to fit on one line,
    # given the recommended line length.
    
    favorite_plant.water(100 * mL)
    # Prevent dehydration.
```

These styles don't need _CoBlack_;
a vanilla rewrapper like any of the following will do:
- The [Wrap to Column](https://plugins.jetbrains.com/plugin/7234-wrap-to-column) plugin for PyCharm;
- The [Rewrap](https://marketplace.visualstudio.com/items?itemName=stkb.rewrap) extension for VS Code;
- The "Wrap Paragraph at Ruler" command in Sublime Text (`Alt-Q` or `Alt-⌘-Q`) ;
- The `fill-paragraph` command in Emacs; or
- The `gq` operator in Vim.
