from django.db import models

from appchance.sections.models import BaseContent


class CustomContent(BaseContent):
    img = models.URLField(blank=True, null=True)
