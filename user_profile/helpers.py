from io import BytesIO

import requests


def set_user_avatar(user):
    try:
        response = requests.get('http://188.166.8.84:8000/')
        image = BytesIO(response.content)
        user.profile.picture.save('doggo.png', image, True)
    except:
        pass
