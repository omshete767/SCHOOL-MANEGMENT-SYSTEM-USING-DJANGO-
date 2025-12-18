from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date

from .models import Attendance
from courses.models import Course

@login_required
def take_attendance(request, course_id):
    if request.user.profile.role != "TEACHER":
        return redirect("login")

    course = get_object_or_404(Course, id=course_id)

    # security
    if course.teacher != request.user.teacher:
        return redirect("login")

    students = course.students.all()
    today = date.today()

    # prevent duplicate attendance
    if Attendance.objects.filter(course=course, date=today).exists():
        messages.warning(request, "Attendance already taken for today.")
        return redirect("teacher_dashboard")

    if request.method == "POST":
        present_students = request.POST.getlist("students")

        for student in students:
            Attendance.objects.create(
                course=course,
                student=student,
                date=today,
                is_present=str(student.id) in present_students,
                is_absent=str(student.id) not in present_students,
            )

        messages.success(request, "Attendance saved successfully.")
        return redirect("teacher_dashboard")

    return render(request, "teacher/attendance/take.html", {
        "course": course,
        "students": students,
        "today": today
    })
