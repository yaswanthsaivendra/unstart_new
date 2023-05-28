from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import (
    GroupCourseEnrollment,
    Enrollment,
    Lesson,
    LessonProgress,
    GroupMembership
)


@receiver(post_save, sender=GroupCourseEnrollment)
def create_enrollment_and_add_course(sender, instance, created, **kwargs):
    if created:
        group = instance.group
        students = group.students.all()
        course = instance.course

        for student in students:
            Enrollment.objects.create(student=student, course=course)

        group.courses.add(course)


@receiver(post_delete, sender=GroupCourseEnrollment)
def delete_enrollment_and_remove_course(sender, instance, **kwargs):
    group = instance.group
    students = group.students.all()
    course = instance.course

    for student in students:
        enrollment = Enrollment.objects.get(student=student, course=course)
        enrollment.delete()

    group.courses.remove(course)



@receiver(post_save, sender=Enrollment)
def create_lesson_progress(sender, instance, created, **kwargs):
    if created:
        course = instance.course
        student = instance.student

        lessons = Lesson.objects.filter(unit__course=course)
        for lesson in lessons:
            LessonProgress.objects.create(enrollment=instance, lesson=lesson, is_completed=False)



@receiver(post_save, sender=GroupMembership)
def add_student_to_group(sender, instance, created, **kwargs):
    if created:
        group = instance.group
        student = instance.student
        group.students.add(student)

