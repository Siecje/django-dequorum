
from django.db.models import fields

from functools import partial

TitleField = partial(fields.CharField, max_length=1024)
