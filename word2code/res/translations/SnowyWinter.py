from problem_utils import *

class SnowyWinter:
    def snowyHighwayLength(self, startPoints, endPoints):
        input_array0 = startPoints
        input_array1 = endPoints
        # Southern China is suffering from a heavily snowy winter.
        # The heavy snow even causes the closure of an important highway connecting southern and northern China.
        # You've got several reports containing the start and end points of highway segments covered by heavy snow.
        def covered(point): any(contains(range(start,end),point)) 
        # Given those reports as two int[]s startPoints and endPoints , you are to return the total length of highway segments covered by snow.
        return(total(length(highway(covered))))
        # Note that the reported segments may overlap.



def example0():
	cls = SnowyWinter()
	input0 = [17,85,57]
	input1 = [33,86,84]
	returns = 44
	result = cls.snowyHighwayLength(input0, input1)
	return result == returns


def example1():
	cls = SnowyWinter()
	input0 = [45,100,125,10,15,35,30,9]
	input1 = [46,200,175,20,25,45,40,10]
	returns = 132
	result = cls.snowyHighwayLength(input0, input1)
	return result == returns


def example2():
	cls = SnowyWinter()
	input0 = [4387,711,2510,1001,4687,3400,5254,584,284,1423,3755,929,2154,5719,1326,2368,554]
	input1 = [7890,5075,2600,6867,7860,9789,6422,5002,4180,7086,8615,9832,4169,7188,9975,8690,1423]
	returns = 9691
	result = cls.snowyHighwayLength(input0, input1)
	return result == returns


def example3():
	cls = SnowyWinter()
	input0 = [4906,5601,5087,1020,4362,2657,6257,5509,5107,5315,277,6801,2136,2921,5233,5082,497,8250,3956,5720]
	input1 = [4930,9130,9366,2322,4687,4848,8856,6302,5496,5438,829,9053,4233,4119,9781,8034,3956,9939,4908,5928]
	returns = 9510
	result = cls.snowyHighwayLength(input0, input1)
	return result == returns


def example4():
	cls = SnowyWinter()
	input0 = [51,807,943,4313,8319,3644,481,220,2161,448,465,1657,6290,22,6152,647,3185,4474,2168]
	input1 = [1182,912,1832,7754,9557,7980,4144,3194,7129,5535,1172,2043,6437,7252,9508,4745,8313,8020,4017]
	returns = 9535
	result = cls.snowyHighwayLength(input0, input1)
	return result == returns


def example5():
	cls = SnowyWinter()
	input0 = [8786,7391,201,4414,5822,5872,157,1832,7487,7518,2267,1763,3984,3102,7627,4099,524,1543,1022,3060]
	input1 = [9905,7957,3625,6475,9314,9332,4370,8068,8295,8177,7772,2668,7191,8480,9211,4802,2625,1924,9970,4180]
	returns = 9813
	result = cls.snowyHighwayLength(input0, input1)
	return result == returns



if __name__ == '__main__':
	print(example0())