from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from cf_core.router import router

from cf_users.api import PublishedProfileVewSet, UserProfileViewSet

router.register('profiles', PublishedProfileVewSet, base_name='profiles')
router.register('published-profiles', UserProfileViewSet,
                base_name='published-profiles')

urlpatterns = [
    url(r'^api/v1/', include(router.get_urls())),
    url(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
