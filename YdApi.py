from datetime import datetime
import json
import requests
from tqdm import tqdm


class YdApi:

    @staticmethod
    def create_file_names(photos):
        # print(type(photos))
        # print(len(photos))
        for photo in photos:
            photo.name = str(photo.likes)
            if [p.likes for p in photos].count(photo.likes) > 1:
                photo.name += '_' + str(photo.date)
            photo.name += '.jpg'

    @staticmethod
    def check_folder_name(n_folder, ex_folders):
        if n_folder not in ex_folders:
            return n_folder
        n = 1
        n_folder += '_' + str(n)
        while n_folder in ex_folders:
            n_folder = n_folder.replace('_' + str(n), '_' + str(n + 1))
            n += 1
        return n_folder

    def __init__(self, token: str):
        self.auth = f'OAuth {token}'

    def get_folders(self):
        return [p['name'] for p in (requests.get("https://cloud-api.yandex.net/v1/disk/resources",
                                                 params={"path": '/'},
                                                 headers={"Authorization": self.auth})
                                    .json().get('_embedded').get('items')) if p['type'] == 'dir']

    def create_folder(self, folder_name):
        resp = requests.put("https://cloud-api.yandex.net/v1/disk/resources",
                            params={"path": '/' + folder_name},
                            headers={"Authorization": self.auth})
        # print(f'Creating folder "{folder_name}":' + str(resp.status_code))
        print()
        print(f'На Яндекс.Диске создаётся папка: {folder_name}')
        print()
        return resp.ok

    def upload(self, uid, photos):
        upload_folder = self.check_folder_name(uid, self.get_folders())
        self.create_file_names(photos)
        if self.create_folder(upload_folder):
            log_result = []
            for photo in tqdm(photos):
                response = requests.post("https://cloud-api.yandex.net/v1/disk/resources/upload",
                                         params={"path": '/' + upload_folder + '/' + photo.name,
                                                 "url": photo.url},
                                         headers={"Authorization": self.auth})
                if response.status_code == 202:
                    # print(f'Photo "{photo.name}" uploaded.')
                    log_result.append({"file_name": photo.name, "size": photo.size_type})
                else:
                    print(f'Error uploading photo "{photo.name}": '
                          f'{response.json().get("message")}. Status code: {response.status_code}')
            with open(f'{uid}_{datetime.now().strftime("%m_%d_%Y_%H_%M_%S")}_files.json', "w") as f:
                json.dump(log_result, f, ensure_ascii=False, indent=2)
