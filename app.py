from flask import Flask, render_template
from flask_login import LoginManager
from auth import auth
from notes import notes
from models import db, User, Note

app = Flask(__name__)
app.config['SECRET_KEY'] = "Bgo7iaPEFueVnDkzRtGMSohD4YtPyAvG"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

@app.route("/")
def index():
    return render_template("base.html")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(auth)
app.register_blueprint(notes)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)

