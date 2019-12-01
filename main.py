import sys
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image, ImageDraw
from datetime import datetime
import random
from collections import OrderedDict

from parser import Parser

their_name: str = ""

def main():
   global their_name
   parser = Parser()
   name: str = sys.argv[2]       # name of JSON file
   platform: str = sys.argv[1]   # platform of messages

   if platform == "messenger":
      parser.parse_messenger(name)
   elif platform == "whatsapp":
      parser.parse_whatsapp(name)

   me_message_count: int = parser.me_message_count
   them_message_count: int = parser.them_message_count
   me_word_count: int = parser.me_word_count
   them_word_count: int = parser.them_word_count
   my_val: dict = parser.my_val
   their_val: dict = parser.their_val
   total: dict = parser.total
   messages: list = parser.messages
   their_name = parser.their_name

   ###########################################################
   ############# Plotting ####################################
   ###########################################################

   messages_per_person(me_message_count, them_message_count)
   words_per_person(me_word_count, them_word_count)

   # Exclusion list of basic words
   exclusions: list = ["the", "to", "so", "do", "can", "are", "of", "on", "is", "that", "on", "is", "just", "in",
                       "it", "a", "it's", "and", "at", "for", "was", "but", "be", "as", "too", "this", "or", "did",
                       "with", "its", "i", "you", "u", "have", "if", "me", "he", "her", "your", "not"]

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
   #####################

   my_values: list = []
   their_values: list = []
   for key in keys:
      if key in my_val:
         my_values.append(my_val[key])
      else:
         my_values.append(0)

      if key in their_val:
         their_values.append(their_val[key])
      else:
         their_values.append(0)

   if platform == "messenger":
      plot_bar_me(keys, my_values)
      plot_bar_them(keys, their_values)
      gen_start(messages[-1]["timestamp_ms"])

   gen_wordcloud(total, exclusions)


# Produces your bar graph of your frequency for most used words
def plot_bar_me(keys: list, values: list):
   fig, ax = plt.subplots(facecolor="black")
   y_pos: list = np.arange(len(keys))

   ax.barh(y_pos, values, align="center", color="blue")
   ax.set_yticks(y_pos)
   ax.set_yticklabels("")
   ax.invert_yaxis()
   ax.set_xlabel("Frequency")
   ax.set_clip_on(False)
   ax.spines['bottom'].set_color("white")
   ax.xaxis.label.set_color("white")
   ax.tick_params(axis='x', colors="white")

   plt.savefig("{}/me.svg".format(their_name), bbox_inches="tight", facecolor=fig.get_facecolor(), transparent=True)


# Produces their bar graph of their frequency for most used words
def plot_bar_them(keys: list, values: list):
   fig, ax = plt.subplots(facecolor="black")
   y_pos: list = np.arange(len(keys))

   ax.barh(y_pos, values, align="center", color="deeppink")
   ax.set_yticks(y_pos)
   ax.set_yticklabels(keys)
   ax.invert_yaxis()
   ax.invert_xaxis()
   ax.set_xlabel("Frequency")
   ax.set_clip_on(False)
   ax.spines['bottom'].set_color("white")
   ax.spines['left'].set_color("white")
   ax.xaxis.label.set_color("white")
   ax.tick_params(axis='x', colors="white")
   ax.tick_params(axis='y', colors="white")

   plt.savefig("{}/them.svg".format(their_name), bbox_inches="tight", facecolor=fig.get_facecolor(), transparent=True)


# Generate the wordcloud image from the input data
def gen_wordcloud(total: dict, exclusions: list):
   cloud_dict: dict = OrderedDict()
   for (k, v) in total.items():
      # if v > 100 and k not in exclusions:
      if v > 1 and k not in exclusions:
         cloud_dict[k] = v

   mask: np.array = np.array(Image.open("mother.png"))
   # mask: np.array = np.array(Image.open("mask.png"))

   # wordcloud = WordCloud(width=1000, height=500, relative_scaling=1, mask=mask).generate_from_frequencies(cloud_dict)
   wordcloud = WordCloud(width=2000, height=2000, relative_scaling=1, mask=mask, background_color="white").generate_from_frequencies(cloud_dict)
   wordcloud.recolor(color_func=recolour, random_state=3)

   plt.imshow(wordcloud, interpolation='bilinear')
   plt.axis("off")
   wordcloud.to_file("{}/wordcloud.png".format(their_name))


# Recolour function to change the wordcloud text colours
# I chose the RGB values between the values of two colours
def recolour(word, font_size, position, orientation, random_state=None, **kwargs):
   # red: int = random.randint(0, 255)
   # green: int = random.randint(0, 20)
   # blue: int = random.randint(147, 255)

   red: int = random.randint(0, 32)
   green: int = random.randint(100, 178)
   blue: int = random.randint(0, 170)

   return "rgb({0}, {1}, {2})".format(red, green, blue)


# Used as a helper function to calculate the pie chart
def func(pct, allvals):
   absolute = int(pct / 100. * np.sum(allvals))
   return "{:.1f}%\n({:d})".format(pct, absolute)


# Produces an image that shows the pie ratio for number of messages sent per person
def messages_per_person(me: int, them: int):
   fig, ax = plt.subplots(figsize=(3, 3), subplot_kw=dict(aspect="equal"), facecolor="black")

   wedges, _, autotexts = ax.pie([me, them], autopct=lambda pct: func(pct, [me, them]), textprops=dict(color="w"), colors=["blue", "deeppink"])
   plt.setp(autotexts, size=8, weight="bold")
   ax.set_title("Messages per Person", color="white")
   ax.set_clip_on(False)

   plt.savefig("{}/messages.svg".format(their_name), facecolor=fig.get_facecolor())


# Produces an image that shows the pie ratio for number of words sent per person
def words_per_person(me: int, them: int):
   fig, ax = plt.subplots(figsize=(3, 3), subplot_kw=dict(aspect="equal"), facecolor="black")

   wedges, _, autotexts = ax.pie([me, them], autopct=lambda pct: func(pct, [me, them]), textprops=dict(color="w"), colors=["blue", "deeppink"])
   plt.setp(autotexts, size=8, weight="bold")
   ax.set_title("Words per Person", color="white")
   ax.set_clip_on(False)

   plt.savefig("{}/words.svg".format(their_name), facecolor=fig.get_facecolor())


# Produces an image that is the first day you started messaging the person
def gen_start(timestamp: int):
   timestamp = int("{}".format(timestamp)[:-3])
   date: str = datetime.utcfromtimestamp(timestamp).strftime("%d-%m-%Y")

   img = Image.new('RGB', (100, 40), (0, 0, 0))
   d = ImageDraw.Draw(img)
   d.text((20, 15), date, fill="purple")
   img.save("{}/start.png".format(their_name))


if __name__ == "__main__":
   main()
