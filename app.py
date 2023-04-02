from flask import Flask, render_template, request, jsonify
import pymongo, random, json
from datetime import datetime
from flask_ngrok import run_with_ngrok
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.secret_key = "bffsubmission123"
CORS(app,resources={r"/api/*":{"origins":"*"}})                                                                                          // temperory change 
CORS(app) 
# app.config['CORS_HEADERS']='Content-Type'                                                                                                // temperory change 
run_with_ngrok(app)

Private_Repl_URL = "https://c6752e41-659a-4829-ba1b-3a9aac357be2.id.repl.co/"  # Found this Private URL in "Toggle Developers Tool" in "Webview" section inside "Resources" tab. Scroll a bit to find it with "https://*.id.repl.co/".
MONGO_URI = "mongodb+srv://kuwar:JvKRvzRUKWVrCbSH@cluster0.kgwnehm.mongodb.net/"
# "mongodb+srv://devTeam:FamLearn123@cluster0.uxghxpb.mongodb.net/"

# Connect to the MongoDB cluster
client = pymongo.MongoClient(MONGO_URI, connect=False)

MONGO_DATABASE = "platform"
FEED_COLLECTION = "feed"
USER_COLLECTION = "user"

# Get the database
dbs = client[MONGO_DATABASE]

# Get the collection: College
feed = dbs[FEED_COLLECTION]
user = dbs[USER_COLLECTION]


# 404 Error Handler
@app.errorhandler(404)
def not_found_error(error):
    return jsonify(error=str(error)), 404


# Define the custom error handler for 503 errors
@app.errorhandler(503)
def handle_503_error(error):
    return jsonify(error=str(error)), 503


# Define the custom error handler for 500 errors
@app.errorhandler(500)
def handle_500_error(error):
    return jsonify(error=str(error)), 500


@app.route('/')
def main():
    return render_template("index.html")


def updateMongoDocumentUser(uuid, query, collection):

    update = {"$push": {'posts_array': query}}
    user.update_one({"user_google_uuid": uuid}, update)
    return update, list(collection.find({"user_google_uuid": uuid}))


def add_feed_function(json):

    print(json)
    inserted_id = feed.insert_one(json).inserted_id
    return {"status": 200, "msg": "Sucessfully created post."}


@app.route('/profile/<uuid>', methods=['GET'])
def get_profile_by_uuid(uuid):
    if request.method == 'GET':
        particularUserData = list(user.find({"user_google_uuid": uuid}))[0]
        print(particularUserData)
        del particularUserData['_id']
        return particularUserData


@app.route('/get_feed', methods=['GET'])
def get_feed_function():
    if request.method == 'GET':
        allFeed = list(feed.find())
        print(list(feed.find()))
        for ele in allFeed:
            del ele['_id']
        return jsonify(allFeed)


@app.route('/create_user', methods=['POST'])
def create_user_function():
    if request.method == 'POST':
        data = request.form
        userdata = data.getlist('userdata')[0]
        userdata = json.loads(userdata)
        # nextSno = 1
        nextSno = list(user.find({}))[-1]["sno"] + 1
        user_json = User(
            user_name=userdata['user_name'],
            user_google_uuid=userdata['user_google_uuid'],
            user_email=userdata['user_email'],
            total_posts=userdata['total_posts'],
            user_total_health=userdata['user_total_health'],
            posts_array=userdata['posts_array'],
            sno=nextSno,
        )
        user_data = user_json.generate_document_JSON()
        print(user_json)
        inserted_id = user.insert_one(user_data).inserted_id
        return userdata['user_name']


@app.route('/publish_post', methods=['POST'])
def publish_post_function():
    if request.method == 'POST':
        data = request.form
        feeddata = data.getlist('feeddata')[0]
        feeddata = json.loads(feeddata)
        # nextSno = 1
        nextSno = list(user.find({}))[-1]["sno"] + 1
        # nextId = 1
        nextId = list(feed.find({}))[-1]["post_id"] + 1
        feed_json = Feed(uuid=feeddata['uuid'],
                         user_name=feeddata['user_name'],
                         post_id=nextId,
                         image_url=feeddata['image_url'],
                         health_index=feeddata['health_index'],
                         food_name=feeddata['food_name'],
                         carbs=feeddata['carbs'],
                         fat=feeddata['fat'],
                         cal=feeddata['cal'],
                         protein=feeddata['protein'],
                         sugar=feeddata['sugar'],
                         sno=nextSno)

        feed_data = feed_json.generate_document_JSON()
        print(feed_json)
        updateMongoDocumentUser(feed_data['uuid'], feed_data, user)
        add_feed_function(feed_data)
        return feeddata['food_name']


@app.route('/archive_post', methods=['POST'])
def archive_post_function():
    if request.method == 'POST':
        data = request.form
        feeddata = data.getlist('feeddata')[0]
        feeddata = json.loads(feeddata)
        # nextSno = 1
        nextSno = list(user.find({}))[-1]["sno"] + 1
        # nextId = 1
        nextId = list(feed.find({}))[-1]["post_id"] + 1
        feed_json = Feed(uuid=feeddata['uuid'],
                         user_name=feeddata['user_name'],
                         post_id=nextId,
                         image_url=feeddata['image_url'],
                         health_index=feeddata['health_index'],
                         food_name=feeddata['food_name'],
                         carbs=feeddata['carbs'],
                         fat=feeddata['fat'],
                         cal=feeddata['cal'],
                         protein=feeddata['protein'],
                         sugar=feeddata['sugar'],
                         sno=nextSno)

        feed_data = feed_json.generate_document_JSON()
        print(feed_json)
        updateMongoDocumentUser(feed_data['uuid'], feed_data, user)
        return feeddata['food_name']


def deleteMongoDocumentUser(sno, collection):

    collection.delete_one({"sno": sno})
    return "Deleted for" + str(sno)


def deleteMongoDocumentFeed(sno, collection):

    collection.delete_one({"sno": sno})
    return "Deleted for" + str(sno)


class User:
    def __init__(
        self,
        user_name,
        user_google_uuid,
        user_email,
        total_posts,
        user_total_health,
        posts_array,
        sno,
    ):
        self.user_name = user_name
        self.user_google_uuid = user_google_uuid
        self.user_email = user_email
        self.total_posts = total_posts
        self.user_total_health = user_total_health
        self.posts_array = posts_array
        self.sno = sno

    def generate_document_JSON(self):
        return {
            "user_name": self.user_name,
            "user_google_uuid": self.user_google_uuid,
            "user_email": self.user_email,
            "total_posts": self.total_posts,
            "user_total_health": self.user_total_health,
            "posts_array": self.posts_array,
            "sno": self.sno,
        }


class Feed:
    def __init__(
        self,
        uuid,
        user_name,
        post_id,
        image_url,
        health_index,
        food_name,
        carbs,
        fat,
        cal,
        protein,
        sugar,
        sno,
    ):
        self.user_name = user_name
        self.uuid = uuid
        self.post_id = post_id
        self.image_url = image_url
        self.health_index = health_index
        self.food_name = food_name
        self.carbs = carbs
        self.fat = fat
        self.cal = cal
        self.protein = protein
        self.sugar = sugar
        self.sno = sno

    def generate_document_JSON(self):
        return {
            "user_name": self.user_name,
            "uuid": self.uuid,
            "post_id": self.post_id,
            "image_url": self.image_url,
            "health_index": self.health_index,
            "food_name": self.food_name,
            "carbs": self.carbs,
            "fat": self.fat,
            "cal": self.cal,
            "protein": self.protein,
            "sugar": self.sugar,
            "sno": self.sno,
        }


@app.route('/json')
def get_json():
    # url = 'https://AWS14.arnavgoyal4.repl.co'
    url = 'https://4e0dea13-5e39-40b4-9f1e-a6fdd1915319.id.repl.co'
    return str(url)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=random.randint(2000, 9000))
