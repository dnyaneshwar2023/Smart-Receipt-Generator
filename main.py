# Smart-Receipt App
# Made by : Dnyaneshwar Ware (Dnyaneshwar-dev)
# Walchand College Of Engineering Sangli 

# importing modules
import kivy
from kivy.app import App 
from kivy.uix.label import Label 
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.graphics import Rectangle, Color
import smtplib
import os
from fpdf import FPDF
from datetime import date
from email.message import EmailMessage
from validate_email import validate_email
 

# get system date
today = date.today()
dt = today.strftime("%d/%m/%Y")

# e-mail data
global_mail=""
global_password=""

# loginpage screen
class LoginPage(BoxLayout):
	def __init__(self,**kwargs):
		super(LoginPage,self).__init__(**kwargs)
		
		self.window = BoxLayout(orientation='vertical',padding=10)
		self.logo=Image(source='Smart-Receipt.jpg')
		self.logo.size_hint=(0.7,2)
		self.window.add_widget(self.logo)
		self.window.add_widget(Label(text='E-mail :',font_size=20))
		self.email_ip = TextInput(multiline=False,hint_text='Enter E-mail',font_size=20)
		self.window.add_widget(self.email_ip)
		self.window.add_widget(Label(text = 'Password :',font_size=20))
		self.password = TextInput(multiline=False,hint_text='Enter Password',password=True,font_size=20)
		self.window.add_widget(self.password)
		self.btn = Button(text='Submit',font_size=20)
		self.window.add_widget(self.btn)
		self.btn.bind(on_press=self.accept)
		self.login = Popup(title='Log-in with Google Account',content=self.window)
		self.login.open()
		
	def accept(self,event):
		global global_mail
		global global_password
		global_mail = self.email_ip.text
		global_password = self.password.text
		
		global_mail.strip()
		global_password.strip()

		with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
			try:
				smtp.login(global_mail,global_password)
				self.login.dismiss()
				SmartReceipt.screen_manager.current = 'mainpage'
			except smtplib.SMTPAuthenticationError:
				self.page = GridLayout(rows=3,padding=30)
				self.error = Image(source='error.jpg')
				self.page.add_widget(self.error)
				self.page.add_widget(Label(text='Wrong E-maiil or Password, Try Again !!',font_size=22))
				self.retry = Button(text='Retry',font_size=22)
				self.page.add_widget(self.retry)
				self.p = Popup(title='Error',content=self.page)
				self.retry.bind(on_press=self.back)
				self.p.open()		
	def back(self,event):
		SmartReceipt.screen_manager.current = 'login'
		self.p.dismiss()

# menu
class Menu(GridLayout):
	def __init__(self,**kwargs):
		super(Menu,self).__init__(**kwargs)
		# defining screen property
		self.rows = 6 
		self.column = 2
		self.padding = 10
		self.spacing = 10
		self.sr = Label(text = "SR. NO : ",font_size=22)
		self.add_widget(self.sr)
		
		self.sr_no = TextInput(multiline = False,font_size=20)
		self.add_widget(self.sr_no)

		self.name = Label(text = "Name: ",font_size=22)
		self.add_widget(self.name)

		self.name_input= TextInput(multiline = False,font_size=20)
		self.add_widget(self.name_input)

		self.mail = Label(text = "e-mail : ",font_size=22)
		self.add_widget(self.mail)		

		self.mail_input = TextInput(multiline = False,font_size=20)
		self.add_widget(self.mail_input)
		
		self.contents = Label(text = "Contents : ",font_size=22)
		self.add_widget(self.contents)

		self.contents_input = TextInput(font_size=20)
		self.add_widget(self.contents_input)

		self.total = Label(text = "Total : ",font_size=22)
		self.add_widget(self.total)

		self.total_input= TextInput(multiline = False,font_size=20)
		self.add_widget(self.total_input)
		
		# clear button
		self.clear = Button(text = "CLEAR",font_size=22)
		self.add_widget(self.clear)
		self.clear.bind(on_press = self.erase)
		
		# sending button
		self.send = Button(text = "SEND",font_size=22)
		self.add_widget(self.send)
		self.send.bind(on_press = self.delivery)

	# clearing the all fields
	def erase(self,event):
		self.sr_no.text = ""
		self.name_input.text=""
		self.mail_input.text=""
		self.contents_input.text=""
		self.total_input.text=""

	# deliver the mail 
	def delivery(self,event):
		# grabing the inputed data
		name = self.name_input.text
		email = self.mail_input.text
		content = self.contents_input.text
		tot = self.total_input.text
		self.make_pdf()
		print(global_mail,global_password)
		with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
			smtp.login(global_mail,global_password)
			msg = EmailMessage()
			msg['Subject'] = 'Thank You For Shopping..'
			msg['From'] = 'wcestuffs@gmail.com'
			msg['To'] = email
			msg.set_content(f"Hi {name},\nPlase check your recepit of your recent transaction through SmartShop in attachment section.\n\nThanking You.\n\nRegards,\nSmartReceipt Testing by Dnyaneshwar.")
			files = ['sample.pdf']
			for file in files:
				with open(file,'rb') as f:
					file_data = f.read()
					file_name = f"{name} - Receipt.pdf"
				msg.add_attachment(file_data,maintype='application',subtype='octet-stream',filename=file_name)
			smtp.send_message(msg)
			print('Done')
			# generating popup
			self.page = GridLayout(rows=3,padding=30)
			self.sent = Image(source='sent.jpg')
			self.page.add_widget(self.sent)
			self.page.add_widget(Label(text='Sent Successfully',font_size=22))
			self.close = Button(text='Close',font_size=22)
			self.page.add_widget(self.close)
			self.p = Popup(title='Sent',content=self.page)
			self.close.bind(on_press=self.p.dismiss)
			self.p.open()
		

	# creating a pdf using FPDF
	def make_pdf(self,**kwargs):
		#  grabing the inputed values
		serial_no = self.sr_no.text 
		name = self.name_input.text
		email = self.mail_input.text
		content = self.contents_input.text
		tot = self.total_input.text

		doc = FPDF(orientation='P',unit='mm',format='A4')
		doc.add_page()
		doc.rect(5,5,200,287,'D')
		doc.image('logo.jpg',165,10,30,30,type='JPG')
		doc.set_font('Times',size=28,style='B')
		doc.ln(10)
		doc.cell(90)
		doc.cell(10,10,txt="SMART-RECEIPT",align='C')
		doc.ln(25)
		doc.set_font('Arial',size=17,style='B')
		doc.cell(20)
		doc.cell(30,7,txt = f"SR No : {serial_no}",align='L')
		doc.ln()
		doc.cell(20)
		doc.cell(30,7,txt=f"Name : {name}",align='L')
		doc.ln()
		doc.cell(20)
		doc.cell(30,7,txt=f"E-mail : {email}",align='L')
		doc.ln(15)
		doc.cell(20)
		doc.set_font('Arial',size=20,style='B')
		doc.cell(30,10,txt="Contents : ",align='L')
		doc.ln(10)
		doc.cell(20)
		doc.set_font('Arial',size=14,style='B')
		doc.multi_cell(150,10,txt=f"{content}",align='L',border=1)
		doc.ln(20)
		doc.cell(20)
		doc.cell(90,15,txt =f" Total : RS. {tot}",align='L',border=1)
		doc.ln(20)
		doc.cell(20)
		doc.cell(20,10,txt=f"Date : {dt}",align='L')
		doc.ln(50)
		doc.cell(150)
		doc.cell(30,15,txt =" VERIFIED",align='L',border=1)
		doc.set_font('Times',style='B',size=15)
		doc.ln(40)
		doc.cell(50,5,txt="Please Check the receipt carefully and acknowledge probems if any.",align='L')
		doc.ln()
		doc.set_font('Times',style='B',size=15)
		doc.cell(50,5,txt='For any queries write to : ')
		doc.cell(10)
		doc.set_text_color(0,0,255)
		doc.set_font('Times',style='U',size=15)
		doc.cell(30,7,txt='wcestuffs@gmail.com',link='wcestuffs@gmail.com')
		doc.output('sample.pdf')	

# SmartReceipt app starter
class SmartReceiptApp(App):
	def build(self):
		# manage screens using screen manager
		self.screen_manager = ScreenManager()
		self.log_in = LoginPage()
		screen = Screen(name='login')
		screen.add_widget(self.log_in)
		self.screen_manager.add_widget(screen)
		self.main_page = Menu()
		screen = Screen(name='mainpage')
		screen.add_widget(self.main_page)
		self.screen_manager.add_widget(screen)
		return self.screen_manager

# running the app
if __name__ == '__main__':
	SmartReceipt = SmartReceiptApp()
	SmartReceipt.run()