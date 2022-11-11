from django.urls import path
from . import views


urlpatterns = [
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('', views.CourseListView.as_view(), name='course_list'),
    path('<int:pk>/', views.CourseView.as_view(), name='course_detail'),
    path('<int:pk>/lesson/', views.LessonListView.as_view(), name='lesson_list'),
    path('lesson/<int:pk>/', views.LessonView.as_view(), name='lesson_detail'),
    path('lesson/task/realization_task/',
         views.RealizationTaskView.as_view({'post':'create'}),
         name='realization_task_create'),
    path('lesson/task/realization_task/<int:pk>/',
         views.RealizationTaskView.as_view({'get':'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='realization_task_detail'),
    path('lesson/<int:pk>/task/', views.TaskListView.as_view(), name='task_list'),
    path('lesson/<int:pk>/comment/', views.CommentListView.as_view(), name='comment_list'),
    path('lesson/comment/', views.CommentView.as_view({'post':'create'}), name='comment_create'),
    path('lesson/comment/<int:pk>/',
         views.CommentView.as_view({'get':'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='comment_detail'),
    path('signup/', views.SignUpForCourseView.as_view(), name='course_signup'),
    path('signout/', views.SignOutForCourseView.as_view(), name='course_signout'),
]
