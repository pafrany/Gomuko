import socket
import threading
import time
from io import StringIO
from GUI import *

SLEEPTIME=.1

class Communicator(object):
	def __init__(self, game):
	    self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    self.socket.connect((self.get_ip(), 12321))
	    self.game=game
	    self.lock=threading.RLock()
	    self.threads_run=False
	    self.rematch_out=False
	    self.rematch_in=False
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
			self.game.challenged_popup.attributes('-topmost', 'true')
			self.game.frames['Room'].disable()
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
			self.game.frames['Room'].enable()
			self.game.challenged_popup.destroy()
			if res=='megse':
				self.game.frames['Room'].i_listNodes.insert(END, name + ' withdrawed the challenge')
			if res=='gone':
				print('This disappeared')
				self.game.frames['Room'].i_listNodes.insert(END, name + ' disappeared :(')
	def decline(self):
		print('release')
		self.game.frames['Room'].enable()
		self.game.challenged_popup.destroy()
		print('released')
		self.lock.acquire()
		print('I said no')
		self.print('no\r\n')
		#res=self.read_line()
		self.challenged=False
		self.lock.release()
		print('released')
	def accept(self):
		self.game.frames['Room'].enable()
		self.game.challenged_popup.destroy()
		self.lock.acquire()
		self.print('ok\r\n')
		self.threads_run=False
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
		self.i_challenge=True
		self.lock.release()
		self.game.i_challenge_popup=ChallengeInProgress(self.game, self, player)
		self.game.i_challenge_popup.attributes('-topmost', 'true')
		self.game.frames['Room'].disable()
		threading.Thread(target=self.i_challenge_thread, args=[player], daemon=True).start()
	def cancel(self):
		self.lock.acquire()
		self.game.frames['Room'].enable()
		self.game.i_challenge_popup.destroy()
		self.print('megse\r\n')
		self.i_challenge=False
		self.lock.release()

	def i_challenge_thread(self, player):
		print('szál indul')
		self.lock.acquire()
		
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
				self.threads_run=False
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
		self.game.frames['Room'].enable()
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
		self.game.frames['Room'].enable()
		self.game.destroy()
	def in_game_comm(self):
		
		while self.game.game_runs:
			time.sleep(SLEEPTIME)
			self.lock.acquire()
			self.print('valamiHir?\r\n')
			print(str(self.game.selfdata['id'])+'valamihir?')
			res=self.read_line()
			print(res)
			self.lock.release()	
			if res=='lepett':
				r=int(self.read_line())
				c=int(self.read_line())
				self.game.opponent_step(r, c)
			elif res=='vesztettel':
				self.game.endGame(2)
				return
			elif res=='nyertel':
				self.game.endGame(3)
				return
			elif res=='dontetlen':
				self.game.endGame(1)
				return
	def giveup(self, giveup):
		self.game.give_up_popup.destroy()
		self.game.frames['Board'].enable()
		if giveup:
			self.lock.acquire()
			self.print('felad\r\n')
			self.lock.release()
		else:
			self.game.frames['Board'].visszvag.configure(state=DISABLED)
	
	def rematch_watcher_thread(self, who):
		res='-'
		while res not in ['y', 'gone'] and not self.rematch_out and self.game.on_board:
			time.sleep(SLEEPTIME)
			self.lock.acquire()
			self.print('visszavago?\r\n')
			res=self.read_line()
			self.lock.release()
		if res=='gone' or self.rematch_out:
			self.game.frames['Board'].turn_label.config(text=who+' left the game')
			return
		self.game.rematch_in_popup=RematchProposalIn(self.game, self, who)
		self.game.rematch_in_popup.attributes('-topmost', 'true')
		self.game.frames['Board'].visszvag.configure(state=DISABLED)
		res='-'
		self.rematch_in=True
		while res!='gone' and self.rematch_in and self.game.on_board:
			time.sleep(SLEEPTIME)
			self.lock.acquire()
			self.print('kihivMeg?\r\n')
			res=self.read_line()
			self.lock.release()
		if res=='gone':
			self.game.frames['Board'].turn_label.config(text=who+' left the game')
			self.game.rematch_in_popup.destroy()
	def i_propose_rematch(self):
		self.lock.acquire()
		self.print('Visszvag\r\n')
		self.rematch_out=True
		self.lock.release()
		self.game.rematch_out_popup=RematchProposalOut(self.game, self)
		self.game.frames['Board'].visszvag.configure(state=DISABLED)
		self.game.rematch_out_popup.attributes('-topmost', 'true')
		threading.Thread(target=self.i_propose_rematch_thread, args=[], daemon=True).start()
	def i_propose_rematch_thread(self):
		res=''
		while res not in ['y', 'no', 'gone'] and self.rematch_out and self.game.on_board:
			time.sleep(SLEEPTIME)
			self.lock.acquire()
			if self.rematch_out==False:
				self.lock.release()
				break
			self.print('kihivRes\r\n')
			res=self.read_line()
			self.lock.release()
		self.game.rematch_out_popup.destroy()
		self.rematch_out=False
		if res=='y':
			self.game.frames['Board'].clear()
			self.game.game_runs=True
			self.game.frames['Board'].visszvag.configure(state=DISABLED)
			self.game.myplayerid=self.game.myplayerid%2+1
			self.game.myturn=(self.game.myplayerid==1)
			text='It\'s your turn' if self.game.myturn else self.game.opponent+'\'s turn'
			self.game.frames['Board'].turn_label.config(text=text)
			threading.Thread(target=self.in_game_comm, args=[], daemon=True).start()
			return
		elif res=='gone':
			kifogas=' left the game'
		else:
			kifogas=' declined the proposal'
		self.game.frames['Board'].turn_label.config(text=self.game.opponent+kifogas)
	def rematch_cancel(self):
		self.lock.acquire()
		self.print('megse\r\n')
		self.rematch_out=False
		self.lock.release()	
	def rematch_decline(self):
		self.game.rematch_in_popup.destroy()
		self.lock.acquire()
		print('I said no')
		self.print('elutasit\r\n')
		#res=self.read_line()
		self.rematch_in=False
		self.lock.release()
		self.game.frames['Board'].visszvag.configure(state='normal')
		print('released')
	def rematch_accept(self):
		self.game.rematch_in_popup.destroy()
		self.lock.acquire()
		self.print('elfogad\r\n')
		self.lock.release()
		self.game.frames['Board'].clear()
		self.game.game_runs=True
		self.rematch_in=False
		self.game.myplayerid=self.game.myplayerid%2+1
		self.game.myturn=(self.game.myplayerid==1)
		text='It\'s your turn' if self.game.myturn else self.game.opponent+'\'s turn'
		self.game.frames['Board'].turn_label.config(text=text)
		threading.Thread(target=self.in_game_comm, args=[], daemon=True).start()