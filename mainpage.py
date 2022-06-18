import os
# Modules for QR code generation
import pyqrcode
import pandas as pd

import png
from pyqrcode import QRCode
#Modules for PDF generation
from fpdf import FPDF
from datetime import *
from time import *
#Modules for Backend
from flask import *
from werkzeug.utils import secure_filename

data_all = pd.read_excel('test_data.xlsx')


UPLOAD_FOLDER = '/Users/pavan/PycharmProjects/firebase/QR/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#Modules for Server
from firebase import firebase
#modules for sending emails
import smtplib
from email.message import EmailMessage
#---------------------------------department data sorter--------------------------------------------

entered,exited={},{}
ece,cse,mech,eee,eie,cvl={},{},{},{},{},{}
ecel,csel,mechl,eeel,eiel,cvll={},{},{},{},{},{}
def data_sorter(n,m):
    brn = {'1': "mech", '2': "eee", '3': "eie", '4': "ece", '5': "cse", '6': "cvl"}
    for i in n:
        for j,k in zip(list(data_all['id']),list(data_all['name'])):
            if i==j:
                x={}
                # print(brn[i[7]])
                if brn[i[7]] =='mech':
                    mech[i]=k
                    x['branch']='MECH'
                elif brn[i[7]] == 'eee':
                    eee[i] = k
                    x['branch']='EEE'
                elif brn[i[7]] == 'eie':
                    eie[i] = k
                    x['branch']='EIE'
                elif brn[i[7]] == 'ece':
                    ece[i] = k
                    x['branch']='ECE'
                elif brn[i[7]] == 'cse':
                    cse[i] = k
                    x['branch']='CSE'
                elif brn[i[7]] == 'cvl':
                    cvl[i] = k
                    x['branch']='CIVIL'
                x['name'] = k
                entered[i] = x
    for i in m:
        for j,k in zip(list(data_all['id']),list(data_all['name'])):
            if i==j:
                x = {}
                # print(brn[i[7]])
                if brn[i[7]] == 'mech':
                    mechl[i] = k
                    x['branch'] = 'MECH'
                elif brn[i[7]] == 'eee':
                    eeel[i] = k
                    x['branch'] = 'EEE'
                elif brn[i[7]] == 'eie':
                    eiel[i] = k
                    x['branch'] = 'EIE'
                elif brn[i[7]] == 'ece':
                    ecel[i] = k
                    x['branch'] = 'ECE'
                elif brn[i[7]] == 'cse':
                    csel[i] = k
                    x['branch'] = 'CSE'
                elif brn[i[7]] == 'cvl':
                    cvll[i] = k
                    x['branch'] = 'CIVIL'
                x['name'] = k
                exited[i] = x
                # # print(brn[i[7]])
                # if brn[i[7]] =='mech': mechl[i]=k
                # elif brn[i[7]] == 'eee': eeel[i] = k
                # elif brn[i[7]] == 'eie': eiel[i] = k
                # elif brn[i[7]] == 'ece': ecel[i] = k
                # elif brn[i[7]] == 'cse': csel[i] = k
                # elif brn[i[7]] == 'cvl': cvll[i] = k


#---------------------------------QR PDF CREATOR--------------------------------------------
def create_pdf(name,id,stop,fname):
    # Generate QR code and encryption
    url = pyqrcode.create(id)
    # Create and save the png file naming "myqr.png"
    url.png('QR/myqr.png', scale=8)

    v= datetime.now()
    temp=int(str(v.year)[2:])-int(id[:2])
    year= temp if temp<=4 else "passed out"
    details={"ECE":"Electronic and Communication",
            "CSE":"Computer Science",
            "CVL":"Civil Engineering",
            "MECH":"Mechanical Engineering",
            "EEE":"Electrical and Electronics",
            "EIE":"Electrical and Instrumentation"
    }
    brn={"1":"MECH","2":"EEE","3":"EIE","4":"ECE","5":"CSE","6":"CVL"}
    x=FPDF()
    x.add_page()
    branch=brn[id[7]]

    #adding image
    x.image("QR/logo.png",3,10,w=200) #logo
    x.image("QR/{}".format(fname),145,55,w=50)

    x.image("QR/myqr.png",67,140,w=80)
    #adding text to the pdf
    #
    x.set_font('Arial',size=15)
    x.text(60,45,"VIGNAN TRANSPORT DEPARTMENT")
    x.set_font('Arial',size=12)
    x.text(30,60,"NAME")
    x.text(30,70,"ID NUMBER")
    x.text(30,80,"COURSE")
    x.text(30,90,"YEAR")
    x.text(30,100,"STOP:")
    # x.text(30,110,"ROUTE NUMBER")

    #ADD YOUR INFORMATION

    x.text(75,60,": {}".format(name))
    x.text(75,70,": {}".format(id))
    x.text(75,80,": {}".format(details[branch]))
    x.text(75,90,": {} Year".format(str(year)+"th" if year in [1,4] else str(year)+"nd" if year==2 else str(year)+"rd" if year==3 else year ))
    x.text(75,100,": {}".format(stop))
    # x.text(75,110,": {}".format(route))

    x.text(20,130,"________________________________________________________________________")
    x.text(95,135,"YOUR QR")
    x.text(20, 230, "________________________________________________________________________")
    x.text(20, 290, "Created on {}".format(v.ctime()))

    x.output("QR/output.pdf")

#-------------------------------------------------------------------------------------------
username="ece4ma4@gmail.com"
password="buspassproject"
def send_mail(name,email):
    msg=EmailMessage()
    msg['Subject']="Thank you for choosing Vignan Transport QR system"
    msg['From']=username
    msg['To']=email
    msg.set_content("Hi {},\n Hope You are Doing Good and having a good time at Vignan Institute of technology and science.\nHere is Your QR file for Travelling along with Vignan's Safe Mode of Transport for reaching your destination on Time".format(name))
    with open('QR/output.pdf', 'rb') as f:
        file_data = f.read()
        file_name = f.name
    msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(username, password)
        smtp.send_message(msg)


#-------------------------------------------------------------------------------------------
#encryption code

#--------------------------------------------------------------------------------------------
firebase=firebase.FirebaseApplication("https://buspass-b03-default-rtdb.firebaseio.com/",None)
# try:
#     result=firebase.get('https://buspass-b03-default-rtdb.firebaseio.com/student',"")
#     result=list(result.values())[-1]
#     xx,yy,drv=result['entry'],result['left'],result['driver']
# except:
#     xx, yy, drv = [],[],[]
result=firebase.get('https://buspass-b03-default-rtdb.firebaseio.com/student',"")
result=list(result.values())[-1]
# print(result)
xx,yy,drv=result['entry'],result['left'],result['driver']
# print(x)
x=0
#--------------------------------------------------------------------------------------------
app=Flask(__name__,template_folder="templete")
@app.route("/")
def mainpage():
    return render_template('index.html')
#--------------------------------------------------------------------------------------------
@app.route("/dashboard")
def dashboard():
    # x, y, drv = result['entry'], result['left'], result['driver']
    data_sorter(xx, yy)
    # try:
    return render_template('dashboard.html',results=entered,extres=exited,driver=drv)
    # except:
        # return render_template('dashboard.html')
#--------------------------------------------------------------------------------------------
@app.route("/about")
def about():
    return render_template('about.html')
#--------------------------------------------------------------------------------------------
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route("/Generate",methods=["GET","POST"])

def generate():
    global x
    if request.method == "POST":
        # req = request.form
        name = request.form.get("candidatename")
        id = request.form.get("registrationid")
        stop = request.form.get("stop")
        email=request.form.get("email")
        file = request.files["image"]
        x=0
        filename=None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            sleep(2)
        if len(name)!=0 and len(id)!=0 and len(stop)!=0 and len(email)!=0:
            x=1
            create_pdf(name,id,stop,filename)
            if request.form.get("check")=="1":
                send_mail(name,email)
            print("name:{}".format(name))
            print("id:{}".format(id))
            print("stop:{}".format(stop))

            return redirect(request.url)

    return render_template("sample.html",temp=x,me=request.form.get("check"))
#--------------------------------------------------------------------------------------------

@app.route("/department",methods=["GET","POST"])
def department():
    opt,alt,result,resultl= 0,0,{},{}
    brn = {"1": "MECH", "2": "EEE", "3": "EIE", "4": "ECE", "5": "CSE", "6": "CVL"}
    data_sorter(xx, yy)
    if request.method == "POST":
        # req = request.form
        opt = request.form.get("option")
        if opt=="SELECT YOUR DEPARTMENT":
            alt=1
        else:
            if brn[opt]=="Mech": result,resultl = mech,mechl
            if brn[opt] == "EEE": result,resultl = eee,eeel
            if brn[opt] == "ECE": result,resultl = ece,ecel
            if brn[opt] == "EIE": result,resultl = eie,eiel
            if brn[opt] == "CSE": result,resultl = cse,csel
            if brn[opt] == "CVL": result,resultl = cvl,cvll
        # print(opt)
    return render_template('deparment.html',done=alt,result=result,resultl=resultl)
#--------------------------------------------------------------------------------------------
# xx,yy,drv=result['entry'],result['left'],result['driver']


@app.route("/download")
def download_file():
    p="QR/output.pdf"
    return send_file(p,as_attachment=True)
#--------------------------------------------------------------------------------------------
# print(len(result))
app.run(debug=True)

