OnlineLDA
=================

This Python code (based on the implementation of `ONLINE VARIATIONAL BAYES FOR 
LATENT DIRICHLET ALLOCATION` by Matthew D. Hoffman) uses the online Variational 
Bayes (VB) algorithm presented in the paper "Online Learning for Latent Dirichlet
Allocation" by Matthew D. Hoffman, David M. Blei, and Francis Bach.

The algorithm uses stochastic optimization to maximize the variational
objective function for the Latent Dirichlet Allocation (LDA) topic model.
It only looks at a subset of the total corpus of documents (namely, text files
whose content has been extracted from Web APIs documentation archives) 
each iteration, and thereby is able to find a locally optimal setting of
the variational posterior over the topics more quickly than a batch
VB algorithm could for large corpora.


##Files provided:
* `onlineldavb.py`: A package of functions for fitting LDA using stochastic
  optimization (by Matthew D. Hoffman).
* `online_lda_wsdl.py`: A Python script which uses online VB for LDA to analyze a 
  bunch of text files whose content has been extracted from SOAP API descriptors 
  (WSDLs). The script is based on Matthew D. Hoffman's 'onlinewikipedia.py'.
* `printtopics.py`: A Python script that displays the topics fit using the
  functions in onlineldavb.py and stores them as a text file in 'outcome/topics.txt'
  (based on the 'printtopics.py' script by Matthew D. Hoffman).
* `printtopicdistributions.py`: A Python script that displays the per-document topic 
  distributions and stores them as a text file in 'outcome/per-document-topics.txt' 
  (based on the 'printtopics.py' script by Matthew D. Hoffman).
* `dictnostops.txt`: A vocabulary of English words with the stop words removed.
* `plot_topic_distributions.m`: A simple octave script for displaying the per-document
  topic distribution of 12 text files analized by the algorithm (the files are selected at random).
* `onlinewikipedia.py` and `wikirandom.py` original scripts by Matthew D. Hoffman.
* `README.md`: This file.

You will need to have the numpy and scipy packages installed somewhere
that Python can find them to use these scripts.


##Example:
```
python online_lda_wsdl.py path/to/the/folder/of/textFiles 
python printtopics.py dictnostops.txt parameters/lambda-<#>.dat
python printtopicdistributions.py parameters/gamma-all.dat
```

This would run the algorithm for a number of iterations which depends on the size of 
the corpus, display the (expected value under the variational posterior of the) 
topics fit by the algorithm and the per-document-distributions.
