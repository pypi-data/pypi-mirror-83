# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class GridRow(Component):
    """A GridRow component.
24 Grids System.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): The children of this component
- id (string; optional): The ID of this component, used to identify dash components in callbacks.
The ID needs to be unique across all of the components in an app.
- className (string; optional): Container className
- align (a value equal to: 'top', 'middle', 'bottom'; optional): Vertical alignment
- gutter (number | dict | list; optional): Spacing between grids, could be a number or a object like { xs: 8, sm: 16, md: 24}.
Or you can use array to make horizontal and vertical spacing work at the same time [horizontal, vertical]
- justify (a value equal to: 'start', 'end', 'center', 'space-around', 'space-between'; optional): Horizontal arrangement"""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, className=Component.UNDEFINED, align=Component.UNDEFINED, gutter=Component.UNDEFINED, justify=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'className', 'align', 'gutter', 'justify']
        self._type = 'GridRow'
        self._namespace = 'dash_antd_components'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'className', 'align', 'gutter', 'justify']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(GridRow, self).__init__(children=children, **args)
