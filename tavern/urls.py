from django.urls import path

from . import views

app_name = 'tavern'

urlpatterns = [
    #this is going to be the path for my home page
    path('', views.HomeView.as_view(), name='home'),

    #this route has value capturing so it will grab the lunch poll id as the pk var
    #example: localhost:8000/5/ <-- the # 5 is saved to a variable pk that we
    #can use in the view.
    path('<int:pk>/', views.LunchDetailView.as_view(), name='detail'),

    #This route includes value capturing to grab the contest id as the pk var
    path('<int:pk>/results/', views.LunchResultsView.as_view(), name='results'),

    #so does this one
    path('<int:pk>/vote/', views.LunchVoteView.as_view(), name='vote'),
]
