import sys
import json
import re
from collections import defaultdict


def main():
   name: str = sys.argv[1]    # name of JSON file

   message_file: dict
   with open(name) as json_file:
      message_file = json.load(json_file)

   participants: list = message_file["participants"]
   me: str = participants[0]["name"]
   them: str = participants[1]["name"]
   messages: list = message_file["messages"]

   total: dict = defaultdict(int)
   my_val: dict = defaultdict(int)
   their_val: dict = defaultdict(int)

   for message in messages:
      if "content" in message:
         sentence: str = message["content"]
         sentence = sentence.lower()

         word_list: list = re.findall("[A-Za-z]+", sentence)

         for word in word_list:
            total[word] += 1
            if message["sender_name"] == me:
               my_val[word] += 1
            elif message["sender_name"] == them:
               their_val[word] += 1

   print(total.__str__())


if __name__ == "__main__":
   main()
