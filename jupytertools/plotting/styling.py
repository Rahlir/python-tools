"""Functions to be used in Jupyter Notebook"""

import cycler
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sb
from jupyterthemes import jtplot

__all__ = ['set_default_style', 'set_figsize', 'get_style_func', 'gruvbox_style', 'seaborn_style', 'default_style',
           'minor_grid_color', 'current_style', 'folder_to_save', 'current_color_array', 'plot_current_color_cycle',
           'save_to_disk']


class PlottingStyle:
    def __init__(self, default_style_name):
        self.default_style = default_style_name
        self.current_style = ''
        self.minor_grid_color = mpl.rcParams["grid.color"]
        self.folder_to_save = "figures"
        self.figsize = mpl.rcParams["figure.figsize"]


style = PlottingStyle("gruvbox")


def set_default_style(style_name, set_as_current=True):
    """Set style with the given name as the default style. Currently,
    there are two styles available: 'gruvbox' and 'seaborn'

    Parameters
    ----------
    style_name : string containing the style to be used as default
    set_as_current: set the given default style as the current style.
        Default is `True`, optional
    """
    style.default_style = style_name
    if set_as_current:
        default_style()


def set_figsize(width, height):
    """Set new size for figures in px. Default is 17.5 x 13.0

    Parameters
    ----------
    width : new width of figures in px
    height : new height of figures in px
    """
    style.figsize = (width, height)
    func = get_style_func(current_style())
    func()


def get_style_func(style_name):
    """Get function that sets the style with given name

    Parameters
    ----------
    style_name : name of the style

    Returns
    -------
    func: function that sets the style of the given name

    """
    try:
        function_name = "{:s}_style".format(style_name)
        func_obj = globals()[function_name]
        return func_obj
    except KeyError:
        raise KeyError("The style with the name: {:s} doesn't exist".format(style_name))


def gruvbox_style(pallete="higher_contrast"):
    """Set the current plotting style to gruvbox with higher contrast
    pallete
    """
    palletes = {
        "higher_contrast": [
            '#3572C6',
            '#83a83b',
            '#c44e52',
            '#d5c4a1',
            '#8172b2',
            '#b57614',
            '#8ec07c',
            '#ff711a',
            '#d3869b',
            '#6C7A89',
            '#77BEDB',
            '#4168B7',
            '#27ae60',
            '#e74c3c',
            '#ff914d',
            '#bc89e0',
            '#3498db',
            '#fabd2f',
            '#fb4934',
            '#b16286',
            '#83a598',
            '#fe8019',
            '#b8bb26',
            '#a89984'
        ],
        "bright": [
            '#77BEDB',
            '#fb4934',
            '#8ec07c',
            '#ff914d',
            '#bc89e0',
            '#fabd2f',
            '#fbf1c7',
            '#3498db'
        ],
        "paired": [
            '#77BEDB',
            '#4168B7',
            '#8ec07c',
            '#b8bb26',
            '#d3869b',
            '#fb4934',
            '#bdae93',
            '#ebdbb2'
        ]
    }

    new_cycler = cycler.cycler("color", palletes[pallete])

    jtplot.style(theme='gruvboxd', context='notebook', figsize=style.figsize)
    mpl.rcParams["axes.prop_cycle"] = new_cycler
    mpl.rcParams["axes.axisbelow"] = True
    style.minor_grid_color = "#32302f"
    style.current_style = "gruvbox"


def seaborn_style(pallete=None):
    """Set the current plotting style to seaborn

    Parameters
    ----------
    pallete : pallete of the seaborn style, optional
    """
    sb.set(style='darkgrid', rc={'figure.figsize': [*style.figsize]})
    if pallete is not None:
        sb.set_palette(pallete, 12)
    style.minor_grid_color = "#f4f4f8"
    style.current_style = "seaborn"


def default_style():
    """Set the default style as the current style"""
    if style.default_style == 'seaborn':
        seaborn_style()
    elif style.default_style == 'gruvbox':
        gruvbox_style()
    else:
        jtplot.reset()


def minor_grid_color():
    """Return the color of the minor grid for the current plotting style

    Returns
    -------
    minor_grid_color: hex value of the minor grid color for the current style
    """
    return style.minor_grid_color


def current_style():
    """Return the name of the current plotting style

    Returns
    -------
    current_style: name of the current plotting style
    """
    return style.current_style


def folder_to_save(fname=None):
    """Set the folder to be used for saving figures. If no argument is given,
    then the current folder used for saving figures is returned.

    Parameters
    ----------
    fname : folder name where figures should be saved, optional

    Returns
    -------
    fname : name of the folder where figures are currently stored
    """
    if fname is not None:
        style.folder_to_save = fname
    return style.folder_to_save


def save_to_disk(fname, dpi=None, format='png'):
    """Save the current figure to disk

    Parameters
    ----------
    fname : name of the file for the saved figure
    dpi : dpi of the saved figure, when not specified, dpi is calculated to optimize
        for 4K monitors, optional
    format : format for the saved figure, such as 'png', 'pdf', etc. Default is 'png',
        optional
    """
    if dpi is None:
        x, y = mpl.rcParams["figure.figsize"]
        dpi = max(4096.0/x, 2160.0/y)

    if style.current_style == "seaborn":
        facecolor = "white"
        edgecolor = "white"
    else:
        styleMap, clist = jtplot.get_theme_style("gruvboxd")
        facecolor = styleMap["figureFace"]
        edgecolor = styleMap["figureFace"]

    prefix = style.folder_to_save

    plt.savefig('{:s}/{:s}.{:s}'.format(prefix, fname, format), dpi=dpi,
                facecolor=facecolor, edgecolor=edgecolor, format=format)


def current_color_array():
    """Return array of colors currently used for plotting
    Returns
    -------
    colors : array of hex values of colors used in the current color cycle for plotting

    """
    prop_cycle = plt.rcParams['axes.prop_cycle']
    return prop_cycle.by_key()['color']


def plot_current_color_cycle():
    """Plots color cycle currently in use"""
    colors = current_color_array()
    sb.palplot(colors)
