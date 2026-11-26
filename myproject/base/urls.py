from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('article/<slug:slug>/', views.read, name='read'),
    path('read/<int:id>/', views.read_by_id, name='read_by_id'),
    path('news/', views.news, name='news'),
    path('events/', views.events, name='events'),
    path('about/', views.about, name='about'),
    path('api/live-news/', views.live_news_api, name='live_news_api'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
]
