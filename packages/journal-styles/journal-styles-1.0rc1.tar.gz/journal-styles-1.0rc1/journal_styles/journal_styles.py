#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__all__ = ['standard_figsize', 'standard_rect', 'figure_frame', 
           'create_matplotlib_style', 'journals']
#################################### Import modules ############################
import os
if __name__ == "__main__":
    from parameters import *
else:
    from .parameters import *
DECIMALS = 3 #decimal precision
################### Functions for figsizes and axes rectangles #################
def standard_figsize(journal = 'PR', aspect_ratio = golden_ratio):
    '''returns the standard figsize for a given journal (1-D plot)
    example of usage 
    fs = standard_figsize('PR')
    plt.figure(figsize = fs)'''
    d = journals[journal]
    w = d['onecolumn']
    h = w / aspect_ratio
    return (round(w, DECIMALS), round(h, DECIMALS))

def standard_rect(journal = 'PR', aspect_ratio = golden_ratio):
    '''returns the standard axes rectangle for a given journal (1-D plot)
    example of usage 
    as = standard_rect('PR')
    plt.axes(rect = as)'''
    d = journals[journal]
    w = d['onecolumn']
    h = w / aspect_ratio
    return [round(d['hspace_l'] / w, DECIMALS), 
            round(d['vspace_l'] / h, DECIMALS),
            round(1. - (d['hspace_s'] + d['hspace_l']) / w, DECIMALS),
            round(1. - (d['vspace_s'] + d['vspace_l']) / h, DECIMALS)]
class figure_frame():
    '''Class for composing non-standard figures. 
    Example of usage :
    ff = figure_frame('lMs','lMs')
    plt.figure(figsize = ff.figsize)
    plt.axes(ff.rects[0])
    
    methods
    -------
    __init__

    attributes
    ----------
    figsize (tuple) : figure width and height in inches
    rects (list) : each element is a list of type [left, bottom, width, height] 
    representinx axes position expressed in units of figure width and height.
    '''
    def __init__(self,
                 h_spacing = 'lMs', v_spacing = 'lMs', 
                 aspect_ratio = golden_ratio, 
                 journal = 'PR', 
                 column = 'onecolumn', 
                 additional_axes= []):
        '''
        parameters 
        -----------
        h_spacing : string, horizontal division of the figure (left to right).
            Can contain 's' (small space), 'l' (large space), 'h' (half small space), 
            'H' (half large space). Must contain 'M' (position of the main axes)
        v_spacing : string, vertical division of the figure (bottom to top).
        aspect_ratio : float, aspect ratio (width/heigth) of the main axes
        journal : string, name of an available journal
        column : string or float, name of an available column type (journal dependent)
            or float (column width in inches)
        additional_axes : list of (int, int) tuples, integer coordinates of the 
            rectangle corresponding to secondary axes
        ---------
        returns 
        ---------
        instance of the class 
        '''
        d = journals[journal]
        if type(column) == float:
            fig_width = column
        else:
            fig_width = d[column]
        dic_h = {'s' : d['hspace_s'], 
                'l' : d['hspace_l'], 
                'h' : d['hspace_s']/2., 
                'H' : d['hspace_l']/2., 
                'M' : 0.}
        dic_v = {'s' : d['vspace_s'], 
                'l' : d['vspace_l'], 
                'h' : d['vspace_s']/2., 
                'H' : d['vspace_l']/2., 
                'M' : 0.}
        diff = sum([dic_h[x] for x in h_spacing])
        dic_h['M'] = (fig_width - diff) / h_spacing.count('M')
        dic_v['M'] = dic_h['M'] / aspect_ratio
        fig_height = sum([dic_v[x] for x in v_spacing])
        figsize = (round(fig_width, DECIMALS), round(fig_height, DECIMALS))
        h_indices = [i for i, a in enumerate(h_spacing) if a == 'M']
        v_indices = [i for i, a in enumerate(v_spacing) if a == 'M']
        axes = [(i,j) for j in v_indices for i in h_indices ]     + additional_axes
        #[(h_spacing.index('M'), v_spacing.index('M'))] 
        

        rects = []
        for ax in axes:
            x0 = sum([dic_h[h_spacing[i]] for i in range(ax[0])])
            y0 = sum([dic_v[v_spacing[i]] for i in range(ax[1])])
            rects.append([round(x0 / fig_width, DECIMALS),
                        round(y0 / fig_height, DECIMALS),
                        round(dic_h[h_spacing[ax[0]]] / fig_width, DECIMALS),
                        round(dic_v[v_spacing[ax[1]]] / fig_height, DECIMALS)])
        self.figsize = figsize 
        self.rects = rects
############## Creating matplotlib style files #################################
def create_matplotlib_style(journal = 'PR', folder = ''):
    '''Creates a matplotlib style file in a given folder'''
    d = journals[journal]
    figsz = standard_figsize(journal)
    rect = standard_rect(journal)
    if not os.path.exists(folder):
        os.makedirs(folder)
    with open(folder + '/{}.mplstyle'.format(journal), 'w') as f:
        f.write('figure.figsize : {},{}\n'.format(*figsz))
        f.write('figure.subplot.left : {}\n'.format(rect[0]))
        f.write('figure.subplot.bottom : {}\n'.format(rect[1]))
        f.write('figure.subplot.right : {}\n'.format(
            round(rect[0] + rect[2], DECIMALS)))
        f.write('figure.subplot.top : {}\n'.format(
            round(rect[1] + rect[3], DECIMALS)))
        try:
            for par in d['rcparameters']:
                f.write('{} : {}\n'.format(par, d['rcparameters'][par]))
        except:
            pass
########## Utility functions ###################################################
def diff_dic(dic1,dic2):
    ''' returns the dfference of two dictionaries as sorted set'''
    mismatch = sorted({key for key in dic1.keys() & dic2 if dic1[key] != dic2[key]})
    return mismatch

def _figure_frame_benchmark():
    'Checks figure_frame results'
    for journal in journals:
        ff = figure_frame('lMs', 'lMs', journal = journal)
        assert ff.figsize == standard_figsize(journals[journal])
        assert ff.rects[0] == standard_rect(journals[journal])
########## Installation ########################################################
if __name__ == "__main__":
    import sys
    if sys.argv[1] == '--help' or sys.argv[1] == '-h':
        #help
        print('''options are \n
              install \n
              uninstall \n
              update-styles \n''')

    elif sys.argv[1] == 'install':
        from pathlib import Path
        from matplotlib import get_configdir
        cdir = get_configdir() 
        line = 'c.InlineBackend.rc = { }\n'
        config_file = '{}/.ipython/profile_default/ipython_kernel_config.py'.format(str(Path.home()))

        print('1) Copy matplotlibrc file from /styles to {}'.format(cdir))
        for journal in journals:
            create_matplotlib_style(journal = journal, folder = 'styles')
        print('2) Copy new files from /styles to {}'.format(get_configdir() +'/stylelib'))
        print('3) Add the line \n \n {} \n \n to the ipython configuration file.'.format(line))
        print('Location should be \n{}'.format(config_file))
                
    elif sys.argv[1] == 'uninstall':
        # only gives instructions
        from pathlib import Path
        from matplotlib import get_configdir
        cdir = get_configdir()
        line = 'c.InlineBackend.rc = { }\n'
        config_file = '{}/.ipython/profile_default/ipython_kernel_config.py'.format(
            str(Path.home()))

        print('1) go to ', cdir, ' and restore the old matplotlibrc file')
        print('2) delete unwanted styles in ', cdir +'/stylelib')
        print('3) go to ', config_file, 'and delete the line \n\n', line)

    elif sys.argv[1] == 'update-styles':
        #update styles in local styles directory
        from matplotlib import get_configdir
        for journal in journals:
            create_matplotlib_style(journal = journal, folder = 'styles')
        print('Copy new files from /styles to {}'.format(get_configdir() +'/stylelib'))

    else:
        print('unkwnon option {}'.format(sys.argv[1]))