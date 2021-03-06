from app import app
from ..db.schema import *
import datetime
import os
import random
import uuid

USER_LIST = ['danwen', 'humaira', 'muhammad', 'arvind', 'sebastian', 'daniel', 'rene', 'narin', 'onur', 'yosef', 'rao', 'zardosht']

def getRandomUser():
    return USER_LIST[random.randint(0, 11)]

# Mainly for seeding the database
# TODO: Figure out a way to seed database when app starts, and only ONCE
def insert_training_data_and_create_labels():
    cwd = os.listdir(app.config['UPLOAD_FOLDER'])
    user = None
    for username in USER_LIST:
        user = User(
            usertype="admin", name="admin", username= username, 
            password="password", createdOn=datetime.datetime.now(), 
            lastLogin=datetime.datetime.now()
        )
        user.save()

    for dir in cwd:
        label_path = os.path.join(app.config['UPLOAD_FOLDER'], dir)
        lb = Label(
                name=dir, path=label_path,
                createdOn=datetime.datetime.now(), createdBy=getRandomUser()
            )
        lb.save()
        files = os.listdir(label_path)
        for file in files:
            file_path = os.path.join(label_path, file)
            Image(
                name=file, path=file_path, label=lb.name, 
                createdOn=datetime.datetime.now(), createdBy=getRandomUser()
            ).save()        

def create_user(username):
    if User.objects(username=username).count() == 0:
        User(
            usertype="admin", name="admin", username=username, 
            password="test", createdOn=datetime.datetime.now(),
            lastLogin=datetime.datetime.now()
        ).save() 

def create_label(label_name, username="dummy"):
    if username == 'dummy':
        username = getRandomUser()
    label_path = os.path.join(app.config['UPLOAD_FOLDER'], label_name)
    if Label.objects(name=label_name).count() == 0:
        # user = schema.User.objects.get(username=username)
        lb = Label(
            name=label_name, path=label_path,
            createdOn=datetime.datetime.now(), createdBy=username
        ).save()
        return lb
    
def add_label_and_image(label_name, image_name, username="dummy"):
    if username == 'dummy':
        username = getRandomUser()
    create_user(username)
    create_label(label_name, username)
    file_path = os.path.join(os.path.join(app.config['UPLOAD_FOLDER'], label_name), image_name)
    lb = Label.objects.get(name=label_name)
    user = User.objects.get(username=username)
    img = Image(
        name=image_name, path=file_path, label=lb.name, 
        createdOn=datetime.datetime.now(), createdBy=username
    ).save()

def add_random_resources():
    Link(
        name="A-23 Features",
        path="http://ec2-23213-das.mic.com/a23-specs/",
        label="microwave",
        createdOn=datetime.datetime.now(),
        createdBy="Zichstopher",
        url="http://ec2-23213-das.mic.com/a23-specs/"
    ).save()
    Document(
        name="A-23 Features",
        path="/ec2-user/resources/document/microwave-features.pdf",
        label="microwave",
        createdOn=datetime.datetime.now(),
        createdBy="Zichstopher",
        extension="pdf",
        size="1012392"
    ).save()
    Audio(
        name="A-23 Alarm",
        path="/ec2-user/resources/document/microwave-Alarm.mp3",
        label="microwave",
        createdOn=datetime.datetime.now(),
        createdBy="Zichstopher",
        extension="mp3",
        size="1012392",
    ).save()
    Video(
        name="A-23 Spinning",
        path="/ec2-user/resources/document/microwave-spin.mp4",
        label="microwave",
        createdOn=datetime.datetime.now(),
        createdBy="Zichstopher",
        extension="mp4",
        size="1012392222",
    ).save()

def isImageNameUnique(name):
    return (Image.objects(name=name).count() == 0)

# only use for purge DB
def rename_images():
    cwd = os.listdir(app.config['UPLOAD_FOLDER'])
    for dir in cwd:
        label_path = os.path.join(app.config['UPLOAD_FOLDER'], dir)
        files = os.listdir(label_path)
        for file in files:
            oldPath = os.path.join(os.path.join(app.config['UPLOAD_FOLDER'], dir), file)
            imgName = str(dir) + "_" + str(uuid.uuid4()) + ".jpeg"
            newPath = os.path.join(os.path.join(app.config['UPLOAD_FOLDER'], dir), imgName)
            while not isImageNameUnique(imgName):
                imgName = str(dir) + "_" + str(uuid.uuid4()) + ".jpeg"
                newPath = os.path.join(os.path.join(app.config['UPLOAD_FOLDER'], dir), imgName)
            os.rename(oldPath, newPath)
            Image(
                name=imgName, path=newPath, label=str(dir), 
                createdOn=datetime.datetime.now(), createdBy=getRandomUser()
            ).save()   


