# Install the development version of mpld3

Survival Volume is most fully featured with mpld3 version 0.3dev post commit 559dfc6.  

When originally released you needed to install the development version to get all of the interactive features.
These notes now exist only for people who are developing or debugging Survival Volume and may need to install the development version of mpld3.
To install the development version of mpld3 you will need to

```
git clone https://github.com/mpld3/mpld3
cd mpld3/
python3 setup.py submodule
python3 setup.py install
```

In your jupyter notebooks you will also need to redirect mpld3 to the local javascript files.

```
import mpld3
mpld3.enable_notebook(d3_url='file://d3.v3.min.js',
                     mpld3_url='file://mpld3.v0.3git.js')
```

