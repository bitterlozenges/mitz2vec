'''
    Functions I used for analysis 
    l m a o
'''
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
import json
import matplotlib.pyplot as plt
import seaborn as sns
import bokeh
from sklearn.mixture import GaussianMixture as GMM
from sklearn.decomposition import PCA
import pandas as pd
from bokeh.plotting import figure, show
from bokeh.io import output_notebook
import hdbscan
import random

def adjListFromFile(fpath):
    ''' 
        function that constructs a dictionary 
        of nodes -> list of nodes they're connected to
        (an adjacency list representation of the graph)
        from a file
    '''
    adjList = {}
    with open(fpath, 'r') as f: 
        for i, line in enumerate(f): 
            # first line of a file is a marker 
            # of whether or not theg graph is 
            # weighted -- we know our 
            # graph isn't weighted so 
            # we don't care
            if i != 0: 
                totalList = line.strip().split(' ')
                adjList[totalList[0]] = [x.strip() for x in totalList[1:]]
    return adjList 


def testPrediction(fullGraph, partialGraph, model):
    '''
        given a full graph, a sparsified graph, 
        and a word2vec model for the sparsified graph, 
        this function returns a tuple of 
        
        (numExisting, numFound, numWrong) 
        
        for each vector representation of a node in the graph, 
        we take the top 10 most similar node-vectors
        as according to word2vec and see if there are links
        between them 
        
        
        numExisting += 1 implies that the link already exists
        in the sparsified graph 
        
        numFound += 1 implies that we correctly predicted a link
        that is not in the full graph but is in the sparsified graph
        
        numWrong +=1 implies the link is neither in the full graph
        nor the sparsified graph 
    '''
    numExisting, numFound, numWrong = 0, 0, 0
    for i, user_id in enumerate(model.vocab.keys()):
        most_similar = [t[0] for t in model.most_similar(user_id)]
        for similar_user in most_similar: 
            if similar_user in partialGraph[user_id]:
                numExisting += 1
            elif similar_user in fullGraph[user_id]: 
                numFound += 1 
            else: 
                numWrong += 1 
    return (numExisting, numFound, numWrong)


def randomBaseline(fullGraph, partialGraph, totalGuesses):
    '''
        function that returns the same output as
        testPrediction, except predicting
        random links each time 
        
        chooses from the list of nodes at each
        time and sees if the link later appears
        in the fullGraph
    '''
    numExisting, numFound, numWrong = 0, 0, 0
    total = list(partialGraph.keys())
    while totalGuesses > 0: 
        node1 = random.choice(total)
        node2 = random.choice(total)
        
        while node1 == node2: 
            node2 = random.choice(total)
            
        if node2 in partialGraph[node1]: 
            numExisting += 1
        elif node2 in fullGraph[node1]: 
            numFound += 1
        else: 
            numWrong += 1 
        
        totalGuesses -= 1 

    return (numExisting, numFound, numWrong)

def comparisonPlot(comparisonPercentage): 
    '''
        poorly named function that 
        returns a dictionary with keys 
        as word2vec file names and values
        as a tuple of return values 
        for (testPrediction, randomBaseline)
        
        
        basically, allows you to see how each word2vec
        model did against the random baseline 
    '''
    partialGraphPath = '..graphs/'
    partialGraphs = {}
    
    # get all the graphs 
    for filename in os.listdir(partialGraphPath): 
        if filename.endswith('.txt'):
            percentage = filename.split('_')[1][-1]
            partialGraphs[int(percentage)] = adjListFromFile(partialGraphPath + filename)
    modelsPath = '..models/' + str(comparisonPercentage)
    
    accuracyDict = {}
    
    # store all of the numExisting, numFound, numWrong for each model 
    comparisonPercentage = int(comparisonPercentage / 10) 
    for filename in os.listdir(modelsPath): 
        if filename.endswith('.txt'):
            model = Word2Vec.load(modelsPath + '/' + filename)
            model_guesses = testPrediction(partialGraphs[1], partialGraphs[comparisonPercentage], model)
            total_guesses = sum(model_guesses)
            accuracyDict[filename] = [model_guesses, randomBaseline(partialGraphs[1], partialGraphs[comparisonPercentage], total_guesses)]
    return accuracyDict 



# FUNCTIONS FOR PLOTTING FOUND BELOW 
# REALLY BAD CODE
# PYTHON GODS FORGIVE ME, FOR I HAVE SINNED 


def genDataFrames(comparisonDict): 
    # helper for genPlots
    order_mapping = {'.01': 0,'.005': 1, '.001': 2, '1': 0, '5': 1, '10': 2}
    dataFrames = [[None for _ in range(3)] for _ in range(3)]
    for k, v in comparisonDict.items(): 
        randomRestart, numDocs = k.split('_')[1], k.split('_')[2][:-4]
        word2vec, random = v[0], v[1]
        word2vec_correct = word2vec[1] / float(sum(word2vec))
        random_correct = random[1] / float(sum(random))
        df = pd.DataFrame({'method': ['word2vec', 'random'], 'correct': [word2vec_correct, random_correct]})
        dataFrames[order_mapping[numDocs]][order_mapping[randomRestart]] = df
    return dataFrames

def genPlots(comparisonDict): 
    # generate plots for comparison for one accuracyDict between 
    # random and predictions
    
    # our predictions were so much better than random that you can't even see
    # random on this bar plot so we should probably do this as at able instead 
    f, axes = plt.subplots(nrows = 3, ncols = 3, sharex = False, sharey = True, squeeze=False, figsize = (20,10))
    dataFrames = genDataFrames(comparisonDict)
    for i, ax in enumerate(axes): 
        for j, subplot in enumerate(ax): 
            df = dataFrames[i][j]
            sns.barplot(x = 'method', y = 'correct', data = df, ax = subplot, alpha = .8)

def genDataFramesTwo(comparisonDicts): 
    # helper fucntion for genPlotsTwo 
    order_mapping = {'.01': 0,'.005': 1, '.001': 2, '1': 0, '5': 1, '10': 2}
    sparsity_mapping = {0: '70%', 1: '80%', 2: '90%'}
    dataFrames = [[None for _ in range(3)] for _ in range(3)]
    for i, comparisonDict in enumerate(comparisonDicts): 
        for k, v in comparisonDict.items(): 
            randomRestart, numDocs = k.split('_')[1], k.split('_')[2][:-4]
            word2vec, random = v[0], v[1]
            word2vec_correct = word2vec[1] / float(sum(word2vec)) * 100
            random_correct = random[1] / float(sum(random)) * 100
            df = pd.DataFrame({'correct': [word2vec_correct], 'sparsity': [sparsity_mapping[i]]})
            og = pd.DataFrame()
            if dataFrames[order_mapping[numDocs]][order_mapping[randomRestart]] is not None:
                og = dataFrames[order_mapping[numDocs]][order_mapping[randomRestart]]
            dataFrames[order_mapping[numDocs]][order_mapping[randomRestart]] = og.append(df)
    return dataFrames

def genPlotsTwo(comparisonDicts): 
    # generates comparison plot of link prediction accuracy across all numbers
    # of documents and all random restart probabilities 
    f, axes = plt.subplots(nrows = 3, ncols = 3, sharex = False, sharey = True, squeeze=False, figsize = (20,10))
    dataFrames = genDataFramesTwo(comparisonDicts)
    for i, ax in enumerate(axes): 
        for j, subplot in enumerate(ax): 
            df = dataFrames[i][j]
            sns.barplot(x = 'sparsity', y = 'correct', data = df, ax = subplot, alpha = .8)
            subplot.set(ylabel='Correct % of Links Predicted')
    axes[0][0].set(ylabel = '100,000 Documents \n Correct % of Links Predicted')
    axes[1][0].set(ylabel = '500,000 Documents \n Correct % of Links Predicted ')
    axes[2][0].set(ylabel = '1,000,000 Documents \n Correct % of Links Predicted')
    axes[0][0].set_xlabel('Random Walk Restart Probability .01') 
    axes[0][1].set_xlabel('Random Walk Restart Probability .005')    
    axes[0][2].set_xlabel('Random Walk Restart Probability .001')    
    for i in range(3): 
        axes[0][i].xaxis.set_label_position('top')
    return 
        