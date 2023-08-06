
__all__ = ['descriptive', 'paired_t_test', 'unpaired_t_test']


def initiate(names_submodules_raw=None):

    if names_submodules_raw is None:
        names_submodules = __all__
    elif isinstance(names_submodules_raw, str):
        names_submodules = [names_submodules_raw]
    else:
        names_submodules = names_submodules_raw

    # M = len(names_submodules)

    for name_m in names_submodules:

        if name_m == 'descriptive':
            try:
                descriptive
            except NameError:
                from . import descriptive
                globals().update(descriptive=descriptive)

        elif name_m == 'paired_t_test':
            try:
                paired_t_test
            except NameError:
                from . import paired_t_test
                globals().update(paired_t_test=paired_t_test)

        elif name_m == 'unpaired_t_test':
            try:
                unpaired_t_test
            except NameError:
                from . import unpaired_t_test
                globals().update(unpaired_t_test=unpaired_t_test)

        else:
            raise ValueError('Unknown submodule "{}"'.format(name_m))
