import requests
import urllib
import os
from textblob import TextBlob
from textblob.sentiments import  NaiveBayesAnalyzer
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

def get_user_info(insta_username):
    user_id= get_user_id(insta_username)
    if user_id==None:
        print "user dont exist"
        exit()

    request_url = (BASE_URL + 'users/%s?access_token=%s')  %(user_id, ACCESS_TOKEN)
    print "GET request utl is %s" % request_url
    user_info = requests.get(request_url).json()

    if user_info['meta']['code']==200:
        if len(user_info['data']):
            print "Username %s" %(user_info['data']['username'])
            print  "No of followers %s" % (user_info['data']['counts']['followed_by'])
            print  "No of peoople you are following %s" % (user_info['data']['counts']['follows'])
            print "media %s" % (user_info['data']['counts']['media'])
            print "userid %s" %(user_info['data']['id'])

        else:
            print "There is no data"

    else:
        print "error"

# get_user_info("mayank0324")


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

    if post_a_like['meta']['code']==200:
        print"like was successful"
    else:
        print "Sorry"
# like_a_post("mayank0324")/

def recent_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments?access_token=%s') %(media_id, ACCESS_TOKEN)
    comment_posted= requests.get(request_url).json()
    print comment_posted

# recent_comment("mayank0324"


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

# make_a_comment("mayank0324")


def delete_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url =(BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id , ACCESS_TOKEN)
    print "GET request url %s" %(request_url)
    comment_delete= requests.get(request_url).json()

    if comment_delete['meta']['code']--200:
        if len(comment_delete['data']):
         for x in range(0, len(comment_delete['data'])):
             comment_id= comment_delete['data'][x]['id']
             comment_text= comment_delete['data'][x]['text']
             blob= TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
             if(blob.sentiment.p_neg> blob.sentiment.p_pos):
                 print "Negative comment %s" % comment_text

                 delete_url = (BASE_URL +'media/%s/comments/%s/?access_token=%s' ) % (media_id, comment_id,ACCESS_TOKEN)
                 print "Delete request url %s" % delete_url
                 delete_info = requests.delete(delete_url).json()

                 if delete_info['mata']['code']==200:
                   print "comment deleted"

                 else:
                   print "no comments"

             else:
                 print "postive commenst %s" % comment_text

         else:
             print "no comments"

    else:
        print "error"

# delete_a_comment("mayank0324")


def Start_instagrambot():

     while True:
         print "Welcome to Instagram bot"
         print "Choose your choice"
         print "a. Get your own details"
         print "b. Get user info"
         print "b. get your own post "
         print "d. get user post by username"
         print "e. Get list of people who likes your post"
         print "f. like on a user post"
         print "g. Get recent comment on ypur post"
         print "h. Make a comment on user post"
         print "i. exit"

         choice= raw_input("enter your choice")
         if choice== "a":
             self_info()

         elif choice=="b":
             insta_username= raw_input("enter the userrname for your info")
             get_user_info(insta_username)

         elif choice=="c":
             get_own_post()

         elif choice=="d":
             insta_username=raw_input("enter the username")
             get_user_post(insta_username)

         elif choice=="e":
             insta_username= raw_input("enter the username")
             get_likes_list(insta_username)

         elif choice=="f":
             insta_username= raw_input("enter the username to whom you want to like")
             like_a_post(insta_username)

         elif choice=="g":
             insta_username= raw_input("enter username")
             recent_comment(insta_username)


         elif choice == "h":
             insta_username=raw_input("enter username")
             make_a_comment(insta_username)


         elif choice=="i":
             exit()

         else:
             print"wromg choice"

Start_instagrambot()