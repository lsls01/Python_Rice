"""
Function to generate permutations of outcomes
Repetition of outcomes not allowed
"""

def gen_permutations(outcomes, length):
    """
    Iterative function that generates set of permutations of
    outcomes of length num_trials
    No repeated outcomes allowed
    """
    if length == 0:
        return []
    
    if length == 1:
        return outcomes
    
    new_perm = []
    
    for idx in range(len(outcomes)):
        new_list = list(outcomes)
        new_list.pop(idx)
        sub_perm = gen_permutations(new_list, length - 1)
        
        for iter in sub_perm:
            new_iter = str(outcomes[idx]) + str(iter)
            new_perm.append(new_iter)
    
    return new_perm
    

def run_example():

    outcome = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    length = 3
    permtutations = gen_permutations(outcome, length)
    print "Computed", len(permtutations), "permutations of length", str(length)
    print "Permutations were", sorted(permtutations)

run_example()
