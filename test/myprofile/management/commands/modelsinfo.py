from django.conf import settings
from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list
    help = 'Prints model names for all applications and object count.'
    requires_model_validation = True

    def handle_noargs(self,**options):
        from django.db.models import get_models,get_app
        lines = []
        apps = settings.INSTALLED_APPS
        for app in apps:
            app = app.split('.')[-1]
            for model in get_models(get_app(app)):
                lines.append('[%s] - %s objects'
                             % (model.__name__,model._default_manager.count()))
        return '\n'.join(lines)
