
from django.urls import path

from main.views.HomeTeacherView import ListVideoChatView, CreateVideoChatView
from main.views.attendance_view import AttendanceView
from main.views.edit_profile import ProfileView
from main.views.homeMillFormaView import HomeView

app_name = 'main'
urlpatterns = [
    path('teacher/<uuid:formation_id>/',ListVideoChatView.as_view(), name="session"),
    path('session/<uuid:formation_id>/',CreateVideoChatView.as_view(), name="create_session"),
    path('',HomeView.as_view(),name="home"),
    path('view_attendance/<uuid:formation_id>/',AttendanceView.as_view(), name="attendance_list"),
    path('edit-profile/',ProfileView.as_view(), name="edit-profile")

]