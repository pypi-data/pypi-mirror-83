# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class ButtonGroup(Component):
    """A ButtonGroup component.
Deprecated Button Group

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): The children of this component
- id (string; optional): The ID of this component, used to identify dash components in callbacks.
The ID needs to be unique across all of the components in an app.
- size (a value equal to: 'large', 'middle', 'small'; optional): Set the size of button"""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, size=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'size']
        self._type = 'ButtonGroup'
        self._namespace = 'dash_antd_components'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'size']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(ButtonGroup, self).__init__(children=children, **args)
