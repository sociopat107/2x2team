# coding: utf-8
from __future__ import unicode_literals
from flask import Flask,session, request, flash, url_for, redirect, render_template, abort ,g
from flask.ext.login import login_user , logout_user , current_user , login_required
from app import app,db,MAX_SEARCH_RESULTS
from forms import LoginForm, RegisterForm
from models import User, Tovar, Category
from flask.ext.admin import Admin, BaseView, expose, AdminIndexView
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.contrib.fileadmin import FileAdmin
import os.path as op
from flask.ext.babelex import Babel

class AdminIndex(AdminIndexView):
    def is_accessible(self):
        return g.user.is_admin()

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('login', next=request.url))


admin = Admin(app, index_view=AdminIndex(name='Администрация'))

babel = Babel(app)

@babel.localeselector
def get_locale():
        return 'ru'


class MyView(BaseView):
    def is_accessible(self):
        return g.user.is_admin()

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('login', next=request.url))

class MyFileAdmin(MyView, FileAdmin):
    pass
    
class MyModelView(MyView, ModelView):
    pass

class LogoutView(MyView):
    @expose('/')
    def index(self):
        return redirect('/logout')


path = op.join(op.dirname(__file__), 'static')
admin.add_view(MyFileAdmin(path, '/static/', name='Файлы на сервере'))
admin.add_view(MyModelView(User, db.session, name='Пользователи'))
admin.add_view(MyModelView(Category, db.session, name='Категории'))
admin.add_view(MyModelView(Tovar, db.session, name='Товары'))
admin.add_view(LogoutView(name='Выход'))


@app.route('/')
@app.route('/index', methods = ['GET', 'POST'])
def index():
    form = LoginForm(csrf_enabled=False)
    if form.validate_on_submit():
        login = form.login.data
        password = form.password.data
        user2 = User.query.filter_by(login=login,password=password).first()
        if user2:
            login_user(user2)
            flash(u'Вы авторизовались, как %s' % login)
            return redirect('/index')
        else:
            flash(u'Вы не авторизованы')            
            return redirect('/login')
        
    posts = Category.query.all()
    return render_template('index.html',
                           title = 'Сервис-Бит', posts=posts,
                           form=form)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm(csrf_enabled=False)
    if form.validate_on_submit():
        login = form.login.data
        password = form.password.data
        user2 = User.query.filter_by(login=login,password=password).first()
        if user2:
            login_user(user2)
            flash(u'Вы авторизовались, как %s' % login)
            return redirect('/index')
        else:
            flash(u'Вы не авторизованы')            
            return redirect('/login')
             
    return render_template('login.html', 
        title = 'Вход',
        form = form
    )

@app.route('/reg' , methods=['GET','POST'])
def reg():
    form = RegisterForm(csrf_enabled=False)
    if form.validate_on_submit():
        login = form.login.data
        password = form.password.data
        email = form.email.data
        user2 = User.query.filter_by(login=login).first()
        user = User(login, email, password)
        if user2:
            flash('Вам не удалось зарегистрироваться')
            return redirect('/reg')            
        else:
            db.session.add(user)
            db.session.commit()
            flash('Вы зареганы')
            return redirect(url_for('login'))
    return render_template('register.html',
                           title="Страница регистрации",
                           form = form,
    )

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index')) 


@app.route('/korzina')
@login_required
def korzina():
    return render_template('korzina.html',
        title='Список покупок',
        session=session
    )

@app.route('/tovar/<id>')
def tovar(id):
    g.tovar = Tovar.query.get(id)
    return render_template('tovar.html',
        title='Страница товара',
        id=id                   
    )

@app.route('/cat/<id>')
def category(id):
    g.category = Category.query.get(id)
    posts = g.category.tovari.all()
    return render_template('cat.html',
        title='Категория товара',
                           id=id,
                           posts=posts
    )


@app.route('/tovar_add/<id>')
def tovar_add(id):
    session['korzina'] = Tovar.query.get(id)
    return redirect(url_for('korzina'))

@app.route('/clear')
def clear():
    session['korzina'] = None
    return redirect(url_for('korzina'))


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        db.session.add(g.user)
        db.session.commit()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
