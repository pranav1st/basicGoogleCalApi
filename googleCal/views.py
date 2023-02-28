from django.shortcuts import redirect

def redirect_view(request):
    response = redirect('/rest/v1/calendar/init/')
    return response