import logging

from django.shortcuts import render
from django.views.decorators.http import require_http_methods

logger = logging.getLogger(__name__)


@require_http_methods(["GET"])
def imprint(request):
    return render(request, "legal/imprint.html")


@require_http_methods(["GET"])
def privacy(request):
    return render(request, "legal/privacy.html")


@require_http_methods(["GET"])
def about(request):
    return render(request, "legal/about.html")


@require_http_methods(["GET"])
def license(request):
    return render(request, "legal/license.html")


@require_http_methods(["GET"])
def faq(request):
    return render(request, "legal/faq.html")
