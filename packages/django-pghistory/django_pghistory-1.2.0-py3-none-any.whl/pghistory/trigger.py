from django.db import models
import pgtrigger


def _get_pgh_obj_pk_col(history_model):
    """
    Returns the column name of the PK field tracked by the history model
    """
    return history_model._meta.get_field(
        'pgh_obj'
    ).related_model._meta.pk.column


class Event(pgtrigger.Trigger):
    """
    Events a model with a label when a condition happens
    """

    label = None
    snapshot = 'NEW'
    event_model = None
    when = pgtrigger.After

    def __init__(self, label=None, snapshot=None, event_model=None, **kwargs):
        super().__init__(**kwargs)

        self.label = label or self.label
        if not self.label:  # pragma: no cover
            raise ValueError('Must provide "label"')

        self.event_model = event_model or self.event_model
        if not self.event_model:  # pragma: no cover
            raise ValueError('Must provide "event_model"')

        self.snapshot = snapshot or self.snapshot
        if not self.snapshot:  # pragma: no cover
            raise ValueError('Must provide "snapshot"')

    def get_func(self, model):
        fields = {
            f.column: f'{self.snapshot}."{f.column}"'
            for f in self.event_model._meta.fields
            if not isinstance(f, models.AutoField)
            and hasattr(self.event_model.pgh_tracked_model, f.name)
        }
        fields['pgh_created_at'] = 'NOW()'
        fields['pgh_label'] = f"'{self.label}'"

        if hasattr(self.event_model, 'pgh_obj'):
            fields[
                'pgh_obj_id'
            ] = f'NEW."{_get_pgh_obj_pk_col(self.event_model)}"'

        if hasattr(self.event_model, 'pgh_context'):
            fields['pgh_context_id'] = '_pgh_attach_context()'

        cols = ', '.join(f'"{col}"' for col in fields)
        vals = ', '.join(val for val in fields.values())
        return f'''
            INSERT INTO "{self.event_model._meta.db_table}"
                ({cols}) VALUES ({vals});
            RETURN NULL;
        '''
