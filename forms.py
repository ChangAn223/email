from flask_wtf import FlaskForm
from wtforms import  StringField, SubmitField, PasswordField
from wtforms.validators import  DataRequired


# 联系人
class LinkmanForm(FlaskForm):
    name = StringField(
        label='备注',
        validators=[
            DataRequired("请添加备注!"),
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "请为联系人添加备注"
        }
    )
    email = StringField(
        label='邮箱',
        validators=[
            DataRequired("请添加邮箱!"),
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "请添加联系人的邮箱"
        }
    )
    phone = StringField(
        label='手机',
        render_kw={
            "class": "form-control",
            "placeholder": "添加联系人的手机"
        }
    )
    submit = SubmitField(
        '编辑',
        render_kw={
            "class": "btn btn-primary",
        }
    )


# 个人信息
class MyInfoForm(FlaskForm):
    nickname = StringField(
        label='昵称',
        render_kw={
            "class": "form-control",
        }
    )
    sign = StringField(
        label='个性签名',
        render_kw={
            "class": "form-control",
        }
    )
    phone = StringField(
        label='手机',
        render_kw={
            "class": "form-control",
        }
    )
    submit = SubmitField(
        '编辑',
        render_kw={
            "class": "btn btn-primary",
        }
    )

# 修改密码
class PwdForm(FlaskForm):
    oldpwd = PasswordField(
        label='旧密码',
        validators=[
            DataRequired("请输入旧密码!"),
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "请输入旧密码!"
        }
    )
    newpwd = PasswordField(
        label='新密码',
        validators=[
            DataRequired("请输入新密码!"),
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "请输入新密码!"
        }
    )
    repwd = PasswordField(
        label='重复新密码',
        validators=[
            DataRequired("请再次输入新密码!"),
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "请再次输入新密码!"
        }
    )
    submit = SubmitField(
        '修改',
        render_kw={
            "class": "btn btn-primary",
        }
    )
