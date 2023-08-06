# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class GridCol(Component):
    """A GridCol component.
24 Grids System.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): The children of this component
- id (string; optional): The ID of this component, used to identify dash components in callbacks.
The ID needs to be unique across all of the components in an app.
- className (string; optional): Container className
- offset (number; optional): The number of cells to offset Col from the left
- order (number; optional): Raster order
- pull (number; optional): The number of cells that raster is moved to the left
- push (number; optional): The number of cells that raster is moved to the right
- span (number; optional): Raster number of cells to occupy, 0 corresponds to display: none
- xs (number; optional): screen < 576px and also default setting, could be a span value or an object containing above props	number | object	-
- sm (number; optional): screen ≥ 576px, could be a span value or an object containing above props	number | object	-
- md (number; optional): screen ≥ 768px, could be a span value or an object containing above props	number | object	-
- lg (number; optional): screen ≥ 992px, could be a span value or an object containing above props	number | object	-
- xl (number; optional): screen ≥ 1200px, could be a span value or an object containing above props	number | object	-
- xxl (number; optional): screen ≥ 1600px, could be a span value or an object containing above props	number | object"""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, className=Component.UNDEFINED, offset=Component.UNDEFINED, order=Component.UNDEFINED, pull=Component.UNDEFINED, push=Component.UNDEFINED, span=Component.UNDEFINED, xs=Component.UNDEFINED, sm=Component.UNDEFINED, md=Component.UNDEFINED, lg=Component.UNDEFINED, xl=Component.UNDEFINED, xxl=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'className', 'offset', 'order', 'pull', 'push', 'span', 'xs', 'sm', 'md', 'lg', 'xl', 'xxl']
        self._type = 'GridCol'
        self._namespace = 'dash_antd_components'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'className', 'offset', 'order', 'pull', 'push', 'span', 'xs', 'sm', 'md', 'lg', 'xl', 'xxl']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(GridCol, self).__init__(children=children, **args)
