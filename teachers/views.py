from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from courses.models import Course
from accounts.models import Profile
from .models import Teacher


# =====================================================
# LIST TEACHERS (ADMIN ONLY)
# =====================================================
@login_required
def teacher_list(request):
    if request.user.profile.role != "ADMIN":
        return redirect("login")

    teachers = Teacher.objects.select_related("user").all()
    return render(request, "admin/teachers/list.html", {
        "teachers": teachers
    })


# =====================================================
# ADD TEACHER (ADMIN ONLY)
# =====================================================
@login_required
def teacher_add(request):
    if request.user.profile.role != "ADMIN":
        return redirect("login")

    if request.method == "POST":
        # READ INPUTS
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")
        employee_id = request.POST.get("employee_id")
        department = request.POST.get("department")

        # -------------------------------
        # VALIDATIONS (DATABASE SAFETY)
        # -------------------------------
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("teacher_add")

        if Teacher.objects.filter(employee_id=employee_id).exists():
            messages.error(request, "Employee ID already exists.")
            return redirect("teacher_add")

        # -------------------------------
        # CREATE USER
        # -------------------------------
        user = User.objects.create_user(
            username=username,
            password=password
        )
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # -------------------------------
        # CREATE / UPDATE PROFILE (SAFE)
        # -------------------------------
        profile, created = Profile.objects.get_or_create(user=user)
        profile.role = "TEACHER"
        profile.save()

        # -------------------------------
        # CREATE TEACHER
        # -------------------------------
        Teacher.objects.create(
            user=user,
            employee_id=employee_id,
            department=department
        )

        messages.success(request, "Teacher added successfully.")
        return redirect("teacher_list")

    return render(request, "admin/teachers/add.html")


# =====================================================
# EDIT TEACHER (ADMIN ONLY)
# =====================================================
@login_required
def teacher_edit(request, id):
    if request.user.profile.role != "ADMIN":
        return redirect("login")

    teacher = get_object_or_404(Teacher, id=id)
    user = teacher.user

    if request.method == "POST":
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")
        employee_id = request.POST.get("employee_id")
        department = request.POST.get("department")

        # VALIDATIONS
        if User.objects.filter(username=username).exclude(id=user.id).exists():
            messages.error(request, "Username already exists.")
            return redirect("teacher_edit", id=id)

        if Teacher.objects.filter(employee_id=employee_id).exclude(id=teacher.id).exists():
            messages.error(request, "Employee ID already exists.")
            return redirect("teacher_edit", id=id)

        # UPDATE USER
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        if password:
            user.set_password(password)
        user.save()

        # UPDATE TEACHER
        teacher.employee_id = employee_id
        teacher.department = department
        teacher.save()

        messages.success(request, "Teacher updated successfully.")
        return redirect("teacher_list")

    return render(request, "admin/teachers/edit.html", {
        "teacher": teacher
    })


# =====================================================
# DELETE TEACHER (ADMIN ONLY)
# =====================================================
@login_required
def teacher_delete(request, id):
    if request.user.profile.role != "ADMIN":
        return redirect("login")

    teacher = get_object_or_404(Teacher, id=id)
    teacher.user.delete()

    messages.success(request, "Teacher deleted successfully.")
    return redirect("teacher_list")
@login_required
def teacher_dashboard(request):
    if request.user.profile.role != "TEACHER":
        return redirect("login")

    teacher = request.user.teacher
    courses = Course.objects.filter(teacher=teacher)

    return render(request, "teacher/dashboard.html", {
        "courses": courses
    })