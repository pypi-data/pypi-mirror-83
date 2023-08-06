# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Icon(Component):
    """An Icon component.
Semantic vector graphics.

Keyword arguments:
- id (string; optional): The ID of this component, used to identify dash components in callbacks.
The ID needs to be unique across all of the components in an app.
- name (string; optional): The computed class name of the svg element
- className (string; optional): The computed class name of the svg element
- fill (string; optional): Define the color used to paint the svg element
- height (string | number; optional): The height of the svg element
- width (string | number; optional): The width of the svg element"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, name=Component.UNDEFINED, className=Component.UNDEFINED, fill=Component.UNDEFINED, height=Component.UNDEFINED, width=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'name', 'className', 'fill', 'height', 'width']
        self._type = 'Icon'
        self._namespace = 'dash_antd_components'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'name', 'className', 'fill', 'height', 'width']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Icon, self).__init__(**args)
