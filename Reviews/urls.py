
from django.urls import path,re_path
from . import views

app_name = 'Reviews'
urlpatterns = [

	path('', views.review_list, name='review_list'),
	path('login_user/',views.login_user, name='login_user'),
	path('create_new_user/', views.create_new_user ,name='create_new_user'),
	path('logout_user/',views.logout_user, name='logout_user'),
	path('review/<int:review_id>/', views.review_detail, name='review_detail'),
	path('college/', views.college_list ,name='college_list'),
	path('college/<int:college_id>/add_review/', views.add_review, name='add_review'),
	path('college/<int:college_id>/', views.college_detail, name='college_detail'),
	path('searched/', views.searched, name='searched'),
	path('search/', views.autocomplete_college, name='autocomplete_college'),
	path('add_college/', views.add_college, name='add_college'),
	path('req_query/', views.req_query, name='req_query'),
	path('answer_query/', views.answer_query, name='answer_query'),
	path('submit_query/', views.submit_query, name='submit_query'),
	path('recommend/', views.recommend, name='recommend'),
	path('get_deps/',views.get_deps, name='get_deps'),
]
