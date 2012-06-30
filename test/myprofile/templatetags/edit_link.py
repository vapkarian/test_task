from django import template

register = template.Library()

@register.inclusion_tag('edit_link.html')
def edit_link(object):
    link = '/admin/'+str(object._meta).replace('.','/')+'/'+str(object.id)+'/'
    return {'link': link}
