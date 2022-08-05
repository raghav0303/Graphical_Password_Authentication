import streamlit as st
import pandas as pd
import numpy as np
import random, os
import json

#modules
import pyrebase
from datetime import datetime

#configuration key
firebaseConfig = {
  'apiKey': "AIzaSyDFg2Gmdct-DylAmp84kpZ89tmk0KC5RAA",
  'authDomain': "graphicalpassword-streamlit.firebaseapp.com",
  'projectId': "graphicalpassword-streamlit",
  'databaseURL': "https://graphicalpassword-streamlit-default-rtdb.europe-west1.firebasedatabase.app/",
  'storageBucket': "graphicalpassword-streamlit.appspot.com",
  'messagingSenderId': "217522918965",
  'appId': "1:217522918965:web:859d61cd0667a79c15037c",
  'measurementId': "G-050CM727TK"
};

#firebase authentication
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
database = firebase.database()

#database
db = firebase.database()
storage = firebase.storage()

def main():

	dataset_path = os.path.join("Dataset/train")

	categorie_paths = []
	for file in os.listdir(dataset_path):
		d = os.path.join(dataset_path, file)
		if os.path.isdir(d):
			categorie_paths.append(d)
	#st.write(categorie_paths)

	cho_sel = []
	cho_not_sel = []
	dic_sel_cat = {}
	dic_uns_cat = {}

	st.title("Graphical Password Authentication")
	menu = ["Home", "Login", "Sign-Up"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.subheader("Home")

	elif choice == "Sign-Up":
		st.subheader("Create New Account")
		email = st.text_input("Email ID")
		username = st.text_input("Username")
		#new_password = st.text_input("Password", type='password')

		# choices = []
		# for choice in os.listdir(dataset_path):
		# 	choices.append(choice)
		choices_present = os.listdir(dataset_path)
		choices_selected = st.multiselect("Select you password choices", choices_present)

		json_user_pass = {"Username": username, "Email ID": email, "Password": choices_selected}

		if st.button("Signup"):

			#database.push(json_user_pass)
			database.child("Users").push(json_user_pass)
			st.success()	

	elif choice == "Login":
		st.subheader("Login Section")

		email = st.text_input("Email ID")
		username = st.text_input("Username")
		users = database.child("Users").get()

		#st.write(username,email)

		user_data = []
		for user in users.each():
			user_data.append(user.val())
		#st.write(user_data)

		current_user_password = []
		for i in range(len(user_data)):
			if (user_data[i]['Email ID'] == email) and (user_data[i]['Username'] == username):
				current_user_password = user_data[i]['Password']
		#st.write(current_user_password)

		current_user_not_password = []
		for choice in os.listdir(dataset_path):
			if choice not in current_user_password:
				current_user_not_password.append(choice)
		#st.write(current_user_not_password)

		dictionary_current_user_password = {}
		for name in current_user_password:
			for i in categorie_paths:
				if name == os.path.basename(os.path.normpath(i)):
					# key = name
					# value = i
					dictionary_current_user_password[name] = i
		#st.write(dictionary_current_user_password)

		dictionary_current_user_not_password = {}
		for name in current_user_not_password:
			for i in categorie_paths:
				if name == os.path.basename(os.path.normpath(i)):
					# key = name
					# value = i
					dictionary_current_user_not_password[name] = i
		#st.write(dictionary_current_user_not_password)

		dictionary_all_password = {}
		for name in os.listdir(dataset_path):
			for i in categorie_paths:
				dictionary_all_password[name]=i
		
		random_image = []
		dictionary_random_images = {}
		#path = "Dataset/train/Apple"

		new_random_images_paths =[]
		dictionary_with_path = {}
		for i in range(9):
			if len(random_image)<8:
				random_object, random_path = random.choice(list(dictionary_current_user_not_password.items()))
				random_filename = random.choice([
		          x for x in os.listdir(random_path)
		          if os.path.isfile(os.path.join(random_path, x))
				])
				random_image.append(random_filename)

			else:
				random_object, random_path = random.choice(list(dictionary_current_user_password.items()))
				random_filename = random.choice([
		          x for x in os.listdir(random_path)
		          if os.path.isfile(os.path.join(random_path, x))
		    ])
				random_image.append(random_filename)
			# key = random_object
			# value = random_filename
			dictionary_random_images[random_object] = random_filename
			dictionary_with_path[dataset_path+'/'+random_object+'/'+random_filename] = random_filename
			new_random_images_paths.append(dataset_path+'/'+random_object+'/'+random_filename)
		
		random.shuffle(new_random_images_paths)
		st.write(new_random_images_paths)

###############################################################		

		if 'images_selected' not in st.session_state:
			st.session_state['images_selected']=[]

		if 'a' not in st.session_state:
			st.session_state['a']=random.randint(5, 7)

		def handle_click(new_type):
			st.session_state.images_selected.append(new_type)

		idx = 0 
		for _ in range(len(new_random_images_paths)-1): 
				cols = st.columns(3) 

				if st.session_state.a == len(st.session_state.images_selected):
					st.write('Please select the Login button to continue :')
					break

				if idx < len(new_random_images_paths): 
				    cols[0].image(new_random_images_paths[idx], width=150, caption=new_random_images_paths[idx].split(os.path.sep)[-2])
				    change = cols[0].button('Image '+str(idx+1), on_click=handle_click, args = [new_random_images_paths[idx]])
				idx+=1

				if idx < len(new_random_images_paths):
				    cols[1].image(new_random_images_paths[idx], width=150, caption=new_random_images_paths[idx].split(os.path.sep)[-2])
				    change = cols[1].button('Image '+str(idx+1), on_click=handle_click, args = [new_random_images_paths[idx]])
				idx+=1

				if idx < len(new_random_images_paths):
				    cols[2].image(new_random_images_paths[idx], width=150, caption=new_random_images_paths[idx].split(os.path.sep)[-2])
				    change = cols[2].button('Image '+str(idx+1), on_click=handle_click, args = [new_random_images_paths[idx]])
				idx+=1 


		st.write(st.session_state.images_selected)
		
		current_user_password_possible_paths=[]
		for name in current_user_password:
			for i in categorie_paths:
				if name == os.path.basename(os.path.normpath(i)):
					for j in os.listdir(i):
						if(j!='Label'):
							current_user_password_possible_paths.append(i+'/'+j)
					
		#st.write(current_user_password_possible_paths)

		if 'count' not in st.session_state:
			st.session_state['count']=0

		for i in st.session_state.images_selected:
			for j in current_user_password_possible_paths:
				if i==j and i==st.session_state.images_selected[len(st.session_state.images_selected)-1]:
					st.session_state.count=st.session_state.count+1
					st.write(i)

		#st.write(st.session_state.images_selected)
		st.write(st.session_state.count)		 

		
		if st.button("Login"):
			if len(st.session_state.images_selected)==st.session_state.count-1 and st.session_state.count!=0:
				st.balloons()
				st.success("Authentication Successful")
				st.session_state.count = 0
			else:
				st.error('Authentication Denied')

if __name__ == '__main__':
	main()
