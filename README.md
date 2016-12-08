# person2vec: Distributed Representations of People in Vector Space 

## 1. Overview 

For this project we experimented with the twitter dataset. The preprocess\_snaps.py script in the scripts folder 
processes the twitter dataset found in the data folder and outputs adjacency lists based on the given 
parameters. As we are interested in testing link prediction, we generated a total of four graphs, which 
can be found in the graphs folder, three of which are purposefully sparsified. The graphs are in 
adjacency list formed, with a header line either 0 or 1 indicating whether or not the graph is weighted 
(the graphs are not weighted). The four graphs found in the graphs folder are: 

* twitter\_combine0.7\_lst.txt : sparisified twitter graph where 70% of the edges from original are kept
* twitter\_combine0.8\_lst.txt : sparisified twitter graph where 80% of the edges from original are kept
* twitter\_combine0.9\_lst.txt : sparsified twitter graph where 90% of the edges from original are kept
* twitter\_combine1\_lst.txt : original, full, twitter graph 

For each of these graphs, we write 9 text files (found in the text\_docs folder, within the subdirectory
that represents which sparsified graph we are looking at) from which we eventually
generate our word2vec model. We write so many different text files because we wish to vary the parameters 
of our random walk. Each text document has a corresponding word2vec models, found in the models folder (also
in the subdirectory corresponding to which sparsified graph we're talking about) 

The text documents (and corresponding models) are formatted as such: 

* twitter\_.001\_1.txt

The _ divides up the filename in to the name of the dataset, the probability of a random restart during
each random walk, and the number of documents written * 100,000. We varied the probability of 
a random restart to be one of .01, .005, and .001, and the number of documents to be 100,000, 500,000
and 1,000,000. 

From each of these text documents, we thne generated a corresponding word2vec model, which are found
in the models folder (as previously stated) 

The word2vec models were generated using the following command from gensim: 

    model = Word2Vec(LineSentence(full_name), size = 100, window = 5, min_count=100, workers=4)

The explanation of paramaters for which I will go in to more detail later

Once the word2vec models were generated, we are then given vector representations for nodes in the graph. 
We test to see if the word2vec similarity metric is good as a predictor by taking the top 10 most
word2vec similar vectors for nodes and seeing if any of those correspond to links in the full graph. 
Functions for comparing given a partial graph, a corresponding word2vec model for the partial graph, 
and a full graph are given in the scripts folder and also in the iPython notebook but don't touch my 
notebook because I don't mess with merge conflicts. 

We also compare against a random baseline, the script for which can also be found in the scripts folder. 


Hope this helps @tiff

