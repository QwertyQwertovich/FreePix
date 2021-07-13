from flask import Flask, render_template, url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from exif import Image
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tp.db'
db = SQLAlchemy(app)


class Photos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo_id = db.Column(db.Integer)
    train_id = db.Column(db.Integer)
    author = db.Column(db.String(300))
    desc = db.Column(db.Text)
    place = db.Column(db.String(300))
    date = db.Column(db.DateTime, default=datetime.utcnow())
    update = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return "<Photo %r>" % self.id


class Trains(db.Model):
    train_id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(300))
    number = db.Column(db.String(300))
    depot = db.Column(db.String(300))
    built = db.Column(db.DateTime, default=datetime.utcnow())
    category = db.Column(db.String(300))
    condition = db.Column(db.String(300))
    desc = db.Column(db.Text)


    def __repr__(self):
        return "<Photo %r>" % self.id



@app.route("/")
def index():
    photoss = Photos.query.all()
    return render_template("index.html", photo=photoss)


@app.route("/add_train", methods=["POST", "GET"])
def add_train():
    print(12341)
    if request.method == "POST":
        print(1234)
        author = request.form['author']
        password = request.form['pass']
        train_id = len(Trains.query.all())+1
        model = request.form['model']
        number = request.form['number']
        depot = request.form['depot']
        built = request.form['built']
        category = request.form['category']
        condition = request.form['condition']
        desc = request.form['desc']
        if author in ["qwerty_qwertovich"] and password in ["1234"]:
            train = Trains(train_id=train_id, model=model, number=number, depot=depot, built=built, category=category, condition=condition, desc=desc)
            print(train_id, model, number, depot, built, category, condition, desc)
            try:
                db.session.add(train)
                db.session.commit()
                return redirect('/')
            except:
                return "error"
        else:
            return "Bad login/password or other error.   Contact <a href=\"https://vk.com/ilter2\">https://vk.com/ilter2</a> for login/password"
    else:
        return render_template("add_train.html")


@app.route("/add_photo", methods=["POST", "GET"])
def add_photo():
    if request.method == "POST":
        #photo_id = request.form['photo_id']
        train_id = request.form['train_id']
        author = request.form['author']
        password = request.form['pass']
        desc = request.form['desc']
        place = request.form['place']
        check = request.form['check']
        file = request.files['file']
        photo_id = len(Photos.query.all())+1
        file.save("static/images/"+str(photo_id)+'.jpg')
        try:
            if check == True:
                x=0/0
            date = datetime.strptime(request.form['date'],"%Y-%m-%dT%H:%M")
        except:
            try:
                with open('static/images/'+str(photo_id)+'.jpg', 'rb') as image_file:
                    my_image = Image(image_file)
                date = datetime.strptime(my_image.datetime_original, "%Y:%m:%d %H:%M:%S")
            except:
                date = datetime.now()
        if author in ["qwerty_qwertovich"] and password in ["1234"]:
            photo = Photos(photo_id=photo_id, train_id=train_id, author=author, desc=desc, date=date, place=place)
            try:
                db.session.add(photo)
                db.session.commit()
                return redirect('/')
            except:
                return "error"
        else:
            return "Bad login/password or other error.   Contact <a href=\"https://vk.com/ilter2\">https://vk.com/ilter2</a> for login/password"
    else:
        return render_template("add_photo.html")


@app.route("/photo/<int:id>/")
def photo(id):
    photo = Photos.query.all()
    return render_template("photo.html", photo=photo[id-1])


if __name__== "__main__":
    app.run(debug=True)