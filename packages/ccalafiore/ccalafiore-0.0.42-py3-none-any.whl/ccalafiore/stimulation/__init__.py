
__all__ = ['display']


def initiate(names_submodules_raw=None):

    if names_submodules_raw is None:
        names_submodules = __all__
    elif isinstance(names_submodules_raw, str):
        names_submodules = [names_submodules_raw]
    else:
        names_submodules = names_submodules_raw

    # M = len(names_submodules)

    for name_m in names_submodules:

        if name_m == 'display':
            try:
                display
            except NameError:
                from . import display
                globals().update(display=display)
        else:
            raise ValueError('Unknown submodule "{}"'.format(name_m))
