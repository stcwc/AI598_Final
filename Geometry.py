"""
Created on Thu Apr 13 2017

Usage:
# defin some geometry functions
# GetIntersection(p1,p2,q1,q2) return the intersection of line segment p1-p2 and q1-q2
# NearestPoint(p1,p2,q) return the nearest point in the line segment p1-p2 to point q

@author: YI HOU
"""

from Util import Point, Graph, Obstacle, Environment

def GetIntersection(p1,p2,q1,q2):
	#return the intersection of line segment p1-p2 and q1-q2
	#return Point(-1,-1) if there is no intersection
	#return Point(-2,-2) if the two line segments overlap
	if p1.y==p2.y:
		if q1.y==q2.y:# p1.y==p2.y  &  q1.y==q2.y:
			if q1.y!=p1.y:
				#print("Line:"+str(p1)+"-"+str(p2)+"and Line:"+str(q1)+"-"+str(q2)+" have NO intersection!")
				return Point(-1,-1)
			elif ( min(q1.x,q2.x)<p1.x<max(q1.x,q2.x) or min(q1.x,q2.x)<p2.x<max(q1.x,q2.x) or min(p1.x,p2.x)<q1.x<max(p1.x,p2.x) or min(p1.x,p2.x)<q1.x<max(p1.x,p2.x) or (min(p1.x,p2.x)==min(q1.x,q2.x) and max(p1.x,p2.x)==max(q1.x,q2.x))):
				print("Line:"+str(p1)+"-"+str(p2)+"and Line:"+str(q1)+"-"+str(q2)+" overlap!")
				return Point(-2,-2)
			elif ( max(p1.x,p2.x)<min(q1.x,q2.x) or min(p1.x,p2.x)>max(q1.x,q2.x) ):
				#print ("Line:"+str(p1)+"-"+str(p2)+"and Line:"+str(q1)+"-"+str(q2)+" have NO intersection!")
				return Point(-1,-1)
			elif (max(p1.x,p2.x)==min(q1.x,q2.x) or min(p1.x,p2.x)==max(q1.x,q2.x)):
				return Point(max(p1.x,p2.x),p1.y) if max(p1.x,p2.x)==min(q1.x,q2.x) else Point(min(p1.x,p2.x),y)
		else:# p1.y==p2.y  &  q1.y!=q2.y:
			y=p1.y
			slop_q=(q1.x-q2.x)*1.0/(q1.y-q2.y)
			x=x=slop_q*(y-q1.y)+q1.x
	else: 
		if q1.y==q2.y:#p1.y!=p2.y  &  q1.y==q2.y
			y=q1.y
			slop_p=(p1.x-p2.x)*1.0/(p1.y-p2.y)
			x=slop_p*(y-p1.y)+p1.x
		else: #p1.y!=p2.y  &  q1.y!=q2.y
			slop_p=(p1.x-p2.x)*1.0/(p1.y-p2.y)
			slop_q=(q1.x-q2.x)*1.0/(q1.y-q2.y)
			if slop_p!=slop_q:
				y=(q1.x-p1.x+slop_p*p1.y-slop_q*q1.y)*1.0/(slop_p-slop_q)
				x=slop_p*(y-p1.y)+p1.x
			# slop_p==slop_q:
			elif (p1.x-slop_p*p1.y)!=(q1.x-slop_q*q1.x):
				#print ("Line:",str(p1),"-",str(p2),"and Line:",str(q1),"-",str(q2)," have NO intersection!")
				return Point(-1,-1)
			elif ( min(q1.y,q2.y)<p1.y<max(q1.y,q2.y) or min(q1.y,q2.y)<p2.y<max(q1.y,q2.y) or min(p1.y,p2.y)<q1.y<max(p1.y,p2.y) or min(p1.y,p2.y)<q1.y<max(p1.y,p2.y) or (min(p1.y,p2.y)==min(q1.y,q2.y) and max(p1.y,p2.y)==max(q1.y,q2.y))):
				print("Line:"+str(p1)+"-"+str(p2)+"and Line:"+str(q1)+"-"+str(q2)+" overlap!")
				return Point(-2,-2)
			elif ( max(p1.y,p2.y)<min(q1.y,q2.y) or min(p1.y,p2.y)>max(q1.y,q2.y) ):
				#print ("Line:"+str(p1)+"-"+str(p2)+"and Line:"+str(q1)+"-"+str(q2)+" have NO intersection!")
				return Point(-1,-1)
			elif (max(p1.y,p2.y)==min(q1.y,q2.y) or min(p1.y,p2.y)==max(q1.y,q2.y)):
				return Point((slop_p*max(p1.y,p2.y)-slop_p*p1.y+p1.x),max(p1.y,p2.y)*1.0) if max(p1.y,p2.y)==min(q1.y,q2.y) else Point((slop_p*min(p1.y,p2.y)-slop_p*p1.y+p1.x),min(p1.y,p2.y)*1.0)

	if (min(p1.x,p2.x)<=x<=max(p1.x,p2.x)) and (min(q1.x,q2.x)<=x<=max(q1.x,q2.x)):
		return Point(x,y)
	else:
		#print ("Line:",str(p1),"-",str(p2),"and Line:",str(q1),"-",str(q2)," have NO intersection!")
		return Point(-1,-1)

def NearestPoint(p1,p2,q):
	# return the nearest point in the line segment p1-p2 to point q
	# return Point(-1,-1) if point q is in the line segment p1-p2
	if p1.y!=p2.y and q.x==(p1.x-p2.x)*(q.y-p1.y)/(p1.y-p2.y)+p1.x : 	# q is in the line  &  the line is horizontal
		# q is NOT in the line segment
		if q.y>max(p1.y,p2.y) or q.y<min(p1.y,p2.y) :
			return Point(((p1.x-p2.x)*(max(p1.y,p2.y)-p1.y)/(p1.y-p2.y)+p1.x),max(p1.y,p2.y)) if q.y>max(p1.y,p2.y) else Point(((p1.x-p2.x)*(min(p1.y,p2.y)-p1.y)/(p1.y-p2.y)+p1.x),min(p1.y,p2.y))
		# q is in the line segment
		else:
			print("point"+str(q)+"is in the line segment"+str(p1)+"-"+str(p2))
			return Point(-1,-1)
	# q is in the line  &  the line is NOT horizontal
	elif p1.y==p2.y==q.y:
		# q is NOT in the line segment
		if q.x>max(p1.x,p2.x) or q.x<min(p1.x,p2.x) :
			return Point(max(p1.x,p2.x)*1.0,p1.y) if q.x>max(p1.x,p2.x) else Point(min(p1.x,p2.x)*1.0,p1.y)
		# q is in the line segment
		else:
			print("point"+str(q)+"is in the line segment"+str(p1)+"-"+str(p2))
			return Point(-1,-1)
	# q is NOT in the line 
	else:
		if p1.y==p2.y: #horizontal line
			if min(p1.x,p2.x)<q.x<max(p1.x,p2.x):
				return Point(q.x,p1.y)
			else:
				return Point(min(p1.x,p2.x),p1.y) if (min(p1.x,p2.x)>=q.x) else Point(max(p1.x,p2.x),p1.y)
		elif p1.x==p2.x: #vertical line
			if min(p1.y,p2.y)<q.y<max(p1.y,p2.y):
				return Point(p1.x,q.y)
			else:
				return Point(p1.x,min(p1.y,p2.y)) if (min(p1.y,p2.y)>=q.y) else Point(p1.x,max(p1.y,p2.y))
		else: #oblique line
			slop=(p1.x-p2.x)*1.0/(p1.y-p2.y)
			y=(slop*p1.y-p1.x+q.y/slop)/(slop+1/slop)
			x=slop*(y-p1.y)+p1.x
			if min(p1.y,p2.y)<y<max(p1.y,p2.y):
				return Point(x,y)
			else:
				return p1 if ((p1.x-q.x)**2+(p1.y-q.y)**2)<((p2.x-q.x)**2+(p2.y-q.y)**2) else p2

		

#print(GetIntersection(Point(80,0),Point(80,200),Point(120,20),Point(60,100)))
#print(NearestPoint(Point(0,0),Point(1,1),Point(0,5)))