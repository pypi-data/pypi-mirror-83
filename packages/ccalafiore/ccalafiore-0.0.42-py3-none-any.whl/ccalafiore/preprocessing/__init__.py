
__all__ = ['axes_to_variables_table', 'reorder_trials', 'reshape',
           'rotate_indexes', 'variables_table_to_axes']


def initiate(names_submodules_raw=None):

    if names_submodules_raw is None:
        names_submodules = __all__
    elif isinstance(names_submodules_raw, str):
        names_submodules = [names_submodules_raw]
    else:
        names_submodules = names_submodules_raw

    # M = len(names_submodules)

    for name_m in names_submodules:

        if name_m == 'axes_to_variables_table':
            try:
                axes_to_variables_table
            except NameError:
                from . import axes_to_variables_table
                globals().update(axes_to_variables_table=axes_to_variables_table)

        elif name_m == 'reorder_trials':
            try:
                reorder_trials
            except NameError:
                from . import reorder_trials
                globals().update(reorder_trials=reorder_trials)

        elif name_m == 'reshape':
            try:
                reshape
            except NameError:
                from . import reshape
                globals().update(reshape=reshape)

        elif name_m == 'rotate_indexes':
            try:
                rotate_indexes
            except NameError:
                from . import rotate_indexes
                globals().update(rotate_indexes=rotate_indexes)

        elif name_m == 'variables_table_to_axes':
            try:
                variables_table_to_axes
            except NameError:
                from . import variables_table_to_axes
                globals().update(variables_table_to_axes=variables_table_to_axes)

        else:
            raise ValueError('Unknown submodule "{}"'.format(name_m))
