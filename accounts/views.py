from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            role = user.profile.role

            if role == 'ADMIN':
                return redirect('admin_dashboard')
            elif role == 'TEACHER':
                return redirect('teacher_dashboard')
            elif role == 'STUDENT':
                return redirect('student_dashboard')

        return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def admin_dashboard(request):
    return render(request, 'admin/dashboard.html')


@login_required
def teacher_dashboard(request):
    return render(request, 'teacher/dashboard.html')


@login_required
def student_dashboard(request):
    return render(request, 'student/dashboard.html')
