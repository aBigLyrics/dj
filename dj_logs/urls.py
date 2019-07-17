from django.conf import settings
from django.contrib import admin
from django.templatetags.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('topics/', views.topics, name='topics'),
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    path('new_topic/', views.new_topic, name='new_topic'),
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    path('search/', views.search, name='search'),
    path('topics/delete/<int:delete_id>/', views.delete_entry, name='delete_entry'),
    path('delete/<int:topic_id>/', views.delete_topic, name='delete_topic'),
    path('translation/', views.translation, name='translation'),
    path('other/', views.other, name='other'),
    path('other/face/', views.baidu, name='face'),
    path('trans_aip/', views.trans_aip, name='trans_aip'),

]
# handler404 = views.page_not_found
