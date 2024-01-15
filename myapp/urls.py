from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
   path('', views.home, name="home"),
   path('signup', views.signup, name="signup"),
   path('signin', views.signin, name="signin"),
   path('signout', views.signout, name="signout"),
   path('myquiz', views.myquiz, name="myquiz"),
   path('myprofile', views.myprofile, name="myprofile"),
   path('createquiz', views.createquiz, name="createquiz"),
   path('save_quiz/', views.save_quiz, name='save_quiz'),
   path('update_quiz/', views.update_quiz, name='update_quiz'),
   path('my_quiz_page', views.my_quiz_page, name='my_quiz_page'),
   path('account', views.account, name='account'),
   path('<int:quiz_id>', views.quiz_details, name='quiz_details'),
   path('<int:quiz_id>solve_quiz', views.solve_quiz, name='solve_quiz'),
   path('<int:quiz_id>save', views.save_quiz_view, name='save_quiz_view'),
   path('<int:quiz_id>back', views.back, name='back'),
   path('edit_quiz/<int:quiz_id>/', views.edit_quiz, name='edit_quiz'),
   path('show_results/<int:quiz_id>/', views.show_results, name='show_results'),
   path('add_user_to_quiz/<int:quiz_id>/', views.addUserToQuizView, name='add_user_to_quiz'),
   path('add_user_to_quiz/', views.addUserToQuizView, name='add_user_to_quiz'),

]
