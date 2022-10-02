import requests
from Photo import Photo


class VkApi:

    @staticmethod
    def find_largest(sizes):
        sizes_chart = ['x', 'z', 'y', 'r', 'q', 'p', 'o', 'x', 'm', 's']
        for chart in sizes_chart:
            for size in sizes:
                if size['type'] == chart:
                    return size

    def __init__(self, token, version, user, qty):
        self.token = token
        self.version = version
        self.qty = qty
        if user.isdigit():
            self.user_id = user
        else:
            self.user_id = requests.get('https://api.vk.com/method/utils.resolveScreenName', params={
                'access_token': self.token,
                'v': self.version,
                'screen_name': user,
                }).json()['response']['object_id']

    def get_photos(self, qty):
        get_url = 'https://api.vk.com/method/photos.get'
        resp = requests.get(get_url, params={
            'access_token': self.token,
            'v': self.version,
            'owner_id': self.user_id,
            'album_id': 'profile',
            'photo_sizes': 1,
            'extended': 1
        }).json()['response']['items']

        return sorted([Photo(photo.get('date'),
                             photo.get('likes')['count'],
                             self.find_largest(photo.get('sizes'))) for photo in resp],
                      key=lambda p: p.maxsize, reverse=True)[:qty]
