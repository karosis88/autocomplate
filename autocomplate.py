import sys
from pynput import keyboard
import colorama



class Trie:

	def __init__(self, val='') -> None:
		self.val = val
		self.childs = []
		self.__words = []

	def insertWord(self, word) -> None:
		if not word:
			return
		self.__words.append(word)
		for child in self.childs:
			if child.val == word[0]:
				return child.insertWord(word[1:])
		self.childs.append(Trie(word[0]))
		return self.childs[-1].insertWord(word[1:])

	def insertWords(self, words:list):
		for i in words:
			self.insertWord(i)

	def searchNode(self, chars):
		startnode = self
		while chars:
			for nd in startnode.childs:
				if nd.val == chars[0]:
					chars = chars[1:]
					startnode = nd
					break
			else:
				return
		return startnode

	@property
	def getWords(self, lvl=0):
		return self.__words

	def __repr__(self) -> str:
		return self.val

class AutoComplate:

	def __init__(self) -> None:
		self.curtext = ''
		self.lastfillerlen = 0
		self.a=Trie()
		self.ind = 0
		self.curmax = 0

	def start(self):
		with keyboard.Listener(on_press=self.on_press,on_release=self.on_release) as listener:
			listener.join()

	def on_press(self, key):
		if type(key).__name__ == 'Key':

			if key.name == 'backspace':
				if self.curtext:
					if self.lastfillerlen:
							sys.stdout.write(f"\033[1D")
							sys.stdout.write(f"\033[1;30m{self.curtext[-1]}")
							sys.stdout.write("\033[1D")
							self.lastfillerlen+=1
					else:
						sys.stdout.write("\033[1D")
				else:
					return
				key.char = ''
				self.curtext = self.curtext[:-1]
			elif key.name == 'space':
				key.char = ' '
			elif key.name == 'tab':
				if not self.curtext:
					return
				key.char = ''
				if self.curmax == 1:
					return
				if self.ind+1 < self.curmax:
					self.ind+=1
				else:
					self.ind = 0		
			else:
				return
		else:
			self.ind = 0
			
		self.curtext+=key.char
		sys.stdout.write(key.char)
		txt = self.a.searchNode(self.curtext)
		if txt:	
			words = txt.getWords
			if words:
				self.curmax = len(words)
				sys.stdout.write("\033[1;30m" + words[self.ind])
				sys.stdout.write(f"\033[{len(words[self.ind])}D")
				self.lastfillerlen = len(words[self.ind])
		else:
			sys.stdout.write('\033[K')
			self.ind=0

		if not self.curtext:
			sys.stdout.write('\033[K')
			self.ind=0

	def on_release(self, key):
		pass

if __name__ == '__main__':
	colorama.init(autoreset=True)
	ac = AutoComplate()
	ac.a.insertWords(["Apple",
	"Appij",
    "Apricot",
    "Avocado",
    "Banana",
    "Bilberry",
    "Blackberry",
    "Blackcurrant",
    "Blueberry",
    "Boysenberry",
    "Currant",
    "Cherry",
    "Cherimoya",
    "Chico fruit",
    "Cloudberry",
    "Coconut",
    "Cranberry",
    "Cucumber",
    "Custard apple",
    "Damson",
    "Date",
    "Dragonfruit",
    "Durian",
    "Elderberry",
    "Feijoa",
    "Fig",
    "Goji berry",
    "Gooseberry",
    "Grape",
    "Raisin",
    "Grapefruit",
    "Guava",
    "Honeyberry",
    "Huckleberry",
    "Jabuticaba",
    "Jackfruit",
    "Jambul",
    "Jujube",
    "Juniper berry",
    "Kiwano",
    "Kiwifruit",
    "Kumquat",
    "Lemon",
    "Lime",
    "Loquat",
    "Longan",
    "Lychee",
    "Mango",
    "Mangosteen",
    "Marionberry",
    "Melon",
    "Cantaloupe",
    "Honeydew",
    "Watermelon",
    "Miracle fruit",
    "Mulberry",
    "Nectarine",
    "Nance",
    "Olive",
    "Orange",
    "Blood orange",
    "Clementine",
    "Mandarine",
    "Tangerine",
    "Papaya",
    "Passionfruit",
    "Peach",
    "Pear",
    "Persimmon",
    "Physalis",
    "Plantain",
    "Plum",
    "Prune",
    "Pineapple",
    "Plumcot",
    "Pomegranate",
    "Pomelo",
    "Purple mangosteen",
    "Quince",
    "Raspberry",
    "Salmonberry",
    "Rambutan",
    "Redcurrant",
    "Salal berry",
    "Salak",
    "Satsuma",
    "Soursop",
    "Star fruit",
    "Solanum quitoense",
    "Strawberry",
    "Tamarillo",
    "Tamarind",
    "Ugli fruit",
    "Yuzu"])
	ac.start()
