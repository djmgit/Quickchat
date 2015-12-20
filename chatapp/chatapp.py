from Tkinter import *
from PIL import *
import socket
import time
import threading

import PIL.Image
import PIL.ImageTk
from ScrolledText import ScrolledText

class recv(threading.Thread):
     def __init__(self,name,sock,status):
           threading.Thread.__init__(self)
           self.sock=sock
           self.status=status
           self.shutdown=False
           self.tLock=threading.Lock()
     
     def run(self):
           while not self.shutdown:
			try:
			    self.tLock.acquire()
			    while True:
				data, addr = self.sock.recvfrom(1024)
                                #self.status.configure(state='normal')
				self.status.insert(END,str(data)+'\n')
                                print str(data)+'\n'
                                #self.status.configure(state='disabled')
			except:
			    pass
			finally:
			    self.tLock.release()
    
           
     def close(self):
             self.shutdown=True

     










class App(Frame):
        
        def __init__(self,master):
              Frame.__init__(self,master)
              self.master=master
              self.pack(fill=BOTH,expand=1)
              self.shutdown=False
              self.tLock=threading.Lock()
              self.init()
         

        def setname(self):
                self.name=self.chat_name.get()
                print self.name
                self.lb0.destroy()
                self.chat_name.destroy()
                self.set_name.destroy()
                
                self.lb_name=Label(self,text=str(self.name)+' is the Chat Room holder',justify=LEFT,fg='black',bg='white',font = 'verdana 12')
                self.lb_name.place(x=50,y=10)
                self.status2.configure(state='normal')
                self.startchat()
        
        def receving(self,name, sock):
                   
		    while not self.shutdown:
			try:
			    self.tLock.acquire()
			    while True:
				data, addr = sock.recvfrom(1024)
                                #self.status.configure(state='normal')
				self.status.insert(END,str(data)+'\n')
                                print str(data)+'\n'
                                #self.status.configure(state='disabled')
			except:
			    pass
			finally:
			    self.tLock.release()
        
	def startchat(self):

                
		self.server = ('',80)

		self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.s.bind(('127.0.0.1',5002 ))
		self.s.setblocking(0)

	 	self.rt=recv('recvthread',self.s,self.status)
                self.rt.start()
                
		self.alias = self.name
                self.s.sendto(self.alias+' has joined the chat room',self.server)
                self.livechat()
		
                    
        def sendmessage(self):
               
                message = self.status2.get("1.0",'end-1c')
                if message is not 'q':
                        if message is not '':
                              self.s.sendto(self.alias+" : "+message,self.server)
                              self.status2.delete("1.0",END)
                        self.tLock.acquire()
                        #message = self.status2.get("1.0",'end-1c')
                        self.tLock.release()
                        
                        
                
        def quitchat(self):
                self.s.sendto(self.alias+' has left the chat ',self.server)
                self.rt.close()
                self.rt.join()
                self.s.close()
                self.lb_name.destroy()
                self.lb0=Label(self,text='Ur Chat Name ',justify=LEFT,padx=10,font='verdana 10',fg='black',bg='white')
                self.lb0.place(x=5,y=10)
                self.chat_name=Entry(self)
                self.chat_name.place(x=130,y=10)
                self.chat_name.insert(10,'OWNER')
                self.set_name=Button(self,text='save',font='verdana 10',fg='black',bg='white',command=self.setname)
                self.set_name.place(x=315,y=10)
                self.qchat.destroy()
                self.qchatlbl.destroy()
        def quitapp(self):
                #self.quitchat()
                self.master.quit()
                
        
        
        def livechat(self):
                	self.qchat=Button(self,text="Leave Chat",command=self.quitchat,bg='white')
                        self.qchat.place(x=245,y=250)  
                        qchatimg=PIL.Image.open('qchat.png')
                        qchatimg=qchatimg.resize((30,30))
                        load_qchatimg=PIL.ImageTk.PhotoImage(qchatimg)
                        self.qchatlbl=Label(self,image=load_qchatimg)
                        self.qchatlbl.image=load_qchatimg
                        self.qchatlbl.place(x=340,y=250)

              
        def init(self):
                self.master.title("QuickChat")
                background=PIL.Image.open('paisley.png')
                #backgorund=background.resize((466,450),PIL.Image.ANTIALIAS)
                background=background.resize((400,500))
                load=PIL.ImageTk.PhotoImage(background)
                bk=Label(self,image=load)
                bk.image=load
                bk.place(x=0,y=0)


                qappimg=PIL.Image.open('qapp.png').resize((30,30))
                load_qappimg=PIL.ImageTk.PhotoImage(qappimg)
                qappimgbtn=Button(self,image=load_qappimg,command=self.quitapp)
                qappimgbtn.image=load_qappimg
                qappimgbtn.place(x=337,y=45)
                
                
                lb1=Label(self,text='Chat Room Status',justify=LEFT,padx=10,font='verdana 12',fg='black',bg='white')
                
                lb1.place(x=5,y=50)
                
                self.lb0=Label(self,text='Ur Chat Name ',justify=LEFT,padx=10,font='verdana 10',fg='black',bg='white')
                self.lb0.place(x=5,y=10)
                self.chat_name=Entry(self)
                self.chat_name.place(x=130,y=10)
                self.chat_name.insert(10,'OWNER')

                self.set_name=Button(self,text='save',font='verdana 10',fg='black',bg='white',command=self.setname)
                self.set_name.place(x=315,y=10)
                
                
		
		self.status = ScrolledText(root, height=10, width=50,relief=SUNKEN)
                self.status.tag_configure('color', foreground='#476042', 
						font=('Tempus Sans ITC', 12, 'bold'))
                #self.status.configure(state='disabled')
                
		self.status.place(x=5,y=80)
                
                
                
                
                lb2=Label(self,text='Speak ur Mind!!',justify=LEFT,padx=10,font='verdana 12',fg='black',bg='white')
                lb2.place(x=5,y=250)
                chat_img=PIL.Image.open('chat_img.gif')
                chat_img=chat_img.resize((40,30))
                loadchatimg=PIL.ImageTk.PhotoImage(chat_img)
                lb2=Label(self,text='Speak ur Mind!!',justify=LEFT,padx=10,font='verdana 12',fg='black',bg='white')
                
                lb2.place(x=5,y=250)

                lb_img=Label(self,image=loadchatimg)
                lb_img.place(x=150,y=250)
                lb_img.image=loadchatimg
                

                
                
		self.status2 = ScrolledText(root, height=10, width=50,relief=SUNKEN)
                self.status2.tag_configure('color', foreground='#476042', 
						font=('Tempus Sans ITC', 12, 'bold'))
		self.status2.place(x=5,y=280)
                self.status2.configure(state='disabled')
                send_image=PIL.Image.open('send2.png')
                send_image=send_image.resize((40,40))
                load_send=PIL.ImageTk.PhotoImage(send_image)
                send=Button(self,image=load_send,bg='white',command=self.sendmessage)
                send.image=load_send
                send.place(x=328,y=440)
       
		

root = Tk()

root.geometry("400x500")


app = App(root)



root.mainloop()  
         
                   
