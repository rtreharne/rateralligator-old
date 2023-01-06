from django.urls import path

from . import views

app_name = 'gator'
urlpatterns = [
    path('', views.index, name='index'),
    path('thanks/', views.thanks, name='thanks'),
    path('agree/', views.agree, name='agree'),  
    path('disagree/', views.disagree, name='disagree'),
    path('abuse/', views.abuse, name='abuse'),
    path('<str:slug>/', views.detail, name='detail'),
    path('<int:response_id>/comment/', views.comment, name='comment'),
    path('<str:slug>/results/', views.results, name='results')
]