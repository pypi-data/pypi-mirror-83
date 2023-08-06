# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Tooltip(Component):
    """A Tooltip component.
Handling the overall sidebar of a page.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): The children of this component
- id (string; optional): The ID of this component, used to identify dash components in callbacks.
The ID needs to be unique across all of the components in an app.
- title (a list of or a singular dash component, string or number; optional): The text shown in the tooltip
- align (dict; optional): This value will be merged into placement's config, please refer to the settings rc-tooltip
- arrowPointAtCenter (boolean; optional): Whether the arrow is pointed at the center of target
- autoAdjustOverflow (boolean; optional): Whether to adjust popup placement automatically when popup is off screen
- color (string; optional): The background color
- destroyTooltipOnHide (boolean; optional): Whether destroy tooltip when hidden, parent container of tooltip will be destroyed when keepParent is false
- mouseEnterDelay (number; optional): Delay in seconds, before tooltip is shown on mouse enter
- mouseLeaveDelay (number; optional): Delay in seconds, before tooltip is hidden on mouse leave
- overlayClassName (string; optional): Class name of the tooltip card
- placement (a value equal to: 'top', 'left', 'right', 'bottom', 'topLeft', 'topRight', 'bottomLeft', 'bottomRight', 'leftTop', 'leftBottom', 'rightTop', 'rightBottom'; optional): The position of the tooltip relative to the target
- trigger (a value equal to: 'hover', 'focus', 'click', 'contextMenu' | list of a value equal to: 'hover', 'focus', 'click', 'contextMenu's; optional): Tooltip trigger mode. Could be multiple by passing an array
- visible (boolean; optional): Whether the floating tooltip card is visible or not"""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, title=Component.UNDEFINED, align=Component.UNDEFINED, arrowPointAtCenter=Component.UNDEFINED, autoAdjustOverflow=Component.UNDEFINED, color=Component.UNDEFINED, destroyTooltipOnHide=Component.UNDEFINED, mouseEnterDelay=Component.UNDEFINED, mouseLeaveDelay=Component.UNDEFINED, overlayClassName=Component.UNDEFINED, placement=Component.UNDEFINED, trigger=Component.UNDEFINED, visible=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'title', 'align', 'arrowPointAtCenter', 'autoAdjustOverflow', 'color', 'destroyTooltipOnHide', 'mouseEnterDelay', 'mouseLeaveDelay', 'overlayClassName', 'placement', 'trigger', 'visible']
        self._type = 'Tooltip'
        self._namespace = 'dash_antd_components'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'title', 'align', 'arrowPointAtCenter', 'autoAdjustOverflow', 'color', 'destroyTooltipOnHide', 'mouseEnterDelay', 'mouseLeaveDelay', 'overlayClassName', 'placement', 'trigger', 'visible']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Tooltip, self).__init__(children=children, **args)
