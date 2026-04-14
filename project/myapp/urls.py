"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('test_page', views.test_page, name='test_page'),

    path('admin_login', views.admin_login, name='admin_login'),
    path('admin_changepassword', views.admin_changepassword, name='admin_changepassword'),
    path('admin_logout', views.admin_logout, name='admin_logout'),
    path('admin_home', views.admin_home, name='admin_home'),
    path('admin_feature_pending', views.admin_feature_pending, name='admin_feature_pending'),

    path('admin_designation_settings_add', views.admin_designation_settings_add, name='admin_designation_settings_add'),
    path('admin_designation_settings_view', views.admin_designation_settings_view, name='admin_designation_settings_view'),
    path('admin_designation_settings_delete', views.admin_designation_settings_delete, name='admin_designation_settings_delete'),
    path('admin_designation_settings_edit', views.admin_designation_settings_edit, name='admin_designation_settings_edit'),

    path('admin_staff_details_add', views.admin_staff_details_add, name='admin_staff_details_add'),
    path('admin_staff_details_view', views.admin_staff_details_view, name='admin_staff_details_view'),
    path('admin_staff_details_delete', views.admin_staff_details_delete, name='admin_staff_details_delete'),
    path('admin_staff_details_edit', views.admin_staff_details_edit, name='admin_staff_details_edit'),
    path('admin_staff_search', views.admin_staff_search, name='admin_staff_search'),

    path('admin_student_details_add', views.admin_student_details_add, name='admin_student_details_add'),
    path('admin_student_details_view', views.admin_student_details_view, name='admin_student_details_view'),
    path('admin_student_details_delete', views.admin_student_details_delete, name='admin_student_details_delete'),
    path('admin_student_details_edit', views.admin_student_details_edit, name='admin_student_details_edit'),
    path('admin_student_search', views.admin_student_search, name='admin_student_search'),

    path('admin_batch_student_details_add', views.admin_batch_student_details_add, name='admin_batch_student_details_add'),
    path('admin_batch_student_details_delete', views.admin_batch_student_details_delete, name='admin_batch_student_details_delete'),
    path('admin_batch_student_details_view', views.admin_batch_student_details_view, name='admin_batch_student_details_view'),

    path('admin_dataset_add', views.admin_dataset_add, name='admin_dataset_add'),
    path('admin_dataset_edit', views.admin_dataset_edit, name='admin_dataset_edit'),
    path('admin_dataset_view', views.admin_dataset_view, name='admin_dataset_view'),
    path('admin_dataset_delete', views.admin_dataset_delete, name='admin_dataset_delete'),

    path('admin_train_model', views.admin_train_model, name='admin_train_model'),

    path('staff_login', views.staff_login_check, name='staff_login'),
    path('staff_logout', views.staff_logout, name='staff_logout'),
    path('staff_home', views.staff_home, name='staff_home'),
    path('staff_changepassword', views.staff_changepassword, name='staff_changepassword'),
    path('staff_profile_view', views.staff_profile_view, name='staff_profile_view'),
    path('staff_feature_pending', views.staff_feature_pending, name='staff_feature_pending'),

    path('staff_staff_details_view', views.staff_staff_details_view, name='staff_staff_details_view'),

    path('staff_batch_student_details_view', views.staff_batch_student_details_view, name='staff_batch_student_details_view'),

    path('staff_student_assignment_view', views.staff_student_assignment_view, name='staff_student_assignment_view'),
    path('staff_student_assignment_pending_view', views.staff_student_assignment_pending_view, name='staff_student_assignment_pending_view'),
    path('staff_student_assignment_details_view', views.staff_student_assignment_details_view, name='staff_student_assignment_details_view'),
    path('staff_student_assignment_analysis', views.staff_student_assignment_analysis, name='staff_student_assignment_analysis'),

    path('staff_messages_add', views.staff_messages_add, name='staff_messages_add'),
    path('staff_messages_delete', views.staff_messages_delete, name='staff_messages_delete'),
    path('staff_messages_view', views.staff_messages_view, name='staff_messages_view'),


    path('student_login', views.student_login_check, name='student_login'),
    path('student_logout', views.student_logout, name='student_logout'),
    path('student_home', views.student_home, name='student_home'),
    path('student_changepassword', views.student_changepassword, name='student_changepassword'),
    path('student_profile_view', views.student_profile_view, name='student_profile_view'),

    path('student_assignment_details_1_add', views.student_assignment_details_1_add, name='student_assignment_details_1_add'),
    path('student_assignment_details_2_add', views.student_assignment_details_2_add, name='student_assignment_details_2_add'),
    path('student_assignment_details_3_add', views.student_assignment_details_3_add, name='student_assignment_details_3_add'),


    path('student_assignment_view', views.student_assignment_view, name='student_assignment_view'),
    path('student_assignment_details_view', views.student_assignment_details_view, name='student_assignment_details_view'),

    path('student_staff_messages_view', views.student_staff_messages_view, name='student_staff_messages_view'),

    path('student_staff_details_view', views.student_staff_details_view, name='student_staff_details_view'),


    path('user_login', views.user_login_check, name='user_login'),
    path('user_logout', views.user_logout, name='user_logout'),
    path('user_home', views.user_home, name='user_home'),
    path('user_details_add', views.user_details_add, name='user_details_add'),
    path('user_changepassword', views.user_changepassword, name='user_changepassword'),

    path('test_doc', views.test_doc, name='test_doc'),

]
