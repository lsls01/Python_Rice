"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    new_list = []
    for element in list1:
        if element not in new_list:
            new_list.append(element)
    return new_list

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    intersected_list = []
    for element_in_list2 in list2:
        if element_in_list2 in list1:
            intersected_list.append(element_in_list2)
    return intersected_list

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """
    index1 = 0
    index2 = 0
    new_list = []
    while index1 < len(list1) and index2 < len(list2):
        if list1[index1] < list2[index2]:
            new_list.append(list1[index1])
            index1 += 1
        else:
            new_list.append(list2[index2])
            index2 += 1
    if index1 == len(list1):
        new_list.extend(list2[index2:])
    else:
        new_list.extend(list1[index1:])
    return new_list
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1) < 2:
        return list1
    mid = len(list1) / 2
    left = list1[:mid]
    right = list1[mid:]
    sorted_left = merge_sort(left)
    sorted_right = merge_sort(right)
    return merge(sorted_left, sorted_right)

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if len(word) == 0:
        return ['']
        
    new_strings = []
    first_char = word[0]
    remained_chars = word[1:]
    remained_strings = gen_all_strings(remained_chars)
    
    for a_string in remained_strings:
        for idx in range(len(a_string)):
            new_strings.append(str(a_string[:idx]) + str(first_char)
                              + str(a_string[idx:]))
        new_strings.append(str(a_string) + str(first_char))
    
    return new_strings + remained_strings

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    url = codeskulptor.file2url(filename)
    netfile = urllib2.urlopen(url)
    words = []
    for line in netfile.readlines():
        words.append(line.strip())

    return words

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
# run()

    
    
