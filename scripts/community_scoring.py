'''
Algorithm for scoring communities as a function of community 
significance factors, and potential fraud indicators. 

Goal of the algorithm is to return a prioritized list of 
the most influential communities that have the highest 
potential of fraudulent activity. 
'''

def count_fraud_indicators(G):
    counter = 0
    for edge in G.edges(data=True):
        if edge[-1]["properties"]['weight'] == 2:
            counter += 1
    print(f'Total potential fraud edges: {counter}')
    return counter