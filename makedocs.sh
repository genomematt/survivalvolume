#commands for making documentation prior to release
#html files should be moved to gh-pages branch
pdoc --html --html-dir docs survivalvolume/parse.py
pdoc --html --html-dir docs survivalvolume/plot.py
jupyter nbconvert --to 'html_toc' --output-dir docs user_guide.ipynb

