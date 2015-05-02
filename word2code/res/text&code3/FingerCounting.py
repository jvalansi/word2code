
class FingerCounting:
    def maxNumber(self, weakFinger, maxCount):
        input_int1 = weakFinger
        input_int2 = maxCount
        # Your little son is counting numbers with his left hand.  
        # Starting with his thumb and going toward his pinky, he counts each finger in order.
        # After counting his pinky, he reverses direction and goes back toward his thumb.  
        # He repeats this process until he reaches his target number.  		
        # He never skips a finger.  
        # For example, to count to ten, he would count: thumb, index, middle, ring, pinky, ring, middle, index, thumb, index.
        
        
        inf =1000
        fingers = [1, 2, 3, 4, 5, 4, 3, 2]*inf
        
        # Sadly, one of his fingers hurts and he can only count on it a limited number of times.  
        # His fingers are numbered 1 through 5 from thumb to pinky.  
        # You are given an int weakFinger, the finger that hurts, and an int maxCount, the maximum number of times he can use that finger.  
        valid = lambda(i): fingers[:i].count(input_int1) <=  input_int2
        
        #Return the largest number he can count to.
        #### return(largest(number for number in range(inf) if valid(number)))
        return(max(i for i in range(inf) if valid(i)))
        
        #If he cannot even begin counting, return 0.
#         if can_begin else 0

if __name__ == '__main__':
    weakFinger, maxCount = [2,3]
    fc = FingerCounting()
    print(fc.maxNumber(weakFinger, maxCount))
