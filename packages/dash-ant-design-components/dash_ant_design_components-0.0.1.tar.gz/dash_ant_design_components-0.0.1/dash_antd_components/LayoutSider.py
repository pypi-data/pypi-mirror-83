# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class LayoutSider(Component):
    """A LayoutSider component.
Handling the overall sidebar of a page.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): The children of this component
- id (string; optional): The ID of this component, used to identify dash components in callbacks.
The ID needs to be unique across all of the components in an app.
- className (string; optional): Container className
- collapsed (boolean; optional): To set the current status
- collapsedWidth (number; optional): Width of the collapsed sidebar, by setting to 0 a special trigger will appear
- collapsible (boolean; optional): Whether can be collapsed
- reverseArrow (boolean; optional): Reverse direction of arrow, for a sider that expands from the right
- theme (a value equal to: 'light', 'dark'; optional): Color theme of the sidebar
- trigger (a list of or a singular dash component, string or number; optional): Specify the customized trigger, set to null to hide the trigger
- width (number; optional): Width of the sidebar"""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, className=Component.UNDEFINED, collapsed=Component.UNDEFINED, collapsedWidth=Component.UNDEFINED, collapsible=Component.UNDEFINED, reverseArrow=Component.UNDEFINED, theme=Component.UNDEFINED, trigger=Component.UNDEFINED, width=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'className', 'collapsed', 'collapsedWidth', 'collapsible', 'reverseArrow', 'theme', 'trigger', 'width']
        self._type = 'LayoutSider'
        self._namespace = 'dash_antd_components'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'className', 'collapsed', 'collapsedWidth', 'collapsible', 'reverseArrow', 'theme', 'trigger', 'width']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(LayoutSider, self).__init__(children=children, **args)
