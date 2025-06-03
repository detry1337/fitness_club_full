from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from club import views as club_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', club_views.home, name='home'),
    path('about/', club_views.about, name='about'),
    path('services/', club_views.services, name='services'),
    path('register/', club_views.register, name='register'),
    path('login/', club_views.user_login, name='login'),
    path('logout/', club_views.user_logout, name='logout'),
    path('profile/', club_views.profile, name='profile'),
    path('memberships/', club_views.membership_list, name='memberships'),
    path('membership/add/', club_views.add_membership, name='add_membership'),
    path('services/<int:service_id>/', club_views.service_detail, name='service_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)