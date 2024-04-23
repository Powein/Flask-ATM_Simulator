import wtforms
from wtforms.validators import Email, Length, EqualTo, InputRequired
from db_and_mail import db, mail
from sqlalchemy.types import Numeric
from flask_mail import Message

def money_change_email(amount, user):
    if amount > 0:
        message = f"用户{user.username},您名下ID为:{user.id}的银行账户有{amount}元到账,余额为{user.balance}元。"
    elif amount < 0:
        message = f"用户{user.username},您名下ID为:{user.id}的账户有{-amount}元被支取得,余额为{user.balance},如非本人操作,请及时到行处理。"
    msg = Message(subject = '银行余额变动通知', recipients = [user.email])
    msg.body = message
    mail.send(msg)
    return 'success'
#用户模型
class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    balance = db.Column(Numeric(20,2), default=0.0)

# 邮箱验证码模型
class EmailCaptchaModel(db.Model):
    __tablename__ = "email_captcha"
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    email = db.Column(db.String(100),nullable = False)
    captcha = db.Column(db.String(100),nullable = False)
    # used = db.Column(db.Boolean,default=False)

class LogModel(db.Model):
    __talbename__ = "log"
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    time = db.Column(db.DateTime,default=db.func.now())
    amount = db.Column(Numeric(20,2), nullable = False)
    balance = db.Column(Numeric(20,2), nullable = False)
    message = db.Column(db.String(100), nullable = False)
    related_user_id = db.Column(db.Integer, nullable = False)

class RegisterForm(wtforms.Form):
    #StringField表示一个字符串字段，validators表示验证器，Email表示验证邮箱格式
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误!")])#这个message是错误提示信息
    captcha = wtforms.StringField(validators=[Length(min=6, max=6, message="验证码格式错误!")])#验证码长度是6
    username = wtforms.StringField(validators=[Length(min=3, max=20, message="用户名格式错误!")])#用户名长度是3-20个字符
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误!")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password", message="两次输入密码不一致")])
    #自定义验证
    #邮箱是否已经被注册，验证码是否正确 validate_开头的方法名表示自定义验证方法，后面加上字段名表示验证的字段
    def validate_email(self, field):
        """检查邮箱是否已经被注册"""
        email = field.data
        user = UserModel.query.filter_by(email=email).first()#查询数据库中是否有该邮箱
        if user:
            raise wtforms.ValidationError(message="该邮箱已经被注册!")#防止重复注册

    def validate_captcha(self, field):
        """检查验证码是否正确"""
        captcha = field.data
        email = self.email.data
        captcha_model = EmailCaptchaModel.query.filter_by(email=email, captcha=captcha).first()
        if not captcha_model:
            raise wtforms.ValidationError(message="验证码错误!")
            # TODO: 可以删除 captcha_model
            # else:
            #     db.session.delete(captcha_model)
            #     db.session.commit()
        else:#这个会浪费时间,换成Redis的时候会更好
            db.session.delete(captcha_model)
            db.session.commit()

class LoginForm(wtforms.Form):
    email= wtforms.StringField(validators=[Email(message="邮箱格式错误!")])
    password = wtforms.StringField(validators=[Length(min=6,max=20,message="密码格式错误!")])

class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[Length(min=3,max=100,message="标题格式错误!")])
    content = wtforms.StringField(validators=[Length(min=3,message="内容格式错误!")])
