from django.shortcuts import render, redirect
from .forms import LoginForm, RegistrationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login


def index(request):
    # if User is authenticated redirect to dashboard.
	if request.user.is_authenticated:
		print('User is authenticated !!')
	return render(request, 'main/index.html')

def login(request):
	# if User is authenticated redirecr to dashboard
	if request.user.is_authenticated:
		print('User is authenticated !!')

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
				 	# TODO: Change this to redirect user to 'Dashboard'
					return redirect(index)
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

			# TODO: Change this to redirect user to 'Dashboard'
			return redirect(index)
	return render(request, 'main/authentication.html', data)
