from django.shortcuts import render

def index(request):
    # if User is authenticated redirect to dashboard.
	if request.user.is_authenticated:
		print('User is authenticated !!')
	return render(request, 'main/index.html')

def login(request):
    return render(request, 'main/base_template.html')
