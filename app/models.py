from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

db = SQLAlchemy()

c_a = db.Table('c_a',
    db.Column('a_id',db.Integer, db.ForeignKey('article.article_id')),
    db.Column('c_id', db.Integer, db.ForeignKey('category.category_id'))
)


class Article(db.Model):
    article_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    article_title = db.Column(db.String(50), nullable=False)
    article_text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    article_keyword = db.Column(db.String(50), nullable=True)
    article_describe = db.Column(db.String(255), nullable=True)
    create_time = db.Column(db.DateTime,default=datetime.now())
    cou = db.relationship('Category', secondary=c_a, backref='c')
    __tablename__ = 'article'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Article %s>' % (self.article_id)

class Category(db.Model):
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_title = db.Column(db.String(50), unique=True, nullable=False)
    category_name = db.Column(db.String(50), nullable=False)
    category_keyword = db.Column(db.String(50), nullable=True)
    category_describe = db.Column(db.String(255), nullable=True)
    aou = db.relationship('Article', secondary=c_a, backref='a')
    __tablename__ = 'category'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Category %s>' % (self.category_id)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now())
    __tablename__ = 'user'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

