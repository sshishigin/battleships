from django.shortcuts import render

# Create your views here.

from django.shortcuts import render

def index(request):
    return render(request, 'chat/index.html')


def room(request, room_name):
    return render(request, 'chat/widget.html', {
        'room_name': room_name,
        'user': request.user,
    })


def register(request):
    if request.method.lower() == 'get':
        return render(request, 'registration/register.html')
    user = request.body.data
