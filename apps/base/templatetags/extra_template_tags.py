from django import	template

# from apps.pages.models import Contact

# para registrar etiqueta de plantilla
register = template.Library()

# @register.simple_tag
# def contact_state_count():
    
#     qs = Contact.objects.filter(state=True)
#     if qs.exists():
#         return qs.count()
#     return 0

# este recibe el contexto de la vista 
@register.simple_tag(takes_context=True)
def activate_on(context, name):
    
    if context['request'].resolver_match.url_name == name:
        return 'font-bold text-red-500'
    return 'text-gray-800'