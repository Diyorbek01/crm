from main.models import Markaz


def get_hostname(request):
    print(request.get_host().split(':')[0].lower())
    return request.get_host().split(':')[0].lower()

def get_markaz(request):
    hostname = get_hostname(request)
    subdomain = hostname.split('.')[0]
    return Markaz.objects.filter(subdomain=subdomain).first()