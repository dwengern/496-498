import re
from django.http import HttpResponse
from django.utils.timezone import datetime
from django.shortcuts import render
from django.shortcuts import redirect
from hello.forms import LogMessageForm
from hello.models import LogMessage, Movie
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'hello/movies_list.html', {'movies': movies})

class HomeListView(ListView):
    """Renders the home page, with a list of all messages."""
    model = LogMessage

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        return context

def about(request):
    return render(request, "hello/about.html")

def contact(request):
    return render(request, "hello/contact.html")

def hello_there(request, name):
    print(request.build_absolute_uri())
    return render(
        request,
        'hello/hello_there.html',
        {
            'name': name,
            'date': datetime.now()
        }
    )

def log_message(request):
    form = LogMessageForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            message = form.save(commit=False)
            message.log_date = datetime.now()
            message.save()
            return redirect("log")
    else:
        return render(request, "hello/log_message.html", {"form": form})
    
def delete_message(request, message_id):
    message = get_object_or_404(LogMessage, id=message_id)

    if request.method == "POST":
        message.delete()
        return redirect("log")
    
    return render(request, "hello/delete_message.html", {"message": message})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to a success page
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')