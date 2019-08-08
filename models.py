from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from os import path

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:westos@localhost/email'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['FILM_SOURCE_URI'] = path.join(path.abspath(path.dirname(__name__)), 'static/files')
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)


class User(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(40), unique=True)
    nickname = db.Column(db.String(40), default=email)
    passwd = db.Column(db.String(150))
    phone = db.Column(db.String(20))
    sign = db.Column(db.String(60), default='你这家伙还没有个性签名！')
    register_time = db.Column(db.DATETIME, default=datetime.now())
    emails = db.relationship('Email', backref='user')
    drafts = db.relationship('Draft', backref='user')
    folders = db.relationship('Folder', backref='user')
    linkmans = db.relationship('Linkman', backref='user')
    tasks = db.relationship("Task", backref='user')
    logs = db.relationship('UserLog', backref='user')

    def __repr__(self):
        return '<User：%s>' % self.email


class Email(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    send_man = db.Column(db.String(40), nullable=False)
    theme = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)
    attachment = db.Column(db.String(250))
    receive_time = db.Column(db.DATETIME, default=datetime.now())
    folder_id = db.Column(db.Integer, db.ForeignKey('folder.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Task_id：%s>' % self.theme


class Draft(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    from_man = db.Column(db.String(40))
    receive_man = db.Column(db.String(40))
    theme = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)
    attachment = db.Column(db.String(50))
    add_time = db.Column(db.DATETIME, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Draft：%s>' % self.theme


class Linkman(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    remark = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(40), unique=True)
    phone = db.Column(db.String(20), default='')
    last_contact = db.Column(db.DATETIME)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<remark：%s>' % self.remark


class Folder(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(15))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    emails = db.relationship('User', backref='folder')


class Task(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    add_time = db.Column(db.DateTime, default=datetime.now())  # 创建时间
    status = db.Column(db.Boolean, default=False)  # 任务状态， 默认为Flase(未完成)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Todo: %s>' % (self.id)


class UserLog(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    time = db.Column(db.DATETIME, default=datetime.now())
    ip = db.Column(db.String(40), nullable=False)
    area = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Login_ip：%s>' % self.ip


if __name__ == "__main__":
    db.create_all()
    # my = User(nickname='长安223',email='admin',passwd='admin',phone='11111111111',sign='在下就是传说中的管理员')
    # db.session.add(my)
    # db.session.commit()
    # fo = Folder(name='默认收件箱',user_id=1)
    # em = Email(send_man='abcdeff',theme='测试邮件主题223呀，测试邮件呀，测试邮件呀',
    #            content='测试邮件内容223呀，测试邮件内容呀测试邮件内容呀测试邮件呀，测试邮件呀',
    #            folder_id=1,user_id=1
    #            )
    # db.session.add(fo)
    # db.session.commit()
    # db.session.add(em)
    # db.session.commit()
    # l = Linkman(nickname='昵称3',remark='备注3',email='dufhdi@qq.com',user_id=1)
    # l2 = Linkman(nickname='昵称4', remark='备注4', email='684651846@qq.com', user_id=1)
    # db.session.add_all([l,l2])
    # db.session.commit()
    # fo = Folder(name='公司邮件箱', user_id=1)
    # fo2 = Folder(name='学校邮件箱', user_id=1)
    # fo3 = Folder(name='其他邮件箱', user_id=1)
    # db.session.add_all([fo,fo2,fo3])
    # db.session.commit()
