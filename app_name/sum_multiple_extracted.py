from django.urls import path
from django.shortcuts import HttpResponse, render

# This helped method is called from views.py in sum_multiples. 
# If the second number is larger than the first, we return an error.
# If the first number is larger than the second, we take all the multiples of the first number up until the second (larger) number
# i.e. if given 2, 8, it will sum 2+4+6+8 = 20. If given 2,9, it will be the same.
def main(num1, num2):
    return_string = ""
    if num1 > num2:
        return_string = 'Your second number must be greater than or equal to your first number'
    else:
        result = 0
        i = num1
        while i <= num2:
            result += i
            i += num1
        return_string = f"The sum of all multiples of {num1} below {num2} is {result}"
    return return_string