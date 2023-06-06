from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import (
    Course,
    Unit,
    Lesson,
    LessonFile,
    LessonLink,
    Enrollment,
    Group,
    GroupMembership,
    GroupCourseEnrollment,
    Announcement,
    AnnouncementFile,
    AnnouncementLink,
)

from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    ListView,
    View
)


@login_required
def home(request):
    if request.user.profile.status == 't':
        courses = Course.objects.filter(created_by = request.user)
        # courses.count
        return render(request, 'teacher/example.html' , {'courses': courses})


# Course Views
class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    fields = ['title', 'category', 'image', 'course_price', 'is_paid', 'course_level']
    template_name = 'teacher/course_create.html'
    success_url = reverse_lazy('teacher:course-list')

class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'teacher/course_detail.html'
    context_object_name = 'course'


class CourseUpdateView(LoginRequiredMixin, UpdateView):
    model = Course
    fields = ['title', 'category', 'image', 'course_price', 'is_paid', 'course_level']
    template_name = 'teacher/course_update.html'
    context_object_name = 'course'

    def get_success_url(self):
        return reverse_lazy('teacher:course-detail', kwargs={'pk': self.kwargs['pk']})


class CourseDeleteView(LoginRequiredMixin, DeleteView):
    model = Course
    success_url = reverse_lazy('teacher:course-list')
    template_name = 'teacher/course_delete.html'
    context_object_name = 'course'


class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'teacher/course_list.html'
    context_object_name = 'courses'


# Unit Views
class UnitCreateView(LoginRequiredMixin, CreateView):
    model = Unit
    fields = ['title', 'description', 'due_date']
    template_name = 'teacher/unit_create.html'

    def get_success_url(self):
        return reverse_lazy('teacher:unit-list', kwargs={'course_pk': self.kwargs['course_pk']})

    def get_initial(self):
        initial = super().get_initial()
        course_pk = self.kwargs.get('course_pk')
        if course_pk:
            initial['course'] = get_object_or_404(Course, pk=course_pk)
        return initial

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class UnitDetailView(LoginRequiredMixin, DetailView):
    model = Unit
    template_name = 'teacher/unit_detail.html'
    context_object_name = 'unit'


class UnitUpdateView(LoginRequiredMixin, UpdateView):
    model = Unit
    fields = ['title', 'description', 'due_date']
    template_name = 'teacher/unit_update.html'
    context_object_name = 'unit'

    def get_success_url(self):
        return reverse_lazy('teacher:unit-detail', kwargs={'pk': self.kwargs['pk']})


class UnitDeleteView(LoginRequiredMixin, DeleteView):
    model = Unit
    success_url = reverse_lazy('teacher:unit-list')
    template_name = 'teacher/unit_delete.html'
    context_object_name = 'unit'


class UnitListView(LoginRequiredMixin, ListView):
    model = Unit
    template_name = 'teacher/unit_list.html'
    context_object_name = 'units'


# Lesson Views
class LessonCreateView(LoginRequiredMixin, CreateView):
    model = Lesson
    fields = ['lesson_number', 'title', 'description']
    template_name = 'teacher/lesson_create.html'
    success_url = reverse_lazy('teacher:lesson-list')

    def get_initial(self):
        initial = super().get_initial()
        initial['unit'] = get_object_or_404(Unit, pk=self.kwargs['unit_pk'])
        return initial

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class LessonDetailView(LoginRequiredMixin, DetailView):
    model = Lesson
    template_name = 'teacher/lesson_detail.html'
    context_object_name = 'lesson'


class LessonUpdateView(LoginRequiredMixin, UpdateView):
    model = Lesson
    fields = ['lesson_number', 'title', 'description']
    template_name = 'teacher/lesson_update.html'
    context_object_name = 'lesson'

    def get_success_url(self):
        return reverse_lazy('teacher:lesson-detail', kwargs={'pk': self.kwargs['pk']})


class LessonDeleteView(LoginRequiredMixin, DeleteView):
    model = Lesson
    success_url = reverse_lazy('teacher:lesson-list')
    template_name = 'teacher/lesson_delete.html'
    context_object_name = 'lesson'


class LessonListView(LoginRequiredMixin, ListView):
    model = Lesson
    template_name = 'teacher/lesson_list.html'
    context_object_name = 'lessons'


# LessonFile Views
class LessonFileCreateView(LoginRequiredMixin, CreateView):
    model = LessonFile
    fields = ['file']
    template_name = 'teacher/lesson_file_create.html'

    def get_success_url(self):
        return reverse_lazy('teacher:lesson-detail', kwargs={'pk': self.kwargs['lesson_pk']})

    def get_initial(self):
        initial = super().get_initial()
        initial['lesson'] = get_object_or_404(Lesson, pk=self.kwargs['lesson_pk'])
        return initial


class LessonFileDeleteView(LoginRequiredMixin, DeleteView):
    model = LessonFile
    template_name = 'teacher/lesson_file_delete.html'
    context_object_name = 'lesson_file'

    def get_success_url(self):
        lesson = self.object.lesson
        return reverse_lazy('teacher:lesson-detail', kwargs={'pk': lesson.pk})


# LessonLink Views
class LessonLinkCreateView(LoginRequiredMixin, CreateView):
    model = LessonLink
    fields = ['link']
    template_name = 'teacher/lesson_link_create.html'

    def get_success_url(self):
        return reverse_lazy('teacher:lesson-detail', kwargs={'pk': self.kwargs['lesson_pk']})

    def get_initial(self):
        initial = super().get_initial()
        initial['lesson'] = get_object_or_404(Lesson, pk=self.kwargs['lesson_pk'])
        return initial


class LessonLinkDeleteView(LoginRequiredMixin, DeleteView):
    model = LessonLink
    template_name = 'teacher/lesson_link_delete.html'
    context_object_name = 'lesson_link'

    def get_success_url(self):
        lesson = self.object.lesson
        return reverse_lazy('teacher:lesson-detail', kwargs={'pk': lesson.pk})




# For student stats and enrollments


class EnrollmentListView(LoginRequiredMixin, ListView):
    model = Enrollment
    template_name = 'teacher/enrollment_list.html'
    context_object_name = 'enrollments'

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Enrollment.objects.filter(course_id=course_id)


class EnrollmentCreateView(LoginRequiredMixin, CreateView):
    model = Enrollment
    template_name = 'teacher/enrollment_form.html'
    success_url = reverse_lazy('teacher:enrollment-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class EnrollmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Enrollment
    template_name = 'teacher/enrollment_form.html'
    context_object_name = 'enrollment'
    success_url = reverse_lazy('teacher:enrollment-list')


class EnrollmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Enrollment
    template_name = 'teacher/enrollment_confirm_delete.html'
    context_object_name = 'enrollment'
    success_url = reverse_lazy('teacher:enrollment-list')





## Groups

class GroupCreateView(LoginRequiredMixin, CreateView):
    model = Group
    fields = ['name']
    template_name = 'teacher/group_form.html'
    success_url = reverse_lazy('teacher:group-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class GroupListView(LoginRequiredMixin, ListView):
    model = Group
    template_name = 'teacher/group_list.html'
    context_object_name = 'groups'


class GroupStudentListView(LoginRequiredMixin, ListView):
    model = GroupMembership
    template_name = 'teacher/group_student_list.html'
    context_object_name = 'students'
    paginate_by = 10

    def get_queryset(self):
        group_id = self.kwargs['group_id']
        return GroupMembership.objects.filter(group_id=group_id)


class AddStudentToGroupView(LoginRequiredMixin, CreateView):
    model = GroupMembership
    template_name = 'teacher/add_student_form.html'
    context_object_name = 'students'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['student'].queryset = self.get_available_students()
        return form

    def get_available_students(self):
        group_id = self.kwargs['group_id']
        enrolled_students = GroupMembership.objects.filter(group_id=group_id).values_list('student_id', flat=True)
        return User.objects.exclude(id__in=enrolled_students).filter(profile__status='s')

    def form_valid(self, form):
        group_id = self.kwargs['group_id']
        form.instance.group_id = group_id

        group = get_object_or_404(Group, id=group_id)
        student = form.cleaned_data['student']
        group.students.add(student)

        return super().form_valid(form)

    def get_success_url(self):
        group_id = self.kwargs['group_id']
        return reverse_lazy('teacher:group-student-list', kwargs={'group_id': group_id})


class RemoveStudentFromGroupView(LoginRequiredMixin, DeleteView):
    model = GroupMembership
    template_name = 'teacher/remove_student_confirm.html'

    def get_success_url(self):
        group_id = self.kwargs['group_id']
        return reverse_lazy('teacher:group-student-list', kwargs={'group_id': group_id})

    def delete(self, request, *args, **kwargs):
        group_membership = self.get_object()
        group = group_membership.group
        student = group_membership.student

        group.students.remove(student)
        return super().delete(request, *args, **kwargs)


## Group enrollments in course
class CreateGroupCourseEnrollmentView(View):
    def get(self, request, group_id, course_id):
        group = get_object_or_404(Group, id=group_id)
        course = get_object_or_404(Course, id=course_id)
        group_course_enrollment = GroupCourseEnrollment(group=group, course=course)
        group_course_enrollment.save()
        return redirect('teacher:group-detail', group_id=group_id)

class DeleteGroupCourseEnrollmentView(View):
    def get(self, request, group_id, course_id):
        group_course_enrollment = get_object_or_404(GroupCourseEnrollment, group_id=group_id, course_id=course_id)
        group_course_enrollment.delete()
        return redirect('teacher:group-detail', group_id=group_id)



## announcements

class AnnouncementListView(LoginRequiredMixin, ListView):
    model = Announcement
    template_name = 'teacher/announcement_list.html'
    context_object_name = 'announcements'
    ordering = ['-created_at']

    def get_queryset(self):
        course = get_object_or_404(Course, pk=self.kwargs['course_pk'])
        return self.model.objects.filter(course=course)


class AnnouncementCreateView(LoginRequiredMixin, CreateView):
    model = Announcement
    template_name = 'teacher/announcement_create.html'
    fields = ['title', 'description']
    context_object_name = 'announcement'

    def form_valid(self, form):
        course = get_object_or_404(Course, pk=self.kwargs['course_pk'])
        form.instance.course = course
        form.instance.user_profile = self.request.user.profile
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('teacher:announcement_list', kwargs={'course_pk': self.kwargs['course_pk']})


class AnnouncementDetailView(LoginRequiredMixin, DetailView):
    model = Announcement
    template_name = 'teacher/announcement_detail.html'
    context_object_name = 'announcement'


class AnnouncementUpdateView(LoginRequiredMixin, UpdateView):
    model = Announcement
    template_name = 'teacher/announcement_update.html'
    fields = ['title', 'description']
    context_object_name = 'announcement'

    def get_success_url(self):
        return reverse_lazy('teacher:announcement_detail', kwargs={'pk': self.object.pk})


class AnnouncementDeleteView(LoginRequiredMixin, DeleteView):
    model = Announcement
    template_name = 'teacher/announcement_delete.html'
    context_object_name = 'announcement'

    def get_success_url(self):
        course_pk = self.object.course.pk
        return reverse_lazy('teacher:announcement_list', kwargs={'course_pk': course_pk})



class AnnouncementFileCreateView(LoginRequiredMixin, CreateView):
    model = AnnouncementFile
    template_name = 'teacher/announcement_file_create.html'
    fields = ['file']
    context_object_name = 'announcement_file'

    def form_valid(self, form):
        announcement = get_object_or_404(Announcement, pk=self.kwargs['announcement_pk'])
        form.instance.announcement = announcement
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('teacher:announcement_detail', kwargs={'pk': self.kwargs['announcement_pk']})


class AnnouncementFileDeleteView(LoginRequiredMixin, DeleteView):
    model = AnnouncementFile
    template_name = 'teacher/announcement_file_delete.html'
    context_object_name = 'announcement_file'

    def get_success_url(self):
        announcement_pk = self.object.announcement.pk
        return reverse_lazy('teacher:announcement_detail', kwargs={'pk': announcement_pk})


class AnnouncementLinkCreateView(LoginRequiredMixin, CreateView):
    model = AnnouncementLink
    template_name = 'teacher/announcement_link_create.html'
    fields = ['link']
    context_object_name = 'announcement_link'

    def form_valid(self, form):
        announcement = get_object_or_404(Announcement, pk=self.kwargs['announcement_pk'])
        form.instance.announcement = announcement
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('teacher:announcement_detail', kwargs={'pk': self.kwargs['announcement_pk']})


class AnnouncementLinkDeleteView(LoginRequiredMixin, DeleteView):
    model = AnnouncementLink
    template_name = 'teacher/announcement_link_delete.html'
    context_object_name = 'announcement_link'

    def get_success_url(self):
        announcement_pk = self.object.announcement.pk
        return reverse_lazy('teacher:announcement_detail', kwargs={'pk': announcement_pk})


def testing(request):
    return render(request,'teacher/announcements.html')