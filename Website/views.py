from flask import Blueprint,render_template,request,flash,jsonify
from flask_login import  login_required, current_user
from  .models import messages_table
from . import db
import json

views = Blueprint('views',__name__)

@views.route('/', methods=['GET','POST'])
@login_required
def homeView():
    if request.method == 'GET':
        userName = request.args.get('userName')

    if request.method == 'POST':
        message = request.form.get('message')
        if message == "":
            flash("Empty Message Can't be sent", category="error")
        else:
            new_message = messages_table(message_text=messages) #user_id=current_user.id)
            db.session.add(new_message)
            db.session.commit()
            flash("Message sent Successfully", category="success")

        print(userName)
    return render_template("home.html", user=current_user,userName=userName)



main = Blueprint('main', __name__)

@main.route('/')
def index():
    return "Hello, World!"
@views.route('/delete-message',methods=["POST"])
def delete_message():
    message = json.loads(request.data)
    messageId = date['messageId']
    message = Messages_table.query.get(messageId)
    if message:
        if message.user_id == current_user.id :
            db.session.delete(message);
            db.session.commit();

    return Jsonify({})