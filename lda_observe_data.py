import json
import os
import numpy as np
from datetime import date
from collections import OrderedDict

filename = 'news_2016_adding_topic_5.json'
dir_name = filename.split('.')[0]
#os.mkdir(dir_name)
with open(filename, 'r') as f:
  data = json.load(f)

print(data.keys())
max_topic_idx = max(data['topic'].values())
num_documents = len(data['title'].values())
timeline = [[] for i in range(max_topic_idx + 1)]
min_d_i = min(list(map(lambda x: int(x), list(data['topic'].keys()))))
max_d_i = max(list(map(lambda x: int(x), list(data['topic'].keys()))))

# Cluster documents by their topics
for d_i in range(len(list(data['topic'].values()))):
  topic_idx = list(data['topic'].values())[d_i]
  timeline[topic_idx].append(min_d_i + d_i)

# For each topic, Sort the documents using their date
sorted_timeline = [[] for i in range(max_topic_idx + 1)]

for topic_idx, topic in enumerate(timeline):
  initial_date = data[' time'][str(topic[-1])].split(" ")[0]
  within_day = []
  topic.reverse()
  for d_i in topic:
    d_date = data[' time'][str(d_i)].split(" ")[0]
    # Same Date
    if d_date == initial_date:
      within_day.append(d_i)
    else:
      sorted_timeline[topic_idx].append(within_day)
      initial_date = d_date
      within_day = [d_i]


# For now, time chunk: 1 day  
event_dict = OrderedDict()
for topic_idx, topic in enumerate(sorted_timeline):
  year, month, day = data[' time'][str(topic[0][0])].split(" ")[0].split("-")
  start_date = date(int(year), int(month), int(day))
  year, month, day = data[' time'][str(topic[-1][0])].split(" ")[0].split("-")
  end_date = date(int(year), int(month), int(day))
  total_days = (end_date - start_date).days
  total_article = sum(list(map(lambda x: len(x), topic)))
  mu = float(total_article) / float(total_days)
  sigma = np.std(list(map(lambda x: len(x), topic)))

  print(f"1 - sigma bordor line for topic {topic_idx} : mu: {mu}, sigma: {sigma} - mu + 2*sigma: {mu + 2*sigma}")
  events = list(filter(lambda x: len(x) > mu + 2*sigma, topic))
  event_dict[str(topic_idx)] = events

# For each topic, calculate mean and std of newspaper articles appearing in a day.
# If a day contains newspaper article more than mean + 1*\sigma, consider it as an event.
for keys in event_dict.keys():
  print(f"biggest event in topic : {keys}")
  biggest_event = max(event_dict[keys], key=len)

  with open(f'{dir_name}/{dir_name}_topic_{keys}_biggest_event_titles.txt', 'wb') as f:
    for idx in biggest_event:
      f.write((data['title'][str(idx)] + '\n').encode())
