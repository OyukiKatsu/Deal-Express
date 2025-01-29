from django.urls import path
from marketplace_empresa import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index.as_view(), name='index_marketplace_empresa'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)