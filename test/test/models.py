from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class WatchedMixin(models.Model):
    created_by = models.ForeignKey(User, verbose_name=_('Created by'),
        related_name='%(class)s_created_items', 
    )
    edited_by = models.ForeignKey(User, verbose_name=_('Edited by'),
        related_name='%(class)s_edited_items',
    )
    deleted_by = models.ForeignKey(User, verbose_name=_('Deleted by'),
        related_name='%(class)s_deleted_items',
    )
    
    class Meta:
        abstract=True
