import socket
import threading
import time
from io import StringIO

class Communicator(object):
	def __init__(self, game):
	    self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    self.socket.connect((self.get_ip(), 12321))
	    self.game=game
	    self.lock=threading.RLock()
	    self.threads_run=False
	def print(self, message):
	    self.socket.send(message.encode())
	def read_line(self):
		buff = StringIO()          # Some decent size, to avoid mid-run expansion
		while True:
			data = self.socket.recv(1).decode('utf-8')                 # Pull what it can
			buff.write(data)
			print(data)                    # Append that segment to the buffer
			if '\n' in data: break              # If that segment had '\n', break
		a=buff.getvalue().splitlines()[0]
		print(a)
		return(a)
	def challange_watcher_thread(self):
		while True:
			print('')
	def get_data(self):
		print(1)
		self.lock.acquire()
		print(2)
		self.print('selfdata\r\n')
		s = self.read_line()
		print(s)
		id = int(s)
		s = self.read_line()
		print(s)
		a = int(s);
		print(4)
		s = self.read_line()
		print(s)
		print(5)
		b = int(s);
		s = self.read_line()#fölösleges adat
		print(s)
		print(6)
		s = self.read_line()
		print(s)
		print(7)
		selfdata={'name': s, 'id': id, 'played': a, 'won': b}
		self.print('runninggames\r\n');
		s = self.read_line()
		n = int(s)
		runninggames=[]
		print(8)
		for i in range(n):
			s1 = self.read_line()
			s2 = self.read_line()
			runninggames.append(s1+' vs '+s2)
		print(9)
		self.print('players\r\n')
		s = self.read_line()
		n = int(s)
		playerdata=[]
		plist=[]
		for i in range(n):
			s = self.read_line()
			id = int(s)
			s = self.read_line()
			a = int(s);
			s = self.read_line()
			b = int(s);
			s = self.read_line()
			s = self.read_line()
			plist.append(s)
			playerdata.append({'name': s, 'id': id, 'played': a, 'won': b})
		self.lock.release()
		return (selfdata, plist, playerdata)
	def data_update_thread(self):
		while True:
			self.lock.acquire()
			print(self.threads_run)
			if self.threads_run==False:
				self.lock.release()
				time.sleep(.300)
				continue
			self.game.selfdata, self.game.plist, self.game.playerdata=self.get_data()
			self.lock.release()
			self.game.frames['Room'].set_player_list(self.game.plist)
			time.sleep(.100)
	def get_ip(self):
		return 'localhost'

