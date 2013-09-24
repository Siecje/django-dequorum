
from nap.models import ModelSerialiser
from nap import fields

from . import models

class CategorySerialiser(ModelSerialiser):

    class Meta:
        model = models.Category

class ThreadSerialiser(ModelSerialiser):

    class Meta:
        model = models.Thread

class ForumSerialiser(ModelSerialiser):

    class Meta:
        model = models.Forum

class PostSerialiser(ModelSerialiser):

    class Meta:
        model = models.Post

