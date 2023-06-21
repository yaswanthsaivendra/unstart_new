from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Count
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
    Assignment,
    AssignmentFile,
    AssignmentLink,
    AssignmentSubmission
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
        return render(request, 'teacher/home.html' , {'courses': courses})

def testing(request):
    return render(request,'mainabout.html')

# Course Views
class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    fields = ['title', 'image', 'course_price', 'is_paid', 'course_level']
    template_name = 'teacher/courses.html'
    success_url = reverse_lazy('teacher:course-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'teacher/course.html'
    context_object_name = 'course'


class CourseUpdateView(LoginRequiredMixin, UpdateView):
    model = Course
    fields = ['title', 'image', 'course_price', 'is_paid', 'course_level']
    template_name = 'teacher/course.html'
    context_object_name = 'course'

    def get_success_url(self):
        return reverse_lazy('teacher:course-detail', kwargs={'pk': self.kwargs['pk']})


class CourseDeleteView(LoginRequiredMixin, DeleteView):
    model = Course
    success_url = reverse_lazy('teacher:course-list')
    template_name = 'teacher/course.html'
    context_object_name = 'course'

class CourseReleaseView(LoginRequiredMixin, View):
    def post(self, request, course_id):
        course = Course.objects.get(pk=course_id)
        course.is_released = not course.is_released
        course.save()
        return redirect('teacher:course-detail', pk=course_id)


class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'teacher/courses.html'
    context_object_name = 'courses'


    def get_queryset(self):
        return Course.objects.filter(created_by=self.request.user).order_by('-created_at')

# Unit Views
class UnitCreateView(LoginRequiredMixin, CreateView):
    model = Unit
    fields = ['title', 'description', 'due_date']
    template_name = 'teacher/units.html'

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
        course_pk = self.kwargs.get('course_pk')
        course = get_object_or_404(Course, pk=course_pk)
        form.instance.course = course
        return super().form_valid(form)


class UnitDetailView(LoginRequiredMixin, DetailView):
    model = Unit
    template_name = 'teacher/unit_detail.html'
    context_object_name = 'unit'


class UnitUpdateView(LoginRequiredMixin, UpdateView):
    model = Unit
    fields = ['title', 'description', 'due_date']
    template_name = 'teacher/lessons.html'
    context_object_name = 'unit'

    def get_success_url(self):
        return reverse_lazy('teacher:lessons-list', kwargs={'unit_pk': self.kwargs['pk']})

class UnitDeleteView(LoginRequiredMixin, DeleteView):
    model = Unit
    template_name = 'teacher/units.html'
    context_object_name = 'unit'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_id = self.kwargs['course_id']
        context['course_id'] = course_id
        return context

    def get_success_url(self):
        course_id = self.kwargs['course_id']
        return reverse_lazy('teacher:unit-list', kwargs={'course_pk': course_id})

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        course_id = self.kwargs['course_id']
        pk = self.kwargs['pk']
        return get_object_or_404(queryset, course_id=course_id, pk=pk)




class UnitListView(LoginRequiredMixin, ListView):
    model = Unit
    template_name = 'teacher/units.html'
    context_object_name = 'units'

    def get_queryset(self):
        course_id = self.kwargs.get('course_pk')
        queryset = super().get_queryset().filter(course_id=course_id)
        released_units = queryset.filter(is_released=True)
        draft_units = queryset.filter(is_released=False)
        return draft_units, released_units

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_id = self.kwargs['course_pk']
        context['course_id'] = course_id
        draft_units, released_units = self.get_queryset()
        context['released_units'] = released_units
        context['draft_units'] = draft_units
        return context


class UnitReleaseView(LoginRequiredMixin, View):
    def post(self, request, unit_id):
        unit = Unit.objects.get(pk=unit_id)
        unit.is_released = not unit.is_released
        unit.save()
        return redirect('teacher:lesson-list', unit_pk=unit_id)


# Lesson Views
class LessonCreateView(LoginRequiredMixin, CreateView):
    model = Lesson
    fields = ['title', 'description']
    template_name = 'teacher/lessons.html'

    def get_success_url(self):
        return reverse_lazy('teacher:lesson-list', kwargs={'unit_pk': self.kwargs['unit_pk']})

    def get_initial(self):
        initial = super().get_initial()
        initial['unit'] = get_object_or_404(Unit, pk=self.kwargs['unit_pk'])
        return initial

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        unit_pk = self.kwargs.get('unit_pk')
        unit = get_object_or_404(Unit, pk=unit_pk)
        form.instance.unit = unit
        return super().form_valid(form)


class LessonDetailView(LoginRequiredMixin, DetailView):
    model = Lesson
    template_name = 'teacher/lesson_detail.html'
    context_object_name = 'lesson'


class LessonReleaseView(LoginRequiredMixin, View):
    def post(self, request, lesson_id):
        lesson = Lesson.objects.get(pk=lesson_id)
        lesson.is_released = not lesson.is_released
        lesson.save()
        return redirect('teacher:lesson-detail', pk=lesson_id)


class LessonUpdateView(LoginRequiredMixin, UpdateView):
    model = Lesson
    fields = ['lesson_number', 'title', 'description']
    template_name = 'teacher/lesson_update.html'
    context_object_name = 'lesson'

    def get_success_url(self):
        return reverse_lazy('teacher:lesson-detail', kwargs={'pk': self.kwargs['pk']})


class LessonDeleteView(LoginRequiredMixin, DeleteView):
    model = Lesson
    template_name = 'teacher/lessons.html'
    context_object_name = 'lesson'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        unit_id = self.kwargs['unit_id']
        context['unit_id'] = unit_id
        return context

    def get_success_url(self):
        unit_id = self.kwargs['unit_id']
        return reverse_lazy('teacher:lesson-list', kwargs={'unit_pk': unit_id})

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        unit_id = self.kwargs['unit_id']
        pk = self.kwargs['pk']
        return get_object_or_404(queryset, unit_id=unit_id, pk=pk)


class LessonListView(LoginRequiredMixin, ListView):
    model = Lesson
    template_name = 'teacher/lessons.html'
    context_object_name = 'lessons'

    def get_queryset(self):
        unit_id = self.kwargs.get('unit_pk')
        queryset = super().get_queryset().filter(unit_id=unit_id)
        queryset = queryset.annotate(
            lessonfile_count=Count('files'),
            lessonlink_count=Count('links')
        )
        released_lessons = queryset.filter(is_released=True)
        draft_lessons = queryset.filter(is_released=False)
        return draft_lessons, released_lessons
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        unit_id = self.kwargs['unit_pk']
        unit = Unit.objects.filter(id = unit_id).first()
        context['unit'] = unit
        draft_lessons, released_lessons = self.get_queryset()
        context['released_lessons'] = released_lessons
        context['draft_lessons'] = draft_lessons
        return context


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




class EnrollmentListView(View):
    template_name = 'teacher/enrollment_list.html'

    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        student_enrollments = course.enrollment_set.all().select_related('student')
        # print(enrolled_students)
        all_students = User.objects.filter(profile__status = 's')

        not_enrolled_students = all_students.exclude(enrollment__course=course)

        context = {
            'course': course,
            'student_enrollments': student_enrollments,
            'not_enrolled_students': not_enrolled_students
        }

        return render(request, self.template_name, context)



class EnrollmentCreateView(View):
    def get(self, request, course_id, student_id):
        course = Course.objects.get(id=course_id)
        student = User.objects.get(id=student_id)

        Enrollment.objects.create(course=course, student=student)
        
        return redirect('teacher:enrollment-list', course_id=course_id)


class EnrollmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Enrollment
    template_name = 'teacher/enrollment_form.html'
    context_object_name = 'enrollment'
    success_url = reverse_lazy('teacher:enrollment-list')


class EnrollmentDeleteView(View):
    def get(self, request, course_id, enrollment_id):
        enrollment = get_object_or_404(Enrollment, course_id=course_id, id=enrollment_id)
        enrollment.delete()
        return redirect('teacher:enrollment-list', course_id=course_id)


def course_stats_view(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollments = Enrollment.objects.filter(course=course)

    completion_data = []
    for enrollment in enrollments:
        student = enrollment.student
        completion_percentage = enrollment.calculate_completion_percentage()
        completion_data.append({
            'student': student,
            'completion_percentage': completion_percentage
        })

    context = {
        'course': course,
        'completion_data': completion_data
    }
    return render(request, 'teacher/course_stats.html', context)






## Groups

class GroupCreateView(LoginRequiredMixin, CreateView):
    model = Group
    fields = ['name']
    template_name = 'teacher/group_form.html'
    success_url = reverse_lazy('teacher:group-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class GroupListView(View):
    template_name = 'teacher/group_list.html'

    def get(self, request):

        # Separate public and private groups
        public_groups = Group.objects.filter(is_private=False)
        private_groups = Group.objects.filter(is_private=True, created_by=request.user)

        context = {
            'public_groups': public_groups,
            'private_groups': private_groups,
        }

        return render(request, self.template_name, context)



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
    template_name = 'teacher/announcements.html'
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





# Assignment views
class AssignmentListView(LoginRequiredMixin, ListView):
    model = Assignment
    template_name = 'teacher/assignment_list.html'
    context_object_name = 'assignments'


class AssignmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Assignment
    template_name = 'teacher/assignment_update.html'
    fields = ['title', 'description', 'max_grade', 'due_date', 'is_released']
    success_url = reverse_lazy('teacher:assignment-list')


class AssignmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Assignment
    template_name = 'teacher/assignment_confirm_delete.html'
    success_url = reverse_lazy('teacher:assignment-list')


class AssignmentDetailView(LoginRequiredMixin, DetailView):
    model = Assignment
    template_name = 'teacher/assignment_detail.html'
    context_object_name = 'assignment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        assignment = self.get_object()
        context['linked_files'] = assignment.assignmentfile_set.all()
        context['linked_links'] = assignment.assignmentlink_set.all()
        return context


class AssignmentCreateView(LoginRequiredMixin, CreateView):
    model = Assignment
    template_name = 'teacher/assignment_create.html'
    fields = ['title', 'description', 'max_grade', 'due_date']
    success_url = reverse_lazy('teacher:assignment-list')


# AssignmentFile views
class AssignmentFileCreateView(LoginRequiredMixin, CreateView):
    model = AssignmentFile
    template_name = 'teacher/assignmentfile_create.html'
    fields = ['file']
    success_url = reverse_lazy('teacher:assignment-list')

    def form_valid(self, form):
        assignment = get_object_or_404(Assignment, pk=self.kwargs['assignment_pk'])
        form.instance.assignment = assignment
        return super().form_valid(form)


class AssignmentFileDeleteView(LoginRequiredMixin, DeleteView):
    model = AssignmentFile
    template_name = 'teacher/assignmentfile_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('teacher:assignment-detail', kwargs={'pk': self.object.assignment.pk})


# AssignmentLink views
class AssignmentLinkCreateView(LoginRequiredMixin, CreateView):
    model = AssignmentLink
    template_name = 'teacher/assignmentlink_create.html'
    fields = ['assignment', 'link']
    success_url = reverse_lazy('teacher:assignment-list')

    def form_valid(self, form):
        assignment = get_object_or_404(Assignment, pk=self.kwargs['assignment_pk'])
        form.instance.assignment = assignment
        return super().form_valid(form)


class AssignmentLinkDeleteView(LoginRequiredMixin, DeleteView):
    model = AssignmentLink
    template_name = 'teacher/assignmentlink_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('teacher:assignment-detail', kwargs={'pk': self.object.assignment.pk})


# Update release status view
class AssignmentReleaseUpdateView(LoginRequiredMixin, UpdateView):
    model = Assignment
    template_name = 'teacher/assignment_release_update.html'
    fields = ['is_released']
    success_url = reverse_lazy('teacher:assignment-list')
