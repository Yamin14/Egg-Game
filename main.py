import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.uix.label import Label
from kivy.clock import Clock
import random

class Game(Widget):
	def __init__(self, **kwargs):
		super(Game, self).__init__(**kwargs)
		self.bg = (0.9,0.7, 0)
		self.egg_color = (0.8, 0.8, 0.6)
		self.stick_color = (0.58, 0.29, 0)
		self.stick_length, self.stick_height = 100, 20
		self.speed = 3
		self.score = 0
		self.sticks = []
		self.directions = []
		self.jumping = False
		self.landed = False
		self.land_pos = 0
		self.jump_count = 10
		self.neg = 1
		self.x, self.y = 300, 100
		self.game_over = False
		self.scroll = False
		self.flag = False
		self.flag2 = True
		self.scroll_speed = 5
		self.positions = ["", "", "", "", "", ""]

		#direction of movement of stick	
		for i in range(6):
			self.directions.append(1)
		
		#background
		with self.canvas:
			Color(rgb=self.bg)
			Rectangle(size=(800, 1500))
			
		#the sticks
		with self.canvas:
			Color(rgb=self.stick_color)
			self.sticks.append(Rectangle(size=(self.stick_length, self.stick_height), pos=(300, 80)))
			
			for i in range(5):
				self.sticks.append(Rectangle(size=(self.stick_length, self.stick_height), pos=(random.randint(1, 600), 380+(i*300))))
		
		#the egg
		with self.canvas:
			Color(rgb=self.egg_color)
			self.egg = Ellipse(size=(100, 100), pos=(self.x, self.y))
			
		#score
		self.score_label = Label(text=f"Score: {self.score}", pos=(30, 1350), font_size=40, color=(1, 0, 0, 1))
		self.add_widget(self.score_label)
		
		#game over label
		self.game_over_label = Label(text="", pos=(300, 700), font_size=100, color=(1, 0, 0, 1))
		self.add_widget(self.game_over_label)
		
		#game over label
		
		Clock.schedule_interval(self.play, 0)
		Clock.schedule_interval(self.scroll_func, 0)
		
	def play(self, dt):
		#jumping
		if self.jumping == True:
			if self.jump_count >= -50:
				self.neg = 1
				if self.jump_count < 0:
					self.neg = -1
				self.y += (self.jump_count**2) * self.neg
				self.jump_count -= 1
			else:
				self.jump_count = 10
				self.jumping = False

		#check if egg has landed
		if self.jumping == True and self.neg == -1:
			for i in range(len(self.sticks)):
				if self.y >= self.sticks[i].pos[1] and self.y <= self.sticks[i].pos[1]+self.stick_height:
					if self.x+50 >= self.sticks[i].pos[0] and self.x+50 <= self.sticks[i].pos[0]+self.stick_length:
						self.jumping = False
						self.neg = 1
						self.jump_count = 10
						self.landed = True
						if i != self.land_pos:
							self.score += 1
						self.land_pos = i
						self.speed += 0.5
						if self.y >= 680 and self.y <= 720:
							if self.flag2 == True:
								self.flag2 = False
								self.scroll = True
								self.flag = True

		#direction update
		for i in range(len(self.sticks)):
			if self.sticks[i].pos[0] >= 600 and self.directions[i] == 1:
				self.directions[i] = 0
			elif self.sticks[i].pos[0] <= 0 and self.directions[i] == 0:
				self.directions[i] = 1

		#update stick and egg position
		for i in range(len(self.sticks)):
			if i != 0:
				if self.directions[i] == 1:
					self.sticks[i].pos = (self.sticks[i].pos[0]+self.speed, self.sticks[i].pos[1])
				elif self.directions[i] == 0:
					self.sticks[i].pos = (self.sticks[i].pos[0]-self.speed, self.sticks[i].pos[1])
					
		if self.landed == True:
			self.x = self.sticks[self.land_pos].pos[0]
			self.y = self.sticks[self.land_pos].pos[1] + self.stick_height
		
		self.egg.pos = (self.x, self.y)
		
		#score update
		self.score_label.text = f"Score: {self.score}"
			
		#game over		
		if self.y <= -100:
			self.game_over_label.text = f"""Game Over
Score: {self.score}"""
			self.speed = 0
			self.scroll_speed = 0
			self.jumping = False
			self.game_over = True

	#scroll screen
	def scroll_func(self, dt):
		if self.flag == True:
			self.flag = False
			for i in range(2):
				self.directions.append(1)
				
			with self.canvas:
				Color(rgb=self.stick_color)
				for i in range(2):
					if i == 0:
						self.sticks.append(Rectangle(size=(self.stick_length, self.stick_height), pos=(random.randint(1, 600), 1880)))
					elif i == 1:
						self.sticks.append(Rectangle(size=(self.stick_length, self.stick_height), pos=(random.randint(1, 600), 2180)))
				
				for i in range(len(self.sticks)):
					self.positions.append("")
					self.positions[i] = self.sticks[i].pos[1]
					
		if self.scroll == True:
			if self.y > 100:
				self.y -= self.scroll_speed
			else:
				self.scroll = False
				self.flag2 = True
			
			self.egg.pos = (self.x, self.y)
			for i in range(len(self.sticks)):
				if self.sticks[i].pos[1] >= self.positions[i]-600:
					self.sticks[i].pos = (self.sticks[i].pos[0], self.sticks[i].pos[1]-self.scroll_speed)
			
	def on_touch_down(self, touch):
		if self.game_over == False:
			self.jumping = True
		if self.landed == True:
			self.landed = False
		if self.game_over == True:
			self.game_over_label.text = ""
			self.score = 0
			self.speed = 3
			self.scroll_speed = 5
			self.jumping = False
			self.game_over = False
			self.jumping = False
			self.landed = False
			self.land_pos = 0
			self.jump_count = 10
			self.neg = 1
			self.x, self.y = 300, 100
			self.scroll = False
			self.flag = False
			for i in self.directions:
				i = 1
			z = len(self.sticks)
			for i in range(z):
				if i == 0:
					self.sticks[i].pos = (300, 80+(i*300))	
				else:
					self.sticks[i].pos = (random.randint(1, 600), 80+(i*300))

class MyApp(App):
	def build(self):
		return Game()
		
if __name__ == "__main__":
	MyApp().run()
