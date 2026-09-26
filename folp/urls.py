from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.http import HttpResponse
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as admin_urls
from wagtail.documents import urls as document_urls

urlpatterns = [path('health/', lambda request: HttpResponse('ok', content_type='text/plain')), path('admin/', include(admin_urls)), path('documents/', include(document_urls))]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [path('', include(wagtail_urls))]
