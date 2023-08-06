import logging

from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from wagtail.admin.edit_handlers import BaseChooserPanel

from .widgets import AdminPollChooser

logger = logging.getLogger(__name__)


class BasePollChooserPanel(BaseChooserPanel):
    object_type_name = "item"

    _target_model = None

    @classmethod
    def widget_overrides(cls):
        target_model = cls.target_model()
        ct = ContentType.objects.get_for_model(target_model)
        return {cls.field_name: AdminPollChooser(content_type=ct)}  # noqa

    @classmethod
    def target_model(cls):
        if cls._target_model is None:
            cls._target_model = cls.model._meta.get_field(cls.field_name).related_model  # noqa

        return cls._target_model

    def render_as_field(self):
        instance_obj = self.get_chosen_item()
        return mark_safe(
            render_to_string(
                self.field_template,
                {
                    "field": self.bound_field,
                    self.object_type_name: instance_obj,
                    "snippet_type_name": self.get_snippet_type_name(),
                },
            )
        )

    @classmethod
    def get_snippet_type_name(cls):
        return str(cls.target_model()._meta.verbose_name)  # noqa


class PollChooserPanel:
    def __init__(self, field_name, snippet_type=None):
        self.field_name = field_name
        self.snippet_type = snippet_type

    def bind_to_model(self, model):
        new = type(
            str("_PollChooserPanel"),
            (BasePollChooserPanel,),
            {
                "model": model,
                "field_name": self.field_name,
                "snippet_type": self.snippet_type,
            },
        )(field_name=self.field_name)
        logger.debug(f"PollChooserPanel::bind_to_model() new = {new}")
        return new
