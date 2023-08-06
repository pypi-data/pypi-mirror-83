# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class MultiRangeInput(Component):
    """A MultiRangeInput component.


Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks.
- labels (list; optional): A label that will be printed when this component is rendered.
- values (list; optional): Values of the range sliders
- values_mouse_up (list; optional): Values of the range sliders on mouse-up
- value (number; optional): The value displayed in the input."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, labels=Component.UNDEFINED, values=Component.UNDEFINED, values_mouse_up=Component.UNDEFINED, value=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'labels', 'values', 'values_mouse_up', 'value']
        self._type = 'MultiRangeInput'
        self._namespace = 'denis_dash_components'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'labels', 'values', 'values_mouse_up', 'value']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(MultiRangeInput, self).__init__(**args)
