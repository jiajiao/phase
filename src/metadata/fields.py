from django.db import models


def get_choices_from_list(list_index):
    """Creates a list of values from data in db."""
    from .models import ListEntry
    values = ListEntry.objects \
        .filter(values_list__index=list_index) \
        .values_list('index', 'value')
    return values


class ConfigurableChoiceField(models.CharField):
    def __init__(self, list_index, *args, **kwargs):
        self.list_index = list_index
        defaults = {
            'max_length': 50,
            'choices': None,
        }
        defaults.update(kwargs)
        super(ConfigurableChoiceField, self).__init__(*args, **defaults)

    def _get_choices(self):
        if self._choices is None:
            self._choices = get_choices_from_list(self.list_index)

        return self._choices