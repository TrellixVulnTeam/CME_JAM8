import errno
import reportlab 
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import CMYKColor, yellow, red, black,white
from reportlab.graphics.shapes import Rect
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

import time

import email
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

import smtplib
from smtplib import SMTP
from email import encoders

from kivy.storage.jsonstore import JsonStore

import webbrowser
import subprocess
import pathlib
import os
import shutil


class Home(Screen):
    pass


class Add_club(Screen):

    def __init__(self, **kargs):
        super(Add_club,self).__init__() 
        
        self.dicc_json = JsonStore('club_d.json')

        ## A PARTIR DEL FITXER CREAREM UN DICCIONARI (MES COMODE DE JUGAR)
        self.dicc = {}
        
        # PASS VALUES FROM FILE TO DICTIONARY
        for key in self.dicc_json:
        # 1r. Guardem a club i name els valors
        # 2n. Ho posem en un diccionari local

            club = self.dicc_json.get(key)["Club"] # obté el nom del club del fitxer json 
            mail= self.dicc_json.get(key)["Mail"]
            
            self.dicc.update({club : mail})

        self.club_names = list(self.dicc.keys())
        self.club_mail = list(self.dicc.values()) 
        
        # self.club_mail_dicc = {'5 COPES' : '5copes@gmail.com', 'CYG' : 'cygsalud@hotmail.com', 'ALBERT' : 'albert.cambras@estudiantat.upc.edu', 'DanielGras':'adelaros7@gmail.com'}

    def add(self,club,mail):
        # self.club_mail_dicc.update(a)
        
        # afegeix al fitxer
        self.dicc_json.put(club, Club = club , Mail=mail)

        # SELF.CLUB_MAIL_DICC.UPDATE()=file.readLINES...
    
    def update(self,club,mail):
        # actualitzo fitxer de mails
        self.dicc_json.put(club,Club=club,Mail=mail)
        
    def delete(self,c):
        pass
        #self.club_mail_dicc.pop(c)
    

    
class Maker(Screen):
    def __init__(self, **kargs):
        super(Maker,self).__init__() 
        self.name_file = ""
        self.prev= 0
        self.reenv = 0
   
    def rename_file(self):
        
        name = self.ids.name.text
        nif = self.ids.nif.text

        # problems with whitespaces (Albert Cambras)
        # so i rename without spaces 
        name_string = name.split(' ')

        name_fitx = ""

        for i in name_string:
            name_fitx = name_fitx +  i # join words 
        
        self.name_file = name_fitx

    def create_dir(self):

        dir_name = self.ids.club.text

        # function os.mkdir give an error if the dir already exists. To fix it we do that:
        try:
        
            os.mkdir(dir_name)
        
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    def move_pdf(self):

        src_path = os.path.join(os.getcwd(), self.name_file+'.pdf') # current directory + name_fitx 
        dst_path = os.path.join(os.getcwd(), self.ids.club.text, self.name_file+'.pdf')

        shutil.move(src_path,dst_path)
      
    def save_file(self):
            
            # create a dir to save pdf
            # the dir will have club name
            self.create_dir() 
 
            if self.prev != 1: #if we'd press previa --> we will not have to save or move
                
                self.CME()

                # when we save pdf it saves in any folder --> we move to club folder
                self.move_pdf()

    def visualize(self):
        
        
        if self.name_file == "":
            self.rename_file()
            self.save_file()
            path = os.path.join(os.getcwd(), self.ids.club.text, self.name_file+'.pdf') # current directory + name_fitx 

        else:
            path = os.path.join(os.getcwd(), self.ids.club.text, self.name_file+'.pdf') # current directory + name_fitx 
        
        self.prev= 1 # if we press previa and not save --> we will not save again the file
        webbrowser.open_new(path)

    def e_mail(self):
        
        if self.ids.mail.text != "ERROR 101":
                            

            ## file is on club/name_file
            dir_fitx = os.path.join(os.getcwd(), self.ids.club.text, self.name_file) # current directory + name_fitx 

            org="cygvigilanciasalud@gmail.com"

            d_class = Add_club()

            dst = d_class.dicc.get(self.ids.club.text)
            ## message to club ( asunto will say: club cme albert.pdf ) 
            msg= MIMEMultipart()
            msg["From"]=org
            msg["To"]=dst

            msg["subject"]= "CME "+ self.name_file
            body="Aquí lo tienes"
            
            msg.attach(MIMEText(body,'plain'))
            

            adjunto=open(dir_fitx+".pdf",'rb')

            adjunto_MIME= MIMEBase('application','octet-stream') 
            adjunto_MIME.set_payload((adjunto).read())

            encoders.encode_base64(adjunto_MIME)

            adjunto_MIME.add_header('Content-Disposition','attachment; filename="CME.pdf"')
            
            msg.attach(adjunto_MIME)

            smtp= SMTP("smtp.gmail.com")
            smtp.starttls()
            smtp.login(org,"Elvipere1960")
            smtp.sendmail(org,dst,msg.as_string())
            smtp.quit()
 
    def CME(self):

        if self.name_file == "":
            self.rename_file()
            name_fitx = self.name_file
        else:
            name_fitx = self.name_file
        
        name = self.ids.name.text
        nif = self.ids.nif.text
        cme  = canvas.Canvas(name_fitx +'.pdf', pagesize=A4)
        width, height = A4 # keep for later

        ##########################################
        title = cme.beginText()
        title.setTextOrigin(inch, 10.5*inch)
        title.setFont("Helvetica", 14)

        sub = cme.beginText()
        sub.setTextOrigin(inch, 10.5*inch)
        sub.setFont("Helvetica", 10)

        sub2 = cme.beginText()
        sub2.setTextOrigin(inch, 10.5*inch)
        sub2.setFont("Helvetica", 12)

        sub3 = cme.beginText()
        sub3.setFont("Helvetica", 10)

        sub4 = cme.beginText()
        sub4.setFont("Helvetica", 12)




        ##########################################

        ##  TITLE
        title.setXPos(1.75*inch)
        title.textLines("CERTIFICAT MÈDIC ESPORTIU")
        cme.drawText(title)

        sub.textLines("")
        sub.textLines("")

        ## SUB
        
        cme.drawImage("GEN_CAT.jpg", inch,9.9*inch ,width=inch/4,height=inch/4,preserveAspectRatio=True)

        sub.setXPos(inch/3)
        sub.textLines("Generalitat de Catalunya")
        sub.textLines("Departament de Salut")
        cme.drawText(sub)

        sub2.textLines("")
        sub2.textLines("")
        sub2.textLines("")
        sub2.textLines("")
        sub2.textLines("")
        sub2.textLines("")

        # SUB2
        sub2.textLines("Certificat Mèdic Esportiu (CME)")
        (x,y)=sub2.getCursor()
        cme.line(x,y+0.1*inch,7.5*inch,y+0.1*inch)

        sub2.textLines("")
        sub2.textLines("")


        ## DADES ESPORTISTA

        sub2.textLines("Dades de l'esportista")
        (x,y)=sub2.getCursor()
        cme.line(x,y+0.1*inch,7.5*inch,y+0.1*inch)

        sub2.textLines("")
        sub2.textLines("")
        sub2.textLines("Nom i cognoms                                                              NIF")

        (x,y)=sub2.getCursor()

        sub4.setTextOrigin(x,y)
        sub4.textLines(name)
        
        sub4.setTextOrigin(x+4*inch,y)
        sub4.textLines(nif)

        cme.drawText(sub4)
        sub2.setFont("Helvetica", 12)


        sub2.textLines("")
        sub2.textLines("")

        (x,y)=sub2.getCursor()
        cme.line(x,y,7.5*inch,y)

        cme.drawText(sub2)
        ## RESULTAT PROVES
        sub2.textLines("")
        sub2.setFont("Helvetica-Bold", 10)

        sub2.textLines("Dades de la valoració funcional medicoesportiva")
        (x,y)=sub2.getCursor()
        cme.line(x,y+0.1*inch,7.5*inch,y+0.1*inch)

        sub2.textLines("")

        sub2.textLines("Nom del centre mèdic")
        sub2.textLines("")

        sub2.setFont("Helvetica", 10)
        sub2.textLines("'El CIM'")

        (x,y)=sub2.getCursor()
        cme.line(x,y+0.1*inch,7.5*inch,y+0.1*inch)
        sub2.textLines("")
        sub2.setFont("Helvetica-Bold", 10)

        sub2.textLines("Proves mèdiques")
        sub2.textLines("(Cal marcar les realitzades i/o, si escau, afegir-ne d'altres)")

        cme.drawText(sub2)

        ## CASELLES ESQUERRA
        
        black = CMYKColor(0,0,0,1)
        cme.setFillColor(black)

        sub2.textLines("")
        sub2.textLines("")
        (x1,y1)=sub2.getCursor()
        cme.rect(x1 , y1 , width=10 , height=10 , fill=True)
        
        

        sub3.setTextOrigin(x1+15, y1)
        sub3.textLines("Antecedents personals i familiars")

        sub2.textLines("")
        sub2.textLines("")
        (x2,y2)=sub2.getCursor()
        cme.rect(x2,y2,width=10,height=10, fill = True)

        sub3.setTextOrigin(x2+15, y2)

        sub3.textLines("Exploració cardiorespiratoria bàsica")

        sub2.textLines("")
        sub2.textLines("")
        (x3,y3)=sub2.getCursor()
        cme.rect(x3,y3,width=10,height=10, fill=True)

        sub3.setTextOrigin(x3+15, y3)
        sub3.textLines("Exploració bàsica de l'aparell locomotor")

        ## CASELLES DRETA
        sub2.textLines("")
        sub2.textLines("")
        cme.rect(x1+3*inch,y1,width=10,height=10, fill=True)

        sub3.setTextOrigin(3*inch+x1+15, y1)
        sub3.textLines("Exploració per aparells")

        sub2.textLines("")
        sub2.textLines("")
        cme.rect(x2+3*inch,y2,width=10,height=10, fill=True)
        

        sub3.setTextOrigin(3*inch+x2+15, y2)
        sub3.textLines("Electrocardiograma")

        sub2.textLines("")
        sub2.textLines("")

        cme.rect(x3+3*inch,y3,width=10,height=10)

        sub3.setTextOrigin(3*inch+x3+15, y3)
        sub3.textLines("Ergometria (Prova esforç)")

        cme.drawText(sub3)

        ## CASELLES ABAIX
        sub3.textLines("")
        sub3.textLines("")

        (x,y)=sub3.getCursor()

        sub3.setTextOrigin(x3,y)
        sub3.textLines("Indicacions per a la pràctica d'exercici físic en funció dels resultats de les proves mèdiques")

        (x,y)=sub3.getCursor()
        cme.line(x,y+0.1*inch,7.5*inch,y+0.1*inch)

        sub3.textLines("")
        (x,y)=sub3.getCursor()
        cme.rect(x,y,width=10,height=10, fill=True)

        sub3.setTextOrigin(x+15, y)
        sub3.textLines("Sense contradiccions aparents per a la pràctica d'exercici físic i/o esport")

        sub3.textLines("")
        (x,y)=sub3.getCursor()
        cme.rect(x-15,y,width=10,height=10)

        sub3.setTextOrigin(x, y)
        sub3.textLines("Amb limitacions específiques per a l'exercici físic")
        cme.drawText(sub3)

        sub3.textLines("")
        (x,y)=sub3.getCursor()
        cme.rect(x-15,y,width=10,height=10)

        sub3.setTextOrigin(x, y)
        sub3.textLines("Contradicció absoluta per a la pràctica esportiva")
        cme.drawText(sub3)

        sub3.textLines("")
        sub3.textLines("")


        ## METGE
        (x,y)=sub3.getCursor()

        cme.line(x,y+0.1*inch,7.5*inch,y+0.1*inch)
        sub3.textLines("")

        (x,y)=sub3.getCursor()
        sub3.setTextOrigin(x,y)
        sub3.textLines("Dades del metge o metgessa declarant")



        sub3.setFont("Helvetica", 10)

        sub3.textLines("Nom i cognoms               Col·legi                    Núm. de col·legiat/ada")
        sub3.setFont("Helvetica", 12)
        sub3.textLines("")
        sub3.textLines("Pere Cambras Morales        Barcelona                    22843")

        (x,y)=sub3.getCursor()
        cme.line(x,y,7.5*inch,y)

        (x,y4)=sub3.getCursor()
        sub3.setTextOrigin(x,y4-10)
        sub3.textLines(self.ids.dia.text)
        (x,y)=sub3.getCursor()
        sub3.setTextOrigin(x+1/2+inch,y4-10)
        sub3.textLines("de")
        
        (x,y)=sub3.getCursor()
        sub3.setTextOrigin(x+1/2+inch,y4-10)
        sub3.textLines(self.ids.mes.text)        

        (x,y)=sub3.getCursor()
        sub3.setTextOrigin(x+1/2+inch,y4-10)
        sub3.textLines("del")
        
        (x,y)=sub3.getCursor()
        sub3.setTextOrigin(x+1/2+inch,y4-10)
        sub3.textLines(self.ids.any.text)


        cme.drawText(sub3)



        sub3.textLines("")
        sub3.textLines("")
        sub3.textLines("")
        sub3.textLines("")
        sub3.textLines("")
        sub3.textLines("")
        sub3.textLines("")
        sub3.textLines("")
        sub3.textLines("")
        sub3.textLines("")
        sub3.textLines("")

        (x,y)=sub3.getCursor()

        cme.drawImage("FIRMA.png", x,y ,width=2*inch,height=2*inch,preserveAspectRatio=True)


        cme.save()

        ## mostrar_pdf("CME.pdf")

    def clear(self):


        self.ids.name.text= ""
        self.ids.nif.text= ""
        self.ids.submit.text = " ENVIAR "
        self.ids.submit.background_color=(0.5,0.5,0.5,0.5)
   
    def yes(self):
        
        self.rename_file() # we save on self.name_file the name
        dir_fitx = os.path.join(os.getcwd(), self.ids.club.text, self.name_file+'.pdf') # current directory + name_fitx 
        os.remove(dir_fitx)
        
        self.save_file()
        self.e_mail()
        self.prev = 0
        self.name_file = ""

        self.ids.submit.text="ENVIAR"
        self.ids.submit.background_color=(0.7,0.7,0.7,0.7)
        self.ids.prev.text="Previa"
        self.ids.clea.text="Clear"
        self.reenv = 0 # torna a estar tot igual


    def no(self):
        self.reenv = 0

        self.ids.submit.text="ENVIAR"
        self.ids.submit.background_color=(0.7,0.7,0.7,0.7)
        self.ids.prev.text="Previa"
        self.ids.clea.text="Clear"

    def is_correct(self): ## create label telling if is right
       
        if self.c != "0" and self.reenv == 0:  # changed in comp() case we didn't send any file with these name
            ## update send button
            self.ids.submit.text = " ENVIAT CORRECTAMENT "
            self.ids.submit.background_color=(0,0,1,1)  
               
            self.save_file()
            self.e_mail()
            self.prev = 0
            self.name_file = ""
        
        elif self.c!= "0" and self.reenv == 1: # cas que ja sha enviat un fitxer igual
            
            self.ids.submit.text = "VOLS TORNAR A ENVIAR?"
            self.ids.prev.text = "SI" # label previa becomes yes
            self.ids.clea.text = "NO" # label clear becomes no
        else:
            ## update send button  
            self.ids.submit.text = "NO S'HA POGUT ENVIAR"   
            self.ids.submit.background_color=(1,0,0,1)

    def comp(self , club ):
        
        A = Add_club() # creat object class 

        search_= A.dicc.get(club) # can be a mail or None
         # we need mail club to comprove 
        if search_ != None:
            self.c = search_  # we'll use after (is_correct)
            self.ids.mail.text = search_ # update label mail from Maker
        else:
            self.c = "0"
            self.ids.mail.text = "ERROR 101"
    


class List_club(Screen):
    def __init__(self, **kargs):
        
        super(List_club,self).__init__() 

        A = Add_club() #we need to have the dictionary
        self.dicc = A.dicc
        self.club_mail = A.club_mail # get dictionary from file
        self.club_names = A.club_names
        
        self.count=0


    def plus_function(self):
        
        leng = len(self.dicc)

        if self.count<(leng-1):

            self.count=self.count+1       
            self.ids.list.text="NOM: "+self.club_names[self.count]+"\n"+" CORREU: "+self.club_mail[self.count]


    def neg_function(self):

        
        if self.count>0:
            self.count=self.count-1 
            self.ids.list.text="NOM: "+self.club_names[self.count]+ "\n"+" CORREU: "+self.club_mail[self.count]
    
        


class WindowManager(ScreenManager):
    pass



kv = Builder.load_file('app.kv')

class Application(App):

    def build(self):
        self.c=0
       
        return kv 

if __name__=='__main__':
    Application().run()
