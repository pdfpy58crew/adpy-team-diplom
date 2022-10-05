import vk_api
import operator
token = input('Token: ')

vk = vk_api.VkApi(token=token)

def get_my_information():
    req = vk.method('users.get',{'fields':'bdate, city, sex'})
    ages = req[0]['bdate']
    ages = int(ages.split('.')[2])
    myself = {'city': req[0]['city']['title'],
              'ages':ages,
              'sex': req[0]['sex']}
    return myself

def get_photos(user_id, status):
    tools = vk_api.VkTools(vk)
    photo_album= []
    photo_links=[]
    if status == False:
        photo_links.append('Закрытый профиль')
    else:
        photo = tools.get_all_slow(
            'photos.get',
            100,
            {'owner_id': user_id,
             'album_id': 'profile',
             'extended': 1,})
        for file in photo['items']:
            photo_album.append({
                'photo_link':file['sizes'][-1]['url'],
                'photo_likes':file['likes']['count']
                })
            photo_album = sorted(photo_album, key = operator.itemgetter('photo_likes'), reverse = True)
            if len(photo_album)>3:
                photo_album = photo_album[:3]    
    return photo_album
    
def search_friends(): 
    result =[]
    tools = vk_api.VkTools(vk)
    myself = get_my_information()
    friends = tools.get_all(
        'users.search', 
        100,
        {'hometown': myself['city'],
          'sex': myself['sex'],
          'birth_year': myself['ages'],
          'has_photo': 1,
          })       
    for friend in friends['items']:
        result.append({
            'first_name':friend['first_name'],
            'last_name':friend['last_name'],
            'link_user':f"https://vk.com/id{friend['id']}",
            'link_photo': get_photos(friend['id'], friend['can_access_closed'])
            })
    return result


if __name__ == '__main__':
    # print(get_my_information())
    # with open ('result.txt', 'w') as file:
    #     for n, row in enumerate(search_friends()):
    #         file.write(f'{n}) {str(row)}' + '\n')
    #     print('Done') 
    print(search_friends())
    # print(get_photos('214553814', True))