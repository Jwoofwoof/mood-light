from flask import Blueprint, render_template, request


views = Blueprint('views', __name__)
session ={}


@views.route('/', methods=['GET','POST'])
def home():

    print(session)
    if request.method == 'POST':
        #data = request.get_json(silent=True)
        data = request.form
        session["mood"] = str(data["mood"])
        session["tempo"] = data["tempo"]
    print(session)
    return session["mood"]



@views.route('/map', methods=['GET', 'POST'])
def map():

    print(session)
    if request.method == 'POST':
        data = request.form
        session["mapping"] = data
        print(session)


    return render_template("sign_up.html")


@views.route('/getInfo', methods=['GET', 'POST'])
def getInfo():
    #print(session["mood"])
    # return tempo (session["tempo"]) and color (session[session["mood"]])
    #mood = session["mood"]
    if "mapping" in session: 
        print(session["mapping"])
        #return {"tempo": session["tempo"],  "color": session["mapping"][session["mood"]]}
        return session["tempo"] + " " + session["mapping"][session["mood"]]

    else:
        return "1"
 


@views.route('/test', methods=['GET', 'POST'])
def test():
    #print(session["mood"])
    # return tempo (session["tempo"]) and color (session[session["mood"]])
    #mood = session["mood"]
    return "2"