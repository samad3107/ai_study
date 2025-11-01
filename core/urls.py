# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    
    path('register/', views.register_view, name='register'),
    
    # Summarization
    path('summarize/', views.pdf_upload_view, name='pdf_summarizer'), 
    path('notes/<int:pk>/', views.note_detail_view, name='note_detail'), 
    
    # Explanation
    path('explain/', views.topic_explanation_view, name='topic_explanation'), 
    
    # Quiz (Placeholders)
    path('quizzes/', views.quiz_list_view, name='quiz_list'),           
    path('quiz/<int:pk>/take/', views.take_quiz_view, name='take_quiz'), 
    path('quiz/<int:pk>/grade/', views.grade_quiz_view, name='grade_quiz'), 
    path('quiz/results/<int:pk>/', views.quiz_results_view, name='quiz_results'), 
]