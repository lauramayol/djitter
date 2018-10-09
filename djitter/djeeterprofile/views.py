# Import django and models


from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from djeeterprofile.forms import SignupForm, SigninForm
from djeet.forms import DjeetForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

# Views


def frontpage(request):
    if request.user.is_authenticated:
        return redirect('/' + request.user.username + '/')  # Change this line
    else:
        if request.method == 'POST':
            if 'signupform' in request.POST:
                signupform = SignupForm(data=request.POST)
                signinform = SigninForm()

                if signupform.is_valid():
                    username = signupform.cleaned_data['username']
                    password = signupform.cleaned_data['password1']
                    signupform.save()
                    user = authenticate(username=username, password=password)
                    login(request, user)
                    return redirect('/')
            else:
                signinform = SigninForm(data=request.POST)
                signupform = SignupForm()

                if signinform.is_valid():
                    login(request, signinform.get_user())
                    return redirect('/')
        else:
            signupform = SignupForm()
            signinform = SigninForm()

        return render(request, 'frontpage.html', {'signupform': signupform, 'signinform': signinform})


@login_required
def signout(request):
    logout(request)
    return redirect('/')


@login_required
def profile(request, username):  # Replace the old profile view with this one
    if request.user.is_authenticated:
        user = User.objects.get(username=username)

        if request.method == 'POST':
            form = DjeetForm(data=request.POST)

            if form.is_valid():
                djeet = form.save(commit=False)
                djeet.user = request.user
                djeet.save()

                redirecturl = request.POST.get('redirect', '/')

                return redirect(redirecturl)
        else:
            form = DjeetForm()

        return render(request, 'profile.html', {'form': form, 'user': user})
    else:
        return redirect('/')


@login_required
def follows(request, username):
    user = User.objects.get(username=username)
    djeeterprofiles = user.djeeterprofile.follows.select_related('user').all()

    return render(request, 'users.html', {'title': 'Follows', 'djeeterprofiles': djeeterprofiles})


@login_required
def followers(request, username):
    user = User.objects.get(username=username)
    djeeterprofiles = user.djeeterprofile.followed_by.select_related('user').all()

    return render(request, 'users.html', {'title': 'Followers', 'djeeterprofiles': djeeterprofiles})


@login_required
def follow(request, username):
    user = User.objects.get(username=username)
    request.user.djeeterprofile.follows.add(user.djeeterprofile)

    return HttpResponseRedirect('/' + user.username + '/')


@login_required
def stopfollow(request, username):
    user = User.objects.get(username=username)
    request.user.djeeterprofile.follows.remove(user.djeeterprofile)

    return HttpResponseRedirect('/' + user.username + '/')
