from flask import Flask, render_template, request, jsonify, redirect, url_for, session, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_migrate import Migrate
from db_and_mail import db, mail
from exts import UserModel
from flask_mail import Message
import string
import random
from exts import EmailCaptchaModel
from exts import RegisterForm
from exts import LoginForm
from exts import LogModel
from decimal import Decimal
from werkzeug.security import generate_password_hash, check_password_hash
from exts import money_change_email
import re
app = Flask(__name__)
import config
import exts
# HOSTNAME = 'localhost'
# PORT = 3306
# USERNAME = 'root'
# PASSWORD = 'kirisame'
# DATABASE = 'flask_learn'
# app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8"
# db = SQLAlchemy(app)

# migrate = Migrate(app, db)


mail_pass = 'wgpwybxthxdudeig'
app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)
#当数据库表项发生改变的时候，需要在终端中输入这些命令
#flask db migrate
#flask db upgrade


migrate = Migrate(app, db)

#测试
# @app.route('/index/<indexID>')#
# def index(indexID):
#     return render_template('index.html', indexID=indexID)

# @app.route("/request_data/")
# def request_data():
#     requestval = request.args.get('requestval')
#     return f"The value of requestval is: {requestval}"

#登陆页面
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = LoginForm(request.form)
        print(form.data)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                #验证成功
                session['user_id'] = user.id
                return redirect(url_for('action'))
            else:
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))
    elif request.method == 'GET':
        return render_template('login.html')

#存钱
@app.route('/deposit', methods={'POST'})
def deposit():
    print(request.args.get('amount'))
    amount = request.args.get('amount')
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    user = UserModel.query.get(user_id)
    try:
        amount = Decimal(amount)
        print(amount)
        assert amount > 0
        final_balance = user.balance + amount
        user.balance = final_balance
        db.session.add(LogModel(amount = amount, balance = final_balance, message = "用户存款", related_user_id = user.id))
        db.session.commit()
        money_change_email(amount=amount, user=user)
        print(f"{user.username} Deposit {amount} successful")
        # db.session.add(UserModel(username = username, email =
        #  email, password = generate_password_hash(password)))
        # db.session.commit()
        return jsonify({'code': 200, 'message': 'Deposit successful', 'balance' : final_balance})
    except:
        print(f"Invalid amount from User {user.username}")
        return jsonify({'code': 400, 'message': 'Invalid amount'})

#取钱
@app.route('/withdraw', methods={'POST'})
def withdraw():
    print(request.args.get('amount'))
    amount = (request.args.get('amount'))
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    user = UserModel.query.get(user_id)
    try:
        amount = Decimal(amount)
        assert (float(amount) > 0 and float(amount) <= float(user.balance))
        remain_balance = user.balance - amount
        user.balance = remain_balance
        # message = "取钱"
        # log = LogModel(amount=amount, balance=remain_balance, message = message)
        # db.add(log)
        db.session.add(LogModel(amount = -amount, balance = remain_balance, message = "用户支取", related_user_id = user.id))
        db.session.commit()
        money_change_email(amount=-amount, user=user)
        print(f"{user.username} Withdraw {amount} successful")
        return jsonify({'code': 200, 'message': 'Withdraw successful', 'balance' : remain_balance})
    except:
        print(f"Invalid amount from User {user.username}")
        return jsonify({'code': 400, 'message': 'Invalid amount'})

#转账
@app.route('/transfer', methods={'POST'})
def transfer():
    amount =request.args.get('amount')
    to_user_id = request.args.get('to_user_id')
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    user = UserModel.query.get(user_id)
    try:
        to_user = UserModel.query.get(to_user_id)
        assert to_user.id!= user.id
        assert to_user != None
    except:
        return jsonify({'code': 400, 'message': 'Invalid target user id'})
    try:
        amount = Decimal(amount)
        assert (amount > 0 and amount <= user.balance)
        from_balance = user.balance - amount
        to_balance =  to_user.balance + amount
        to_user.balance = to_balance
        user.balance = from_balance
        db.session.add(LogModel(amount = -amount, balance = from_balance, message = f"转出给{to_user.username}", related_user_id = user.id))
        db.session.add(LogModel(amount = amount, balance = to_balance, message = f"{user.username}转入", related_user_id = to_user.id))
        db.session.commit()
        money_change_email(amount=-amount, user=user)
        money_change_email(amount=amount, user=to_user)
        print(f"{user.username} Transfer {amount} to {to_user.username} successful")
        return jsonify({'code': 200, 'message': 'Transfer successful', 'balance' : from_balance})
    except:
        return jsonify({'code': 400, 'message': 'Invalid amount'})

@app.route('/log', methods=['GET'])
def log():
    opreations = LogModel.query.filter_by(related_user_id=session.get('user_id')).all()
    return render_template('log.html', operations = opreations)

#注册页面
#TODO: 注册页面的处理函数
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        form = RegisterForm(request.form)
        print(request.form)
        if form.validate():#这个validate函数会自动调用RegisterForm里面的那些验证器
            username = form.username.data
            email = form.email.data
            password = form.password.data
            db.session.add(UserModel(username = username, email = email, password = generate_password_hash(password)))
            db.session.commit()
            
            return redirect(url_for("login"))
        else:
            print(form.errors)
            return redirect(url_for("register"))

    elif request.method == 'GET':
        return render_template('register.html')

@app.route('/action')
def action():
    return render_template('action.html')

@app.route('/mail_test')
def mail_test():
    msg = Message(subject = '邮箱测试', recipients = ['powein2@outlook.com'])
    msg.body = 'I love you'
    mail.send(msg)
    return 'Sent email'

#邮件验证码 API
@app.route('/send_captcha')
def send_captcha():
    #TODO: 发送验证码的处理函数
    email = request.args.get('email')
    source = string.digits * 6
    random.sample(source, 6)
    captcha = ''.join(random.sample(source, 6))
    #TODO: 保存验证码到数据库
    if (UserModel.query.filter_by(email=email).first()):
        return jsonify({'code': 400, 'message': '邮箱已经存在'})
    if not email:
        return jsonify({'code': 400, 'message': '邮箱不存在'})
    else:
        if not re.match(r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)*@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email):
            return jsonify({'code': 400, 'message': '邮箱格式不合法'})
    email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    #TODO: 发送验证码邮件
    msg = Message(subject = '验证码', recipients = [email])
    msg.body = f'欢迎注册天地银行资产管理平台，您的验证码是:{captcha}，十分钟内有效，请勿与他人共享。'
    mail.send(msg)
    #restful接口返回验证码
    # return Flask.jsonify({'status': 'ok', 'captcha': captcha})
    ret_val = jsonify({'code': 200, 'message':'验证码已成功发送，请注意查收'})
    return ret_val

@app.before_request
def my_Hook_0():
    user_id = session.get('user_id')
    if user_id:
        user = UserModel.query.get(user_id)
        setattr(g, 'user', user)
    else:
        setattr(g, 'user', None)

@app.route('/logout',methods=['POST'])
def logout():
    session.clear()
    return jsonify({'code' : '200'})

@app.context_processor
def my_Hook_1():
    return {'user':g.user}

@app.context_processor
def inject_navigation_links():
    navigation_links = [
        {"url": "/action", "name": "主页"},
        {"url": "/login", "name": "登陆"},
        {"url": "/register", "name": "注册"}
    ]
    return dict(navigation_links=navigation_links)

@app.route('/speedtest', methods=['GET', 'POST'])
def speedtest():
    if request.method == 'POST':
        return jsonify({'code': 200,})
    elif request.method == 'GET':
        return render_template('speedtest.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)