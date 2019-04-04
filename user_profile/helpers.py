from io import BytesIO

import requests


def set_user_avatar(user):
    try:
        response = requests.get('http://gooddoggo.dog')
        image = BytesIO(response.content)
        user.profile.picture.save('doggo.png', image, True)
    except:
        pass
