from django.urls import path

from .views import (
    home,
testing,
    CourseCreateView,
    CourseDetailView,
    CourseUpdateView,
    CourseDeleteView,
    CourseListView,
    CourseReleaseView,

    UnitCreateView,
    UnitDetailView,
    UnitUpdateView,
    UnitDeleteView,
    UnitListView,
    UnitReleaseView,

    LessonCreateView,
    LessonDetailView,
    LessonUpdateView,
    LessonDeleteView,
    LessonListView,
    LessonFileCreateView,
    LessonFileDeleteView,
    lesson_link_create,
    lesson_link_delete,
    LessonReleaseView,

    EnrollmentListView,
    EnrollmentCreateView,
    EnrollmentUpdateView,
    EnrollmentDeleteView,
    course_stats_view,

    GroupCreateView,
    GroupListView,
    GroupStudentListView,
    AddStudentToGroupView,
    RemoveStudentFromGroupView,
    CreateGroupCourseEnrollmentView,
    DeleteGroupCourseEnrollmentView,

    AnnouncementListView,
    AnnouncementCreateView,
    AnnouncementDetailView,
    AnnouncementUpdateView,
    AnnouncementDeleteView,
    AnnouncementFileCreateView,
    AnnouncementFileDeleteView,
    AnnouncementLinkCreateView,
    AnnouncementLinkDeleteView,
)

app_name = 'teacher'


urlpatterns = [
    path('', home, name='home'),
    # Course URLs
    path('testing',testing,name="testing"),
    path('course/create/', CourseCreateView.as_view(), name='course-create'),
    path('course/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('course/<int:pk>/update/', CourseUpdateView.as_view(), name='course-update'),
    path('course/<int:pk>/delete/', CourseDeleteView.as_view(), name='course-delete'),
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('course/release/<int:course_id>/', CourseReleaseView.as_view(), name='course-release'),

    # Unit URLs
    path('course/<int:course_pk>/units/create/', UnitCreateView.as_view(), name='unit-create'),
    path('units/<int:pk>/', UnitDetailView.as_view(), name='unit-detail'),
    path('units/<int:pk>/update/', UnitUpdateView.as_view(), name='unit-update'),
    path('course/<int:course_id>/units/<int:pk>/delete/', UnitDeleteView.as_view(), name='unit-delete'),
    path('course/<int:course_pk>/units/', UnitListView.as_view(), name='unit-list'),
    path('unit/<int:unit_id>/release/', UnitReleaseView.as_view(), name='unit-release'),

    # Lesson URLs
    path('units/<int:unit_pk>/lessons/create/', LessonCreateView.as_view(), name='lesson-create'),
    path('courses/<int:course_id>/lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),
    path('lessons/<int:pk>/update/', LessonUpdateView.as_view(), name='lesson-update'),
    path('course/<int:unit_id>/lessons/<int:pk>/delete/', LessonDeleteView.as_view(), name='lesson-delete'),
    path('courses/<int:course_id>/units/<int:unit_pk>/lessons/', LessonListView.as_view(), name='lesson-list'),
    path('lesson/<int:lesson_id>/release/', LessonReleaseView.as_view(), name='lesson-release'),

    # LessonFile URLs
    path('lessons/<int:lesson_pk>/files/create/', LessonFileCreateView.as_view(), name='lesson-file-create'),
    path('lesson-files/<int:pk>/delete/', LessonFileDeleteView.as_view(), name='lesson-file-delete'),

    # LessonLink URLs
    path('lessons/<int:lesson_pk>/links/create/', lesson_link_create, name='lesson-link-create'),
    path('lesson-links/<int:pk>/delete/', lesson_link_delete, name='lesson-link-delete'),

    #FOr student stats and enrollments
    path('course/<int:course_id>/enrollment/', EnrollmentListView.as_view(), name='enrollment-list'),
    path('enrollment/create/<int:course_id>/<int:student_id>/', EnrollmentCreateView.as_view(), name='enrollment-create'),
    path('course/<int:course_id>/enrollment/<int:pk>/update/', EnrollmentUpdateView.as_view(), name='enrollment-update'),
    path('enrollment/<int:course_id>/<int:enrollment_id>/delete/', EnrollmentDeleteView.as_view(), name='enrollment-delete'),
    path('course/<int:course_id>/stats/', course_stats_view, name='course-stats'),

    ## groups
    path('groups/create/', GroupCreateView.as_view(), name='group-create'),
    path('groups/', GroupListView.as_view(), name='group-list'),
    path('groups/<int:group_id>/students/', GroupStudentListView.as_view(), name='group-student-list'),
    path('groups/<int:group_id>/add-student/', AddStudentToGroupView.as_view(), name='group-add-student'),
    path('groups/<int:group_id>/remove-student/<int:pk>/', RemoveStudentFromGroupView.as_view(), name='group-remove-student'),


    ##group course enrollments
    path('group/<int:group_id>/course/<int:course_id>/enroll/', CreateGroupCourseEnrollmentView.as_view(), name='group-course-enroll'),
    path('group/<int:group_id>/course/<int:course_id>/enroll/delete/', DeleteGroupCourseEnrollmentView.as_view(), name='group-course-enrollment-delete'),

    ## announcements
    path('course/<int:course_pk>/announcements/', AnnouncementListView.as_view(), name='announcement-list'),
    path('course/<int:course_pk>/announcements/create/', AnnouncementCreateView.as_view(), name='announcement-create'),
    path('announcement/<int:pk>/', AnnouncementDetailView.as_view(), name='announcement-detail'),
    path('announcement/<int:pk>/update/', AnnouncementUpdateView.as_view(), name='announcement-update'),
    path('announcement/<int:pk>/delete/', AnnouncementDeleteView.as_view(), name='announcement-delete'),
    path('announcement/<int:announcement_pk>/files/create/', AnnouncementFileCreateView.as_view(), name='announcement-file-create'),
    path('announcement/files/<int:pk>/delete/', AnnouncementFileDeleteView.as_view(), name='announcement-file-delete'),
    path('announcement/<int:announcement_pk>/links/create/', AnnouncementLinkCreateView.as_view(), name='announcement-link-create'),
    path('announcement/links/<int:pk>/delete/', AnnouncementLinkDeleteView.as_view(), name='announcement-link-delete'),


]



