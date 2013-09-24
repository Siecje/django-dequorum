
from django.db import models
from django.utils.functional import lazy, SimpleLazyObject

from . import fields

from taggit.managers import TaggableManager

from datetime import datetime

class TimestampedMixin(models.Model):
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            created = datetime.now()
        modified = datetime.now()
        return super(TimestampedMixin, self).super(*args, **kwargs)

    class Meta:
        abstract = True

class Category(models.Model):
    title = fields.TitleField()

    def __unicode__(self):
        return self.title

class Forum(TimestampedMixin):
    title = fields.TitleField()
    categories = models.ManyToManyField('Category')

    def __unicode__(self):
        return self.title

class ThreadManager(models.Manager):
    def with_counts(self):
        return self.get_query_set().annotate(
            post_count=models.Count('posts'),
            most_recent=models.Max('posts__created'),
            involved_count=models.Count('posts__user'), # Will this be distinct?
        )

class Thread(TimestampedMixin):
    subject = fields.TitleField()
    forum = models.ForeignKey('Forum', related_name='threads')
    tags = TaggableManager(blank=True)

    objects = ThreadManager()

class Post(TimestampedMixin):
    thread = models.ForeignKey('Thread', related_name='posts')
    subject = fields.TitleField(blank=True)
    author = models.ForeignKey('Profile', related_name='posts')
    content = models.TextField(blank=True)
    tags = TaggableManager(blank=True)

##
## Profile
##

class Profile(models.Model):
    user = models.OneToOneField('auth.User')
    nickname = fields.TitleField(blank=True)

    avatar = models.ImageField(blank=True)

##
## Permission models
##
from django.contrib.contenttypes.models import ContentType

class ThreadAdmin(models.Model):
    profile = models.ForeignKey('Profile', related_name='thread_perms')
    thread = models.ForeignKey('Thread', related_name='admin_perms')
    permissions = models.ManyToManyField('auth.Permission',
        limit_choices_to=lambda: {
            'content_type': ContentType.objects.get_for_model(Post),
        },
    )

class ForumAdmin(models.Model):
    profile = models.ForeignKey('Profile', related_name='forum_perms')
    forum = models.ForeignKey('Forum', related_name='admin_perms')
    permissions = models.ManyToManyField('auth.Permission',
        limit_choices_to=lambda: {
            'content_type': ContentType.objects.get_for_model(Thread),
        },
    )

