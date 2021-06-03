# Issue Trend Analysis in South Korea from 2015 to 2017

This project aims at finding the following given the corpus of new articles crawled from [Korea Herald](http://www.koreaherald.com/) in 2015-2017 (Crawled by IR&NLP Lab at School of Computing, KAIST, South Korea):
1. Find the top-10 most significant issues for each year and rank them (according to event frequency).
2. Discover **On-Issue** events, which is a sequence of temporally-relevant events that should be extracted from the article corpus.
3. Discover **Related-Issue** events, which is a set of relevant events that is not temporally-relevant (i.e., no cause-and-effect relation), but shares topical relevance.

## Dependency

Use the `kherald_env.yml` to initialize your conda environment as follows:

```
conda env -f kherald_env.yml
```

## Approach

### Top-10 Event Detection
To detect the top-10 events per year occurring within the articles, we take advantage of the topics clustered by [BERTopic](https://maartengr.github.io/BERTopic) and the fact that the **time** feature is given for each article.
We detect the abnormal number of article frequency along the temporal line and detect an event accordingly. This is based on the intuition that whenever an event occurs, then there is a sudden increase in the number of articles generate within a specific time frame. After extracting the events, we sort them according to the total number of articles per event, ending up with the top-10 events. We repeat this process for every year appearing in the corpus to reveal the year-wise top-10 events.

### On-Issue Event Analysis
Given that we have finished topic modeling and detected events according to the occurrence of articles per topic, we now have to classify whether two events $e1, e2$ are in an **On-Issue** relation or not. For example, assume we detected three events in topic \textbf{Government}; 1) North Korea nuclear missile experiment, 2) President Moon visits USA, 3) Trump criticize North Korean experiment. In this case, events 1) and 3) should be classified as on-issue while event 1) and 2) should not be.

Our work takes the following three steps to exploit topic modeling and the characteristic of the On-Issue articles:
1. Cluster same-topic articles via their BERT-embedding.
2. Calculate the pairwise document embedding similarity within the cluster. 
3. Sort the documents in time, and (iv) apply SRL-BERT for semantic role labeling (SRL) to extract the predicate argument structure to identify the two On-Issue documents.

### Related-Issue Event Analysis
Given a document $d_{i}$, related events can be tracked as follows. Topic modeling allows selecting set of documents $D_{t} = d_{t1}, d_{t2}, \dots d_{tn}$ such that the documents share topics. In our model, filtering On-Event articles of $d_{i}$ in $D_{t}$ will give us the related events. 

