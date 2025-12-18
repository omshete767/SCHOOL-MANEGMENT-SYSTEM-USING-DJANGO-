from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Course
from teachers.models import Teacher
from students.models import Student


# =====================================================
# LIST COURSES (ADMIN ONLY)
# =====================================================
@login_required
def course_list(request):
    if request.user.profile.role != "ADMIN":
        return redirect("login")

    courses = Course.objects.select_related("teacher").prefetch_related("students")
    return render(request, "admin/courses/list.html", {
        "courses": courses
    })


# =====================================================
# ADD COURSE (ADMIN ONLY)
# =====================================================
@login_required
def course_add(request):
    if request.user.profile.role != "ADMIN":
        return redirect("login")

    teachers = Teacher.objects.all()
    students = Student.objects.all()

    if request.method == "POST":
        name = request.POST.get("name")
        code = request.POST.get("code")
        teacher_id = request.POST.get("teacher")
        student_ids = request.POST.getlist("students")
        total_lectures = request.POST.get("total_lectures")  # ✅ NEW

        # -------------------------------
        # VALIDATION
        # -------------------------------
        if Course.objects.filter(code=code).exists():
            messages.error(request, "Course code already exists.")
            return redirect("course_add")

        if not total_lectures or int(total_lectures) <= 0:
            messages.error(request, "Total lectures must be greater than 0.")
            return redirect("course_add")

        # -------------------------------
        # CREATE COURSE
        # -------------------------------
        course = Course.objects.create(
            name=name,
            code=code,
            teacher=Teacher.objects.filter(id=teacher_id).first(),
            total_lectures=total_lectures  # ✅ STORED IN COURSE
        )

        # MANY TO MANY
        if student_ids:
            course.students.set(student_ids)

        messages.success(request, "Course added successfully.")
        return redirect("course_list")

    return render(request, "admin/courses/add.html", {
        "teachers": teachers,
        "students": students
    })


# =====================================================
# EDIT COURSE (ADMIN ONLY)
# =====================================================
@login_required
def course_edit(request, id):
    if request.user.profile.role != "ADMIN":
        return redirect("login")

    course = get_object_or_404(Course, id=id)
    teachers = Teacher.objects.all()
    students = Student.objects.all()

    if request.method == "POST":
        name = request.POST.get("name")
        code = request.POST.get("code")
        teacher_id = request.POST.get("teacher")
        student_ids = request.POST.getlist("students")
        total_lectures = request.POST.get("total_lectures")  # ✅ NEW

        # -------------------------------
        # VALIDATION
        # -------------------------------
        if Course.objects.filter(code=code).exclude(id=course.id).exists():
            messages.error(request, "Course code already exists.")
            return redirect("course_edit", id=id)

        if not total_lectures or int(total_lectures) <= 0:
            messages.error(request, "Total lectures must be greater than 0.")
            return redirect("course_edit", id=id)

        # -------------------------------
        # UPDATE COURSE
        # -------------------------------
        course.name = name
        course.code = code
        course.teacher = Teacher.objects.filter(id=teacher_id).first()
        course.total_lectures = total_lectures  # ✅ UPDATED
        course.save()

        # UPDATE MANY TO MANY
        course.students.set(student_ids)

        messages.success(request, "Course updated successfully.")
        return redirect("course_list")

    return render(request, "admin/courses/edit.html", {
        "course": course,
        "teachers": teachers,
        "students": students
    })


# =====================================================
# DELETE COURSE (ADMIN ONLY)
# =====================================================
@login_required
def course_delete(request, id):
    if request.user.profile.role != "ADMIN":
        return redirect("login")

    course = get_object_or_404(Course, id=id)
    course.delete()

    messages.success(request, "Course deleted successfully.")
    return redirect("course_list")
