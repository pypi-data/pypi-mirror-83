# Track which plots are active, which to draw in. 
# Derek Fujimoto
# Sept 2020

import matplotlib as mpl
import matplotlib.pyplot as plt
import yaml
import os

# =========================================================================== #
class PltTracker(object):
    """
        active:         dictionary, id number of active plot
        plots:          dictionary, list of plots drawn for type
    """
    
    # ======================================================================= #
    def __init__(self):
        
        # track which plots exist
        self.plots = []
        
        # track the active plot 
        self.active = 0
    
    # ======================================================================= #
    def _close_figure(self,event):
        """Remove figure from list"""
        
        # get number and style
        number = event.canvas.figure.number
        
        # disconnect events
        event.canvas.mpl_disconnect(event.canvas.user_close)
        event.canvas.mpl_disconnect(event.canvas.user_active)
        
        # close the winow
        plt.figure(number).clf()
        plt.close(number)
        
        # remove from list 
        self.plots.remove(number)
        
        # reset active
        try:
            self.active = self.plots[-1]
            plt.figure(self.active)
        except IndexError:
            self.active = 0
                        
    # ======================================================================= #
    def _decorator(self,fn,*args,id=None,unique=True,**kwargs):
        """
            Function wrapper
            
            fn: matplotlib function to operate on 
            args: passed to fn
            kwargs: passed to fn
        """
        
        # switch 
        fig = plt.figure(self.active)
        ax = plt.gca()
            
        # clear old objects
        if unique and id is not None:
            self._remove_drawn_object(ax,id)
        
        # run function 
        output = fn(*args,**kwargs)
        
        # track the drawn object
        if id is not None:
            ax.draw_objs.setdefault(id,[]).append((output,kwargs)) 
        
        return output
    
    # ======================================================================= #
    def _remove_drawn_object(self,ax,draw_id):
        """
            Remove an object labelled by draw_id from the figure, based on draw 
            style.
        """
        
        # check if id is present in drawn data
        if draw_id in ax.draw_objs.keys():

            # get item
            for item in ax.draw_objs[draw_id]:
            
                # strip saveas dict
                item = item[0]
            
                # remove line
                try:
                    item[0].remove()
                except TypeError:
                    try:
                        item.remove()
                    except AttributeError:
                        pass
                else: 
                    # remove errorbars
                    if type(item) is mpl.container.ErrorbarContainer:    
                        for i in item[1]:   i.remove()
                        for i in item[2]:   i.remove()
                        del ax.containers[ax.containers.index(item)]
                        
                    # remove lines
                    elif type(item) is mpl.lines.Line2D:
                        del ax.lines[ax.lines.index(item)]
                        
                    # remove images
                    elif type(item) is mpl.image.AxesImage:
                        del ax.image[ax.image.index(item)]
                
                if type(item) is mpl.contour.QuadContourSet:
                    for coll in item.collections: 
                        if coll in ax.collections:
                            del ax.collections[ax.collections.index(coll)]
                    
            plt.draw()
                
            # clear labels
            del ax.draw_objs[draw_id]
        
   # ======================================================================= #
    def _update_active_id(self,event):
        """
            Update the active figure id based on click event.
        """
        number = event.canvas.figure.number
        self.active = number
    
    # ======================================================================= #
    def annotate(self,id,*args,unique=True,**kwargs):
        return self._decorator(plt.annotate,*args,id=id,unique=unique,**kwargs)
    
    # ======================================================================= #
    def axhline(self,id,*args,unique=True,**kwargs):
        return self._decorator(plt.axhline,*args,id=id,unique=unique,**kwargs)
        
    # ======================================================================= #
    def axvline(self,id,*args,unique=True,**kwargs):
        return self._decorator(plt.axvline,*args,id=id,unique=unique,**kwargs)
        
    # ======================================================================= #
    def clf(self):
        """Clear the figure for a given style"""
        out = self._decorator(plt.clf)
        ax = plt.gca()
        ax.draw_objs = {}
        
    # ======================================================================= # 
    def contour(self, id, X, Y, Z, levels=5, unique=True, info=None, **kwargs):
        
        # get active for this style
        active_style = self.active
        
        # make new figure if needed 
        if active_style == 0:   
            self.figure()
            active_style = self.active
        fig = plt.figure(active_style)
        ax = fig.axes[0]
        
        # redraw old objects and lines
        if unique:  self._remove_drawn_object(ax,id)
        self._remove_drawn_object(ax,'line')
        
        obj = ax.contour(X, Y, Z, levels, **kwargs)
        
        # check input
        if info is None: info = {}
        
        saveas = {'id'              :id,
                  'levels'          :levels,
                  **info,
                  **kwargs
                  }
        
        # save the drawn object to the file
        ax.draw_objs.setdefault(id,[]).append((obj,saveas))
        
        return obj
        
    # ======================================================================= # 
    def errorbar(self, id, x, y, yerr=None, xerr=None, fmt='', ecolor=None, 
                 elinewidth=None, capsize=None, barsabove=False, lolims=False, 
                 uplims=False, xlolims=False, xuplims=False, errorevery=1, 
                 capthick=None, *, data=None, unique=True, annot_label=None,
                 **kwargs):
        """
            Plot data.
            
            annot_label: list of annotations for each point
            other arguments: defaults for matplotlib.pyplot.plot
        """
        
        # get active for this style
        active_style = self.active
        
        # make new figure if needed 
        if active_style == 0:   
            self.figure()
            active_style = self.active
        fig = plt.figure(active_style)
        ax = fig.axes[0]
        
        # redraw old objects and lines
        if unique:  self._remove_drawn_object(ax,id)
        self._remove_drawn_object(ax,'line')
        
        # set up labelling of line objects for mouseover
        if 'label' in kwargs:
            label = kwargs.pop('label')
        else:
            label = ''
        
        # draw in active style 
        obj = plt.errorbar(x, y, yerr=yerr, xerr=xerr, fmt=fmt, ecolor=ecolor, 
                     elinewidth=elinewidth, capsize=capsize, 
                     barsabove=barsabove, lolims=lolims, uplims=uplims, 
                     xlolims=xlolims, xuplims=xuplims, errorevery=errorevery, 
                     capthick=capthick, data=data, **kwargs)

        # label the line object
        ax.lines[-1].set_label(label)
        
        # set the annotation
        if annot_label is not None: 
            ax.lines[-1].annot_label = annot_label
            
        saveas = {'id'          :id,
                  'fmt'         :fmt,
                  'color'       :color,
                  'ecolor'      :ecolor,
                  'elinewidth'  :elinewidth, 
                  'capsize'     :capsize, 
                  'barsabove'   :barsabove, 
                  'lolims'      :lolims, 
                  'uplims'      :uplims, 
                  'xlolims'     :xlolims,
                  'xuplims'     :xuplims,
                  'errorevery'  :errorevery, 
                  'capthick'    :capthick,
                  **kwargs,
                  }
            
        # save the drawn object to the file
        ax.draw_objs.setdefault(id,[]).append((obj,saveas))
        
        return obj
    
    # ======================================================================= #
    def figure(self,**kwargs):
        """
            Make new figure.
            
            kwargs: keyword arguments to pass to plt.figure
        """
        
        # make figure
        fig = plt.figure(**kwargs)
        
        # make events and save as canvas attribute
        fig.canvas.user_close = fig.canvas.mpl_connect('close_event', self._close_figure)
        fig.canvas.user_active = fig.canvas.mpl_connect('button_press_event', self._update_active_id)
        
        # set window name 
        fig.canvas.set_window_title('Figure %d' % (fig.number))
        
        # update lists
        self.plots.append(fig.number)
        self.active = fig.number
        
        # track drawn objects
        ax = plt.gca()
        if not hasattr(ax,'draw_objs'):
            ax.draw_objs = {}
        
        # setup saveas
        fig.saveas = fig.savefig
        fig.savefig = self.savefig_new
        
        return fig

    # ======================================================================= #
    def gca(self):
        if not self.plots: self.figure()
        return self._decorator(plt.gca)
    
    # ======================================================================= #
    def gcf(self):
        if not self.plots: self.figure()
        return self._decorator(plt.gcf)
    
    # ======================================================================= #
    def imshow(self, id, X, cmap=None, norm=None, aspect=None, interpolation=None, 
                alpha=None, vmin=None, vmax=None, origin=None, extent=None, 
                filternorm=1, filterrad=4.0, resample=None, url=None, data=None,
                unique=True, info=None, **kwargs):
        """
            unique: force only one of this id in the figure
            info: dict of other info to pass to plttracker, save for writing later
        """
        
        
        # get active for this style
        active_style = self.active
        
        # make new figure if needed 
        if active_style == 0:   
            self.figure()
            active_style = self.active
        fig = plt.figure(active_style)
        ax = fig.axes[0]
        
        # redraw old objects and lines
        if unique:  self._remove_drawn_object(ax,id)
        
        # set up labelling of line objects for mouseover
        if 'label' in kwargs:
            label = kwargs.pop('label')
        else:
            label = ''
        
        # draw in active style 
        obj = plt.imshow(X=X, cmap=cmap, norm=norm, aspect=aspect, 
                interpolation=interpolation, alpha=alpha, vmin=vmin, vmax=vmax, 
                origin=origin, extent=extent, filternorm=filternorm, 
                filterrad=filterrad, resample=resample, url=url, data=data,
                **kwargs)
            
        # check input
        if info is None: info = {}
            
        # save the drawn object to the file
        saveas = {'id'              :id,
                  'cmap'            :cmap,
                  'norm'            :norm,
                  'aspect'          :aspect,
                  'interpolation'   :interpolation,
                  'alpha'           :alpha,
                  'vmin'            :vmin,
                  'vmax'            :vmax,
                  'origin'          :origin,
                  'extent'          :extent,
                  'filternorm'      :filternorm,
                  'filterrad'       :filterrad,
                  'resample'        :resample,
                  'url'             :url,
                  **info,
                  **kwargs
                  }
        
        ax.draw_objs.setdefault(id,[]).append((obj,saveas))
        
        return obj
        
    # ======================================================================= #
    def legend(self,*args,**kwargs):
        self._decorator(plt.legend,*args,**kwargs)
        
    # ======================================================================= #
    def plot(self,id,*args,scalex=True,scaley=True,data=None,unique=True,**kwargs):
        """
            Plot data.
            
            other arguments: defaults for matplotlib.pyplot.plot
        """
        
        # get active for this style
        active_style = self.active
        
        # make new figure if needed 
        if active_style not in self.plots:   
            self.figure()
        
        # draw in active style 
        fig = plt.figure(active_style)
        ax = fig.axes[0]
        
        # redraw old objects and lines
        if unique:  self._remove_drawn_object(ax,id)
        self._remove_drawn_object(ax,'line')
        
        obj = plt.plot(*args,scalex=scalex, scaley=scaley, data=data,**kwargs)
        ax.draw_objs.setdefault(id,[]).append(obj)
        
        return obj

    # ======================================================================= #
    def savefig_new(self,filename):            
        """Save figure, alongside yaml file with figure details"""
        fig = self.gcf()
        
        # get paramters for drawn objs
        draw_objs = self.gca().draw_objs.values()
        objs = []
        for drawo in draw_objs:
            
            for i,draw in enumerate(drawo):
                
                if '.bccd/' in draw[1]['id']:
                    draw[1]['id'] = draw[1]['id'].split('.bccd/')[1]
                
                objs.append(draw[1])
        
        # write text file with details
        yaml_file = os.path.splitext(filename)[0]+'.yaml'
        with open(yaml_file,'w') as fid:    
            fid.write(yaml.dump(objs))
        
        # write figure
        fig.saveas(filename)
        
    # ======================================================================= #
    def text(self,*args,id=None,unique=True,**kwargs):
        return self._decorator(plt.text,*args,id=id,unique=unique,**kwargs)

    # ======================================================================= #
    def tight_layout(self,*args,**kwargs):
        return self._decorator(plt.tight_layout,*args,**kwargs)

    # ======================================================================= #
    def xlabel(self,*args,**kwargs):
        return self._decorator(plt.xlabel,*args,**kwargs)
    
    # ======================================================================= #
    def xlim(self,*args,**kwargs):
        return self._decorator(plt.xlim,*args,**kwargs)
    
    # ======================================================================= #
    def xticks(self,*args,**kwargs):
        return self._decorator(plt.xticks,*args,**kwargs)
    
    # ======================================================================= #
    def ylabel(self,*args,**kwargs):
        return self._decorator(plt.ylabel,*args,**kwargs)
    
    # ======================================================================= #
    def ylim(self,*args,**kwargs):
        return self._decorator(plt.ylim,*args,**kwargs)
    
    # ======================================================================= #
    def yticks(self,*args,**kwargs):
        return self._decorator(plt.yticks,*args,**kwargs)
    
    # ======================================================================= #
    def zlabel(self,*args,**kwargs):
        return self._decorator(plt.zlabel,*args,**kwargs)
    
    # ======================================================================= #
    def zlim(self,*args,**kwargs):
        return self._decorator(plt.zlim,*args,**kwargs)
    
    # ======================================================================= #
    def zticks(self,*args,**kwargs):
        return self._decorator(plt.zticks,*args,**kwargs)
    
