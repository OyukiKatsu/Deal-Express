from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'user'
urlpatterns = [
    path('<str:username>', views.ProfileView.as_view(), name='profile_detalle'),
    path('edit/<str:username>', views.ProfileEditView, name='editar_perfil'),
    path('register/', views.register, name='registration'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
