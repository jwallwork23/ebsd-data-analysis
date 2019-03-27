import numpy as N

def disori(a,b,s):
	misori=[]
	for q in s:
		c = N.dot(a,dq(b,q))
		misori.append(c)
	dis= max(N.array(abs(N.array(misori))))
	return  dis

def euler2quat(euler):
	phi1=euler[0]
	phi=euler[1]
	phi2=euler[2]
	
	quat=N.array([0.0,0.0,0.0,0.0])
	quat[0]= N.cos(phi/2.)*N.cos((phi1+phi2)/2.)
	quat[1]=-N.sin(phi/2.)*N.cos((phi2-phi1)/2.)
	quat[2]= N.sin(phi/2.)*N.sin((phi2-phi1)/2.)
	quat[3]=-N.cos(phi/2.)*N.sin((phi1+phi2)/2.)
	quat=N.array(quat)
	if (quat[0]<0):
		quat=quat*-1
		
	return quat	


def dq(a,b): #quaternion product: q1q2=(s1,v1)(s2,v2)=(s1s2-v1.v2,s1v2+s2v1+v1xv2)
	mq=N.array([0.,0.,0.,0.])
	mq[0]=a[0]*b[0]-N.dot(a[1:4],b[1:4])
	mq[1:4]=a[0]*b[1:4]+b[0]*a[1:4]+N.cross(a[1:4],b[1:4])
	if (mq[0]<0):
		mq=-mq
	return mq
	


def symeq(group):

	qsym=[]
	qsym.append(N.array([1.0 , 0.0 , 0.0 , 0.0]))
	
	#from Pete Bate's fspl_orir.f90 code
	#cubic tetrads(100)
	
	qsym.append(N.array([0.7071068 , 0.7071068, 0.0, 0.0]))
	qsym.append(N.array([0.0 , 1.0 , 0.0, 0.0 ]))
	qsym.append(N.array([0.7071068 , -0.7071068, 0.0, 0.0]))
	
	qsym.append(N.array([0.7071068, 0.0, 0.7071068, 0.0 ]))
	qsym.append(N.array([0.0 , 0.0 , 1.0 , 0.0]))
	qsym.append(N.array([0.7071068, 0.0 ,-0.7071068, 0.0]))
	
	qsym.append(N.array([0.7071068, 0.0 , 0.0 , 0.7071068]))
	qsym.append(N.array([0.0 , 0.0 , 0.0 , 1.0]))
	qsym.append(N.array([0.7071068, 0.0 , 0.0 , -0.7071068]))
	
	#cubic dyads (110)
	
	qsym.append(N.array([0.0 , 0.7071068 , 0.7071068 , 0.0]))
	qsym.append(N.array([0.0 , -0.7071068 , 0.7071068 , 0.0]))
	
	qsym.append(N.array([0.0 , 0.7071068 , 0.0 , 0.7071068]))
	qsym.append(N.array([0.0 , -0.7071068 , 0.0 , 0.7071068]))
	
	qsym.append(N.array([0.0 , 0.0 , 0.7071068 , 0.7071068]))
	qsym.append(N.array([0.0 , 0.0 , -0.7071068 , 0.7071068]))
	
	#cubic triads (111)
	
	qsym.append(N.array([0.5, 0.5 , 0.5 , 0.5]))
	qsym.append(N.array([0.5, -0.5 , -0.5 , -0.5]))
	
	qsym.append(N.array([0.5, -0.5 , 0.5 , 0.5]))
	qsym.append(N.array([0.5, 0.5 , -0.5 , -0.5]))
	
	qsym.append(N.array([0.5, 0.5 , -0.5 , 0.5]))
	qsym.append(N.array([0.5, -0.5 , 0.5 , -0.5]))
	
	qsym.append(N.array([0.5, 0.5 , 0.5 , -0.5]))
	qsym.append(N.array([0.5, -0.5 , -0.5 , 0.5]))
	
	#hexagonal hexads
	
	qsym.append(N.array([0.866254 , 0.0 , 0.0 , 0.5]))
	qsym.append(N.array([0.5 , 0.0 , 0.0 , 0.866254]))
	qsym.append(N.array([0.5 , 0.0 , 0.0 , -0.866254]))
	qsym.append(N.array([0.866254 , 0.0 , 0.0 , -0.5]))
	
	#hexagonal diads
	
	qsym.append(N.array([0.0, -0.5 , 0.866254 , 0.0]))
	qsym.append(N.array([0.0, -0.5 , -0.866254 , 0.0]))
	
	if (group =='cubic'):
		symlist=qsym[0:24]
	if (group =='hexagonal'):
		symlist=[qsym[0], qsym[2], qsym[8]] + qsym[-6:30]
	
	return symlist