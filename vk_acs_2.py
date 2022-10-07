import vk_api
import operator

# token = input('Введите ключ доступа пользователя:')
token = 'ae8765185e78516418047c54a9a3be250d2d802db3470c287338769b7343e1f719d3a2a6c214308ce3462'

class Vk_api_access():
    def __init__(self, token = token):
        self.token_group = token
        self.vk = vk_api.VkApi(token = self.token_group)
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
    

    def get_photos(self, user_id):
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
            photo_album = photo_album[:3]    
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


if __name__ == '__main__':
    user = Vk_api_access()
    # print(user.get_user_information())
    # print(user.search_friends(1987,'Орёл', 2))
    # print(get_my_information())
    # with open ('result.txt', 'w') as file:
    #     for n, row in enumerate(user.search_friends(1987,'Орёл', 2)):
    #         file.write(f'{n}) {str(row)}' + '\n')
    #     print('Done') 
    # print(user.get_photos('693428759'))