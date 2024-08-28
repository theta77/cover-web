from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.main, name='main'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('info/<username>', views.info, name='info'),
    path('chinfo', views.chinfo, name='chinfo'),
    path('chpass', views.chpass, name='chpass'),
    path('deluser', views.deluser, name='deluser'),
    path('subscribe/<username>, <idx>', views.subscribe, name='subscribe'),
    path('upload', views.upload, name='upload'),
    path('chvideo/<idx>', views.chvideo, name='chvideo'),
    path('delvideo/<idx>', views.delvideo, name='delvideo'),
    path('watch/<idx>', views.watch, name='watch'),
    path('like/<idx>', views.like, name='like'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)