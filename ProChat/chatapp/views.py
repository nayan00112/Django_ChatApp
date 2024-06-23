from django.shortcuts import render

# Create your views here.

def firstpage(request):
    if request.method == 'POST':
        roomname = request.POST['roomname']
        return render(request, "chatapp/room.html", {'roomname':roomname})
    return render(request, 'chatapp/index.html')
# def home(request):
#     return render(request, "chatapp/room.html")