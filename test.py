import face_recognition
import time
import pymysql
import numpy as np

db = pymysql.connect("localhost","root","jhx123456","face_recognition")
cursor = db.cursor()

# # create database
# create_database = """CREATE DATABASE face_recognition"""
# cursor.execute(create_database)

# # create table
# cursor.execute("DROP TABLE IF EXISTS face_encodings")
# sql = """CREATE TABLE face_encodings (
#             faceid char (20),
#             encoding char ,
#             feature1 TINYINT,
#             feature2 TINYINT,
#             feature3 TINYINT)"""
# cursor.execute(sql)

img1 = face_recognition.load_image_file('/home/jhx/data/junjun.jpg')
img1_encoding = face_recognition.face_encodings(img1)
img1_encoding_list = img1_encoding[0].tolist()
encoding1 = str(img1_encoding_list)

item = np.array(img1_encoding_list)

# img2 = face_recognition.load_image_file('/home/jhx/data/junjun.jpg')
# img2_encoding = face_recognition.face_encodings(img2)

# #insert data
# insert_encoding = "INSERT INTO face_encodings (faceid, encoding) VALUES (2,'"+encoding1+"')"
# cursor.execute(insert_encoding)

select_all_data = "SELECT * FROM face_encodings"
cursor.execute(select_all_data)
all_data = cursor.fetchall()

people = {}
for row in all_data:
    faceid = row[0]
    encoding = row[1]
    people[faceid] = encoding
print(people)

p = []

a = people['1']
b = people['2']
a1 = eval(a)
a2 = np.array(a1)
p.append(a2)

encoding1 = list(np.array(eval(a)))
encoding2 = list(eval(b))

# distances = face_recognition.face_distance(img1_encoding, item)
distances = face_recognition.face_distance(p, np.array(encoding2))

db.commit()
db.close()