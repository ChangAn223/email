from getpass import getpass
from werkzeug.security import generate_password_hash
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from models import app, db, User,Email,Linkman,Folder,UserLog

# 让python支持命令行工作
manager = Manager(app)

# 使用migrate绑定app和db
migrate = Migrate(app,db)

# 添加迁移脚本的命令到manager中,使得可以通过命令进行数据库迁移
manager.add_command('db',MigrateCommand)

# # 自定义一些 命令 ：
#
# @manager.command
# def showadmin():
#     try:
#         admins = Admin.query.all()
#     except:
#         print('查看管理员失败！')
#     else:
#         print('管理员有：',admins)
#
# @manager.command
# def showuser():
#     try:
#         users = User.query.count()
#     except:
#         print('查看用户失败！')
#     else:
#         print('一共有 %s 为用户' %users)
#
# @manager.command
# def createadmin():
#     name = input("管理员帐号：")
#     passwd = getpass("管理员密码：")
#     admin = Admin(name=name,passwd=generate_password_hash(passwd))
#     try:
#         db.session.add(admin)
#         db.session.commit()
#     except:
#         print('创建管理员失败！')
#     else:
#         print("创建管理员 %s 成功！" %name)

if __name__ == "__main__":
    manager.run()