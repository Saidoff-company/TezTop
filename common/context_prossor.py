from django.conf import settings


def project_languages(request):
    return {"LANGUAGES": settings.LANGUAGES}