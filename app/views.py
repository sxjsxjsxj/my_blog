
from flask import Blueprint,request,render_template,redirect,url_for,session
# from utils.functions import login_required
from app.models import db,User,Article,Category

blue = Blueprint('blog',__name__)



###########################业务操作############################
#创建表
@blue.route('/create_db/',methods=['GET'])
def create_db():
    db.create_all()


    return '创建表成功'

#注册
@blue.route('/back_register/',methods=['GET','POST'])
def back_register():
    user = User()
    user.user = request.form.get('username')
    user.name = request.form.get('name')
    user.password = request.form.get('password')
    user.save()
    return redirect('/back_login/')

#登录
@blue.route('/back_login/',methods=['GET','POST'])
def back_login():
    if request.method == 'GET':
        return render_template('back/login.html')
    if request.method == 'POST':
        user = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter(User.user == user,User.password==password).first()
        if user:
            session['user_id'] = user.id
            session['name'] = user.name
            return redirect('/back_home/')
        return render_template('back/login.html')

# @blue.route('/back_index/',methods=['GET','POST'])
# @login_required
# def back_index():
#     return render_template('back/index.html')

#主页
@blue.route('/back_home/',methods=['GET','POST'])
def back_home():
    article_count = len(Article.query.filter(Article.user_id == session['user_id']).all())
    return render_template('back/index.html',
                           username = session['name'],
                           article_count = article_count
                           )
#栏目
@blue.route('/category/',methods=['GET','POST'])
def category():
    categorys = Category.query.filter().all()
    categorys_count = len(categorys)
    for index,category in enumerate(categorys):
        category.index = index+1
        category.update_href = "/update_category/?category_id=" + str(category.category_id)
        category.delete_href = "/delete_category/?category_id=" + str(category.category_id)
        category.count = len(category.aou)#该栏目的文章数目
    return render_template('back/category.html',
                           categorys=categorys,
                           categorys_count=categorys_count)

#添加栏目
@blue.route('/add_category/',methods=['GET', 'POST'])
def add_category():
    category = Category()
    category.category_title = request.form.get('name')
    category.category_name = request.form.get('alias')
    category.category_keyword = request.form.get('keywords')
    category.category_describe = request.form.get('describe')
    category.save()
    return redirect(url_for('blog.category'))

@blue.route('/update_category/',methods=['GET','POST'])
def update_category():
    category_id = request.args['category_id']
    session['category_id'] = category_id
    category = Category.query.filter(Category.category_id == category_id).first()
    return render_template('back/update-category.html',
                    category=category)

@blue.route('/update_Category/',methods=['GET','POST'])
def update_Category():
    category_id = session['category_id']
    category = Category.query.filter(Category.category_id == category_id).first()
    category.category_title = request.form.get('name')
    category.category_name = request.form.get('alias')
    category.category_keyword = request.form.get('keywords')
    category.category_describe = request.form.get('describe')
    category.save()
    return redirect(url_for('blog.category'))

@blue.route('/delete_category/',methods=['GET','POST'])
def delete_category():
    category_id = request.args['category_id']
    category = Category.query.filter(Category.category_id == category_id).first()
    if category.aou:
        category.aou = []
        db.session.commit()
    category.delete()
    return redirect(url_for('blog.category'))

#获取文章
@blue.route('/article/',methods=['GET'])
def article():
    user_id = session['user_id']
    articles = Article.query.filter(Article.user_id == user_id).all()
    for article in articles:
        article.update_href = "/update_article/?article_id=" + str(article.article_id)
        article.delete_href = "/delete_article/?article_id=" + str(article.article_id)
        article.type = '无类型'
        if article.cou:
            article.type = article.cou[0].category_title
    return render_template('back/article.html',
                           articles=articles,
                           articles_count=len(articles)
)

@blue.route('/add_article/',methods=['GET'])
def add_article():
    categorys = Category.query.filter().all()
    return render_template('back/add-article.html',
                           categorys=categorys)

#添加文章
@blue.route('/add_Article/',methods=['GET', 'POST'])
def add_Article():
    article = Article()
    article.article_title = request.form.get('title')
    article.article_text = request.form.get('content')
    article.user_id = session['user_id']
    article.article_keyword = request.form.get('keywords')
    article.article_describe = request.form.get('describe')
    category = Category.query.filter(Category.category_id == request.form.get('category')).first()
    article.cou.append(category)
    category.aou.append(article)
    article.save()
    return redirect(url_for('blog.article'))

@blue.route('/update_article/',methods=['GET','POST'])
def update_article():
    article_id = request.args['article_id']
    session['article_id'] = article_id
    article = Article.query.filter(Article.article_id == article_id).first()
    categorys = Category.query.filter().all()
    return render_template('back/update-article.html',
                           article=article,
                           categorys=categorys)

@blue.route('/update_Article/',methods=['GET','POST'])
def update_Article():
    article_id = session['article_id']
    article = Article.query.filter(Article.article_id == article_id).first()
    category1 = Category.query.filter(Category.category_id == article.cou[0].category_id).first()
    article.cou.remove(category1)
    article.article_title = request.form.get('title')
    article.article_text = request.form.get('content')
    article.user_id = session['user_id']
    article.article_keyword = request.form.get('keywords')
    article.article_describe = request.form.get('describe')
    category2 = Category.query.filter(Category.category_id == request.form.get('category')).first()
    article.cou.append(category2)
    category2.aou.append(article)
    article.save()
    return redirect(url_for('blog.article'))

@blue.route('/delete_article/',methods=['GET','POST'])
def delete_article():
    article_id = request.args['article_id']
    article = Article.query.filter(Article.article_id == article_id).first()
    if article.cou:
        article.cou = []
        db.session.commit()
    article.delete()
    return redirect(url_for('blog.article'))
