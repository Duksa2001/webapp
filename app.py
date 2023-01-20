from flask import Flask, render_template, url_for,request,redirect,session
import mariadb 
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import ast

#######19 jan 11:41 Radi dodavanje i brisanje pitanja


#deklaracija aplikacije
app = Flask(__name__)
app.secret_key = "tajni_kljuc_aplikacije"

#konekcija sa bazom podataka
konekcija=mysql.connector.connect(
    passwd="",
    user="root",
    database="quiz_projekat8",
    port=3306,
    auth_plugin="mysql_native_password"
)

kursor=konekcija.cursor(dictionary=True)
#globalna funkcija koja proverava da li ke korisnik ulogovan
def ulogovan():
        if "ulogovani_user" in session:
                return True
        else:
                return False

def rola():
        if ulogovan():
                return ast.literal_eval(session["ulogovani_user"]).pop("rola")
                




#logika aplikacije
@app.route('/',methods=["GET","POST"])

def render_login():
        return render_template('login.html')     

@app.route("/logout")
def logout():
       session.pop("ulogovani_user",None)
       return redirect(url_for("login"))

@app.route('/login',methods=["GET","POST"])

def login():
        
        if request.method=="GET":
                
                return render_template("login.html")

        elif request.method=="POST":
                
                forma = request.form
                upit="SELECT * FROM user WHERE ime=%s "
                vrednost = (forma["ime"],  )
                kursor.execute(upit, vrednost)
                user=kursor.fetchone()
                
                if user !=None:
                        #if user["lozinka"]==forma["lozinka"]:#za ne hash lozinke
                        if check_password_hash(user["lozinka"], forma["lozinka"]):#za hash lozinke
                                
                                session["ulogovani_user"]=str(user)
                                return redirect(url_for("render_pocetna",id=1,idp=1))
                        else:
                                        
                                        return render_template("login.html")
                else:
                        return render_template("login.html")

@app.route('/provera_odg',methods=["POST"])

def provera_odg():
        upit_provera='select tacno from quiz_question where id=%s'
        vrednost=(id,)
        print("RADIII")


@app.route('/pocetna/<id>/<idp>',methods=["GET","POST"])

def render_pocetna(id=1,idp=1):
        if ulogovan():
                
                #za prikaz kvizova
                upit="SELECT q.*, qq.* from quiz_question qq  join quiz q on q.id = qq.quiz_id order by qq.quiz_id"
                #upit="select * from quiz" 
                upit2="select * from user"
                kursor.execute(upit)
                kvizovi=kursor.fetchall()
                
                
                kursor.execute(upit2)
                korisnici=kursor.fetchall()

                #prikaz kviza sa odredjenim id
                upit6="select * from quiz where id=%s" 
                vrednost1=(id, )
                kursor.execute(upit6, vrednost1)
                kvizovi2=kursor.fetchall()
              #  print("POCETNA KVIZOVI2 :  ",kvizovi2)
               # print("\nid= {0}   idp= {1}   :   ",id,idp)

                return render_template('pocetna.html',kvizovi=kvizovi,korisnici=korisnici,kvizovi2=kvizovi2,rola=rola()) 

        else:
                return redirect(url_for("login"))

@app.route('/modifikuj/<id>/<idp>',methods=["GET","POST"])
def render_modifikuj(id=1,idp=1):
        if rola() == "admin":
                if ulogovan():
                
                        # update bazu podataka
                        if request.method=="POST":
                                
                                upit10="""update quiz_question set 
                                        tekst=%s, odg1=%s, odg2=%s, odg3=%s, odg4=%s, tacno=%s
                                        where broji=%s and quiz_id=%s
                                """
                                forma=request.form
                                vrednost=(
                                        forma["txt"],
                                        forma["odg1"],
                                        forma["odg2"],
                                        forma["odg3"],
                                        forma["odg4"],
                                        forma["sel_odg"],
                                        idp,
                                        id

                                        )
                                        
                                #print(vrednost)

                                
                                kursor.execute(upit10, vrednost)

                                #dodao zato sto ti nisi stavio da se menja ime kviza      /-milan-
                                upitImeKviz="""update quiz  
                                        set ime=%s
                                        where id=%s
                                """
                                forma=request.form
                                vrednostImeKviz=(
                                        forma["txt_kviz"],
                                        id

                                        )
                                kursor.execute(upitImeKviz, vrednostImeKviz)


                                konekcija.commit()

                                
                                #Ovo sam dodao da kada korisnik sacuva promene da ostane na tu stranu a ne da ga vraca stalno na kviz=1 pitanje=1   /-milan-
                                upit6="select * from quiz where id=%s" 
                                vrednost1=(id, )
                                kursor.execute(upit6, vrednost1)
                                kvizovi2=kursor.fetchall()
                                upit3="select * from quiz_question where broji=%s and quiz_id=%s "
                                vrednost=(idp,id )
                                kursor.execute(upit3, vrednost)
                                tekstp=kursor.fetchall()
                                
                                return redirect(url_for("render_modifikuj",id=kvizovi2[0]["id"],idp=tekstp[0]["broji"]))

                                #return render_template("modifikuj.html")
                        elif request.method=="GET":
                                #izvlacenje kvizova
                                upit="SELECT q.*, qq.* from quiz_question qq  join quiz q on q.id = qq.quiz_id order by qq.quiz_id "
                                kursor.execute(upit)
                                kvizovi=kursor.fetchall()
                                
                                #izvlacenje iz baze kviz sa odredjenim id
                                upit6="select * from quiz where id=%s" 
                                vrednost1=(id, )
                                kursor.execute(upit6, vrednost1)
                                kvizovi2=kursor.fetchall()

                                
                                
                                #prikaz korisnika
                                upit2="select * from user"
                                kursor.execute(upit2)
                                korisnici=kursor.fetchall()
                                
                        #prikaz pitanja po id
                        # dodao u upit4 >> order by broji asc  /-milan-
                                upit4="select * from quiz_question where quiz_id=%s order by broji asc"
                                vrednost=(id, )
                                kursor.execute(upit4, vrednost)
                                pitanja=kursor.fetchall()


                                #dodao sam ovo da mi kaze tacno na koji broji pitanja se nalazim i to cu posle proslediti u delete    /-milan-
                                upitBroji="select * from quiz_question where quiz_id=%s and broji=%s order by broji asc"
                                vrednostBroji=(id, idp)
                                kursor.execute(upitBroji, vrednostBroji)
                                pitanja1=kursor.fetchall()
                                
                                
                                #promenio sam u upit3  where broji=%s and quiz_id=%s i u modifikuj.html stavio sam da idp bude pitanje.broji(broj pitanja a ne indeks)

                                upit3="select * from quiz_question where broji=%s and quiz_id=%s "
                                vrednost=(idp,id )
                                kursor.execute(upit3, vrednost)
                                tekstp=kursor.fetchall()
                                #print("KVIZOVI[0].id                :           .........                  ",kvizovi2[0]['id'])
                                #print("PITANJE[0].broji                :         ...........                    ",pitanja1[0]['broji'])
                                
                                
                        konekcija.commit()
                        return render_template('modifikuj.html',kvizovi=kvizovi,korisnici=korisnici,pitanja=pitanja,tekstp=tekstp,kvizovi2=kvizovi2,pitanja1=pitanja1) 
                else:
                        return redirect(url_for("login"))
        else:
                return redirect(url_for("render_pocetna",id=1,idp=1))


@app.route("/delete/<id>/<idp>",methods=["POST"])
def delete_pitanje(id,idp):
        #brisanje odredjenog pitanja
        #umesto id=%s   >>>   broji=%s   /-milan-
        upit=""" DELETE from quiz_question where quiz_id=%s and broji=%s"""
        vrednost=(id,idp )
        kursor.execute(upit, vrednost)
        upitUpdatePitanja="UPDATE quiz_question SET broji=broji-1 WHERE broji>%s and quiz_id=%s"
        vrednostUpdatePitanja=(idp, id)
        kursor.execute(upitUpdatePitanja, vrednostUpdatePitanja)
        
        
        
        
        konekcija.commit()
        
        
        
        return redirect(url_for("render_modifikuj",id=id,idp=1))

#brisanje kviza /-milan-
@app.route("/delete_kviz/<id>",methods=["POST"])
def delete_kviz(id):
        #brisem kviz ovde /-milan-
        upitBrisiKviz=""" DELETE from quiz where id=%s"""
        vrednostBrisiKviz=(id, )
        kursor.execute(upitBrisiKviz, vrednostBrisiKviz)

        

        upitBrisiPitanja=""" DELETE from quiz_question where quiz_id=%s"""
        vrednostBrisiPitanja=(id, )
        kursor.execute(upitBrisiPitanja, vrednostBrisiPitanja)

        

        return redirect(url_for("render_modifikuj",id=1,idp=1))


#ovo sam ja pisao  /-milan-
@app.route("/novo_pitanje/<id>",methods=["GET","POST"])
def novo_pitanje(id):

        print("ULAZZI U NOVO PITANJE>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")


        #nalazi max broji pitanje(zadnje pitanje)
        upitMaxPitanja="SELECT MAX(broji) AS maks from quiz_question where quiz_id=%s"
        vrednostiMax=(id, )
        kursor.execute(upitMaxPitanja, vrednostiMax)
        brojiMax=kursor.fetchall()

        upitInsert = """INSERT INTO quiz_question( tekst, quiz_id, broji, odg1, odg2, odg3, odg4, tacno) VALUES ("", %s, %s, "", "", "", "", 1) """
        vrednostInsert=(id,brojiMax[0]["maks"]+1)
        kursor.execute(upitInsert, vrednostInsert)

        konekcija.commit()



        return redirect(url_for("render_modifikuj",id=id,idp=brojiMax[0]["maks"]+1))



#ovo sam ja pisao  /-milan-
@app.route("/novi_kviz",methods=["GET","POST"])
def novi_kviz():

        


        #nalazi max broji Kviz (zadnji kviz)
        upitMaxKviz="SELECT MAX(id) AS maks from quiz"
        kursor.execute(upitMaxKviz)
        brojiMaxKviz=kursor.fetchall()
        #upit za insertovanje kviza
        upitInsertKviz = """INSERT INTO quiz( id, ime, broj_tacnih_pitanja) VALUES (%s,"Novi Kviz %s",0) """
        vrednostInsertKviz=(brojiMaxKviz[0]["maks"]+1, brojiMaxKviz[0]["maks"]+1)
        kursor.execute(upitInsertKviz, vrednostInsertKviz)
        #upit za insertovanje prvog pitanja u novom kvizu
        upitInsert = """INSERT INTO quiz_question( tekst, quiz_id, broji, odg1, odg2, odg3, odg4, tacno) VALUES ("", %s, 1, "", "", "", "", 1) """
        vrednostInsert=(brojiMaxKviz[0]["maks"]+1, )
        kursor.execute(upitInsert, vrednostInsert)

        konekcija.commit()



        return redirect(url_for("render_modifikuj", id=brojiMaxKviz[0]["maks"]+1,idp=1))





@app.route('/kviz/<id>/<idp>',methods=["GET","POST"])

def render_kviz(id,idp):
        if ulogovan():
                if request.method=="GET":
                        #dodao sam i ovo
                        upitMaxPitanja="SELECT MAX(broji) AS maks, q.*, qq.* from quiz_question qq  join quiz q on q.id = qq.quiz_id where qq.quiz_id=%s"
                        vrednost=(id, )
                        kursor.execute(upitMaxPitanja,vrednost)
                        kvizMaxPitanja=kursor.fetchall()
                        #print("Maxxxxxxxxxxxxx:   ",kvizMaxPitanja)
                        
                        upit6="select * from quiz where id=%s" 
                        vrednost1=(id, )
                        kursor.execute(upit6, vrednost1)
                        kvizovi2=kursor.fetchall()

                        upit="SELECT q.*, qq.* from quiz_question qq  join quiz q on q.id = qq.quiz_id where qq.quiz_id=%s and qq.broji=%s order by qq.id"
                        vrednost2=(id, idp)
                        kursor.execute(upit,vrednost2)
                        kvizovi=kursor.fetchall()

                        upit3="select * from quiz_question where broji=%s and quiz_id=%s "
                        vrednost=(idp, id)
                        kursor.execute(upit3, vrednost)
                        tekstp=kursor.fetchall()

                        upit2="select * from user"
                        kursor.execute(upit2)
                        korisnici=kursor.fetchall()
                        #print("KVIZOVI : {0}",kvizovi)
                        if(int(idp)<=int(kvizMaxPitanja[0]["maks"])):
                                return render_template('kviz.html',kvizovi2=kvizovi2,kvizovi=kvizovi,tekstp=tekstp,kvizMaxPitanja=kvizMaxPitanja,korisnici=korisnici)
                        else:
                                return redirect(url_for("render_pocetna",id=1,idp=1))
                elif request.method=="POST":
                        #krenuo sam da radim: da kada se pritisne dugme vrati vrednost ali ne radi kako treba pa sam vratio izgled kviz.htm kakv je i bio
                        print("Ulazi u post")
                        upit3="select tacno from quiz_question where broji=%s and quiz_id=%s "
                        vrednost=(idp, id)
                        kursor.execute(upit3, vrednost)
                        tekstp=kursor.fetchall()
                        print(tekstp)
                        
                        
                        forma=request.form
                        vrednostforma=(forma["dugme"], )
        
                        print(vrednostforma)
                        
                        

                        
                        if str(tekstp[0]["tacno"]) in vrednostforma:
                     
                                print("tacno")

                        
                                return redirect(url_for("render_kviz",id=1,idp=1))
                        return redirect(url_for("login"))
        else: 
                return redirect(url_for("login"))






@app.route("/user_novi",methods=["GET","POST"])#za registraciju novih korisnika
def user_novi():
        if request.method=="GET":
                return render_template("pocetna.html")

        elif request.method=="POST":
                forma=request.form
                hesovana_lozinka=generate_password_hash(forma["lozinka"])#generise hash lozinku
                vrednosti=(
                        forma["ime"],
                        forma["prezime"],
                        hesovana_lozinka,
                       # forma["lozinka"],
                )
                upit=""" INSERT INTO
                        user(ime,prezime,lozinka)
                        VALUES(%s,%s,%s)        
                """
                #unosi vrednosti u bazu
                kursor.execute(upit, vrednosti)
                konekcija.commit()
                return redirect(url_for("render_pocetna",id=1,idp=1))
#pokretanje aplikacije
app.run(debug=True)