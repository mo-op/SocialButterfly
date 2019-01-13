#author : Imad Mebrouk 

# my work can also be seen at : https://github.com/ImadMebrouk/SocialButterfly , 

import redis

r = redis.Redis(
    host = 'localhost',
    port=6379)




def create_user( **kwargs):  #WORKING

    id_count= r.exists("id_count")

    if(id_count)==1:
        count = int(r.get("id_count"))
    else:
        count = 0
        r.set("id_count", count)

    user = "user:" + str(count + 1)
    r.hset(user, "user_id", count + 1)

    for key, value in kwargs.items():         
        r.hset(user, key, value)
        
        
    r.incr("compteur")
    return r.hget(user, "user_id")

def user_connection(username, pwd): #WORKING
    connection_success = False
    if(get_user_by_username(username)):
        current_password = str(r.hget("user:"+str(get_user_by_username(username)), "password"))
        if(current_password == pwd):
            connection_success = True



    return connection_success

def get_user_by_username(username): #WORKING
    user_id =1
    user = "user:" + str(user_id)
    while r.hget(user,"username") != None:
        current_user =(str(r.hget(user,"username")))
        if current_user == username:
            return user_id  #user id of the corresponding username 
        else:
            user_id+=1
    return false # no user found with this username 

def get_user_by_id(user_id): #WORKING

    username = r.hget("user:" + str(user_id), "username")

    if username != None:
        return username

    else:
        return False


def add_Friend(user_id, friend_id): #WORKING
   

    r.sadd('user:'+str(user_id)+".friends", friend_id)
    r.sadd('user:'+str(friend_id)+".friends",user_id)
 

def  delete_friend(user_id, friend_id): #WORKING    
 
    r.srem('user:'+str(user_id)+".friends", friend_id)
    r.srem('user:'+str(friend_id)+".friends",user_id)
    
def AskFriendship(user_id ,friend_id): #use this for new friends request 
    r.sadd( r.sadd('user:'+str(friend_id)+".friendsRequestsWaiting",user_id))
    r.sadd( r.sadd('user:'+str(user_id)+".friendsRequestsSent",friend_id))

def AcceptRequest(user_id, friends_id):    
     r.sadd('user:'+str(user_id)+".friends", friend_id)
     r.srem('user:'+str(friend_id)+".friendsRequestsWaiting",friends_id)
     r.srem('user:'+str(friends_id)+".friendsRequestsSent",user_id)

def DenyRequest(user_id, friends_id):    
     r.srem('user:'+str(user_id)+".friendsRequestsWaiting",friends_id)
     r.srem('user:'+str(friends_id)+".friendsRequestsSent",user_id)

def UpdateStatus(user_id, newStatut):
   
     r.hset("user:"+str(user_id), "statut" ,str(newStatut) )
     r.rpush('user:'+str(user_id)+".updates", str(newStatut))  #check this list for the latest status


def NewPost(user_id, newPost): # ToDO 
     r.sadd( r.sadd('user:'+str(user_id)+".posts",newPost))

Imad = {
    "username": "coach",
    "password": "password",
    "first_name": "Imad",
    "last_name": "Mebrouk",
    "age":"23",
    "gender":"male",
    "location": "Sannois",
    "statut": ""
    }

Clement = {
    "username": "starkiller",
    "password": "password",
    "first_name": "clement",
    "last_name": "jacques",
    "age":"22",
    "gender":"male",
    "location": "Sannois",
    "statut": ""
    }

Test = {
    "username": "test3",
    "password": "root",
    "first_name": "test",
    "last_name": "trois",
    "age":"22",
    "gender":"male",
    "location": "Paris",
    "statut": ""
    }



create_user(**Imad)

print(get_user_by_id(1))

print(user_connection("b'coach'", "b'password'")) # don't understand why "b" is added when i do hget(something)

print("adding frienID 2")
add_Friend(1,2)
print(r.smembers("user:1.friends"))
print("adding frienID 3")
add_Friend(1,3)
print(r.smembers("user:1.friends"))
print("deleting frienID 2")
delete_friend(1,2)
print(r.smembers("user:1.friends"))

r.flushdb() #cleaning the database for tests 
