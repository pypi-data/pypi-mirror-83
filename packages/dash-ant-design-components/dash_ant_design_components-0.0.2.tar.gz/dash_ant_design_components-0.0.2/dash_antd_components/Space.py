# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Space(Component):
    """A Space component.
Handling the overall sidebar of a page.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): The children of this component
- id (string; optional): The ID of this component, used to identify dash components in callbacks.
The ID needs to be unique across all of the components in an app.
- className (string; optional): Container className
- align (a value equal to: 'start', 'end', 'center', 'baseline'; optional): Align items
- direction (a value equal to: 'horizontal', 'vertical'; optional): The space direction
- size (a value equal to: 'small', 'middle', 'large' | number; optional): The space size
- split (a list of or a singular dash component, string or number; optional): Set split"""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, className=Component.UNDEFINED, align=Component.UNDEFINED, direction=Component.UNDEFINED, size=Component.UNDEFINED, split=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'className', 'align', 'direction', 'size', 'split']
        self._type = 'Space'
        self._namespace = 'dash_antd_components'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'className', 'align', 'direction', 'size', 'split']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Space, self).__init__(children=children, **args)
