import vk_api
import operator

def get_token():
    token = input('Введите ключ доступа пользователя:')
    return token 

class Vk_api_access():
    def __init__(self, token):
        self.token_user = token
        self.vk = vk_api.VkApi(token = self.token_user)
        self.tools = vk_api.VkTools(self.vk)
        
    def get_user_information(self):
        req = self.vk.method('users.get', {'fields':'bdate, city, sex'})
        ages = req[0]['bdate']
        ages = int(ages.split('.')[2])
        user_info = {'first_name': req[0]['first_name'],
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
        photo_album = [{'photo_link':file['sizes'][-1]['url'],
                    'photo_likes':file['likes']['count']} for file in photo['items']]
        photo_album = sorted(photo_album, key = operator.itemgetter('photo_likes'), reverse = True)
        if len(photo_album)>3:
            photo_album = photo_album[:photo_numb]    
        photo_links = [link['photo_link'] for link in photo_album]
        return photo_links
    
    def search_friends(self, ages, city, sex): 
        result =[]
        friends = self.tools.get_all(
            'users.search', 
            100,
            {'hometown': city,
              'sex': sex,
              'birth_year': ages,
              'has_photo': 1,
              })       
        result =[{'first_name':friend['first_name'],
                'last_name':friend['last_name'],
                'link_user':f"https://vk.com/id{friend['id']}"} for friend in friends['items'] if 
                 friend['can_access_closed'] == True]
        return result
    
    def flat_generator(self, friends_list):
        for i in friends_list:
            yield i


if __name__ == '__main__':
    token = get_token()
    user = Vk_api_access(token)
    # print(user.get_user_information())
    # print(user.search_friends(1987,'Орёл', 2))
    # print(user.get_photos('693428759'))
    # for i in user.flat_generator(user.search_friends(1989,'Калуга', 0)):
    #     print(i)
       
            
        
    