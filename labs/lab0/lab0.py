########################################################################################################################
# Class: Computer Networks
# Date: 02/03/2020
# Lab0: Getting Started with Python
# Goal: Learning the basics of Python
# Student Name: Brian Le
# Student ID: 916970215
# Student Github Username: brian-tle
# Instructions: Complete the TODO sections for each problem
# Guidelines: Read each problem carefully, and implement them correctly. Grade is based on lab correctness/completeness
#               No partial credit will be given. Labs #0 and #1 must be submitted by Monday Feb 3rd at 7:00 pm
#               No unit test are provided for lab #0
########################################################################################################################
import unittest # don't modify this line of code.
########################## Problem 0: Print  ###########################################################################
"""
Print your name, student id and Github username
Sample output:
Name: Jose
SID: 91744100
Github Username:
"""
name = "Brian Le" # TODO: your name
SID = 916970215 # TODO: your student id
git_username = "brian-tle" # TODO: your github username
print(name)
print(SID)
print(git_username)
print('\n')

########################## Problem 1: Processing user input ############################################################
"""
Accept two int values from the user, and print their product. If their product is greater than 500, then print their sum

Sample output:
Enter the first integer: 2
Enter the second integer: 4
Result is 8
Enter the first integer: 2
Enter the second integer: 1000
Result is 1002
"""
print("Problem 1 ********************") # problem header (don't modify)
# TODO: your code here
problem_1_a = input("Enter the first integer: ")
problem_1_b = input("Enter the second integer: ")

problem_1_sum = int(problem_1_a) + int(problem_1_b)
if (problem_1_sum > 500):
	print("Result is: " + str(problem_1_sum))
else:
	problem_1_product = int(problem_1_a) * int(problem_1_b)
	print("Result is: " + str(problem_1_product))

########################## Problem 2: String Processing ##############################################################
"""
Given a string print the number of times the string "Alice" appears anywhere in the given string

For example, given the string: "Alice and Bob go to the same school. They learned today in class how to treat a lice 
infestation, and Alice found the lecture really interesting", the sample output would be: 
Alice appeared 2 times. 
"""
print("Problem 2 ********************") # problem header (don't modify)
# the given string
myString = "Alice and Bob go to the same school. They learned today in class how to treat a lice" \
           "infestation, and Alice found the lecture really interesting"
# TODO: your code here
problem_2_count = 0
problem_2_split = myString.split(" ")

for substring in problem_2_split:
	if substring == "Alice":
		problem_2_count += 1

print("Alice appeared " + str(problem_2_count) + " times")

########################## Problem 3: Loops ############################################################################
"""
Given a list of numbers iterate over them and output the sum of the current number and previous one.

Given: [5, 10, 24, 32, 88, 90, 100] 
Outputs: 5, 15, 34, 56, 120, 178, 190.
"""
print("Problem 3 ********************") # problem header (don't modify)
numbers = [5, 10, 24, 32, 88, 90, 100]
# TODO: your code here
print("Given: " + str(numbers))
problem_3_list = []
for i in range(len(numbers)):
	#temp = numbers[i] + numbers[i - 1]
	#Couldnt figure out how to make it not out of range for i = 0
	if i == 0:
		temp = numbers[i]
		problem_3_list.append(temp)
	else:
		temp = numbers[i] + numbers[i - 1]
		problem_3_list.append(temp)

print("Outputs: " + str(problem_3_list))

########################## Problem 4: Functions/Methods/Lists ##########################################################
"""
Create the method mergeOdds(l1, l2) which takes two unordered lists as parameters, and returns a new list with all the 
odd numbers from the first a second list sorted in ascending order. Function signature is provided for you below

For example: Given l1 = [2,1,5,7,9] and l2 = [32,33,13] the function will return odds = [1,5,7,9,13,33] 
"""
print("Problem 4 ********************") # problem header (don't modify)
# function skeleton
def merge_odds(l1, l2):
    odds = []
    # TODO: your code here
    problem_4_join_list = l1 + l2

    for i in problem_4_join_list:
    	if i % 2 == 1:
    		odds.append(i)

    odds.sort()
    return odds
l1 = [2,1,5,7,9]
l2 = [32,33,13]
odds = merge_odds(l1, l2)
print("Given l1 = " + str(l1) + " and l2 = " + str(l2))
print("odds output: " + str(odds))

########################## Problem 5: Functions/Methods/Dictionaries ###################################################
"""
Refactor problem #4 to return a python dictionary instead a list where the keys are the index of the odd numbers in l1,
and l2, and the values are the odd numbers. 

For example: Given l1 = [2,1,5,7,9] and l2 = [32,33,13] the function will return odds = {1: [1, 33], 2: [5,13], 3: [7], 4: [9]} 
"""
print("Problem 5 ********************") # problem header
# function skeleton
def merge_odds(l1, l2):
    odds = {}
    # TODO: your code here
    problem_5_dict = dict()
    list1 = []
    list2 = []
    for i in l1:
    	if i % 2 == 1:
    		list1.append(i)

    for i in l2:
    	if i % 2 == 1:
    		list2.append(i)

    list1.sort()
    #list2.sort() no sort for this one

    for i in range(len(list1)):
    	if (i < len(list2)):
    		problem_5_dict[i + 1] = [list1[i], list2[i]]
    	else:
    		problem_5_dict[i + 1] = [list1[i]]

    	#print(problem_5_dict)
    odds = problem_5_dict

    return odds

l1 = [2,1,5,7,9]
l2 = [32,33,13]
odds = merge_odds(l1, l2)
print("Given l1 = " + str(l1) + " and l2 = " + str(l2))
print("Dictionary odds: " + str(odds))
