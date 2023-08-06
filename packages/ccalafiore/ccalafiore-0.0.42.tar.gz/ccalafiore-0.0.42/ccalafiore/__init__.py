__version__ = '000.000.042'
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
            try:
                array
            except NameError:
                from . import array
                globals().update(array=array)

        elif name_m == 'check_args':
            try:
                check_args
            except NameError:
                from . import check_args
                globals().update(check_args=check_args)

        elif name_m == 'clock':
            try:
                clock
            except NameError:
                from . import clock
                globals().update(clock=clock)

        elif name_m == 'combinations':
            try:
                combinations
            except NameError:
                from . import combinations
                globals().update(combinations=combinations)

        elif name_m == 'directory':
            try:
                directory
            except NameError:
                from . import directory
                globals().update(directory=directory)

        elif name_m == 'download':
            try:
                download
            except NameError:
                from . import download
                globals().update(download=download)

        elif name_m == 'format_args':
            try:
                format_args
            except NameError:
                from . import format_args
                globals().update(format_args=format_args)

        elif name_m == 'maths':
            try:
                maths
            except NameError:
                from . import maths
                globals().update(maths=maths)

        elif name_m == 'mixamo':
            try:
                mixamo
            except NameError:
                from . import mixamo
                globals().update(mixamo=mixamo)

        elif name_m == 'nn':
            try:
                nn
            except NameError:
                from . import nn
                globals().update(nn=nn)

        elif name_m == 'plot':
            try:
                plot
            except NameError:
                from . import plot
                globals().update(plot=plot)

        elif name_m == 'preprocessing':
            try:
                preprocessing
            except NameError:
                from . import preprocessing
                globals().update(preprocessing=preprocessing)

        elif name_m == 'shutdown':
            try:
                shutdown
            except NameError:
                from . import shutdown
                globals().update(shutdown=shutdown)

        elif name_m == 'stats':
            try:
                stats
            except NameError:
                from . import stats
                globals().update(stats=stats)

        elif name_m == 'stimulation':
            try:
                stimulation
            except NameError:
                from . import stimulation
                globals().update(stimulation=stimulation)

        elif name_m == 'strings':
            try:
                strings
            except NameError:
                from . import strings
                globals().update(strings=strings)

        elif name_m == 'txt':
            try:
                txt
            except NameError:
                from . import txt
                globals().update(txt=txt)

        elif name_m == 'hacks':
            try:
                hacks
            except NameError:
                from . import hacks
                globals().update(hacks=hacks)

        else:
            raise ValueError('Unknown submodule "{}"'.format(name_m))



