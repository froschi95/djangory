from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import login
# Create your views here.

def index(request):
    return render(request, 'main/index.html')


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect('home')

    else:
        form = SignUpForm()

    return render(request, 'main/register.html', {'form': form})