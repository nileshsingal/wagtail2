# # oauth2_backend.py

# from django.conf import settings
# from django.shortcuts import redirect
# from django.urls import reverse
# from wagtail.admin.views.account import LoginView as WagtailLoginView

# class OAuth2LoginView(WagtailLoginView):
#     def get(self, request):
#         print("get 10")
#         # Construct the authorization URL for OAuth2
#         # auth_url = settings.OAUTH2_AUTH_URL + '?client_id=' + settings.OAUTH2_CLIENT_ID + '&redirect_uri=' + settings.OAUTH2_REDIRECT_URI + '&response_type=code&scope=' + settings.OAUTH2_SCOPE + '&state=your_state_parameter'
#         auth_url = 'https://accounts.google.com/o/oauth2/auth' + '?client_id=' + '413075880119-0qlrtvh6pfs2i2pa9a2r8m1k1vtufo3a.apps.googleusercontent.com' + '&redirect_uri=' + 'http://localhost:8000/oauth/callback/' + '&response_type=code&scope=' + 'openid profile email'
#         print(auth_url)
        
#         print("*****")
#         # Redirect the user to the authorization URL
#         return redirect(auth_url)


# oauth2_backend.py

import requests
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import path
from wagtail.admin.views.account import LoginView as WagtailLoginView

class OAuth2LoginView(WagtailLoginView):
    def get(self, request):
        # Construct the authorization URL for OAuth2
        auth_url = (
            'https://accounts.google.com/o/oauth2/auth'
            '?client_id=' + '413075880119-0qlrtvh6pfs2i2pa9a2r8m1k1vtufo3a.apps.googleusercontent.com' +
            '&redirect_uri=' + 'http://localhost:8000/oauth/callback/' +
            '&response_type=code&scope=' + 'openid profile email'
        )
        # Redirect the user to the authorization URL
        return redirect(auth_url)

def oauth_callback(request):
    code = request.GET.get('code')
    error = request.GET.get('error')

    if error:
        return render(request, 'error.html', {'error': error})

    # Exchange the authorization code for an access token
    token_url = 'https://oauth2.googleapis.com/token'
    data = {
        'code': code,
        'client_id': '413075880119-0qlrtvh6pfs2i2pa9a2r8m1k1vtufo3a.apps.googleusercontent.com',
        'client_secret': 'your_client_secret',
        'redirect_uri': 'http://localhost:8000/oauth/callback/',
        'grant_type': 'authorization_code',
    }
    response = requests.post(token_url, data=data)
    response_data = response.json()

    if 'error' in response_data:
        return render(request, 'home/templates/home/error.html', {'error': response_data["error_description"]})

    access_token = response_data.get('access_token')
    # Optionally, you can use the access token to fetch user info or perform other actions

    # Redirect to a success page or the main application
    return render(request, 'success.html', {'access_token': access_token})
