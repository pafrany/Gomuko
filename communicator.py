import socket
import threading
import time
from io import StringIO
from GUI import *

class Communicator(object):
	def __init__(self, game):
	    self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    self.socket.connect((self.get_ip(), 12321))
	    self.game=game
	    self.lock=threading.RLock()
	    self.threads_run=False
	    self.challenged=False
	    self.i_challenge=False
	def print(self, message):
	    self.socket.send(message.encode())
	def read_line(self):
		buff = StringIO()
		while True:
			data = self.socket.recv(1).decode('utf-8')
			buff.write(data)
			if '\n' in data: break
		a=buff.getvalue().splitlines()[0]
		return(a)
	def challenge_watcher_thread(self):
		while True:
			time.sleep(.100)
			res = "no";
			while True:
				time.sleep(.100)
				if not self.challenged:
					self.lock.acquire()
					if not self.threads_run:
						self.lock.release()
						return
					self.print('kihiv?\r\n')
					res = self.read_line()
					if not res=='no':
						res=self.read_line()
						self.lock.release()
						break
					self.lock.release()
			self.game.challenged_popup=Challenged(self.game, self, res)
			name=res
			self.challenged=True
			res=''
			while True:
				time.sleep(.100)
				self.lock.acquire()
				if not self.threads_run:
					self.lock.release()
					return
				if not self.challenged:
					self.lock.release()
					break
				self.print('kihivMeg?\r\n')
				res=self.read_line()
				if res in (['megse', 'gone']):
					self.challenged=False
					self.lock.release()
					break
				self.lock.release()
			if res=='megse':
				self.game.frames['Room'].i_listNodes.insert(END, name + 'withdrawed the challenge')
			if res=='gone':
				self.game.frames['Room'].i_listNodes.insert(END, name + 'disappeared :(')
	def decline(self):
		self.game.challenged_popup.destroy()
		self.lock.acquire()
		self.print('no\r\n')
		self.lock.release()
	def accept(self):
		self.game.challenged_popup.destroy()
		self.lock.acquire()
		self.print('ok\r\n')
		self.lock.release()
		self.game.show_frame('Board')

				



	def get_data(self):
		self.lock.acquire()
		self.print('selfdata\r\n')
		s = self.read_line()
		id = int(s)
		s = self.read_line()
		a = int(s);
		s = self.read_line()
		b = int(s);
		s = self.read_line()#fölösleges adat
		s = self.read_line()
		selfdata={'name': s, 'id': id, 'played': a, 'won': b}
		self.print('runninggames\r\n');
		s = self.read_line()
		n = int(s)
		runninggames=[]
		for i in range(n):
			s1 = self.read_line()
			s2 = self.read_line()
			runninggames.append(s1+' vs '+s2)
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
			if self.threads_run==False:
				self.lock.release()
				return
			self.game.selfdata, plist, playerdata=self.get_data()
			self.lock.release()
			if playerdata!=self.game.playerdata:
				self.game.playerdata=playerdata
				
			if plist!=self.game.plist:
				self.game.plist=plist
				self.game.frames['Room'].set_player_list(self.game.plist)
			time.sleep(.100)
	def challenge(self, player):
		self.game.playerbox.destroy()
		self.lock.acquire()
		self.pint('Kihiv\r\n')
		self.print(str(player[id])+'\r\n')
		res=self.read_line()
		if res=='busy':
			self.lock.release()
			self.game.frames['Room'].i_listNodes.insert(END, player['name']+' is currently busy')
			return
		self.game.i_challenge_popup=ChallengeInProgress(self.game, self, player)
		#kihivresszál
	def cancel(self):
		self.lock.acquire()
		self.game.i_challenge_popup.destroy()
		self.print('megse\r\n')
		self.i_challenge=False
		self.lock.release()

	def i_challenge_thread(self, player):
		self.lock.acquire()
		self.i_challenge=True
		self.lock.release()
		kifogas=''
		while True:
			time.sleep(.100)
			self.lock.acquire()
			if not self.i_challenge:
				self.lock.release()
				return
			self.print('kihivRes\r\n')
			res=self.read_line()
			if res=='y':
				self.lock.release()
				self.i_challenge=False
				ok=True
				break
			if res=='n':
				self.lock.release()
				self.i_challenge=False
				ok=False
				kifogas=' declined the challenge'
				break
			if res=='gone':
				self.lock.release()
				self.i_challenge=False
				ok=False
				kifogas=' disappeared :('
				break
			self.lock.release()
		if ok:
			self.game.show_frame['Game']
			return
		self.games.frames['Room'].i_listNodes.iset(END, player['name']+kifogas)

	def get_ip(self):
		return 'localhost'
	def close(self):
		print('finito')
		self.lock.acquire()
		self.threads_run=False
		self.print('logout\r\n')
		self.lock.release()
		self.game.destroy()

