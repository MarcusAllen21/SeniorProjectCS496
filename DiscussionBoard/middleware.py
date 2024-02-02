from .models import Visits
from django.utils import timezone

class VisitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'visited' not in request.session:
            visit_count, created = Visits.objects.get_or_create(date=timezone.now().date())
            visit_count.count += 1
            visit_count.save()
            request.session['visited'] = True
        
        response = self.get_response(request)
        return response
