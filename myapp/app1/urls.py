from.import views
from django.urls import path
from django.contrib.auth import views as auth_views
urlpatterns = [
    path("accounts/login/", auth_views.LoginView.as_view(template_name='login.html', redirect_authenticated_user=True),
         name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page='login'), name="logout"),
    path('', views.home, name='home'),

    path('register/', views.register, name="signup_worker"),
    path('register_owner/', views.register_owner, name="signup"),
    path('accounts/profile/', views.account_settings, name="account_settings"),
    path("single_booked/<int:id>", views.booked_single, name="single_booked"),
    path("single_worker_booked/<int:id>", views.worker_single, name="single_worker_booked"),
    path('about/', views.about, name='about'),
    path('add_bookmark/<int:job_id>/', views.add_bookmark, name='add_bookmark'),
    path('remove_bookmark/<int:job_id>/', views.remove_bookmark, name='remove_bookmark'),
    path('bookmarked_jobs/', views.bookmarked_jobs, name='bookmarked_jobs'),

     
    
    path("worker_action/", views.worker_action, name="worker_action"),
    path("accept_worked/", views.accept_work, name="accept_worked"),
    path("single_worker_booked/worker_profile/<int:id>", views.worker_profile, name="worker_profile"),
    path("worker_profile/<int:id>", views.my_profile, name="my_profile"),
    path("find_job",views.search,name="search_result"),
    path('post_jobs/', views.job_post, name='post_jobs'),

     path('testimonials/', views.testimonials, name='testimonials'),
    
    path('posted_jobs/', views.posted_jobs, name='posted_jobs'),
    path('job_update/<int:job_id>/', views.job_update, name='job_update'),
    path('job_delete/<int:job_id>/', views.job_delete, name='job_delete'),

    path('job_applicants/', views.job_applicants, name='job_applicants'),
    path('favicon.ico/', views.empty_view),
    
    
    path('your_booked/', views.get_work, name="booked"),
    path('owner', views.owner, name="owner"),
    path('<str:room>/', views.room, name='room'),
    path('room/checkview', views.checkview, name='checkview'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),

    
    
    #path('about/', views.about, name='about'),
    

    ]