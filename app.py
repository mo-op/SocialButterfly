import redis
try:
    import Tkinter as tk
except ImportError:
    print ("Error. Try again!")
import ttk

r = redis.Redis(
    host = 'localhost',
    port=6379)


 #window.iconbitmap('butterfly.png')


'''definition of gui functions'''

def replace_window(root):
	"""Destroy current window, create new window"""
	global current_window
	if current_window is not None:
		current_window.destroy()
	current_window = tk.Toplevel(root)
	# if the user kills the window via the window manager, exit the application. 
	current_window.wm_protocol("WM_DELETE_WINDOW", root.destroy)
	return current_window

def showHome(root):
	print ("Loading home page")
	window = replace_window(root)
	window.title("Social Butterfly!")
	window.configure(bg="lightblue")
	window.geometry("750x500")
	lbl1 = tk.Label(window, text="Welcome to Social Butterfly, our Redis based SNS!",font=("Helvetica", 16))
	lbl1.grid(column=0, row=0)

	# Log In

	lbl2 = tk.Label(window ,text="username").grid(row=5,column = 0)
	lbl3 = tk.Label(window ,text="password").grid(row=6,column=0)

	tb1 = tk.Entry(window)
	tb1.grid(row=5,column=1)
	tb2 = tk.Entry(window,show="*")
	tb2.grid(row=6,column=1)

	btn1 = tk.Button(window,text="LOGIN",command=lambda:user_connection(tb1.get(),tb2.get())).grid(row=8,column=0)
	# Register 

	lbl4 = tk.Label(window ,text="username").grid(row=10,column = 0)
	lbl5 = tk.Label(window ,text="password").grid(row=11,column=0)
	lbl6 = tk.Label(window ,text="first name").grid(row=12,column=0)
	lbl7 = tk.Label(window ,text="last name").grid(row=13,column=0)
	lbl8 = tk.Label(window ,text="age").grid(row=14,column=0)
	lbl9 = tk.Label(window ,text="gender").grid(row=15,column=0)
	lbl10 = tk.Label(window ,text="location").grid(row=16,column=0)


	tb3 = tk.Entry(window)
	tb3.grid(row=10,column=1)
	tb4 = tk.Entry(window,show="*")
	tb4.grid(row=11,column=1)
	tb5 = tk.Entry(window)
	tb5.grid(row=12,column=1)
	tb6 = tk.Entry(window)
	tb6.grid(row=13,column=1)
	tb7 = tk.Entry(window)
	tb7.grid(row=14,column=1)
	tb8 = tk.Entry(window)
	tb8.grid(row=15,column=1)
	tb9 = tk.Entry(window)
	tb9.grid(row=16,column=1)

	btn2 = tk.Button(window,text="REGISTER",command=lambda:create_user(tb3.get(),tb4.get(),tb5.get(),tb6.get(),tb7.get(),tb8.get(),tb9.get(),window)).grid(row=18,column=0)
	

def showPage(user_id):
	global root
	print ("Loading user screen")
	window = replace_window(root)
	window.title("Social Butterfly!")
	window.configure(bg="lightblue")
	window.geometry("750x500")
	username = get_user_by_id(user_id)

	tab_control = ttk.Notebook(window)
	tab1 = ttk.Frame(tab_control)
	tab2 = ttk.Frame(tab_control)
	tab3 = ttk.Frame(tab_control)
	tab_control.add(tab1, text='Updates')
	tab_control.add(tab2, text='Profile')
	tab_control.add(tab3, text='Friends')
	tab_control.pack(expand=1, fill='both')

	# lbl2 = tk.Label(tab1, text="Updates",font=("Helvetica", 10)).grid(column=0, row=2)
	# lbl3 = tk.Label(tab2, text="Profile",font=("Helvetica", 10)).grid(column=2,row=2)
	lbl4 = tk.Label(tab2,text="username").grid(row=4,column = 2)
	lbl5 = tk.Label(tab2,text="password").grid(row=5,column=2)
	lbl6 = tk.Label(tab2,text="first name").grid(row=6,column=2)
	lbl7 = tk.Label(tab2,text="last name").grid(row=7,column=2)
	lbl8 = tk.Label(tab2,text="age").grid(row=8,column=2)
	lbl9 = tk.Label(tab2,text="gender").grid(row=9,column=2)
	lbl10 = tk.Label(tab2, text="location").grid(row=10,column=2)

	lbl11 = tk.Label(tab2,text=username).grid(row=4,column = 3)
	lbl12 = tk.Label(tab2,text="*******").grid(row=5,column=3)
	lbl13 = tk.Label(tab2,text=get_user_first_name(user_id)).grid(row=6,column=3)
	lbl14 = tk.Label(tab2,text=get_user_last_name(user_id)).grid(row=7,column=3)
	lbl15 = tk.Label(tab2,text=get_user_age(user_id)).grid(row=8,column=3)
	lbl16 = tk.Label(tab2,text=get_user_gender(user_id)).grid(row=9,column=3)
	lbl17 = tk.Label(tab2, text=get_user_location(user_id)).grid(row=10,column=3)




###################################################################################################################
'''definition of redis based functions'''
def create_user(u,p,f,l,a,g,lo):

    print "User added"
    id_count = r.exists("id_count")
    if id_count > 0:
        count = int(r.get("id_count"))
    else:
        count = 0
        r.set("id_count", count)

    new_user = "user:" + str(count+1)
    r.hset(new_user, "user_id", count+1)

    r.hset(new_user,'username',u)
    r.hset(new_user,'password',p)
    r.hset(new_user,'first_name',f)
    r.hset(new_user,'last_name',l)
    r.hset(new_user,'age',a)
    r.hset(new_user,'gender',g)
    r.hset(new_user,'location',lo)
    r.hset(new_user, 'statut','Hey, there! I am using Social Butterfly')
    showPage(count+1)

def user_connection(username, pwd):

	connection_success = False
	if(get_user_by_username(username)):
		current_password = str(r.hget("user:"+str(get_user_by_username(username)), "password"))
	if(current_password == pwd):
	    connection_success = True
	if connection_success:
		print "Logged In"
	showPage(get_user_by_username(username))

def get_user_by_username(username): 
    user_id =1
    user = "user:" + str(user_id)
    while r.hget(user,"username") != None:
        current_user =(str(r.hget(user,"username")))
        if current_user == username:
            return user_id  #user id of the corresponding username 
        else:
            user_id+=1
    return false # no user found with this username 

def get_user_by_id(user_id): 

	username = r.hget("user:" + str(user_id), "username")

	if username != None:
		return username
	else:
		return False

def get_user_first_name(user_id): 

	first_name = r.hget("user:" + str(user_id), "first_name")

	if first_name != None:
		return first_name
	else:
		return False

def get_user_last_name(user_id): 

	last_name = r.hget("user:" + str(user_id), "last_name")

	if last_name != None:
		return last_name
	else:
		return False

def get_user_age(user_id): 

	age = r.hget("user:" + str(user_id), "age")

	if age != None:
		return age
	else:
		return False

def get_user_location(user_id): 

	location = r.hget("user:" + str(user_id), "location")

	if location != None:
		return location
	else:
		return False

def get_user_gender(user_id): 

	gender = r.hget("user:" + str(user_id), "gender")

	if gender != None:
		return gender
	else:
		return False


def add_Friend(user_id, friend_id): 
   
    r.sadd('user:'+str(user_id)+".friends", friend_id)
    r.sadd('user:'+str(friend_id)+".friends",user_id)
 

def  delete_friend(user_id, friend_id):
 
    r.srem('user:'+str(user_id)+".friends", friend_id)
    r.srem('user:'+str(friend_id)+".friends",user_id)
    
def AskFriendship(user_id ,friend_id): 

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


def NewPost(user_id, newPost): 

     r.sadd( r.sadd('user:'+str(user_id)+".posts",newPost))

###################################################################################################################
## Adding widgets: labels, text boxes and buttons 

# App Screen: Posts & Comment + Friendship List (Modifiable) + List of online friends + Personal Info (Modifiable) + Log Out 

# Friendship List : Modifiable -> Received (accept/decline) | Sent (retract) | Connected (delete)

# Personal Info (Editable)

# Keep the Window running
#window.mainloop() 

## Create a Window for the app interface


root = tk.Tk()
root.withdraw()

current_window = None 

#test user to check login as the app doesn't implement persistence
create_user("test","test","Doctor","Who",1000,"female","TARDIS")

showHome(root)

root.mainloop()
