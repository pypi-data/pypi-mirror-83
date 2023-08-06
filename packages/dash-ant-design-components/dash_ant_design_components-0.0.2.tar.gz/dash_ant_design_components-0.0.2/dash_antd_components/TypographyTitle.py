# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class TypographyTitle(Component):
    """A TypographyTitle component.
Basic text writing, including headings, body text, lists, and more.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): The children of this component
- id (string; optional): The ID of this component, used to identify dash components in callbacks.
The ID needs to be unique across all of the components in an app.
- className (string; optional): Container className
- code (boolean; optional): Code style
- copyable (boolean | dict; optional): Whether to be copyable, customize it via setting an object
- delete (boolean; optional): Deleted line style
- disabled (boolean; optional): Disabled content
- editable (boolean | dict; optional): If editable. Can control edit state when is object
- ellipsis (boolean | dict; optional): Display ellipsis when text overflows, can configure rows and expandable by using object
- level (number; optional): Set content importance. Match with h1, h2, h3, h4, h5
- mark (boolean; optional): Marked style
- strong (boolean; optional): Bold style
- type (a value equal to: 'secondary', 'success', 'warning', 'danger'; optional): Content type
- underline (boolean; optional): Underlined style	boolean	false"""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, className=Component.UNDEFINED, code=Component.UNDEFINED, copyable=Component.UNDEFINED, delete=Component.UNDEFINED, disabled=Component.UNDEFINED, editable=Component.UNDEFINED, ellipsis=Component.UNDEFINED, level=Component.UNDEFINED, mark=Component.UNDEFINED, strong=Component.UNDEFINED, type=Component.UNDEFINED, underline=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'className', 'code', 'copyable', 'delete', 'disabled', 'editable', 'ellipsis', 'level', 'mark', 'strong', 'type', 'underline']
        self._type = 'TypographyTitle'
        self._namespace = 'dash_antd_components'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'className', 'code', 'copyable', 'delete', 'disabled', 'editable', 'ellipsis', 'level', 'mark', 'strong', 'type', 'underline']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(TypographyTitle, self).__init__(children=children, **args)
