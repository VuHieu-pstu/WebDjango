from django.urls import path, re_path, register_converter
from . import views
from . import converters


register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    #path('', views.index, name='home'),  # http://127.0.0.1:8000 # day la su dung ham de view
    path('', views.WomenHome.as_view(), name='home'),# day la su dung class de view
    path('about/', views.about, name='about'),
    #path('addpage/', views.addpage, name='add_page'),# Day la su dung ham de view
    path('addpage/', views.AddPage.as_view(), name='add_page'),#day la su dung class de view
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    #path('post/<slug:post_slug>/', views.show_post, name='post'), # day la su dung ham de view
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'), # day la su dung class de view
    #path('category/<slug:cat_slug>/', views.show_category, name='category'), # Day la su dung ham de view
    path('category/<slug:cat_slug>/', views.WomenCategory.as_view(), name='category'), # Day la su dung class de view
    #path('tag/<slug:tag_slug>/', views.show_tag_postlist, name='tag'), # day la su dung ham de view
    path('tag/<slug:tag_slug>/', views.TagPostList.as_view(), name='tag'), # Day la su dung class de view
    #path('edit/<int:pk>/', views.UpdatePage.as_view(), name='edit_page'),
    path('edit/<slug:slug>/', views.UpdatePage.as_view(), name='edit_page'),
]
