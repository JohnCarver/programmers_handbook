# coding: utf-8

import os
import sys
from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User


class Node(models.Model):
    title = models.CharField(max_length=100)
    parent = models.ForeignKey('self', blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User)

    def __unicode__(self):
        return "%s (ID %i)" % (self.title, self.id)


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
