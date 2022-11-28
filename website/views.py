from flask import Blueprint, render_template, request, session

views = Blueprint('views', __name__)


@views.route('/', methods=['POST'])
def home():
    if request.method == 'POST':
        #data = request.get_json(silent=True)
        data = request.form
        session["mood"] = data["mood"]
        session["tempo"] = data["tempo"]
    print(session)
    return session["mood"]



@views.route('/map', methods=['GET', 'POST'])
def map():
    if request.method == 'POST':
        data = request.form
        session["mapping"] = data
    return render_template("sign_up.html")


@views.route('/getInfo', methods=['GET'])
def getInfo():
    print(session["mapping"])
    # return tempo (session["tempo"]) and color (session[session["mood"]])
    return [session["mapping"], session["mapping"][session["mood"]]]