
from boid import *


class Names(Button):
	def __init__(self,text, **kwargs):
		super(Names, self).__init__(**kwargs)
		self.text=text
		

class Option(Slider):

	def __init__(self,**kwargs):
		super(Option,self).__init__(**kwargs)
		self.min=0
		self.max=4
		self.value = 0.2
		self.value_track=True
		self.value_track_color=[1,1,0.03,1]

	
class Options(GridLayout):

	def __init__(self,**kwargs):
		super(Options,self).__init__(**kwargs)
		self.rows=2
		self.size_hint=(1,0.06)

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
		self.n= 70


class Collection(GridLayout):

	def __init__(self,**kwargs):
		super(Collection,self).__init__(**kwargs)
		self.rows=2
		self.canvaswid = CanvasWidget()
		self.add_widget(Options())
		self.add_widget(self.canvaswid)




	def addBoids(self):

		with self.canvas:
			Color(rgba=(1,0,0,1))
			Boids.append(Boid(self.canvas))

			Color(rgba=(0,0,0,1))
			for i in range(1,self.canvaswid.n):
				Boids.append(Boid(self.canvas))





class VisualApp(App):

	def build(self):
		Window.clearcolor=(1,1,1,1)
		self.instance = Collection()
		self.instance.addBoids()
		return self.instance

VisualApp().run()