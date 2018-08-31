from django.shortcuts import render, redirect
from .forms import LoginForm, RegistrationForm
from .models import Message
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def index(request):
    # if User is authenticated redirect to dashboard.
	if request.user.is_authenticated:
		return redirect(dashboard)
	return render(request, 'main/index.html')

def login(request):
	# if User is authenticated redirecr to dashboard
	if request.user.is_authenticated:
		return redirect(dashboard)

	form = LoginForm(request.POST or None)
	data = {
		'title' : 'შესვლა',
		'form'  : form
	}

	if request.method == "POST":
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					auth_login(request, user)
					return redirect(dashboard)
				else:
					data['error_message'] = 'თქვენი ანგარიში დაბლოკილია !'
			else:
				data['error_message'] = 'არასწორი სახელი ან პაროლი!'
	return render(request, 'main/authentication.html', data)

def sign_up(request):
	form = RegistrationForm()
	data = {
		'title' : 'რეგისტრაცია',
		'form'  : form
	}

	if request.method == "POST":
		form = RegistrationForm(data=request.POST)
		data['form'] = form

		if form.is_valid():
			user = form.save(commit=False)

			image = form.cleaned_data['image']
			first_name = form.cleaned_data['first_name']
			last_name = form.cleaned_data['last_name']
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			email = form.cleaned_data['email']

			user.set_password(password)
			user.save()

			auth_login(request, authenticate(username=username, password=password))

			return redirect(dashboard)
	return render(request, 'main/authentication.html', data)


@login_required(login_url='/login')
def logout(request):
	auth_logout(request)
	return redirect(login)

@login_required(login_url='/login')
def dashboard(request):
	user = request.user
	messages = Message.objects.filter(to=user)
	unanswered = len([message for message in messages if message.response == None])
	data = {
		'profile'      : request.user,
		'messages'     : reversed(messages),
		'not_answered' : unanswered
	}
	return render(request, 'main/profile.html', data)

def profile(request, username):
	try:
		unanswered = len(request.user.message_set.filter(response=None))
	except AttributeError:
		unanswered = 0
	data = {
		'not_answered' : unanswered
	}
	try:
		user = User.objects.filter(username=username)[0]
		data['profile'] = user
		data['messages'] = reversed(Message.objects.filter(to=user))
	except IndexError:
		data['username'] = username
		return render(request, 'main/error.html', data)

	return render(request, 'main/profile.html', data)

def comment(request, username):
	if request.method == 'POST':
		user = User.objects.filter(username=username)[0]
		message = Message.objects.create(
				message = request.POST.get('message', ''),
				to      = user
			)
	return redirect(profile, username=username)
