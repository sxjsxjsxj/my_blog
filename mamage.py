from flask import Flask,render_template,session,request,redirect
from flask_script import Manager
from app.views import blue
from app.views_web import blue_web
from app.models import db

app = Flask(__name__)
app.secret_key='safdasdfasdfasdf'
#第三步、注册蓝图，即可使用
app.register_blueprint(blueprint=blue,url_prefile='/app*')
app.register_blueprint(blueprint=blue_web,url_prefile='/app_web')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:950796@127.0.0.1:3306/my_blog'
db.init_app(app)


@app.route('/',methods=['GET','POST'])
def hello():
    return render_template('back/login.html')


if __name__ == '__main__':
    manage = Manager(app)
    manage.run()