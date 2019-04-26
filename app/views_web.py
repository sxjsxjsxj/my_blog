from flask import Blueprint,request,render_template,redirect,url_for,session

from app.models import db, User, Article, Category

from utils.functions import login_required1

blue_web = Blueprint('blog_web',__name__)

@blue_web.route('/web_index1/',methods=['GET'])
def web_index1():
    return render_template('web/index.html')

@blue_web.route('/about/',methods=['GET'])
def about():
    return render_template('web/about.html')

@blue_web.route('/listpic/',methods=['GET'])
def listpic():
    return render_template('web/listpic.html')

@blue_web.route('/newslistpic/',methods=['GET'])
def newslistpic():
    return render_template('web/newslistpic.html')

###################################################################################
#前端登录
@blue_web.route('/web_home/',methods=['GET','POST'])
def web_home():
    user_id = session['user_id']
    user = User.query.filter(User.id == user_id).first()
    articles = Article.query.filter(Article.user_id == user_id).all()
    return render_template('web/index.html',
                           articles=articles,
                           user=user)

@blue_web.route('/web_login/',methods=['GET','POST'])
def web_login():
    if request.method == 'GET':
        return render_template('web/login_index.html')

    if request.method == 'POST':
        #登录校验
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter(User.user == username, User.password == password).first()
        if user:
            session['user_id'] = user.id
            session['name'] = user.name
            return redirect('/web_home/')
        return render_template('web/login_index.html')

@blue_web.route('/web_index/',methods=['GET','POST'])
@login_required1
def web_index():
    return render_template('web/index.html')