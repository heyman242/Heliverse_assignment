from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse
from .models import Quizmaker, Quiz
from django.contrib.auth.models import User


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and hasattr(user, 'quizmaker'):
            login(request, user)
            quizmaker = Quizmaker.objects.get(user=user)
            quizmaker_id = quizmaker.id
            quizmaker_dashboard_url = reverse('quizmaker_dashboard', args=[quizmaker_id])

            return redirect(quizmaker_dashboard_url)
        else:
            error_message = "Invalid username or password."
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email_id = request.POST.get('email_id')
        name = request.POST.get('name')
        location = request.POST.get('location')

        # Check if passwords match
        if password1 != password2:
            return render(request, 'signup.html', {'error': 'Passwords do not match.'})

        # Create user instance
        user = User.objects.create_user(username=username, password=password1)
        user.save()

        # Create quizmaker instance
        quizmaker = Quizmaker(user=user, id=username[:5], email_id=email_id, name=name, location=location)
        quizmaker.save()

        # Redirect to the login page
        return redirect('login')
    else:
        return render(request, 'signup.html')


