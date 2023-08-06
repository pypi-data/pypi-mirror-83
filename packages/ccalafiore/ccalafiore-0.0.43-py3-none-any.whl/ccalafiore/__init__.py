__version__ = '000.000.043'
__author__ = 'Calafiore Carmelo'
__author_email__ = 'c.calafiore@essex.ac.uk'
__maintainer_email__ = 'c.calafiore@essex.ac.uk'
__all__ = [
    'array', 'check_args', 'clock', 'combinations', 'directory', 'download',
    'format_args', 'maths', 'mixamo', 'nn', 'plot', 'preprocessing', 'shutdown', 'stats',
    'stimulation', 'strings', 'txt']


def initiate(names_submodules_raw=None):

    if names_submodules_raw is None:
        names_submodules = __all__
    elif isinstance(names_submodules_raw, str):
        names_submodules = [names_submodules_raw]
    else:
        names_submodules = names_submodules_raw

    # M = len(names_submodules)

    for name_m in names_submodules:

        if name_m == 'array':
            from . import array
            globals().update(array=array)

        elif name_m == 'check_args':
            from . import check_args
            globals().update(check_args=check_args)

        elif name_m == 'clock':
            from . import clock
            globals().update(clock=clock)

        elif name_m == 'combinations':
            from . import combinations
            globals().update(combinations=combinations)

        elif name_m == 'directory':
            from . import directory
            globals().update(directory=directory)

        elif name_m == 'download':
            from . import download
            globals().update(download=download)

        elif name_m == 'format_args':
            from . import format_args
            globals().update(format_args=format_args)

        elif name_m == 'maths':
            from . import maths
            globals().update(maths=maths)

        elif name_m == 'mixamo':
            from . import mixamo
            globals().update(mixamo=mixamo)

        elif name_m == 'nn':
            from . import nn
            globals().update(nn=nn)

        elif name_m == 'plot':
            from . import plot
            globals().update(plot=plot)

        elif name_m == 'preprocessing':
            from . import preprocessing
            globals().update(preprocessing=preprocessing)

        elif name_m == 'shutdown':
            from . import shutdown
            globals().update(shutdown=shutdown)

        elif name_m == 'stats':
            from . import stats
            globals().update(stats=stats)

        elif name_m == 'stimulation':
            from . import stimulation
            globals().update(stimulation=stimulation)

        elif name_m == 'strings':
            from . import strings
            globals().update(strings=strings)

        elif name_m == 'txt':

            from . import txt
            globals().update(txt=txt)

        elif name_m == 'hacks':
            from . import hacks
            globals().update(hacks=hacks)

        else:
            raise ValueError('Unknown submodule "{}"'.format(name_m))



