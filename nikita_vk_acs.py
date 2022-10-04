import requests
import operator
import time
from pprint import pprint

token = ''

class VKuser:
    
    result =[]
    def __init__(self, token, version = '5.131'):
        self.params = {
            'access_token': token,
            'v': version
            }
        
    def get_my_information(self):
        get_my_information_url = 'https://api.vk.com/method/users.get'
        get_my_information_params = {
            'fields':'bdate, city, sex'
            }
        req = requests.get(get_my_information_url, params ={**self.params, **get_my_information_params}).json()  
        ages = req['response'][0]['bdate']
        ages = int(ages.split('.')[2])
        myself = {'city': req['response'][0]['city']['title'],
                  'ages':ages,
                  'sex': req['response'][0]['sex']}
        return myself
    


    def get_photos(self, user_id):
        photo_album = []
        photo_links=[]
        get_photos_url = 'https://api.vk.com/method/photos.get'
        get_photos_params = {
            'owner_id': user_id,
            'album_id': 'profile',
            'extended': 1,
            # 'count':5            
            }
        req_photo = requests.get(get_photos_url, params ={**self.params, **get_photos_params}).json()
        print(req_photo)
        for photo in req_photo['response']['items']:
            photo_album.append({
            'photo_link':photo['sizes'][-1]['url'],
            'photo_likes':photo['likes']['count']
                })
        if len(photo_album)>=3:
            photo_album = sorted(photo_album, key = operator.itemgetter('photo_likes'), reverse = True)[:3]
        for links in photo_album:
            photo_links.append(links['photo_link'])
        return photo_links
    
    def search_friends(self, sorting =0, offset = 0):
        myself = self.get_my_information()
        friend_search_url = 'https://api.vk.com/method/users.search'
        friend_search_params = {
            'sort': sorting,
            'hometown': myself['city'],
            'sex': myself['sex'],
            'birth_year': myself['ages'],
            'has_photo': 1,
            'count': 100,
            'offset': offset
            }
        req = requests.get(friend_search_url, params ={**self.params, **friend_search_params}).json()
        number_of_loops= round(req['response']['count']/100+1)
        
        for i in range(number_of_loops):
            req = requests.get(friend_search_url, params ={**self.params, **friend_search_params}).json()
            time.sleep(15.0)
            for res in req['response']['items']:
                print(res)
                if res['can_access_closed'] == False:
                    link_photo = 'Закрытый профиль'
                else:
                    link_photo =  self.get_photos(res['id'])    
               
                self.result.append({
                    'first_name':res['first_name'],
                    'last_name':res['last_name'],
                    'link_user':f"https://vk.com/id{res['id']}",
                    'link_photo': link_photo
                    })
            offset+=100
           
        return self.result 
        # return req
        

vk_client = VKuser(token)
with open ('result.txt', 'w') as file:
    for n, row in enumerate(vk_client.search_friends()):
        file.write(f'{n}) {str(row)}' + '\n')
    print('Done')
# vk_client.search_friends()
# pprint(vk_client.search_friends())
# pprint(vk_client.get_my_information())
# pprint(vk_client.get_photos('44057299'))