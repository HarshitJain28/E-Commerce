from django.shortcuts import render, redirect
from .forms import UserRegisterationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.

@login_required
def profile(request):
    nxt = request.GET.get("next", None)
    if nxt is None:
        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST or None, instance=request.user)
            p_form = ProfileUpdateForm(request.POST or None, instance=request.user.profile)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, "Profile Updated Successfully")
                return redirect('user-profile')
        else:
            u_form = UserUpdateForm(instance=request.user)
            p_form = ProfileUpdateForm(instance=request.user.profile)
        context = {
            'u_form': u_form,
            'p_form': p_form
        }
    else:
        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST or None, instance=request.user)
            p_form = ProfileUpdateForm(request.POST or None, instance=request.user.profile)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, "Profile Updated Successfully")
                return redirect(request.GET.get('next'))
        else:
            u_form = UserUpdateForm(instance=request.user)
            p_form = ProfileUpdateForm(instance=request.user.profile)
        context = {
            'u_form': u_form,
            'p_form': p_form
        }
    return render(request, 'user/profile.html',context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User Created, You may now Log In")
            return redirect('user-login')
    else:
        form = UserRegisterationForm()
    return render(request, 'user/register.html', {'form': form})

