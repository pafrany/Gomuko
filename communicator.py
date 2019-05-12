import socket
import threading
import time
from io import StringIO
from GUI import *

SLEEPTIME=1

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
			time.sleep(SLEEPTIME)
			res = "no";
			while True:
				time.sleep(SLEEPTIME)
				if not self.i_challenge:
					self.lock.acquire()
					print(str(self.game.selfdata['id'])+'acquired')
					if not self.threads_run:
						print('notrunrelease')
						self.lock.release()
						return
					self.print('kihiv?\r\n')
					res = self.read_line()
					print('kihiv?')
					print(res)
					if not res=='no':
						res=self.read_line()
						print('kihivyes')
						print(res)
						self.lock.release()
						break
					print('release')
					self.lock.release()
			self.game.challenged_popup=Challenged(self.game, self, res)
			name=res
			self.challenged=True
			res=''
			while True:
				time.sleep(SLEEPTIME)
				self.lock.acquire()
				if not self.threads_run:
					self.lock.release()
					return
				if not self.challenged:
					print('Notchallanged, release')
					self.lock.release()
					break
				print('kihivMeg?')
				self.print('kihivMeg?\r\n')
				res=self.read_line()
				print(res)
				if res in (['megse', 'gone']):
					self.challenged=False
					self.lock.release()
					break
				self.lock.release()
			print('destroy kéne')
			print(res)
			self.game.challenged_popup.destroy()
			if res=='megse':
				self.game.frames['Room'].i_listNodes.insert(END, name + ' withdrawed the challenge')
			if res=='gone':
				print('This disappeared')
				self.game.frames['Room'].i_listNodes.insert(END, name + ' disappeared :(')
	def decline(self):
		self.game.challenged_popup.destroy()
		self.lock.acquire()
		print('I said no')
		self.print('no\r\n')
		#res=self.read_line()
		self.challenged=False
		self.lock.release()
		print('released')
	def accept(self):
		self.game.challenged_popup.destroy()
		self.lock.acquire()
		self.print('ok\r\n')
		self.lock.release()
		self.game.start_game()

				



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
			time.sleep(SLEEPTIME)
	def challenge(self, player):
		self.game.playerbox.destroy()
		self.lock.acquire()
		self.print('Kihiv\r\n')
		print(player)
		print(player['id'])
		self.print(str(player['id'])+'\r\n')
		res=self.read_line()
		if res=='busy':
			self.lock.release()
			self.game.frames['Room'].i_listNodes.insert(END, player['name']+' is currently busy')
			return
		self.lock.release()
		self.game.i_challenge_popup=ChallengeInProgress(self.game, self, player)
		threading.Thread(target=self.i_challenge_thread, args=[player], daemon=True).start()
	def cancel(self):
		self.lock.acquire()
		self.game.i_challenge_popup.destroy()
		self.print('megse\r\n')
		self.i_challenge=False
		self.lock.release()

	def i_challenge_thread(self, player):
		print('szál indul')
		self.lock.acquire()
		self.i_challenge=True
		self.lock.release()
		print('ide is eljut')
		kifogas=''
		while True:
			time.sleep(SLEEPTIME)
			self.lock.acquire()
			if not self.i_challenge:
				self.lock.release()
				return
			print('KihivRes')
			self.print('kihivRes\r\n')
			res=self.read_line()
			print(res)
			if res=='y':
				self.lock.release()
				self.i_challenge=False
				ok=True
				break
			if res=='no':
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
		self.game.i_challenge_popup.destroy()
		if ok:
			self.game.start_game()
			return
		self.game.frames['Room'].i_listNodes.insert(END, player['name']+kifogas)


	def get_ip(self):
		return 'localhost'
	def close(self):
		print('finito')
		self.lock.acquire()
		self.threads_run=False
		self.print('logout\r\n')
		res=self.read_line()
		self.lock.release()
		print(res)
		self.game.destroy()
	def in_game_comm(self):
		self.lock.acquire()
		self.print('init\r\n')
		self.game.opponent=self.read_line()
		print(self.game.opponent)
		myturn=self.read_line()
		print(myturn)
		self.game.myturn=bool(myturn=='true')
		print(self.game.myturn)
		self.lock.release()
		if self.game.myturn:
			self.game.frames['Board'].turn_label.config(text='It\'s yout turn')
		else:
			self.game.frames['Board'].turn_label.config(text=self.game.opponent+'\'s turn')
		while self.game.game_runs:
			time.sleep(SLEEPTIME)
			self.lock.acquire()
			self.print('valamiHir?\r\n')
			print(str(self.game.selfdata['id'])+'valamihir?')
			res=self.read_line()
			print(res)
			if res=='lepett':
				r=int(self.read_line())
				c=int(self.read_line())
				self.game.opponent_step(r, c)
			elif res=='vesztettel':
				self.game.endGame(2)
				self.lock.release()
				return
			elif res=='nyertel':
				self.game.endGame(3)
				self.lock.release()
				return
			elif res=='dontetlen':
				self.game.endGame(1)
				self.lock.release()
				return
			self.lock.release()			
