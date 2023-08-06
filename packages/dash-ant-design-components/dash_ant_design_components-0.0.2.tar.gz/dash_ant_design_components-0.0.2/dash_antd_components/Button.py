# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Button(Component):
    """A Button component.
To trigger an operation.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): The children of this component
- id (string; optional): The ID of this component, used to identify dash components in callbacks.
The ID needs to be unique across all of the components in an app.
- n_clicks (number; default 0): An integer that represents the number of times
that this element has been clicked on.
- n_clicks_timestamp (number; default -1): Use of *_timestamp props has been deprecated in Dash in favour of dash.callback_context.
See "How do I determine which Input has changed?" in the Dash FAQs https://dash.plot.ly/faqs.

An integer that represents the time (in ms since 1970)
at which n_clicks changed. This can be used to tell
which button was changed most recently.
- block (boolean; optional): Option to fit button width to its parent width
- danger (boolean; optional): Set the danger status of button
- disabled (boolean; optional): Disabled state of button
- ghost (boolean; optional): Make background transparent and invert text and border colors
- href (string; optional): Redirect url of link button
- htmlType (a value equal to: 'submit', 'reset', 'button'; optional): Set the original html type of button, see: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/button#attr-type
- icon (string; optional): Set the icon name of button
- tooltip (string; optional): Set the tooltip title of button
- loading (boolean | number; optional): Set the loading status of button
- shape (a value equal to: 'circle', 'round'; optional): Can be set button shape
- size (a value equal to: 'large', 'middle', 'small'; optional): Set the size of button
- target (string; optional): Same as target attribute of a, works when href is specified
- type (a value equal to: 'primary', 'ghost', 'dashed', 'link', 'text', 'default'; optional): Can be set to primary / ghost / dashed / link / text / default"""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, n_clicks=Component.UNDEFINED, n_clicks_timestamp=Component.UNDEFINED, block=Component.UNDEFINED, danger=Component.UNDEFINED, disabled=Component.UNDEFINED, ghost=Component.UNDEFINED, href=Component.UNDEFINED, htmlType=Component.UNDEFINED, icon=Component.UNDEFINED, tooltip=Component.UNDEFINED, loading=Component.UNDEFINED, shape=Component.UNDEFINED, size=Component.UNDEFINED, target=Component.UNDEFINED, type=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'n_clicks', 'n_clicks_timestamp', 'block', 'danger', 'disabled', 'ghost', 'href', 'htmlType', 'icon', 'tooltip', 'loading', 'shape', 'size', 'target', 'type']
        self._type = 'Button'
        self._namespace = 'dash_antd_components'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'n_clicks', 'n_clicks_timestamp', 'block', 'danger', 'disabled', 'ghost', 'href', 'htmlType', 'icon', 'tooltip', 'loading', 'shape', 'size', 'target', 'type']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Button, self).__init__(children=children, **args)
