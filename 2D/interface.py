
from boid import *


sc = ScreenManager()

class Names(Button):
	def __init__(self,text, **kwargs):
		super(Names, self).__init__(**kwargs)
		self.text=text
		

class Option(Slider):

	def __init__(self,**kwargs):
		super(Option,self).__init__(**kwargs)
		self.min=0
		self.max=5
		self.value = 0.2
		self.value_track=True
		self.value_track_color=[1,1,0.03,1]

	
class Options(GridLayout):

	def __init__(self,**kwargs):
		super(Options,self).__init__(**kwargs)
		self.rows=2
		self.size_hint=(1,0.08)

		self.add_widget(Names("Seperation"))
		self.add_widget(Names("Cohesion"))
		self.add_widget(Names("Allignment"))


		l=[Option(),Option(),Option()]
		l[0].bind(value=funcSep)
		l[1].bind(value=funcCohe)
		l[2].bind(value=funcAllign)
		self.add_widget(l[0])
		self.add_widget(l[1])
		self.add_widget(l[2])


class CanvasWidget(Widget):

	def __init__(self,**kwargs):
		super(CanvasWidget,self).__init__(**kwargs)
		self.n= 80


class Collection(GridLayout):

	def __init__(self,**kwargs):
		super(Collection,self).__init__(**kwargs)
		self.rows=3
		self.canvaswid = CanvasWidget()
		self.add_widget(Options())
		self.add_widget(self.canvaswid)


		another_grid = FloatLayout()
		button = Button(text="Back",size_hint=(0.1,0.05))
		button.bind(on_press=back)
		another_grid.add_widget(button)
		another_grid.add_widget(Label(text="[color=000000][b]Initially all parameters are set to optimum their values[/b][/color]",
			markup=True,
			pos_hint={"left":0.5,"right":1,"top":0.55,"bottom":1}))

		self.add_widget(another_grid)




	def addBoids(self):

		with self.canvas:
			Color(rgba=(1,0,0,1))
			Boids.append(Boid(self.canvas))

			Color(rgba=(0,0,0,1))
			for i in range(1,self.canvaswid.n):
				Boids.append(Boid(self.canvas))




class Screens(ScreenManager):

	def __init__(self):
		screens = [Screen(name = "FlockingMovement"),Screen(name = "2D"),Screen(name="3D")]
		for each in screens:
			self.add_widget(each)

		#self.current = "FlockingMovement"



class FlockingMovement(FloatLayout):

	def __init__(self,**kwargs):

		super(FlockingMovement,self).__init__(**kwargs)

		self.add_widget(Label(text = "[color=FF0000][size=20][b]Flocks, Herds, and Schools:[/b][/size][/color]\n[i]A Distributed Behavioral Model\nCraig W. Reynolds[/i]\nhttp://www.cs.toronto.edu/~dt/siggraph97-course/cwr87/",
			color=[0,0,0,1],
			valign='top',
			halign='center',
			markup=True,
			size_hint=(1,1.7)))

		button =Button(text="2D",
			size_hint=(0.15,0.05),
			background_color=(0.68,0.30,0.95),
			pos_hint={"x":0.85,"y":0})

		button.bind(on_press=switch)
		self.add_widget(button)

		button =Button(text="Copy",
			size_hint=(0.05,0.02),
			background_color=(0.68,0.30,0.95),
			pos_hint={"x":0.75,"y":0.79})

		button.bind(on_press=copy)
		self.add_widget(button)

		self.add_widget(Image(source="2D/PNG/separation.gif",pos_hint={"left":0.7,"right":0.8,"top":1.15,"bottom":0}))
		self.add_widget(Image(source="2D/PNG/alignment.gif",pos_hint={"left":0.7,"right":0.8,"top":0.9,"bottom":0}))
		self.add_widget(Image(source="2D/PNG/cohesion.gif",pos_hint={"left":0.7,"right":0.8,"top":0.65,"bottom":0}))


		self.add_widget(Label(text = "[color=0000FF][size=15][b]Separation:[/b][/size][/color]\n[i]steer to\navoid crowding local\nflockmates [/i]",
			color=[0,0,0,1],
			markup=True,
			pos_hint={"left":0.7,"right":1.1,"top":1.15,"bottom":0}))

		self.add_widget(Label(text = "[color=0000FF][size=15][b]Alignment:[/b][/size][/color]\n[i]steer\ntowards the average\nheading of local\nflockmates [/i]",
			color=[0,0,0,1],
			markup=True,
			pos_hint={"left":0.7,"right":1.1,"top":0.9,"bottom":0}))

		self.add_widget(Label(text = "[color=0000FF][size=15][b]Cohesion:[/b][/size][/color]\n[i]steer to\nmove toward the\naverage position of\nlocal flockmates [/i]",
			color=[0,0,0,1],
			markup=True,
			pos_hint={"left":0.7,"right":1.1,"top":0.65,"bottom":0}))


def switch(instance):
	sc.transition.direction="left"
	sc.current = "2D"

def back(instance):
	sc.transition.direction="right"
	sc.current = "FlockingMovement"

def copy(instance):
	text = "http://www.cs.toronto.edu/~dt/siggraph97-course/cwr87/"
	Clipboard.copy(text)


class VisualApp(App):

	def build(self):
		Window.clearcolor=(1,1,1,1)
		self.instance = Collection()
		self.instance.addBoids()


		screens = [Screen(name = "FlockingMovement"),Screen(name = "2D"),Screen(name="3D")]
		screens[0].add_widget(FlockingMovement())
		screens[1].add_widget(self.instance)
		for each in screens:
			sc.add_widget(each)

		return sc

Vapp = VisualApp()