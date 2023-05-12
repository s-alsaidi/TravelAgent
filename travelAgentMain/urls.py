from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.home,name='home'),
    path('family/',views.family,name='family'),
    path('work/',views.work,name='work'),
    path('ekamah/',views.ekamah,name='ekamah'),
    path('mandate/',views.mandate,name='mandate'),

    
    # path('blog/detail/<int:post_id>/',views.post_detail,name='detail'),
    # # path('new_post/', views.PostCreateView.as_view(), name='new_post'),

    # path('new_post/', PostCreateView.as_view(), name='new_post'),
    # path('blog/detail/<slug:pk>/update/',PostUpdateView.as_view(),name='post_update'),

]