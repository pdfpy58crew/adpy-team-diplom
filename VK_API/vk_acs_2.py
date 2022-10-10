import vk_api
import operator


class Vk_api_access():

    def __init__(self):
        self.token_user = ''
        self.vk = vk_api.VkApi(token = self.token_user)
        self.tools = vk_api.VkTools(self.vk)

        
    def get_user_information(self):
        req = self.vk.method('users.get', {'fields':'bdate, city, sex'})
        ages = req[0]['bdate']
        ages = int(ages.split('.')[2])
        user_info = { 'user_id': req[0]['id'],
                      'first_name': req[0]['first_name'],
                      'last_name':req[0]['last_name'],
                      'age':ages,
                      'gender': req[0]['sex'],
                      'city': req[0]['city']['title'],
                      'user_link': f"https://vk.com/id{req[0]['id']}"}
        return user_info 
    

    def get_photos(self, user_id, photo_numb = 3):
        photo_album= []
        photo_links=[]
        photo = self.tools.get_all_slow(
                'photos.get',
                100,
                {'owner_id': user_id,
                  'album_id': 'profile',
                  'extended': 1,})
        photo_album = [{'photo_link':file['id'],
                    'photo_likes':file['likes']['count']} for file in photo['items']]
        photo_album = sorted(photo_album, key = operator.itemgetter('photo_likes'), reverse = True)
        if len(photo_album)>3:
            photo_album = photo_album[:photo_numb]    
        photo_links = [link['photo_link'] for link in photo_album]
        return photo_links
    
    def search_friends(self, user_info): 
        result =[]
        if user_info['sex'] == 1:
            sex = 2
        elif user_info['sex'] == 2:
            sex = 1
        else:
            sex = 0
        friends = self.tools.get_all(
            'users.search', 
            100,
            {'hometown': user_info['city'],
              'sex': sex,
              'birth_year': user_info['age'],
              'has_photo': 1,
              })       
        result =[{'user_id':friend['id'],
                'first_name':friend['first_name'],
                'last_name':friend['last_name'],
                'user_link':f"https://vk.com/id{friend['id']}"} for friend in friends['items'] if 
                 (friend['can_access_closed'] == True and friend['friend_status'] == 0)]
        return result
    
    def flat_generator(self, friends_list):
        for i in friends_list:
            yield i
