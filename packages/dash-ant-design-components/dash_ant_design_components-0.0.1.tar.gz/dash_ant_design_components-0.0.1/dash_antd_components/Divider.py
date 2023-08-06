# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Divider(Component):
    """A Divider component.
Handling the overall sidebar of a page.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): The children of this component
- id (string; optional): The ID of this component, used to identify dash components in callbacks.
The ID needs to be unique across all of the components in an app.
- className (string; optional): Container className
- dashed (boolean; optional): Whether line is dashed
- orientation (a value equal to: 'left', 'right', 'center'; optional): The position of title inside divider
- plain (boolean; optional): Divider text show as plain style
- type (a value equal to: 'horizontal', 'vertical'; optional): The direction type of divider"""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, className=Component.UNDEFINED, dashed=Component.UNDEFINED, orientation=Component.UNDEFINED, plain=Component.UNDEFINED, type=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'className', 'dashed', 'orientation', 'plain', 'type']
        self._type = 'Divider'
        self._namespace = 'dash_antd_components'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'className', 'dashed', 'orientation', 'plain', 'type']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Divider, self).__init__(children=children, **args)
