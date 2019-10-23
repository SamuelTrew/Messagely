import sys
import json
import re
from collections import OrderedDict
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image


def main():
   name: str = sys.argv[1]  # name of JSON file

   message_file: dict
   with open(name) as json_file:
      message_file = json.load(json_file)

   participants: list = message_file["participants"]
   me: str = participants[0]["name"]
   them: str = participants[1]["name"]
   messages: list = message_file["messages"]

   total: dict = OrderedDict()
   my_val: dict = OrderedDict()
   their_val: dict = OrderedDict()

   for message in messages:
      if "content" in message:
         sentence: str = message["content"]
         sentence = sentence.lower()

         word_list: list = re.findall("([a-zA-Z'-]+)", sentence)
         # word_list: list = sentence.split(" ")

         for word in word_list:
            if word not in total:
               total[word] = 1
            else:
               total[word] += 1
            if message["sender_name"] == me:
               if word not in my_val:
                  my_val[word] = 1
               else:
                  my_val[word] += 1
            elif message["sender_name"] == them:
               if word not in their_val:
                  their_val[word] = 1
               else:
                  their_val[word] += 1

   # print(total.__str__())

   ###########################################################
   ############# Plotting ####################################
   ###########################################################

   # Exclusion list of basic words
   exclusions: list = ["the", "to", "so", "do", "can", "are", "of", "on", "is", "that", "on", "is", "just", "in",
                       "it",
                       "a", "it's", "and", "at", "for", "was", "but", "be", "as", "too", "this", "or", "did", "with", "its"]

   # Lists of all the keys within a certain range from the keys and values from the dict
   keys: list = [key for (key, value) in total.items() if value > 1000 and key not in exclusions]
   values: list = [value for (key, value) in total.items() if value > 1000 and key not in exclusions]

   # Sort the lists based on the values
   keys = [x for _, x in sorted(zip(values, keys), reverse=True)]
   values.sort(reverse=True)
   values = np.array(values)

   ##### Resize image ##
   fig_size = plt.rcParams["figure.figsize"]
   fig_size[0] = 15
   fig_size[1] = 10
   plt.rcParams["figure.figsize"] = fig_size
   plt.rcParams["axes.facecolor"] = "black"
   #####################

   plot_me(keys, values)
   plot_them(keys, values)
   gen_wordcloud(total, exclusions)


def plot_me(keys: list, values: list):
   fig, ax = plt.subplots()
   y_pos: list = np.arange(len(keys))

   ax.barh(y_pos, values, align="center")
   ax.set_yticks(y_pos)
   ax.set_yticklabels("")
   ax.invert_yaxis()
   ax.set_xlabel("Frequency")

   plt.savefig("me.svg", bbox_inches="tight")


def plot_them(keys: list, values: list):
   fig, ax = plt.subplots()
   y_pos: list = np.arange(len(keys))

   ax.barh(y_pos, values, align="center")
   ax.set_yticks(y_pos)
   ax.set_yticklabels(keys)
   ax.invert_yaxis()
   ax.invert_xaxis()
   ax.set_xlabel("Frequency")

   plt.savefig("them.svg", bbox_inches="tight")


def gen_wordcloud(total: dict, exclusions: list):
   cloud_dict: dict = OrderedDict()
   for (k, v) in total.items():
      if v > 100 and k not in exclusions:
         cloud_dict[k] = v

   mask: np.array = np.array(Image.open("mask.png"))

   wordcloud = WordCloud(width=1000, height=500, relative_scaling=1, mask=mask).generate_from_frequencies(cloud_dict)

   plt.imshow(wordcloud, interpolation='bilinear')
   plt.axis("off")
   wordcloud.to_file("wordcloud.png")


if __name__ == "__main__":
   main()
