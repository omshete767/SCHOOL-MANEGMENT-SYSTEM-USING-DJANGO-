from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Student
from courses.models import Course
from attendance.models import Attendance


# =====================================================
# ADMIN: LIST STUDENTS
# =====================================================
def student_list(request):
    if request.user.profile.role != "ADMIN":
        return redirect("login")

    students = Student.objects.select_related("user").all()
    return render(request, "admin/students/list.html", {
        "students": students
    })


# =====================================================
# ADMIN: ADD STUDENT
# =====================================================
def student_add(request):
    if request.user.profile.role != "ADMIN":
        return redirect("login")

    if request.method == "POST":
        # READ INPUTS
        username = request.POST.get("username")
        roll_no = request.POST.get("roll_no")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        class_name = request.POST.get("class_name")

        # DUPLICATE USERNAME
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose another.")
            return redirect("student_add")

        # DUPLICATE ROLL NUMBER
        if Student.objects.filter(roll_no=roll_no).exists():
            messages.error(request, "Roll number already exists.")
            return redirect("student_add")

        # CREATE USER
        user = User.objects.create_user(
            username=username,
            password=password,
        )
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # CREATE STUDENT
        Student.objects.create(
            user=user,
            roll_no=roll_no,
            class_name=class_name
        )

        messages.success(request, "Student added successfully.")
        return redirect("student_list")

    return render(request, "admin/students/add.html")


# =====================================================
# ADMIN: EDIT STUDENT
# =====================================================
def student_edit(request, id):
    if request.user.profile.role != "ADMIN":
        return redirect("login")

    student = get_object_or_404(Student, id=id)
    user = student.user

    if request.method == "POST":
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")
        roll_no = request.POST.get("roll_no")
        class_name = request.POST.get("class_name")

        # USERNAME UNIQUE
        if User.objects.filter(username=username).exclude(id=user.id).exists():
            messages.error(request, "Username already exists.")
            return redirect("student_edit", id=id)

        # ROLL NO UNIQUE
        if Student.objects.filter(roll_no=roll_no).exclude(id=student.id).exists():
            messages.error(request, "Roll number already exists.")
            return redirect("student_edit", id=id)

        # UPDATE USER
        user.username = username
        user.first_name = first_name
        user.last_name = last_name

        if password:
            user.set_password(password)

        user.save()

        # UPDATE STUDENT
        student.roll_no = roll_no
        student.class_name = class_name
        student.save()

        messages.success(request, "Student updated successfully.")
        return redirect("student_list")

    return render(request, "admin/students/edit.html", {
        "student": student
    })


# =====================================================
# ADMIN: DELETE STUDENT
# =====================================================
def student_delete(request, id):
    if request.user.profile.role != "ADMIN":
        return redirect("login")

    student = get_object_or_404(Student, id=id)

    # Deleting user auto-deletes student
    student.user.delete()

    return redirect("student_list")


# =====================================================
# STUDENT DASHBOARD (STUDENT ONLY)
# =====================================================
@login_required
def student_dashboard(request):
    if request.user.profile.role != "STUDENT":
        return redirect("login")

    student = request.user.student

    # Courses student is enrolled in
    courses = Course.objects.filter(students=student)

    dashboard_data = []

    for course in courses:
        total_lectures = course.total_lectures

        attended_lectures = Attendance.objects.filter(
            course=course,
            student=student,
            is_present=True
        ).count()

        attendance_percentage = (
            (attended_lectures / total_lectures) * 100
            if total_lectures > 0 else 0
        )

        status = (
            "COMPLETED"
            if total_lectures > 0 and attended_lectures >= total_lectures
            else "IN PROGRESS"
        )

        dashboard_data.append({
            "course": course,
            "total": total_lectures,
            "attended": attended_lectures,
            "percentage": round(attendance_percentage, 2),
            "status": status
        })

    return render(request, "student/dashboard.html", {
        "dashboard_data": dashboard_data
    })
