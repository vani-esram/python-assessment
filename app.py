# from flask import Flask, request, render_template

# app = Flask(__name__)


# @app.route("/", methods=['GET', 'POST'])
# def home():
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         return f"welcome:{name} email {email}"
#     return render_template('index.html')


# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource


app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Stem (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(60), nullable=False)

    def to_dist(self):
        return {"id": self.id, "title": self.title, "author": self.author}


@app.before_request
def create_tables():

    db.create_all()


class ItemResource(Resource):
    def get(self, id):

        item = Stem.query.get(id)

        if item:
            return item.to_dist()

    def put(self, id):
        data = request.get_json()

        item = db.session.get(Stem, id)
        if item:
            item.title = data["title"]
            item.author = data["author"]
            db.session.commit()
            return item.to_dist()

        return {
            "message": "Item not found"
        }, 404

    def delete(self, id):
        item = Stem.query.get(id)
        if item:
            db.session.delete(item)
            db.session.commit()
            return {
                "message": "item deleted"
            }, 200


class itemlistResource(Resource):

    def post(self):
        data = request.get_json()

        new_item = Stem(
            title=data['title'],
            author=data['author']
        )
        db.session.add(new_item)
        db.session.commit()

        return new_item.to_dist()

    def get(self):

        items = Stem.query.all()

        return [item.to_dist() for item in items], 200


api.add_resource(ItemResource, '/Stem/<int:id>')
api.add_resource(itemlistResource, '/Stem')


if __name__ == '__main__':
    app.run(debug=True)
