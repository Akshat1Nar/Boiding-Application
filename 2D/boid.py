from headers import *

Boids = []
Lines = []


coheForce = 1.5
sepForce = 2
allignForce = 1




def unsignedDist(a,b):
	return sqrt( ((a[0]-b[0])*(a[0]-b[0])) + ((a[1]-b[1])*(a[1]-b[1])) )

def keepVelocity(velocity,speed):
	sum  = unsignedDist(velocity,(0,0))
	if(sum==0):
		return
	velocity[0]/=sum 
	velocity[1]/=sum 
	velocity[0]*=speed 
	velocity[1]*=speed 

	return velocity


def funcSep(instance,value):
	global sepForce
	sepForce = value
	
def funcCohe(instance,value):
	global coheForce
	coheForce = value

def funcAllign(instance,value):
	global allignForce
	allignForce = value




class Boid(Widget):
	global Boids,Lines

	velocity = ListProperty([2,3])
	acceleration = ListProperty([0,0])

	def __init__(self,canvas_,**kwargs):
		self.Canvas=canvas_
		
		self.flagSight=False
		self.once=True
		super(Boid,self).__init__(**kwargs)
		global neg
		self.angle= random()*1000%60
		self.speed = 4
		self.force = 1
		self.x= (int)(random()*10000%(Window.width))
		self.y= (int)(random()*10000%(Window.height))

		self.velocity[0]=(self.speed*sin(self.angle))
		self.velocity[1]=(self.speed*cos(self.angle))
		self.d=4
		#Triangle(points = [self.x,self.y,self.x+d/3,self.y+d,self.x-d/3,self.y+d])
		self.rectangle=Ellipse(pos=self.pos,size=(self.d,self.d))
			

		Clock.schedule_interval(self.allignment,1/60.)
		Clock.schedule_interval(self.cohesion,1/60.)
		Clock.schedule_interval(self.seperation,1/60.)
		Clock.schedule_interval(self.move,1/60.)


	def keepVelocity(self):
		sum  = unsignedDist(self.velocity,(0,0))
		if(sum==0):
			return
		self.velocity[0]/=sum 
		self.velocity[1]/=sum 

		self.velocity[0]*=self.speed 
		self.velocity[1]*=self.speed 

	def keepAcceleration(self):
		sum  = unsignedDist(self.acceleration,(0,0))
		if(sum==0):
			return

		self.acceleration[0]/=sum 
		self.acceleration[1]/=sum 

		self.acceleration[0]*=self.force
		self.acceleration[1]*=self.force


	def inView(self,a,b):
		alpha = (a+120)%360
		beta = (b-120+360)%360

		if(alpha>beta):
			alpha,beta=beta,alpha

		if(b>alpha and b<beta):
			return True
		return False

	def velAngle(self):
		if(self.velocity[0]==0):
			angle=90
		else:
			angle = (atan((self.velocity[1]/self.velocity[0]))*180+360)%360

		return angle


	def move(self,instance):
		#process = psutil.Process(os.getpid())
		#print(process.memory_info().rss) 

		
		self.x+=self.velocity[0]
		self.y+=self.velocity[1]

		if(self.x==0):
			self.angle=90
		else:
			self.angle = (atan((self.y/self.x))*180+360)%360

		self.velocity[0]+=self.acceleration[0]		
		self.velocity[1]+=self.acceleration[1]
		self.keepVelocity()		
		self.acceleration = [0,0]

		
		self.rectangle.pos=self.pos

		if self.x < 0:
			self.x=Window.width

		if self.x > Window.width:
			self.x=0

		if self.y < 0:
			self.y=Window.height

		if self.y> Window.height:
			self.y=0



	def allignment(self,instance):
		global Boids,allignForce
		AllignVel=[0,0]
		count=0
		for every in Boids:
			if(self==every):
				continue
			distance = unsignedDist((self.x,self.y),(every.x,every.y))
			if(distance<40):  #(self.inView(self.velAngle(),every.angle)) and
				count+=1
				AllignVel[0]+=every.velocity[0]
				AllignVel[1]+=every.velocity[1]


		if(count!=0):
			steerVelocity=[(AllignVel[0]/count),(AllignVel[1]/count)]
			steerVelocity=keepVelocity(steerVelocity,self.speed)
			steerVelocity=[steerVelocity[0]-self.velocity[0],steerVelocity[1]-self.velocity[1]]
			steerVelocity=keepVelocity(steerVelocity,self.force)
			self.acceleration[0]+=steerVelocity[0]*allignForce
			self.acceleration[1]+=steerVelocity[1]*allignForce
			



	def cohesion(self,instance):

		global Boids,coheForce
		AverageLoc=[0,0]
		count=0
		for every in Boids:
			if(self==every):
				continue
			distance = unsignedDist((self.x,self.y),(every.x,every.y))
			if(distance<80):  #(self.inView(self.velAngle(),every.angle)) and
				count+=1
				AverageLoc[0]+=every.x
				AverageLoc[1]+=every.y


		if(count!=0):
			AverageLoc=[(AverageLoc[0]/count),(AverageLoc[1]/count)]
			AverageLoc=[AverageLoc[0]-self.x,AverageLoc[1]-self.y]
			AverageLoc=keepVelocity(AverageLoc,self.speed)
			AverageLoc=[AverageLoc[0]-self.velocity[0],AverageLoc[1]-self.velocity[1]]
			AverageLoc=keepVelocity(AverageLoc,self.force)
			self.acceleration[0]+=AverageLoc[0]*coheForce
			self.acceleration[1]+=AverageLoc[1]*coheForce




	def seperation(self,instance):

		global Boids,sepForce
		Average=[0,0]
		count=0
		for every in Boids:
			if(self==every):
				continue
			distance = unsignedDist((self.x,self.y),(every.x,every.y))
			if(distance<40): #(self.inView(self.angle,every.angle)) and 
				count+=1
				Some = [0,0]
				Some[0]=(self.x-every.x)
				Some[1]=(self.y-every.y)

				Some[0]/=(distance*distance+0.0000001)
				Some[1]/=(distance*distance+0.0000001)

				Average[0]+=Some[0]
				Average[1]+=Some[1]


		if(count!=0):
			steerpos =[(Average[0]/count),(Average[1]/count)]
			steerpos=keepVelocity(steerpos,self.speed)
			steerpos = [steerpos[0]-self.velocity[0],steerpos[1]-self.velocity[1]]
			steerpos = keepVelocity(steerpos,self.force)
			self.acceleration[0]+=steerpos[0]*sepForce
			self.acceleration[1]+=steerpos[1]*sepForce	
