import random
import functools
from datetime import datetime
from flask import session, render_template, redirect, request, url_for, flash
from os import path
from sqlalchemy import or_, desc
from models import app, db, User, Email, Folder, UserLog, Linkman, Draft, Task
from forms import *

app.config['SECRET_KEY'] = random._urandom(24)

global folders
global recent_linkmans


# 判断是否登陆的一个装饰器
def is_login(func):
    @functools.wraps(func)
    # 这个装饰器使得不改变装饰函数的函数名
    def wraper(*args, **kwargs):
        if not (session.get('id') and session['email'] and session['nickname']):
            return redirect(url_for('login'))
        else:
            return func(*args, **kwargs)

    return wraper


@app.route('/')
@app.route('/<int:page>')
@is_login
def zhuye(page=1):
    emails = Email.query.filter_by(user_id=session['id']).paginate(page, 8)
    return render_template('zhuye.html', folders=folders, emails=emails)


@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        passwd = request.form['passwd']
        u = User.query.filter_by(email=email, passwd=passwd).first()
        if u != None:
            session['id'] = u.id
            session['email'] = u.email
            session['nickname'] = u.nickname
            global folders
            folders = Folder.query.filter_by(user_id=session['id']).all()
            global recent_linkmans
            recent_linkmans = Linkman.query.filter_by(user_id=session['id']).order_by(desc(Linkman.last_contact)).limit(
                6).all()
            return redirect(url_for('zhuye'))
        else:
            return render_template('login.html', message='* 用户名或者密码错误')
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('id')
    session.pop('email')
    session.pop('nickname')
    return redirect(url_for('login'))


@app.route('/register.html', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['username']
        phone = request.form['phone']
        passwd = request.form['passwd']
        u = User.query.filter(or_(User.email == email, User.phone == phone)).first()
        if u:
            if email == u.email:
                return render_template(url_for('register'), message='* 该用户名已经存在')
            elif phone == u.phone:
                return render_template(url_for('register'), message='* 该手机号已经注册')
        else:
            try:
                u = User(email=email, phone=phone, passwd=passwd)
                db.session.add(u)
                db.session.commit()
                user_id = (User.query.filter_by(email=email).first()).id
                fo = Folder(name='默认收件箱', user_id=user_id)
                db.session.add(fo)
                db.session.commit()
            except Exception as e:
                print(e)
                return redirect(url_for('error'))
            else:
                session['email'] = email
                return redirect(url_for('success'))
    else:
        return render_template('register.html')


@app.route('/success.html')
def success():
    if session['email']:
        return render_template('success.html')
    else:
        return redirect(url_for('/'))


@app.errorhandler(404)
@app.route('/404.html')
def error():
    return render_template('404.html')


@app.route('/email/<int:id>')
@is_login
def view(id):
    email = Email.query.get(id)
    if email:
        return render_template('view.html', folders=folders, email=email)
    else:
        return redirect(url_for('/'))


@app.route('/write/', methods=['GET', 'POST'])
@is_login
def write():
    if request.method == "POST":
        sendto = request.form['sendto']
        receive_man = User.query.filter_by(email=sendto).first()
        if receive_man:
            from_man = session['email']
            theme = request.form['theme']
            content = request.form['content']
            try:
                file = request.files['file']
            except:
                filename = None
            else:
                file_save_path = path.join(app.config['FILM_SOURCE_URI'], file.filename)
                file.save(file_save_path)
                filename = file.filename

            fo = Folder.query.filter_by(user_id=receive_man.id, name='默认收件箱').first()
            email = Email(send_man=from_man, attachment=filename, theme=theme, content=content, user_id=receive_man.id,
                          folder_id=fo.id)
            db.session.add(email)
            db.session.commit()
            flash(' *发送邮件成功！')
            linkman = Linkman.query.filter_by(user_id=receive_man.id).first()
            if linkman:
                linkman.last_contact = datetime.now()
                db.session.add(linkman)
                db.session.commit()
            else:
                lm = Linkman(email=receive_man.email, remark=receive_man.email, user_id=session["id"])
                db.session.add(lm)
                db.session.commit()
            global recent_linkmans
            recent_linkmans = Linkman.query.filter_by(user_id=session['id']).order_by(desc(Linkman.last_contact)).limit(
                6).all()
            return redirect(url_for('write'))
        else:
            flash(' *收信人不存在！')
            return redirect(url_for('write'))
    else:
        return render_template('write.html', folders=folders, recent_linkmans=recent_linkmans)


@app.route('/email/delete/<int:id>', methods=['POST'])
@is_login
def delete_email(id):
    e = Email.query.filter_by(id=id).first()
    try:
        db.session.delete(e)
        db.session.commit()
    except Exception as e:
        print(e)
        return redirect(url_for('error'))
    else:
        flash(' *删除邮件成功！')
        return redirect(url_for('zhuye'))


@app.route('/email/move/<int:id>', methods=['POST'])
@is_login
def move_email(id):
    folder_id = int(request.form['choice'])
    try:
        e = Email.query.filter_by(id=id).first()
        e.folder_id = folder_id
        db.session.add(e)
        db.session.commit()
    except Exception as e:
        print(e)
        return redirect(url_for('error'))
    else:
        flash(' *移动邮件成功！')
        return redirect(url_for('zhuye'))


@app.route('/linkman/')
@app.route('/linkman/<int:page>')
@is_login
def linkman(page=1):
    linkmans = Linkman.query.filter_by(user_id=session['id']).order_by(desc(Linkman.remark)).paginate(page, 10)
    return render_template('linkman.html', folders=folders, linkmans=linkmans, recent_linkmans=recent_linkmans)


@app.route('/linkman/add', methods=['get', 'post'])
@is_login
def add_linkman():
    form = LinkmanForm()
    if form.validate_on_submit():
        data = form.data
        lm = Linkman(remark=data["name"], email=data["email"], phone=data["phone"], user_id=session["id"])
        db.session.add(lm)
        db.session.commit()
        flash("添加联系人 %s 成功" % (data["name"]))
        return redirect((url_for('add_linkman')))
    else:
        return render_template('addlinkman.html', folders=folders, form=form)


@app.route('/linkman/delete/<int:id>', methods=['post'])
@is_login
def delete_linkman(id):
    l = Linkman.query.filter_by(id=id).first()
    try:
        db.session.delete(l)
        db.session.commit()
    except Exception as e:
        print(e)
        return redirect(url_for('error'))
    else:
        return redirect(url_for('linkman'))


@app.route('/linkman/edit/<int:id>', methods=['get', 'post'])
def edit_linkman(id):
    form = LinkmanForm()
    # 根据主键查找， 如果没有找到， 404报错;
    lm = Linkman.query.get_or_404(id)
    if request.method == 'GET':
        form.name.data = lm.remark
        form.email.data = lm.email
        form.phone.data = lm.phone

    if form.validate_on_submit():
        data = form.data
        t = Linkman.query.filter_by(remark=data['name']).count()
        if form.name.data != lm.remark and t >= 1:
            flash("联系人已经存在！")
            return redirect(url_for('edit_linkman', id=id))
        else:
            # 修改数据库的内容
            lm.remark = form.name.data
            lm.email = form.email.data
            lm.phone = form.phone.data
            db.session.add(lm)
            db.session.commit()

            flash("修改联系人 %s 成功!" % (lm.remark))
            return redirect(url_for('edit_linkman', id=id))
    else:
        return render_template('editlinkman.html', folders=folders, form=form, linkman=lm)


@app.route('/draft/')
@app.route('/draft/<int:page>')
@is_login
def draft(page=1):
    drafts = Draft.query.filter_by(user_id=session['id']).paginate(page, 8)
    return render_template('draft.html', folders=folders, drafts=drafts)


@app.route('/draft/add/', methods=['GET', 'POST'])
@is_login
def add_draft():
    if request.method == 'POST':
        receive_man = request.form['sendto']
        from_man = session['email']
        theme = request.form['theme']
        content = request.form['content']
        try:
            file = request.files['file']
        except:
            filename = None
        else:
            file_save_path = path.join(app.config['FILM_SOURCE_URI'], file.filename)
            file.save(file_save_path)
            filename = file.filename

        draft = Draft(from_man=from_man, receive_man=receive_man, attachment=filename, theme=theme, content=content,
                      user_id=session['id'])
        db.session.add(draft)
        db.session.commit()
        flash(' *添加邮件草稿成功！')
        return redirect(url_for('draft'))
    else:
        return render_template('adddraft.html', folders=folders)


@app.route('/addfolder/', methods=['POST'])
@is_login
def add_folder():
    foldername = request.form['foldername']
    try:
        fo = Folder(name=foldername, user_id=session['id'])
        db.session.add(fo)
        db.session.commit()
    except:
        return redirect(url_for('error'))
    else:
        global folders
        folders = Folder.query.filter_by(user_id=session['id']).all()
        return redirect(url_for('zhuye'))


@app.route('/folder/delete/<int:id>', methods=['post'])
@is_login
def delete_folder(id):
    try:
        emails = Email.query.filter_by(folder_id=id).all()
        default_id = Folder.query.filter_by(user_id=session['id']).first()
        for e in emails:
            e.folder_id = default_id
        db.session.add_all(emails)
        db.session.commit()
        f = Folder.query.filter_by(id=id).first()
        db.session.delete(f)
        db.session.commit()
    except Exception as e:
        print(e)
        return redirect(url_for('error'))
    else:
        global folders
        folders = Folder.query.filter_by(user_id=session['id']).all()
        return redirect(url_for('zhuye'))


@app.route('/email/<string:name>/<int:page>')
@app.route('/email/<string:name>/')
@is_login
def folder(name, page=1):
    folder = Folder.query.filter_by(user_id=session['id'], name=name).first()
    emails = Email.query.filter_by(user_id=session['id'], folder_id=folder.id).paginate(page, 8)
    return render_template('zhuye.html', folders=folders, emails=emails)


@app.route('/zone/', methods=['get', 'post'])
@is_login
def zone():
    form = MyInfoForm()
    # 根据主键查找， 如果没有找到， 404报错;
    u = User.query.get_or_404(session['id'])
    if request.method == 'GET':
        form.nickname.data = u.nickname
        form.sign.data = u.sign
        form.phone.data = u.phone

    if form.validate_on_submit():
        # 修改数据库的内容
        u.nickname = form.nickname.data
        u.sign = form.sign.data
        u.phone = form.phone.data
        db.session.add(u)
        db.session.commit()
        flash("修改信息成功!")
        return redirect(url_for('zone'))
    else:
        return render_template('zone.html', folders=folders, form=form)


@app.route('/passwd/', methods=['get', 'post'])
@is_login
def passwd():
    form = PwdForm()
    u = User.query.get_or_404(session['id'])
    if form.validate_on_submit():
        if form.oldpwd.data != u.passwd:
            flash("原密码输入错误!")
            return redirect(url_for('passwd'))
        elif form.newpwd.data != form.repwd.data:
            flash("新密码两次输入不一致！")
        else:
            u.passwd = form.pwd.data
            db.session.add(u)
            db.session.commit()
            flash("修改密码成功!")
            return redirect(url_for('passwd'))
    else:
        return render_template('passwd.html', folders=folders, form=form)


# 任务的增删改查
@app.route('/task/add/', methods=['POST'])
@is_login
def task_add():
    # 获取提交的任务信息
    name = request.form['todo_name']
    # 添加完成之后， 返回任务列表显示页面
    t = Task(name=name, user_id=session["id"])
    db.session.add(t)
    db.session.commit()
    return redirect(url_for('task_list'))


@app.route('/task/delete/<int:id>')
@is_login
def task_delete(id):
    t = Task.query.filter_by(id=id).first()
    print(t)
    db.session.delete(t)
    db.session.commit()
    return redirect(url_for('task_list'))


@app.route('/task/')
@app.route('/task/<int:page>')
@is_login
def task_list(page=1):
    # 1). 从数据库中查询
    todos = Task.query.filter_by(user_id=session['id']).paginate(page, 10)
    return render_template('task.html', folders=folders, todos=todos)


# 修改任务的状态(变成已完成状态/变成未完成状态)
@app.route('/task/change/<int:id>/')
@is_login
def task_change(id):
    todo = Task.query.filter_by(id=id).first()
    todo.status = not todo.status
    db.session.commit()
    # 更新状态后， 返回任务列表页
    return redirect(url_for('task_list'))

