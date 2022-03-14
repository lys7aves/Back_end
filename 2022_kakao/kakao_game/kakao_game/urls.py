"""kakao_game URL Configuration

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
from django.urls import path
from management_system import views as management_system_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('start', management_system_views.start_api),
    path('waiting_line', management_system_views.waiting_line_api),
    path('game_result', management_system_views.game_result_api),
    path('user_info', management_system_views.user_info_api),
    path('match', management_system_views.match_api),
]
