import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.uic import loadUi
import datetime
import socket as s
import threading


server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
clients = []

class Client(threading.Thread):
	
	conn = 0
	addr = 0
	
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		self.conn, self.addr = server_socket.accept()
		print(self.addr + "connected!")
		while(1):
			msg = self.conn.recv(1024)
			print(self.addr + ": " + msg)


class GUI(QApplication):

	def __init__(self):
		super().__init__(sys.argv)
		self.initUI()
		
	def initUI(self):
		self.ui = loadUi('Projects\serwer.ui')
		self.btn_con = self.ui.pushButton
		self.btn_discon = self.ui.pushButton_3
		self.btn_snd = self.ui.pushButton_2
		self.snd_txt = self.ui.lineEdit
		self.log_txt = self.ui.textEdit
		self.status = self.ui.label_2
		
		self.btn_con.clicked.connect(self.set_online)
		self.btn_discon.clicked.connect(self.set_offline)
		self.btn_snd.clicked.connect(self.proc_msg)
		
		self.ui.show()
		
	def listen(self):
		while(1):
			client = Client()
			clients += [client]
			client.start()
		
	def set_online(self):
		self.status.setText("ONLINE")
		server_socket.bind(('', 50008))
		server_socket.listen(1)
		threading.Thread(target = self.listen).start()
		
		
	def set_offline(self):
		print(threading.enumerate())
		print(threading.current_thread())
		self.status.setText("OFFLINE")
		
	def proc_msg(self):
		self.log_txt.append(self.snd_txt.text())
		self.snd_txt.setText('')

if __name__ == "__main__":
	app = GUI()
	
	sys.exit(app.exec_())