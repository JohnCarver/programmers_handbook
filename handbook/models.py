# coding: utf-8

import os
import sys
from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User


class Node(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    parent = models.ForeignKey('self', blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User)

    def __unicode__(self):
        return "%s (ID %i)" % (self.slug, self.id)

    def get_content(self):
        return Content.objects.filter(node=self, status=2).order_by('-version')[0] # TODO there always has to be a content

    def get_children(self):
        children = Node.objects.filter(parent=self)
        if not children:
            return None
        return children

    def _get_url_part(self, right_part):
        new_part = "/%s%s" % (self.slug, right_part)
        if self.parent:
            return self.parent._get_url_part(new_part)
        return new_part

    def get_url(self):
        return "/page" + self._get_url_part('/')

    def get_edit_url(self):
        return "/page_edit" + self._get_url_part('/')


class Content(models.Model):
    STATUS_CHOICES = (
        (1, "review"),
        (2, "published"),
        (3, "hidden"),
    )

    node = models.ForeignKey(Node)
    version = models.IntegerField()
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User)
    status = models.SmallIntegerField(choices=STATUS_CHOICES)

    def __unicode__(self):
        return "Content for %s (ID %i) Version %i (ID %i)" % (self.node.title, self.node.id, self.version, self.id)
