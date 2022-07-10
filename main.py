import streamlit as st
import pandas as pd
import numpy as np
import random, os
import cv2
from st_clickable_images import clickable_images
from PIL import ImageTk
from PIL import Image as PilImage
import glob
import base64
import json
import random
import tkinter as tk
from tkinter import *
from tkinter import messagebox

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

# # DB Management
# import sqlite3
# conn = sqlite3.connect('data.db')
# c = conn.cursor()

# def create_usertable():
# 	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT, password TEXT)')

# def add_userdata(username, password):
# 	c.execute('INSERT INTO userstable(username, password) VALUES (?,?)',(username, password))
# 	conn.commit()

# def login_user(username, password):
# 	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?', (username, password))
# 	data = c.fetchall()
# 	return data

# def view_all_users():
# 	c.execute('SELECT * FROM userstable')
# 	data = c.fetchall()
# 	return data

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
		#st.write(choices)
		#st.write(choices_selected)

		# choices_not_selected = []
		# for choice in choices_present:
		# 	if choice not in choices_selected:
		# 		choices_not_selected.append(choice)

		# dictionary_selected_categories = {}
		# for name in choices_selected:
		# 	for i in categorie_paths:
		# 		if name == os.path.basename(os.path.normpath(i)):
		# 			# key = name
		# 			# value = i
		# 			dictionary_selected_categories[name] = i
		# #st.write(dictionary_selected_categories)

		# dictionary_unselected_categories = {}
		# for name in choices_not_selected:
		# 	for i in categorie_paths:
		# 		if name == os.path.basename(os.path.normpath(i)):
		# 			# key = name
		# 			# value = i
		# 			dictionary_unselected_categories[name] = i
		#st.write(dictionary_unselected_categories)

		# dictionary_user_password = {}
		# # key = email
		# # value = choices_selected
		# dictionary_user_password[email] = choices_selected
		# st.write(dictionary_user_password)

		json_user_pass = {"Username": username, "Email ID": email, "Password": choices_selected}

		if st.button("Signup"):

			# json_string = json.dumps(dictionary_user_password)
			# st.write(json_string)

			#database.push(json_user_pass)
			database.child("Users").push(json_user_pass)


			# user = auth.create_user_with_email_and_password(email, choices_selected)
			# st.success("You have successfully created an account")
			# st.balloons()

			# #sign in
			# user = auth.sign_in_with_email_and_password(email, choices_selected)
			# db.child(user['localId']).child("Handle").set(handle)
			# db.child(user['localId']).child("ID").set(user['localId'])
			# st.title('Welcome '+ handle)
			# st.info("Go to login menu to login")


			
		#st.write(dic_sel_cat)			


	elif choice == "Login":
		st.subheader("Login Section")

		email = st.text_input("Email ID")
		username = st.text_input("Username")
		users = database.child("Users").get()

		st.write(username,email)

		user_data = []
		for user in users.each():
			st.write(user.val())
			user_data.append(user.val())

		current_user_password = []
		for i in range(len(user_data)):
			if (user_data[i]['Email ID'] == email) and (user_data[i]['Username'] == username):
				current_user_password = user_data[i]['Password']

		st.write(current_user_password)

		current_user_not_password = []
		for choice in os.listdir(dataset_path):
			if choice not in current_user_password:
				current_user_not_password.append(choice)
		st.write(current_user_not_password)

		dictionary_current_user_password = {}
		for name in current_user_password:
			for i in categorie_paths:
				if name == os.path.basename(os.path.normpath(i)):
					# key = name
					# value = i
					dictionary_current_user_password[name] = i
		st.write(dictionary_current_user_password)

		dictionary_current_user_not_password = {}
		for name in current_user_not_password:
			for i in categorie_paths:
				if name == os.path.basename(os.path.normpath(i)):
					# key = name
					# value = i
					dictionary_current_user_not_password[name] = i
		st.write(dictionary_current_user_not_password)

		random_object, random_path = random.choice(list(dictionary_current_user_not_password.items()))
		st.write(random_object, random_path)

		random_image = []
		dictionary_random_images = {}
		#path = "Dataset/train/Apple"

		new_random_images_paths =[]
		dictionary_with_path = {}
		for i in range(9):
			random_object, random_path = random.choice(list(dictionary_current_user_not_password.items()))
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
		st.write(random_image)
		st.write(dictionary_random_images)
		st.write(new_random_images_paths)

		# for i in dic_sel_cat:
		# 	st.write(i)
				
		

	
		images = []
		for file in new_random_images_paths:
			with open(file, "rb") as image:
				encoded = base64.b64encode(image.read()).decode()
				images.append(f"data:image/jpeg;base64,{encoded}")

		clicked = clickable_images(
			images,
			titles=[f"Image #{str(i)}" for i in range(5)],
			div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
			img_style={"margin": "5px", "height": "200px"},
		)

		st.markdown(f"Image #{clicked} clicked" if clicked > -1 else "No image clicked")

		for i in new_random_images_paths:
			st.markdown("![There we go!!!](",i,")")
		
		clicked_images_path_list = []

		for i in range(9):
			clicked_images_path_list.append(image)

		st.write(clicked_images_path_list)		

		# pass_clicks_number = 0
		# count = 0

		# for j in current_user_password:

		# 	if j == os.path.dirname(selected_image_path):
		# 		pass_clicks_number = pass+1
		# 		#shuffle images

		# 	else:
		# 		#shuffle images
		# 	count = count+1

		# if pass_clicks_number == count :
		# 	st.success("Logged in Successfully")

		#st.write(user_data[0]['Password'])

		# for user_object in listOfDicts:
		# 	if username in subVal:
		# 	return subVal[key]

		# st.write(user_data)

		# 2result = database.child("Users").order_by_child("Username").equal_to(username).get()
		# #result = database.child("Users").get()
		# st.write(result.password.val())
		# #password = st.text_input("Password", type='password')

		
		

		# clicked = clickable_images(
		#     [
		#         "https://images.unsplash.com/photo-1565130838609-c3a86655db61?w=700",
		#         "https://images.unsplash.com/photo-1565372195458-9de0b320ef04?w=700",
		#         "https://images.unsplash.com/photo-1582550945154-66ea8fff25e1?w=700",
		#         "https://images.unsplash.com/photo-1591797442444-039f23ddcc14?w=700",
		#         "https://images.unsplash.com/photo-1518727818782-ed5341dbd476?w=700",
		#     ],
		#     titles=[f"Image #{str(i)}" for i in range(5)],
		#     div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
		#     img_style={"margin": "5px", "height": "200px"},
		# )

		# st.markdown(f"Image #{clicked} clicked" if clicked > -1 else "No image clicked")

		#--- functions ---

		
		 

		
		if st.button("Login"):
			create_usertable()
			result = login_user(username, password)
			if result:
				st.success("Logged in as {}".format(username))

				task = st.selectbox("Task",["Add Post", "Analytics", "Profiles"])
				if task == "Add Post":
					st.subheader("Add your post")

				elif task == "Analytics":
					st.subheader("Analytics")
				elif task == "Profiles":
					st.subheader("User Profiles")
					user_result = view_all_users()
					clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
					st.dataframe(clean_db)
			else:
				st.warning("Incorrect Username/Password")

		


if __name__ == '__main__':
	main()
