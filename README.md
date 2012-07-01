Middlewares:
QueriesGetter stores all database queries in special log dirictory 'logs'. One log file is created for one session.

Context Processors:
django.conf.settings is added to context.

Widgets:
Calendar widget use base Django AdminDateWidget with some jacascript lines in templates.

Templatetags:
edit_link is a template tag that gets any model object and renders link of change view in admin interface.
Example of use:
  {% load edit_link %}
    {% edit_link user.profile %}

Commands:
modelsinfo is a command for printing all models and object counts.
Example of use:
  >>> python manage.py modelsinfo

Signals:
django_history is a modified open-source app for creating a notes in database when model is creating/editing/deleting.
Add these two lines to the model for which notes must be kept:
  from django_history.models import HistoricalRecords
  history = HistoricalRecords()
And then sync models with database (python manage.py syncdb)
Method all() of field history return all notes for this object.
Example:
  s = Student.objects.all()[0]
  print s.history.all()[0] #print last action
  print s.history.all() #print all actions  