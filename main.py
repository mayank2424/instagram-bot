import requests
import urllib
import os
from key import ACCESS_TOKEN


BASE_URL = 'https://api.instagram.com/v1/'

def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (ACCESS_TOKEN) #here we have requested the url throuuugh instagra api
    print 'GET request url : %s' % (request_url)
    my_info = requests.get(request_url).json()  #here we have used requests library gor getting data through request_url in json format
    print my_info
    print "My name is : %s\n" % (my_info['data']['full_name'])  #here we are accessing the list items in dictionary in json data we hsve requested
    print "My follower is %s\n" %(my_info['data']['counts']['followed_by'])
    print "Whom i follow %s\n" %(my_info['data']['counts']['follows'])
    print "my media%s\n" % (my_info['data']['counts']['media'])

# self_info()
def get_user_id(insta_username):
    request_url = (BASE_URL+ 'users/search?q=%s&access_token=%s') % (insta_username, ACCESS_TOKEN)
    print "get request url : %s" % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
     if len(user_info['data'])>0:
      return user_info['data'][0]['id']
     else:
        return None
    else:
     print 'Status code other than 200 received!'
    exit()
# get_user_id("mayank0324")

def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (ACCESS_TOKEN)
    print "requesting url %s" % (request_url)

    recent_post = requests.get(request_url).json()

    if recent_post['meta']['code']--200:
        if len(recent_post['data'])>0:
            image= recent_post['data'][0]['id'] + ".jpeg"
            image_url = recent_post['data'][0]['images']['standard_resolution']['url']

            urllib.urlretrieve(image_url , image)
        else:
           print "No posts"
    else:
        print "error"

    return None

# print get_own_post()

def get_user_post(insta_username):
    user_id= get_user_id(insta_username)

    request_url = (BASE_URL +'users/%s/media/recent/?access_token=%s') %(user_id, ACCESS_TOKEN)
    print "requesting url %s" %(request_url)
    recent_post = requests.get(request_url).json()


    if recent_post['meta']['code']==200:
        if len(recent_post['data'])>0:
            image = recent_post['data'][0]['id'] + ".jpeg"
            image_url = recent_post['data'][0]['images']['standard_resolution']['url']

            urllib.urlretrieve(image_url, image)
        else:
            print "no recent post"

    else:
      print "error"


# get_user_post("mayank0324")
#

def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    request_url= (BASE_URL + 'users/%s/media/recent/?access_token=%s') %(user_id, ACCESS_TOKEN)
    print "requested url is %s" % (request_url)
    user_media= requests.get(request_url).json()

    if user_media['meta']['code']==200:
        if len(user_media['data'])>0:
            return user_media['data'][0]['id']
        else:
            print "no media"

    else:
        print "error"

    return None

def get_likes_list(insta_username):
    post_id= get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes?access_token=%s') %(post_id, ACCESS_TOKEN)
    print "requester url is %s" %(request_url)
    likes_list= requests.get(request_url).json()

    if likes_list['meta']['code']==200:
        if len(likes_list['data'])>0:
            for x in range(0, len(likes_list['data'])): #here we have used for loop and xin range means we have givetnt he range from 0 to list item in data
                print likes_list['data'][x]['username']

        else:
            print "there no likes on you post"

    else:
        print "error"

# get_likes_list("mayank0324")

def like_a_post(insta_username):
    media_id= get_post_id(insta_username)
    request_url = (BASE_URL + '/media/%s/likes')% (media_id)
    payload = {"access_token": ACCESS_TOKEN}
    print "liking the post %s" % (request_url)
    post_a_like = requests.post(request_url, payload).json()

# like_a_post("mayank0324")/

def recent_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments?access_token=%s') %(media_id, ACCESS_TOKEN)
    comment_posted= requests.get(request_url).json()
    return comment_posted

# print recent_comment("mayank0324")


def make_a_comment(insta_username):
    media_id= get_post_id(insta_username)
    comment= raw_input("you comment")
    payload = {"access_token": ACCESS_TOKEN , "text": comment}

    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    comment_added= requests.post(request_url,payload).json()
    print comment_added

    if comment_added['meta']['code']==200:
        print "commend added"

    else:
        print "error"

make_a_comment("mayank0324")
