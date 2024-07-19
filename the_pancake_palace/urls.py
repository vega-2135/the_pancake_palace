"""
URL configuration for the_pancake_palace project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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


urlpatterns = [
    path("about/", include("about.urls"), name="about-urls"),
    path("accounts/", include("allauth.urls")),
    path('accounts/', include('allauth.socialaccount.urls')),
    path("admin/", admin.site.urls),
    path("contact/", include("contact.urls"), name="contact-urls"),
    path("summernote/", include('django_summernote.urls')),
    path("", include("recipes.urls"), name="recipes-urls"),
]


handler400 = 'the_pancake_palace.views.error_400'
handler403 = 'the_pancake_palace.views.error_403'
handler404 = 'the_pancake_palace.views.error_404'
handler500 = 'the_pancake_palace.views.error_500'
