from flask import Flask, render_template, url_for,request,redirect,session
import mariadb 
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import ast



#deklaracija aplikacije
app = Flask(__name__)
app.secret_key = "tajni_kljuc_aplikacije"

#konekcija sa bazom podataka
konekcija=mysql.connector.connect(
    passwd="",
    user="root",
    database="quiz_projekat",
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

#Ova funkcija za role
def rola():
        if ulogovan():
                return ast.literal_eval(session["rola_user"]).pop("rola")


                



#logika aplikacije
@app.route('/',methods=["GET","POST"])

def render_login():
        return render_template('login.html')     

@app.route("/logout")
def logout():
       session["ulogovani_user"]=None
       return redirect(url_for("login"))

@app.route('/login',methods=["GET","POST"])

def login():
        
        if request.method=="GET":
                
                return render_template("login.html")

        elif request.method=="POST":
                
                forma = request.form
                upit="SELECT * FROM user WHERE ime=%s"
                vrednost = (forma["ime"],)
                kursor.execute(upit, vrednost)
                user=kursor.fetchone()
                
                if user !=None:
                        #if user["lozinka"]==forma["lozinka"]:#za ne hash lozinke
                        if check_password_hash(user["lozinka"], forma["lozinka"]):#za hash lozinke
                        
                                session["ulogovani_user"]=user["id"]
                                session["rola_user"]=str(user)                                     
                                return redirect(url_for("render_pocetna",id=1,idp=1))
                        else:
                                        
                                        return render_template("login.html")
                else:
                        return render_template("login.html")

@app.route('/pocetna/<id>/<idp>',methods=["GET","POST"])

def render_pocetna(id=1,idp=1):
        if ulogovan():
                
                #za prikaz kvizova
                upit="SELECT q.*, qq.* from quiz_question qq  join quiz q on q.id = qq.quiz_id order by qq.quiz_id"
                
                upit2="select * from user order by score DESC"
                kursor.execute(upit)
                kvizovi=kursor.fetchall()
                
                
                kursor.execute(upit2)
                korisnici=kursor.fetchall()

                #prikaz kviza sa odredjenim id
                upit6="select * from quiz where id=%s" 
                vrednost1=(id, )
                kursor.execute(upit6, vrednost1)
                kvizovi2=kursor.fetchall()
        
                upitBrTacnihPitanja="select broj_tacnih_pitanja from quiz_user where quiz_id=%s and user_id=%s"
                vrednostiBrTacnihPitanja=(id,session.get("ulogovani_user"))
                kursor.execute(upitBrTacnihPitanja, vrednostiBrTacnihPitanja)
                BrTacnihPitanja=kursor.fetchall()

                #Maks Br Pitanja
                upitMaxPitanja="SELECT MAX(broji) AS maks from quiz_question where quiz_id=%s"
                vrednostiMax=(id, )
                kursor.execute(upitMaxPitanja, vrednostiMax)
                brojiMax=kursor.fetchall()



                return render_template('pocetna.html',kvizovi=kvizovi,korisnici=korisnici,kvizovi2=kvizovi2,BrTacnihPitanja=BrTacnihPitanja,brojiMax=brojiMax,rola=rola()) 

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

                                
                                #kada korisnik sacuva promene da ostane na tu stranu a ne da ga vraca stalno na kviz=1 pitanje=1  
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
                                upit2="select * from user order by score DESC"
                                kursor.execute(upit2)
                                korisnici=kursor.fetchall()
                                
                        
                                upit4="select * from quiz_question where quiz_id=%s order by broji asc"
                                vrednost=(id, )
                                kursor.execute(upit4, vrednost)
                                pitanja=kursor.fetchall()


                                #kaze tacno na koji broji pitanja se nalazim i to cu posle proslediti u delete  
                                upitBroji="select * from quiz_question where quiz_id=%s and broji=%s order by broji asc"
                                vrednostBroji=(id, idp)
                                kursor.execute(upitBroji, vrednostBroji)
                                pitanja1=kursor.fetchall()
                                
                                
                                

                                upit3="select * from quiz_question where broji=%s and quiz_id=%s "
                                vrednost=(idp,id )
                                kursor.execute(upit3, vrednost)
                                tekstp=kursor.fetchall()
                                
                                
                                
                        konekcija.commit()
                        return render_template('modifikuj.html',kvizovi=kvizovi,korisnici=korisnici,pitanja=pitanja,tekstp=tekstp,kvizovi2=kvizovi2,pitanja1=pitanja1) 
                else:
                        return redirect(url_for("login"))
        else:
                return redirect(url_for("render_pocetna",id=1,idp=1))

@app.route("/deluser/<id>",methods=["POST"])

def deluser(id):
                
                if ulogovan():
                        upitUserRolaProvera="select rola from user where id=%s"
                        vrednostUserRolaProvera=(id, )
                        kursor.execute(upitUserRolaProvera, vrednostUserRolaProvera)
                        UserRolaProvera=kursor.fetchall()
                        if(UserRolaProvera[0]["rola"]=="admin"):
                                return redirect(url_for("render_modifikuj",id=1,idp=1))
                        else:
                                upit="DELETE FROM user WHERE id=%s"
                                vrednost=(id, )
                                kursor.execute(upit,vrednost)

                                return redirect(url_for("render_modifikuj",id=1,idp=1))
                else:
                        return redirect(url_for("login"))

@app.route("/delete/<id>/<idp>",methods=["POST"])
def delete_pitanje(id,idp):
        if ulogovan():
                #brisanje odredjenog pitanja
               
                upit=""" DELETE from quiz_question where quiz_id=%s and broji=%s"""
                vrednost=(id,idp )
                kursor.execute(upit, vrednost)
                upitUpdatePitanja="UPDATE quiz_question SET broji=broji-1 WHERE broji>%s and quiz_id=%s"
                vrednostUpdatePitanja=(idp, id)
                kursor.execute(upitUpdatePitanja, vrednostUpdatePitanja)

                #update score  kada se brise pitanje
                upitUserID="select id from user"
                kursor.execute(upitUserID)
                userID=kursor.fetchall()
                for UserIDbrojac in userID:
                        upitUpdateScore="UPDATE user SET score=0 WHERE  id=%s"
                        vrednostUpdateScore=(UserIDbrojac["id"], )
                        kursor.execute(upitUpdateScore, vrednostUpdateScore)

                #update broj tacnih pitanja 
                upitUserID="select id from user"
                kursor.execute(upitUserID)
                userID=kursor.fetchall()
                for UserIDbrojac in userID:
                        upitUpdateScore="UPDATE quiz_user SET broj_tacnih_pitanja=0 WHERE user_id=%s"
                        vrednostUpdateScore=(UserIDbrojac["id"], )
                        kursor.execute(upitUpdateScore, vrednostUpdateScore)
                upitProveraPitanja="select COUNT(id) AS brPitanja FROM quiz_question where quiz_id=%s"
                vrednostProveraPitanja=(id, )
                kursor.execute(upitProveraPitanja, vrednostProveraPitanja)
                ProveraPitanja=kursor.fetchall()

                
                
                konekcija.commit()
                
                if(ProveraPitanja[0]["brPitanja"]==0):
                        return redirect(url_for("delete_kviz",id=id))
                        
                        
                
                return redirect(url_for("render_modifikuj",id=1,idp=1))
        else:
                return redirect(url_for("login"))

#brisanje kviza 
@app.route("/delete_kviz/<id>",methods=["GET","POST"])
def delete_kviz(id):
        if ulogovan():
                #brisem kviz ovde 
                upitBrisiKviz=""" DELETE from quiz where id=%s"""
                vrednostBrisiKviz=(id, )
                kursor.execute(upitBrisiKviz, vrednostBrisiKviz)


                
                upitDELETEPrviPutIgraTajKviz="DELETE FROM quiz_user WHERE quiz_id=%s"
                VrednostDELETEPrviPutIgraTajKviz=(id, )
                kursor.execute(upitDELETEPrviPutIgraTajKviz, VrednostDELETEPrviPutIgraTajKviz)
                

                upitBrisiPitanja=""" DELETE from quiz_question where quiz_id=%s"""
                vrednostBrisiPitanja=(id, )
                kursor.execute(upitBrisiPitanja, vrednostBrisiPitanja)

                #update score na 0 kada se brise pitanje
                upitUserID="select id from user"
                kursor.execute(upitUserID)
                userID=kursor.fetchall()
                for UserIDbrojac in userID:
                        upitUpdateScore="UPDATE user SET score=0 WHERE id=%s"
                        vrednostUpdateScore=(UserIDbrojac["id"],)
                        kursor.execute(upitUpdateScore, vrednostUpdateScore)

                #update broj tacnih pitanja na 0 
                upitUserID="select id from user"
                kursor.execute(upitUserID)
                userID=kursor.fetchall()
                for UserIDbrojac in userID:
                        upitUpdateScore="UPDATE quiz_user SET broj_tacnih_pitanja=0 WHERE user_id=%s"
                        vrednostUpdateScore=(UserIDbrojac["id"], )
                        kursor.execute(upitUpdateScore, vrednostUpdateScore)

                upitUpdateKviz="UPDATE quiz SET id=id-1 WHERE id>%s"
                vrednostUpdateKviz=(id, )
                kursor.execute(upitUpdateKviz, vrednostUpdateKviz)
                
                upitProveraKviz="select COUNT(id) AS brKviz FROM quiz"
                kursor.execute(upitProveraKviz)
                ProveraKviz=kursor.fetchall()
                
                konekcija.commit()
                if(int(ProveraKviz[0]["brKviz"])!=0):
                        return redirect(url_for("render_modifikuj",id=1,idp=1))
                else:
                        return redirect(url_for("novi_kviz"))
        else:
                return redirect(url_for("login"))


@app.route("/novo_pitanje/<id>",methods=["GET","POST"])
def novo_pitanje(id):
        if ulogovan():

                


                #nalazi max broji pitanje(zadnje pitanje)
                upitMaxPitanja="SELECT MAX(broji) AS maks from quiz_question where quiz_id=%s"
                vrednostiMax=(id, )
                kursor.execute(upitMaxPitanja, vrednostiMax)
                brojiMax=kursor.fetchall()

                upitInsert = """INSERT INTO quiz_question( tekst, quiz_id, broji, odg1, odg2, odg3, odg4, tacno) VALUES ("", %s, %s, "", "", "", "", 1) """
                vrednostInsert=(id,brojiMax[0]["maks"]+1)
                kursor.execute(upitInsert, vrednostInsert)

                #update score na 0 
                upitUserID="select id from user"
                kursor.execute(upitUserID)
                userID=kursor.fetchall()
                for UserIDbrojac in userID:
                        upitUpdateScore="UPDATE user SET score=0 WHERE  id=%s"
                        vrednostUpdateScore=(UserIDbrojac["id"],)
                        kursor.execute(upitUpdateScore, vrednostUpdateScore)


                #update broj tacnih pitanja na 0 
                upitUserID="select id from user"
                kursor.execute(upitUserID)
                userID=kursor.fetchall()
                for UserIDbrojac in userID:
                        upitUpdateScore="UPDATE quiz_user SET broj_tacnih_pitanja=0 WHERE  user_id=%s"
                        vrednostUpdateScore=(UserIDbrojac["id"],)
                        kursor.execute(upitUpdateScore, vrednostUpdateScore)
                
                
                
                
                

                konekcija.commit()



                return redirect(url_for("render_modifikuj",id=id,idp=brojiMax[0]["maks"]+1))
        else:
                return redirect(url_for("login"))



@app.route("/novi_kviz",methods=["GET","POST"])
def novi_kviz():

        if ulogovan():


                #nalazi max broji Kviz (zadnji kviz)
                upitProveraKviz="select COUNT(id) AS brKviz FROM quiz"
                kursor.execute(upitProveraKviz)
                ProveraKviz=kursor.fetchall()
                
                upitMaxKviz="SELECT MAX(id) AS maks from quiz"
                kursor.execute(upitMaxKviz)
                brojiMaxKviz=kursor.fetchall()
                #upit za insertovanje kviza
                upitInsertKviz = """INSERT INTO quiz( id, ime) VALUES (%s,"Novi Kviz %s") """
                vrednostInsertKviz=(ProveraKviz[0]["brKviz"]+1, ProveraKviz[0]["brKviz"]+1)
                kursor.execute(upitInsertKviz, vrednostInsertKviz)
                #upit za insertovanje prvog pitanja u novom kvizu
                upitInsert = """INSERT INTO quiz_question( tekst, quiz_id, broji, odg1, odg2, odg3, odg4, tacno) VALUES ("", %s, 1, "", "", "", "", 1) """
                vrednostInsert=(ProveraKviz[0]["brKviz"]+1, )
                kursor.execute(upitInsert, vrednostInsert)

                #insetrujem u tabeli quiz_user cim se kreira novi kviz   
                upitUserID="select id from user"
                kursor.execute(upitUserID)
                userID=kursor.fetchall()
                upitInsertPrviPutIgraTajKviz="INSERT INTO quiz_user (user_id, quiz_id, broj_tacnih_pitanja) VALUES (%s, %s, %s)"
                for BrojacUserID in userID:
                        VrednostInsertPrviPutIgraTajKviz=(BrojacUserID["id"],ProveraKviz[0]["brKviz"]+1,0)
                        kursor.execute(upitInsertPrviPutIgraTajKviz, VrednostInsertPrviPutIgraTajKviz)


                #update score na 0 
                upitUserID="select id from user"
                kursor.execute(upitUserID)
                userID=kursor.fetchall()
                for UserIDbrojac in userID:
                        upitUpdateScore="UPDATE user SET score=0 WHERE id=%s"
                        vrednostUpdateScore=(UserIDbrojac["id"],)
                        kursor.execute(upitUpdateScore, vrednostUpdateScore)


                #update broj tacnih pitanja na 0 
                upitUserID="select id from user"
                kursor.execute(upitUserID)
                userID=kursor.fetchall()
                for UserIDbrojac in userID:
                        upitUpdateScore="UPDATE quiz_user SET broj_tacnih_pitanja=0 WHERE user_id=%s"
                        vrednostUpdateScore=(UserIDbrojac["id"], )
                        kursor.execute(upitUpdateScore, vrednostUpdateScore)

                konekcija.commit()



                return redirect(url_for("render_modifikuj", id=ProveraKviz[0]["brKviz"]+1,idp=1))

        else:
                return redirect(url_for("login"))



@app.route('/kviz/<id>/<idp>/<IzborPitanja>',methods=["GET","POST"])

def render_kviz(id,idp,IzborPitanja):
        if ulogovan():


                
                upitMaxPitanja="SELECT MAX(broji) AS maks, q.*, qq.* from quiz_question qq  join quiz q on q.id = qq.quiz_id where qq.quiz_id=%s"
                vrednost=(id, )
                kursor.execute(upitMaxPitanja,vrednost)
                kvizMaxPitanja=kursor.fetchall()
               
                
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

                upit2="select * from user order by score DESC"
                kursor.execute(upit2)
                korisnici=kursor.fetchall()


                # RACUNANJE TACNIH PITANJA    
                #OVO MI TRAZI TACAN ODGOVOR NEKOG PITANJA
                upitTacanOdgovor="select tacno from quiz_question where quiz_id=%s and broji=%s"
                vrednostTacanOdgovor=(id,str(int(idp)-1))
                kursor.execute(upitTacanOdgovor, vrednostTacanOdgovor)
                TacnoOdgovor=kursor.fetchall()
                #OVDE MI KAZE KOLIKO TACNIH PITANJA IMA KORISNIK IZ NEKOG KVIZA   
                upitBrojiTacnihOdgovora="select broj_tacnih_pitanja from quiz_user where quiz_id=%s and user_id=%s"
                vrednostBrojiTacnihOdgovora=(id, session.get("ulogovani_user"))
                kursor.execute(upitBrojiTacnihOdgovora, vrednostBrojiTacnihOdgovora)
                BrojiTacnihOdgovora=kursor.fetchall()
               

                

                #OVO NAM DAJE SCORE KORISNIKA
                upitScore="select score from user where id=%s"
                VrednostScore=(session.get("ulogovani_user"), )
                kursor.execute(upitScore, VrednostScore)
                Score=kursor.fetchall()





                
                if(int(IzborPitanja)==0):
                        global GlobalnaBrTacOdg
                        GlobalnaBrTacOdg=0
                        idp=str(int(idp)+1)
                        return render_template('kviz.html',kvizovi2=kvizovi2,kvizovi=kvizovi,tekstp=tekstp,kvizMaxPitanja=kvizMaxPitanja,korisnici=korisnici,TacnoOdgovor=TacnoOdgovor)
                elif(TacnoOdgovor[0]["tacno"]==int(IzborPitanja)):
                        GlobalnaBrTacOdg=GlobalnaBrTacOdg+1

                

                        



                
                if(int(idp)<=int(kvizMaxPitanja[0]["maks"])):
                        
                        idp=str(int(idp)+1)
                        return render_template('kviz.html',kvizovi2=kvizovi2,kvizovi=kvizovi,tekstp=tekstp,kvizMaxPitanja=kvizMaxPitanja,korisnici=korisnici,TacnoOdgovor=TacnoOdgovor)

        #DA LI KORISNIK PRVI PUT IGRA NEKI KVIZ

                elif(BrojiTacnihOdgovora[0]["broj_tacnih_pitanja"]==0):
                        
                        
                        
                        upitInsertPrviPutIgraTajKviz="UPDATE quiz_user SET broj_tacnih_pitanja=broj_tacnih_pitanja+%s WHERE quiz_id=%s and user_id=%s"
                        VrednostInsertPrviPutIgraTajKviz=(GlobalnaBrTacOdg,id,session.get("ulogovani_user"))
                        kursor.execute(upitInsertPrviPutIgraTajKviz, VrednostInsertPrviPutIgraTajKviz)
                        #konekcija.commit()
                        
                        #Ako korisnik igra prvi put samo mu se dodaje rezultat na score   
                        upitDodajScoreNov="UPDATE user SET score=score+%s WHERE id=%s"
                        vrednostDodajScoreNov=(GlobalnaBrTacOdg, session.get("ulogovani_user"))
                        kursor.execute(upitDodajScoreNov, vrednostDodajScoreNov)

                        konekcija.commit()

                        GlobalnaBrTacOdg=0
                        
                        return redirect(url_for("render_pocetna",id=id,idp=1))

                

                #ako korisnik dobije veci skor nego sto je imao(ili prvi put igra) sacuvaj rezultat ako ne onda rezultat se ne menja
                elif(BrojiTacnihOdgovora[0]["broj_tacnih_pitanja"]<GlobalnaBrTacOdg):


                        


                        upitUPDATEBrojiTacnihOdgovora="UPDATE quiz_user SET broj_tacnih_pitanja=%s WHERE quiz_id=%s and user_id=%s"
                        vrednostUPDATEBrojiTacnihOdgovora=(GlobalnaBrTacOdg, id,session.get("ulogovani_user"))
                        kursor.execute(upitUPDATEBrojiTacnihOdgovora, vrednostUPDATEBrojiTacnihOdgovora)
                        print("BROJ TAC ODG     grana 2 prvo    :  ",BrojiTacnihOdgovora)
                        #konekcija.commit()


                        #Ako korisnik dobije veci rezultat nego sto je imao na nekom kvizu onda score se dodaje ovako
                        upitDodajScore="UPDATE user SET score=score+%s-%s WHERE id=%s"
                        vrednostDodajScore=(GlobalnaBrTacOdg,BrojiTacnihOdgovora[0]["broj_tacnih_pitanja"], session.get("ulogovani_user"))
                        kursor.execute(upitDodajScore, vrednostDodajScore)

                        konekcija.commit()

                        print("GLOBALNA i IZABRAN ODGOVOR i TACAN ODGOVOR   :   ",GlobalnaBrTacOdg,IzborPitanja,TacnoOdgovor[0]["tacno"])
                        print("BROJ TAC ODG     grana 2  drugo    :  ",BrojiTacnihOdgovora)
                        print("KORISNIK:          ",session.get("ulogovani_user"))
                        

                        

                        GlobalnaBrTacOdg=0
                        return redirect(url_for("render_pocetna",id=id,idp=1))
                else:
                        return redirect(url_for("render_pocetna",id=id,idp=1)) 

        else:
                return redirect(url_for("login"))




@app.route("/user_novi",methods=["GET","POST"])#za registraciju novih korisnika
def user_novi():
        if ulogovan():
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
                        
                        upitUserID="select id from user where ime=%s and prezime=%s and lozinka=%s"
                        kursor.execute(upitUserID,vrednosti)
                        userID=kursor.fetchall()
                        upitKviz="select id from quiz"
                        kursor.execute(upitKviz)
                        KvizID=kursor.fetchall()

                        upitInsertPrviPutIgraTajKviz="INSERT INTO quiz_user (user_id, quiz_id, broj_tacnih_pitanja) VALUES (%s, %s, %s)"
                        for BrojacKviz in KvizID:
                                VrednostInsertPrviPutIgraTajKviz=(userID[0]["id"],BrojacKviz["id"],0)
                                kursor.execute(upitInsertPrviPutIgraTajKviz, VrednostInsertPrviPutIgraTajKviz)

                        konekcija.commit()



                        
                        return redirect(url_for("login"))
                else:
                        return redirect(url_for("login"))
#pokretanje aplikacije
app.run(debug=True)