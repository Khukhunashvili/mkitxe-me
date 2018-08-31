from django.shortcuts import render

def index(request):
    # if User is authenticated redirect to dashboard.
	if request.user.is_authenticated:
        pass
	return render(request, 'main/index.html')
