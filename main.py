import configparser
from VkApi import VkApi
from YdApi import YdApi


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("settings.ini")
    TOKEN_VK = config['VK']['VK_token']
    TOKEN_YD = config['YD']['YD_token']
    VK_API_ver = config['VK']['VK_API_version']
    user = input('Введите id или screen_name пользователя: ')
    quantity_foto = input('Введите количество копируемых фотографий: ')
    vk_api = VkApi(TOKEN_VK, VK_API_ver, user, quantity_foto)
    yd_api: YdApi = YdApi(TOKEN_YD)
    yd_api.upload(user, vk_api.get_photos(int(quantity_foto)))
