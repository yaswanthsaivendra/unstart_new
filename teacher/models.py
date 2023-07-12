from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone


## Courses

class Course(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='course_images', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    course_price = models.PositiveBigIntegerField(default=0, blank=True)
    is_paid = models.BooleanField(default=False)
    course_level = models.CharField(max_length=20, choices=[
            ('Beginner', 'Beginner'),
            ('Intermediate', 'Intermediate'),
            ('Advanced', 'Advanced')
        ],
        default='Beginner'
    )
    created_at = models.DateTimeField(default=timezone.now)
    is_released = models.BooleanField(default = False)

    def __str__(self):
        return self.title


class Unit(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField(null=True)
    is_released  = models.BooleanField(default = False)
    slug = models.SlugField(null=True, max_length=300, unique=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title + self.course.title)
        super(Unit, self).save(*args, **kwargs)

    @property
    def lessons_completed(self):
        lesson_ids = self.lesson_set.values_list('id', flat=True)
        completed_lesson_count = LessonProgress.objects.filter(
            enrollment__student=self.request.user,
            lesson__in=lesson_ids,
            is_completed=True
        ).count()
        return completed_lesson_count
    
    @property
    def total_lessons(self):
        return self.lesson_set.count()
    
    @property
    def completion_percentage(self):
        if self.total_lessons > 0:
            return (self.lessons_completed / self.total_lessons) * 100
        return 0


class Lesson(models.Model):
    lesson_number = models.IntegerField(null=True, blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_released = models.BooleanField(default = False)
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.lesson_number:
            # Get the maximum lesson_number for the current unit
            max_lesson_number = Lesson.objects.filter(unit=self.unit).aggregate(
                max_lesson_number=models.Max('lesson_number')
            )['max_lesson_number']
            if max_lesson_number is not None:
                self.lesson_number = max_lesson_number + 1
            else:
                self.lesson_number = 1

        super().save(*args, **kwargs)

class LessonFile(models.Model):
    lesson = models.ForeignKey(Lesson , on_delete = models.CASCADE,related_name='files')
    file = models.FileField(upload_to='resources/', null=True, blank=True)

    def __str__(self):
        return self.lesson.title

class LessonLink(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='links')
    link = models.URLField()

    def __str__(self):
        return self.lesson.title



## for student course enrollment

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    last_accessed = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"

    def calculate_completion_percentage(self):
        total_lessons = self.course.unit_set.aggregate(total_lessons=models.Count('lesson'))['total_lessons']
        lessons_completed = self.lessonprogress_set.filter(is_completed=True).count()
        completion_percentage = (lessons_completed / total_lessons) * 100
        return completion_percentage


class LessonProgress(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('enrollment', 'lesson')

    def __str__(self):
        return f"{self.enrollment.student.username} - {self.lesson.title}"



## for student Groups
class Group(models.Model):
    name = models.CharField(max_length=200)
    students = models.ManyToManyField(User, through='GroupMembership', related_name='student_groups')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')
    created_at = models.DateTimeField(default=timezone.now)
    is_private = models.BooleanField(default=False)
    # courses = models.ManyToManyField(Course, through='GroupCourseEnrollment', related_name='enrolled_groups')

    def __str__(self):
        return self.name


class GroupMembership(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.student.username} - {self.group.name}"

## for student group enrollment in course

class GroupCourseEnrollment(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.group.name} - {self.course.title}"



## announcements

class Announcement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_released = models.BooleanField(default=False)

    slug = models.SlugField(max_length=16, null=True, unique=True, editable=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.slug = slugify(get_unique_string(self.title, self.user))
        super().save(*args, **kwargs)


class AnnouncementFile(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    file = models.FileField(upload_to='announcement_files/')

    def __str__(self) -> str:
        return f"{self.announcement.title} - file {self.id}"


class AnnouncementLink(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    link = models.URLField()

    def __str__(self) -> str:
        return f"{self.announcement.title} - link {self.id}"


## assignments

class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=500)
    description = models.TextField()
    max_grade = models.PositiveIntegerField()
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)
    is_released = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class AssignmentFile(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    file = models.FileField(upload_to='assignment_files/')

    def __str__(self) -> str:
        return f"{self.assignment.title} - file {self.id}"


class AssignmentLink(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    link = models.URLField()

    def __str__(self) -> str:
        return f"{self.assignment.title} - link {self.id}"


class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    submission_date = models.DateTimeField(default=timezone.now)
    file = models.FileField(upload_to='assignment_submissions/')
    grade = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.username}'s submission for {self.assignment.title}"