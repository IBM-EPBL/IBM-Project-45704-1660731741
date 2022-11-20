import smtplib


from flask import *
from flask import Flask

import ibm_db

#===========================================  DB connection ========================================================

collection1 = database['login_datas']
collection2 = database['admin_datas']
collection3 = database['feedbacks']

conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=815fa4db-dc03-4c70-869a-a9cc13f33084.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=30367;Security=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=gtc10732;PWD=LywvRmoeKugENzKr","","")
EMAIL=''
#=========================================== initiating flask application ==============================================

app = Flask(__name__, template_folder='template',static_folder='assets')

# ========================================== welcome page ========================================================================

@app.route('/')
def welcome():
    return render_template('a1.html')

# =========================================== register page ======================================================================

@app.route('/applications/template/register.html', methods=('POST', 'GET'))
def open():
    if request.method == 'POST':
        count = 0
        id_no = 0
        password = ""
        name = request.form['uname']
        email = request.form['mail']
        create_password = request.form['password1']
        confirm_password = request.form['password2']
        if create_password != confirm_password:
            pass
        else:
            password = create_password
        list1 = list()
        list2 = list()
        list3 = list()
        query = collection1.find()
        for x in query:
            list1.append(x["Name"])
            list2.append(x["_id"])
        for x in list1:
            if name == x:
                count = count + 1
            else:
                count = count + 0
        for x in list2:
            if id_no == x:
                id_no = id_no + 1
        if count != 0:
            return "invalid name!"
        if count == 0 and create_password == confirm_password:
            collection1.insert_one({"_id": id_no,"Name": name,"E-Mail":email, "Password": password})
            name = request.form['uname']
            email = request.form['mail']
            EMAIL=email
            create_password = request.form['password1']
            confirm_password = request.form['password2']
            if create_password != confirm_password:
                pass
            else:
                password = create_password
                sql="INSERT INTO USER_DATA(NAME,EMAIL,PASSWORD) VALUES(?,?,?)"
                stmt=ibm_db.prepare(conn,sql)
                ibm_db.bind_param(stmt,1,name)
                ibm_db.bind_param(stmt,2,email)
                ibm_db.bind_param(stmt,3,password)
                ibm_db.execute(stmt)


            #-------------------------------------------------------------------------------------
            message = "Registration successful! \n User name : {} \n Password : {}".format(name,password)
            server = smtplib.SMTP('smtp.gmail.com',587)
            server.starttls()
            server.login('smartfashion428@gmail.com','nylhadslnclozzxe')
            server.sendmail('smartfashion428@gmail.com',email,message)
            #-------------------------------------------------------------------------------------
            return redirect(url_for('login'))
            
        if count==0 and create_password != confirm_password:
            return render_template('inv_pass.html')
    return render_template('register.html')

# ============================================== login page ========================================================================

@app.route('/applications/template/login.html', methods=('POST', 'GET'))
def login():
    global id_no
    if request.method == 'POST':
        name = request.form['uname']
        password = request.form['password']
        id_no = 0
        count1 = 0
        count2 = 0
        count3 = 0
        query = collection1.find()
        list1 = list()
        list2 = list()
        list3 = list()  
        list4 = list()
        for x in query:
            list1.append(x["Name"])
            list2.append(x['Password'])
            list3.append(x['_id'])
        for x in range(1, len(list1)):
            if list1[x] == name and list2[x] == password:
                count1 = count1 + 1
                count2 = count2 + 1
                id_no = list3[x]  
        query1 = collection2.find()
        for x in query1:
            list4.append(x['_id'])
        for x in list4:
            if x == id_no:
                count3 = count3 +1 
        if count1 == 1 and count2 == 1 and count3 == 0:
            return redirect(url_for('home'))
        if count1 != 1 and count2 != 1:
            return redirect(url_for('home'))
        
    return render_template('login.html')

'''  global EMAIL
    if request.method=='POST':
        email=request.form['email']
        EMAIL=email
        password=request.form['password']
        sql="SELECT * FROM USER_DATA WHERE email=? AND password=?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account=ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login.html'))
    return render_template('login.html')'''
    
# =========================================== pre-infos =============================================================
@app.route('/applications/template/index.html')
def home():
    return render_template('index.html')
#=============================================== infos ================================================================
@app.route('/applications/template/admin_login.html',methods = ('POST','GET'))
def admin():
    if request.method == 'POST':
        email = request.form['mail']
        password = request.form['password']
        query = collection2.find()
        list1 = list()
        list2 = list()
        for x in query:
            list1.append(x['E-Mail'])
            list2.append(x['Password'])
        for x in range(len(list1)):
            if list1[x] == email and list2[x] == password:
                return redirect(url_for('dashboard'))
            else:
                return render_template('inv_name_pass_admin.html')
    return render_template('admin_login.html')

#=========================================== dashboard ===========================================================

@app.route('/applications/template/dashboard.html')
def dashboard():
    return render_template('dashboard.html')

#============================================== feed back ======================================================
@app.route('/applications/template/FeedBack.html',methods=('POST','GET'))
def feedback():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        collection3.insert_one({"Name":name,"E-Mail":email,"Message":message})
        #===================================================================================================
        message = "Feed Back from {}! \n E-Mail : {} \n Message : {}".format(name,email,message)
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login('smartfashion428@gmail.com','nylhadslnclozzxe')
        server.sendmail('smartfashion428@gmail.com','prasannajose6@gmail.com',message)
        return redirect(url_for('home'))
        #===================================================================================================
    return render_template('FeedBack.html')

#=============================================================================================================



#===================================== app run part =====================================================================

if __name__ == "__main__":
    app.run(debug=True)

#===================================== nandri vanakkam ===============================================================