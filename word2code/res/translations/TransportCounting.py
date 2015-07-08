from utils import *

class TransportCounting:
    def countBuses(self, speed, positions, velocities, time):
        input_array0 = positions
        input_array1 = velocities
        input_int0 = speed
        input_int1 = time
        # You are studying public transportation, and you want to know how many buses are going down a particular one-way street every minute.
        # You are driving along the street by car, and counting the buses you meet or overtake.
        # After some time, you stop counting and report the result.
        # In this problem, you may assume that the street is a straight line, and that your car and all of the buses can only go along this line in the same direction.
        # You will be given an int, speed , giving your speed in meters per minute.
        # You will also be given a int[] positions , specifying how far ahead of you each of the buses is in meters at time 0, and a int[] velocities , specifying the velocities of the buses in meters per minute.
        # The i th element of velocities and the i th element of positions specify the velocity and position of the i th bus, respectively.
        # Finally, an int, time , tells you how many minutes you should count the buses you pass for.
        # You should return the number of buses you will overtake or meet during time minutes.
        # ROOT-0(root=return-3(nsubj=You-1, aux=should-2, dobj=number-5(det=the-4, prep_of=buses-7(rcmod=overtake-10(nsubj=you-8, aux=will-9, conj_or=meet-12, prep_during=minutes-15(nn=time-14))))))
        return(number(buses(overtake)))
        # If you meet one or several buses at the first or at the final moment, count them also.



def example0():
	cls = TransportCounting()
	input0 = 100
	input1 = [0]
	input2 = [0]
	input3 = 0
	returns = 1
	result = cls.countBuses(input0, input1, input2, input3)
	return result == returns


def example1():
	cls = TransportCounting()
	input0 = 5
	input1 = [10, 10]
	input2 = [0, 1]
	input3 = 2
	returns = 1
	result = cls.countBuses(input0, input1, input2, input3)
	return result == returns


def example2():
	cls = TransportCounting()
	input0 = 5
	input1 = [10, 10]
	input2 = [0, 1]
	input3 = 3
	returns = 2
	result = cls.countBuses(input0, input1, input2, input3)
	return result == returns


def example3():
	cls = TransportCounting()
	input0 = 777
	input1 = [10,20,30,40,50,60,70,80,90,100, 110,120,130,140,150,160,170,180,190,200, 210,220,230,240,250,260,270,280,290,300, 310,320,330,340,350,360,370,380,390,400, 410,420,430,440,450,460,470,480,490,500]
	input2 = [10,20,30,40,50,60,70,80,90,100, 110,120,130,140,150,160,170,180,190,200, 210,220,230,240,250,260,270,280,290,300, 310,320,330,340,350,360,370,380,390,400, 410,420,430,440,450,460,470,480,490,500]
	input3 = 333
	returns = 50
	result = cls.countBuses(input0, input1, input2, input3)
	return result == returns


def example4():
	cls = TransportCounting()
	input0 = 5
	input1 = [0,0,0]
	input2 = [4,5,6]
	input3 = 10
	returns = 3
	result = cls.countBuses(input0, input1, input2, input3)
	return result == returns



if __name__ == '__main__':
	print(example0())