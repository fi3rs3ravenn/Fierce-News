from .forms import CustomUserCreationForm, UserProfileForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render , redirect
from .models import News 

def news_list(request):
    news = News.objects.all().order_by('-published_date')
    return render(request, 'news_list.html', {'news':news})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'news_main/register.html', {'form':form})

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'news_main/profile.html', {'form':form,'user':request.user})
