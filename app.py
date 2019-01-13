import redis
try:
    import Tkinter as tk
except ImportError:
    print ("Error. Try again!")
import ttk

r = redis.Redis(
    host = 'localhost',
    port=6379)

row_count = 10
user_count = 0

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

	btn2 = tk.Button(window,text="REGISTER",command=lambda:create_user(tb3.get(),tb4.get(),tb5.get(),tb6.get(),tb7.get(),tb8.get(),tb9.get())).grid(row=18,column=0)
	
def showPage(user_id):

	global root
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

	row_count = 10

	lbl1 = tk.Label(tab1, text="New Post",font=("Helvetica", 12)).grid(row=3,column=0)
	tb1 = tk.Text(tab1,height=5)
	tb1.grid(row=4,column=0)
	btn1 = tk.Button(tab1, text="POST",command=lambda:new_post(user_id, tb1.get("1.0","end"))).grid(row=5,column=4)

	posts = get_all_posts(1)	

	for post in posts:
		row_count += 2
		user = get_user_first_name(1)+" "+get_user_last_name(1)
		lbl3 = tk.Label(tab1, text=user,font=("Helvetica", 12,'bold'),anchor='w',borderwidth=2, relief="groove").grid(row=row_count)
		lbl4 = tk.Label(tab1, text=post,font=("Helvetica", 12),anchor='w',borderwidth=2, relief="groove").grid(row=row_count+1)

	if user_id != 1:
		posts_user = get_all_posts(user_id)
		if posts_user:
			for post in posts_user:
				row_count += 2
				user = get_user_first_name(user_id)+" "+get_user_last_name(user_id)
				lbl3 = tk.Label(tab1, text=user,font=("Helvetica", 12,'bold'),anchor='w',borderwidth=2, relief="groove").grid(row=row_count)
				lbl4 = tk.Label(tab1, text=post,font=("Helvetica", 12),anchor='w',borderwidth=2, relief="groove").grid(row=row_count+1)


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

	friends = get_friends_list(user_id)
	print friends
	row_count_3 = 4
	lbl18 = tk.Label(tab3, text="List",font=(("Helvetica", 14))).grid(row=2,column = 0)
	if friends:
		for f in friends:
			user = get_user_first_name(f)+" "+get_user_last_name(f)
			lbl19 = tk.Label(tab3, text=user,font=("Helvetica", 12),anchor='w',borderwidth=2, relief="groove").grid(row=row_count_3+1)
			row_count_3 += 2
	lbl20 = tk.Label(tab3, text="Add Friend",font=("Helvetica", 12)).grid(row=row_count_3,column=0)		
	tb9 = tk.Entry(tab3)
	tb9.grid(row=row_count_3,column=1) 
	btn3 = tk.Button(tab3, text="Request",command=lambda:request_friendship(user_id, tb9.get())).grid(row=row_count_3,column=3)


###################################################################################################################
'''definition of redis based functions'''
def create_user(u,p,f,l,a,g,lo):

    r.incr("users.counter",amount=1)
    count = r.get("users.counter")
    r.set("id_count", count)

    new_user = "user:" + str(count)
    r.hset(new_user, "user_id", count)

    r.hset(new_user,'username',u)
    r.hset(new_user,'password',p)
    r.hset(new_user,'first_name',f)
    r.hset(new_user,'last_name',l)
    r.hset(new_user,'age',a)
    r.hset(new_user,'gender',g)
    r.hset(new_user,'location',lo)
    r.hset(new_user, 'statut','Hey, there! I am using Social Butterfly')
    if count != 1:
    	print ("Sending default requests")
    	request_friendship(count, 1)
    	#accept_friend_request(1,count)
    #r.lpush(new_user,'updates','This is a default update!')
    if u != "test":
    	showPage(count)
    	print("Created user", count)
    else:
    	print ("test user created")

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
    return False # no user found with this username 

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

def get_user_status(user_id): 

	statut = r.hget("user:" + str(user_id), "statut")

	if statut != None:
		return statut
	else:
		return False

# def add_friend(user_id, friend_id): 
   
#     r.sadd('user:'+str(user_id)+".friends", friend_id)
#     r.sadd('user:'+str(friend_id)+".friends",user_id)
 
def get_friends_list(user_id):

	friends = r.smembers('user:'+str(user_id)+".friends")
	return friends

def  delete_friend(user_id, friend_id):
 
    r.srem('user:'+str(user_id)+".friends", friend_id)
    r.srem('user:'+str(friend_id)+".friends",user_id)
    
def request_friendship(user_id ,friend_id): 

    r.lpush('user:'+str(user_id)+".friendsRequestsSent",friend_id)
    r.lpush('user:'+str(user_id)+".friendsRequestsSent",friend_id)
    accept_friend_request(friend_id,user_id)

def accept_friend_request(friend_id,user_id):    

     r.sadd('user:'+str(user_id)+".friends", friend_id)
     print(user_id, "and ", friend_id, " are now friends!")
     #print(r.smembers('user:'+str(user_id)+".friends"))

# def deny_friend_request(user_id, friend_id): 

# 	r.lrem
    # r.lrem('user:'+str(user_id)+".friendsRequestsWaiting",1,friend_id)
     #r.('user:'+str(friends_id)+".friendsRequestsSent",user_id)

def update_status(user_id, newStatut):
   
     r.hset("user:"+str(user_id), "statut" ,str(newStatut))
     r.lpush('user:'+str(user_id)+".updates", str(newStatut))  #check this list for the latest status


def new_post(user_id, newPost): 

	print("New post from", user_id)
	user = 'user:'+str(user_id)
	r.hset(user, 'posts', str(newPost))
	r.lpush(user+".updates", str(newPost))
	#displayPosts(user_id)
	showPage(user_id)
	#print(r.lrange(user+".updates",0,-1))

def get_all_posts(user_id): 

	#user = "user:" + str(user_id)
	posts_user = r.lrange("user:"+str(user_id)+".updates",0,3)
	return posts_user

###################################################################################################################

## Create a Window for the app interface


root = tk.Tk()
root.withdraw()

current_window = None 

#test user to check login as the app doesn't implement persistence
create_user("test","test","Doctor","Who",1000,"female","TARDIS")
create_user("test2","test","River","Song",200,"female","TARDIS")
uid = get_user_by_username("test")
#test user to create posts
update_status(uid,'Loving this site already! Hear my screwdriver go zzzzz...')
new_post(uid,'Just spent my weekend at Barcelone! The planet, not the one on Earth. It was fantastic!')
new_post(uid,'On my way to visit River Song! Wish me luck, gonna surprise her with my new face.')
showHome(root)
root.mainloop()

 #cleaning the database for tests 
r.flushdb()
