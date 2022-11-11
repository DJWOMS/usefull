from django.conf import settings
from django.urls import path, include, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from ninja import NinjaAPI
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from src.repository.views import repository
from src.auth.views import auth

schema_view = get_schema_view(
   openapi.Info(
      title="Collab Team Back API",
      default_version='v1',
      description="Docs",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,) if settings.IS_DOC else (permissions.IsAdminUser,),
)

api = NinjaAPI()

api.add_router("auth/", auth, tags=['auth'])
api.add_router("repository/", repository, tags=['repository'])


urlpatterns = [
    re_path(
        '^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'
    ),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # # Optional UI:
    # path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'),
    #      name='swagger-ui'),
    # path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # path('course/', include('src.course.urls')),
    path('wall/', include('src.wall.urls')),
    # path('feed/', include('src.feed.urls')),
    path('follower/', include('src.followers.urls')),
    path('profile/', include('src.profiles.urls')),
    path('team/', include('src.team.urls')),
    path('board/', include('src.dashboard.urls')),
    path('support/', include('src.support.urls')),
    path('chat/', include('src.chat.urls')),
    # path('team-chat/', include('src.team_chat.urls')),
    path('', api.urls),
]
