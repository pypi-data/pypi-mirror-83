#!/usr/bin/env python3
# -*- coding: utf-8 -*-
######################## Units conversion ######################################
#pt is LaTeX point = 1/72.27 inch
pt2inch = 0.013837
inch2pt = 72.27
pt2mm = 0.35145980
mm2pt = 1. / pt2mm
inch2mm = 25.4
mm2inch =1. / inch2mm
golden_ratio = 1.6180
######################## Journal parameters ####################################
# Physical Review family
parameters_PR = { 
'onecolumn' : 246 * pt2inch,
'twocolumn' : 510 * pt2inch,
'hspace_l' : 246 * pt2inch * 0.18,
'hspace_s': 246 * pt2inch * 0.045,
'vspace_l' : 246 * pt2inch / golden_ratio * 0.18,
'vspace_s' : 246 * pt2inch / golden_ratio * 0.045,
#'font' : 'Computer Modern Roman', 
'rcparameters' : {'text.usetex' : True,
                  'savefig.dpi' : 300,
                  'font.size' : 10,
                  'font.family' : 'serif',}
}
# Nature
parameters_nature = {
'onecolumn' : 89 * mm2inch,
'onehalfcolumn120' : 120 * mm2inch,
'onehalfcolumn136' : 136 * mm2inch,
'twocolumn' : 183 * mm2inch,
'hspace_l' : 14 * mm2inch,
'hspace_s': 3.5 * mm2inch,
'vspace_l' : 14 * mm2inch / golden_ratio,
'vspace_s' : 3.5 * mm2inch /golden_ratio,
#'font' : 'Arial',
'rcparameters' : {'text.usetex' : False,
                  'savefig.dpi' : 300,
                  'font.size' : 7,
                  'font.family' : 'sans-serif',}
}
# Nature Communications
parameters_nature_comm = {
'onecolumn' : 88 * mm2inch,
'twocolumn' : 180 * mm2inch,
'hspace_l' : 14 * mm2inch,
'hspace_s': 3.5 * mm2inch,
'vspace_l' : 14 * mm2inch / golden_ratio,
'vspace_s' : 3.5 * mm2inch /golden_ratio,
#'font' : 'Arial',
'rcparameters' : {'text.usetex' : False,
                  'savefig.dpi' : 300,
                  'font.size' : 7,
                  'font.family' : 'sans-serif',}
}
# Science
parameters_science = {
'onecolumn' : 55 * mm2inch,
'twocolumn' : 120 * mm2inch,
'hspace_l' : 14 * mm2inch,
'hspace_s': 3.5 * mm2inch,
'vspace_l' : 14 * mm2inch / golden_ratio,
'vspace_s' : 3.5 * mm2inch /golden_ratio,
#'font' : 'Helvetica',
'rcparameters' : {'text.usetex' : False,
                  'savefig.dpi' : 300,
                  'font.size' : 7,
                  'font.family' : 'sans-serif',}
}
# add new journal here
######################### Available journals ###################################
# update dictionary when a new journal is added
journals = {
'PR' : parameters_PR,
'Nature' : parameters_nature,
'Science' : parameters_science,
'Nature_Comm' : parameters_nature_comm,
}
################################################################################