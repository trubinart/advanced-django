from social_core.exceptions import AuthForbidden

def save_user_profile(backend, user, response, *args, **kwargs):
    print(response)
    print(response['locale'])
    if backend.name == "google-oauth2":
        print('backend')
        if 'locale' in response.keys():
            print('locale')
            locale = response['locale']
            if locale != 'ru':
                user.delete()
                raise AuthForbidden('social_core.backends.google.GoogleOAuth2')
            else:
                user.usersprofile.locate = response['locale']

        user.usersprofile.save()
