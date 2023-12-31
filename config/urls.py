from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from impressions.views import RecommendationView
from video.views import VideoViewSet

router = DefaultRouter()
router.register('', VideoViewSet)


schema_view = get_schema_view(
    openapi.Info(
        title='Hackathon2 API',
        default_version='v1',
        description='Chatting app',
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.IsAdminUser]
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # path('', include(router.urls)),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema_swagger-ui'),
    path('api/account/', include('account.urls')),
    path('api/video/', include(router.urls)),
    path('api/recommendation/', RecommendationView.as_view())
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

