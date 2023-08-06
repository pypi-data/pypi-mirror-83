Module to design figures for scientific journals
Uses python3 and matplotlib 3.2.1, should work for other versions

# Installation 

go to the module directory and execute

python journal_styles.py install

This will generate style files and print installation instructions.
You will need to manually
1) copy the matplotlibrc file from /styles to matplotlib configuration directory (keep a backup copy of the old file).
2) copy the journals styles from /styles to matplotlib configuration directory/stylelib
3) change the ipython matplotlib-inline interface to avoid overriding of parameters while using jupyter notebooks.

# Usage

Most users will only need the class figure_frame.

from journal_styles import figure_frame

an instance of the class can be initializad as

ff = figure_frame('lMs','lMs')

and used as

plt.figure(figsize = ff.figsize)

plt.axes(ff.rects[0])

See webpage for further examples.

# Updating styles

python journal_styles.py update-styles

Will update the styles in the local styles directory.
Must be run after adding or modifying journal parameters.

# Uninstalling

python journal_styles.py uninstall

returns instructions for removing files.
You will need to undo steps 1-2-3 of the installation.

