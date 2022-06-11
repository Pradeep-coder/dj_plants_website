from django.contrib.auth.models import User

from plantswebsite.models import LandingScreen

def project_context(request):
    context = {
        'me': LandingScreen.objects.first(),
    }
    return context