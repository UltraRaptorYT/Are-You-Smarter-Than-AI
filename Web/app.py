from application import db, create_app
from flask_cors import CORS, cross_origin

app = create_app()
CORS(app)

if __name__ == "__main__":
    db.create_all(app=app)
