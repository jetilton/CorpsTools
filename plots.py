# -*- coding: utf-8 -*-
import bokeh
from bokeh.io import show, reset_output
from bokeh.models import Legend, DatetimeTickFormatter
from bokeh.plotting import figure
import matplotlib.pyplot as plt
from bokeh.layouts import gridplot


def bok_sp(plot_dict, **kwargs):
    if kwargs: figsize = kwargs['figsize']
    else: figsize = (800,400)
    plot_list = []
    
    plot_width, plot_height = figsize
    
    for unit,values in plot_dict.items():
        p = figure(plot_width=plot_width, plot_height=plot_height)
        p.xaxis.formatter = DatetimeTickFormatter()

        glyph_list = []
        column_list = []
        for data in values:
            column_name,x,y = data 
            g = p.line(x = x, y = y, line_width = 2)
            column_list.append(column_name)
            glyph_list.append(g)
        items = [(column, [glyph]) for column,glyph in zip(column_list, glyph_list)]
        legend = Legend(items = items, location = (40,0))
        p.add_layout(legend, 'below')
        plot_list.append(p)
    grid = [[p] for p in plot_list]
    p = gridplot(grid)
    reset_output()  
    return p

def mlib_sp(plot_dict, **kwargs):
    if kwargs: figsize = kwargs['figsize']
    else: figsize = (15,10)
    plt.figure(figsize=figsize )
    p = 211
    for unit,values in plot_dict.items():
        plt.subplot(p)
        for data in values:
           
            column_name,x,y = data 
            plt.plot(x,y, label = column_name)
            plt.legend(bbox_to_anchor=(1.04,0), loc=3, borderaxespad=0)

        p += 1


#def simple_plot(dictionary, bok = False, **kwargs):
#    plot_dict = {}
#    for column,value in dictionary['column_data'].items():
#        
#        column_name = value['path']
#        units = value['units']
#        
#        x = dictionary['df'][column].index
#        y = dictionary['df'][column].values
#        try: 
#            plot_dict[units].append((column_name,x,y))
#        except:
#            plot_dict.update({units:[(column_name,x,y)]})
#    if bok:
#       return bok_sp(plot_dict, **kwargs) 
#    else:
#       mlib_sp(plot_dict, **kwargs)





def simple_plot(tso, bok = False, **kwargs):
    plot_dict = {}
    for column,value in tso.__dict__['metadata'].items():
        
        column_name = value['path']
        units = value['units']
        
        x = tso[column].index
        y = tso[column].values
        try: 
            plot_dict[units].append((column_name,x,y))
        except:
            plot_dict.update({units:[(column_name,x,y)]})
    if bok:
       return bok_sp(plot_dict, **kwargs) 
    else:
       mlib_sp(plot_dict, **kwargs)

