
from django.conf.urls import url
# from django.conf.urls import patterns
from . import views


app_name = 'video'

urlpatterns = [
    # patterns('video.views'),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<video_id>[0-9]+)/$', views.details, name='details'),
    url(r'^(?P<video_id>[0-9]+)/video/add/$', views.VideoCreate.as_view(), name='video-add'),
    url(r'^video/(?P<pk>[0-9]+)/$', views.VideoUpdate.as_view(), name='video-update'),
    url(r'^video/(?P<pk>[0-9]+)/delete/$', views.VideoDelete.as_view(),  name='video-delete'),
    url(r'^registration/$', views.UserFormView.as_view(), name='registration'),
    url(r'^login/$', views.UserLoginView.as_view(), name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    # /video/profile/<user_id>
    url(r'^user/(?P<user_id>[0-9]+)/$',  views.UserProfileView,  name='user_profile'),
    # /video/search
    url(r'^discover/$', views.discover, name='discover'),
    url(r'^comment/(?P<video_id>[0-9]+)/$', views.CommentView, name='comment'),
]
