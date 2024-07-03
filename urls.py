# mysite/urls.py

from django.urls import include, path, re_path
from django.contrib import admin
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail_oauth2 import urls as wagtail_oauth2_urls
from home.oauth2_backend import OAuth2LoginView, oauth_callback
from home.views import  Oauth2LogoutView

urlpatterns = [
    path('dadmin/', admin.site.urls),  # Django admin URL
    path('admin/', include(wagtailadmin_urls)),  # Wagtail admin URL
    path('oauth2/', include(wagtail_oauth2_urls)),  # OAuth2 endpoints for Wagtail
    path('admin/login/oauth2/', OAuth2LoginView.as_view(), name='oauth2_login'),
    re_path(r"^login/$", OAuth2LoginView.as_view(), name="wagtailadmin_login"),
    re_path(r"^logout/$", Oauth2LogoutView.as_view(), name="wagtailadmin_logout"),
    path('oauth/callback/', oauth_callback, name='oauth_callback')
]

# Ensure Wagtail page serving is the last pattern
urlpatterns += [
    path("", include(wagtail_urls)),  # Serve Wagtail pages from root
]
