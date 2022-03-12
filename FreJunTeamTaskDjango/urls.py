"""FreJunTeamTaskDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core.views import CreateTeamViewSet, TaskViewset, StatusChangeReportViewset, AvailabilityViewset
from rest_framework.routers import DefaultRouter
from django.conf import settings
from rest_framework.authtoken.views import obtain_auth_token  # <-- Here
from rest_framework_simplejwt import views as jwt_views

from django.conf.urls.static import static


router = DefaultRouter()
router.register(r'task', TaskViewset, basename='task')
router.register(r'report', StatusChangeReportViewset, basename='status-report')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('team', CreateTeamViewSet.as_view(), name='team'),
    path('availability/', AvailabilityViewset.as_view(), name='availability'),
    # path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('', include(router.urls)),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)