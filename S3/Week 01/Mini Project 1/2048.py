"""
Created on Tue Jun 19 09:14:19 2016 AEST
@author: Sheng Li
"""

def merge(line):
    """
    This is a docstring for a function:

    Return a new list which is the result of merge
    """
    newline = [0]*len(line)
    count_num_in_newline = 0
    tmp_store = [num for num in line if num != 0]
    for line_number in range (len(tmp_store) - 1):  #merge near number if they equal
        if tmp_store[line_number] == tmp_store[line_number + 1]:
            tmp_store[line_number] = 2*tmp_store[line_number]
            tmp_store[line_number + 1] = 0
    for number in tmp_store:  #move number to newline
        if number != 0:
            newline[count_num_in_newline] = number
            count_num_in_newline += 1
    return newline
