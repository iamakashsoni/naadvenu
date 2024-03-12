from django.urls import path, include, re_path
from pages import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name='home'),
    path('about-us/', views.aboutUs, name='about-us'),
    path('contact-us/', views.contactUs, name='contact-us'),
    path('gallery', views.gallery, name='gallery'),
    path('gallery/<slug:slug>/', views.galleryitem, name='gallery-item'),
    path('media-coverage', views.media_coverage, name='media-coverage'),
    path('media-coverage/<slug:slug>/', views.media_coverage_item, name='media-coverage-item'),
    path('events-workshops', views.events_workshops, name='events-workshops'),
    path('student-registration', views.studentRegistration, name='student-registration'),
    path('alankar-generator', views.alankarGenerator, name='alankar-generator'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('tinymce/', include('tinymce.urls')),
    re_path(r'^media/(?P<path>.*)/$', views.serve_media_file, name='media_file'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
