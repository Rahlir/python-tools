"""Functions to be used in Jupyter Notebook"""

import cycler
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sb
from jupyterthemes import jtplot

__all__ = ['gruvbox_style', 'seaborn_style', 'default_style', 'minor_grid_color',
           'current_style', 'folder_to_save', 'save_to_disk']


class PlottingStyle:
    def __init__(self, default_style_name):
        self.default_style = default_style_name
        self.current_style = ''
        self.minor_grid_color = mpl.rcParams["grid.color"]
        self.folder_to_save = "figures"


style = PlottingStyle("gruvbox")


def gruvbox_style():
    higher_constrast_pallete = [
        '#3572C6',
        '#83a83b',
        '#c44e52',
        '#a89984',
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
        '#b8bb26'
    ]
    higher_contrast_cycler = cycler.cycler("color", higher_constrast_pallete)

    jtplot.style(theme='gruvboxd', context='notebook', figsize=(17.5, 13.0))
    mpl.rcParams["axes.prop_cycle"] = higher_contrast_cycler
    mpl.rcParams["axes.axisbelow"] = True
    style.minor_grid_color = "#32302f"
    style.current_style = "gruvbox"


def seaborn_style(pallete=None):
    sb.set(style='darkgrid', rc={'figure.figsize': [17.5, 13.0]})
    if pallete is not None:
        sb.set_palette(pallete)
    style.minor_grid_color = "#f4f4f8"
    style.current_style = "seaborn"


def default_style():
    if style.default_style == 'seaborn':
        seaborn_style()
    elif style.default_style == 'gruvbox':
        gruvbox_style()
    else:
        jtplot.reset()


def minor_grid_color():
    return style.minor_grid_color


def current_style():
    return style.current_style


def folder_to_save(fname=None):
    if fname is None:
        return style.folder_to_save
    style.folder_to_save = fname


def save_to_disk(fname, dpi=None, format='png'):
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


if __name__ != "__main__":
    default_style()
