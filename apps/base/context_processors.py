from datetime import datetime
from apps.pages.models import Contact

def extra(request):
    current_datetime = datetime.now()
    qs = Contact.objects.filter(state=True)
    if qs.exists():
        contact_count = qs.count()
    else:
        contact_count = 0
    context = {
        'contact_count' : contact_count,
        'current_year' : current_datetime.year
    }
    return context
