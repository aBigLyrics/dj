from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout, authenticate, login
# Create your views here.



def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('dj_logs:index'))

def register(request):
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            authenticated_uesr = authenticate(username=new_user.username,
                                              password=request.POST['password1'])

            login(request, authenticated_uesr)
            return HttpResponseRedirect(reverse('dj_logs:index'))
    context = {'form': form}
    return render(request, 'users/register.html', context)
