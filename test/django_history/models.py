# Open-source app git://github.com/ildus/django-history.git
import datetime
from django.db import models
from django_history.manager import HistoryDescriptor
import cPickle as pickle
from copy import copy
from django.utils.functional import curry
from django.utils.encoding import force_unicode
from django.core.exceptions import ObjectDoesNotExist

def verbose_value(field, value):
    if isinstance(field, models.BooleanField):
        return 'Yes' if value else 'No'
    elif type(field) in (models.IntegerField, models.PositiveIntegerField, models.CharField):
        if field._choices:
            return force_unicode(dict(field.flatchoices).get(value, value), strings_only=True)
        else:
            return value
    return unicode(value) if value is not None else ''
            
def get_info(model, self, prefix = None):
    date = self.history_date
    result = []
    prefix = prefix + ', ' if prefix else ''
    for attr, (old, new) in self.get_data().iteritems():
        if '_id' in attr:
            field = model._meta.get_field(attr.replace('_id', ''))
            if isinstance(field, models.ForeignKey):
                try:
                    old1 = field.rel.to._default_manager.get(pk = old) if old else old
                    new1 = field.rel.to._default_manager.get(pk = new) if new else new
                    new, old = new1, old1
                except ObjectDoesNotExist:
                    pass
        else:
            field = model._meta.get_field(attr)
            
        result.append({
            'operation': self.history_type,
            'id': self.pk,
            'type': model._meta.module_name,
            'attr': attr,
            'attr_verbose': prefix + (field.verbose_name or 'undefined!'),
            'old': verbose_value(field, old),
            'new': verbose_value(field, new),
            'date': date,
        })
    return result

class HistoricalRecords(object):
    registry = {} #register history models
    
    def __init__(self, exclude = None, include = None):
        self.exclude = exclude
        self.include = include
    
    def contribute_to_class(self, cls, name):
        self.manager_name = name
        models.signals.class_prepared.connect(self.finalize, sender=cls)

    def finalize(self, sender, **kwargs):
        history_model = self.create_history_model(sender)

        models.signals.pre_save.connect(self.pre_save, sender=sender, weak=False)
        models.signals.post_delete.connect(self.post_delete, sender=sender, weak=False)
        models.signals.post_save.connect(self.post_save, sender=sender, weak=False)

        descriptor = HistoryDescriptor(history_model)
        setattr(sender, self.manager_name, descriptor)

    def create_history_model(self, model):
        '''
        Creates a historical model to associate with the model provided.
        '''
        attrs = self.get_history_model_fields(model)
        attrs.update(Meta=type('Meta', (), self.get_meta_options(model)))
        name = 'Historical%s' % model._meta.object_name
        history_model =  type(name, (models.Model,), attrs)
        self.__class__.registry[model._meta.module_name] = history_model
        return history_model
    
    def __contains__(self, module_name):
        return module_name in self.__class__.registry
    
    def get_history_model(self, module_name):
        return self.__class__.registry.get(module_name)

    def get_history_model_fields(self, model):
        '''
        Returns a dictionary of fields that will be added to the historical
        record model, in addition to the ones returned by copy_fields below.
        '''
        rel_nm = '_%s_history' % model._meta.object_name.lower()
        fields =  {
            '__module__': model.__module__,
            
            #fields of history item
            'history_id': models.AutoField(primary_key=True),
            'history_date': models.DateTimeField(default=datetime.datetime.now),
            'history_data': models.TextField(), #here is only the changed data
            'history_all_data': models.TextField(blank = True, null = True), #here saved all data of item
            'history_type': models.CharField(max_length=1, choices=(
                ('+', 'Created'),
                ('~', 'Changed'),
                ('-', 'Deleted'),
            )),
            
            #method of history item
            'get_info': curry(get_info, model),
            'get_data': lambda self: pickle.loads(self.history_data.encode('utf-8')),
            'set_data': lambda self, data: setattr(self, 'data', pickle.dumps(data)),
            '__unicode__': lambda self: u'%s on %s, %s' % (self.get_history_type_display(),self.history_date,self.get_data())
        }
        
        #primary key that point to the main object
        pk_field = copy(model._meta.get_field(model._meta.pk.name))
        pk_field.__class__ = models.IntegerField
        pk_field._unique = False
        pk_field.primary_key = False
        pk_field.db_index = True
        
        fields[model._meta.pk.name] = pk_field
        return fields

    def get_meta_options(self, model):
        '''
        Returns a dictionary of fields that will be added to
        the Meta inner class of the historical record model.
        '''
        return {
            'ordering': ('-history_date',),
            'get_latest_by': 'history_date',
        }

    def pre_save(self, instance, **kwargs):
        if instance.pk:
            self.create_historical_record(instance, '~')
        
    def post_save(self, instance, created, **kwargs):
        if created:
            self.create_historical_record(instance, '+')

    def post_delete(self, instance, **kwargs):
        self.create_historical_record(instance, '-')

    def create_historical_record(self, instance, history_type):
        manager = getattr(instance, self.manager_name)
        
        attrs = {}
        attrs[instance._meta.pk.name] = getattr(instance, instance._meta.pk.name)
        #collecting changed fields
        history_data = {}
        history_all_data = {}
        if instance.pk and history_type != '-':
            old = instance.__class__._default_manager.get(pk = instance.pk)
            for field in instance._meta.fields:
                if (self.exclude and field.name in self.exclude) or (self.include and field.name not in self.include):
                    continue
                                
                if field.editable and type(field) not in (models.ManyToManyField, ):
                    new_value = getattr(instance, field.attname)
                    old_value = getattr(old, field.attname)
                    
                    history_all_data[field.attname] = new_value
                    
                    if new_value != old_value:
                        history_data[field.attname] = (old_value, new_value)
                        
        manager.create(history_type=history_type, 
                       history_data = pickle.dumps(history_data),
                       history_all_data = pickle.dumps(history_all_data), 
                       **attrs)