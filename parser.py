from collections import OrderedDict
import json
import re
import os


class Parser:

   def __init__(self):
      self.messages: list = []

      self.total: dict = OrderedDict()
      self.my_val: dict = OrderedDict()
      self.their_val: dict = OrderedDict()

      self.total_message_count: int = 0
      self.me_message_count: int = 0
      self.them_message_count: int = 0

      self.me_word_count: int = 0
      self.them_word_count: int = 0

      self.their_name: str = ""

   # Parses the messenger format of the file: JSON
   def parse_messenger(self, name: str):
      message_file: dict
      with open(name) as json_file:
         message_file = json.load(json_file)

      participants: list = message_file["participants"]
      me: str = participants[1]["name"]
      them = participants[0]["name"]
      self.their_name = them

      if not os.path.exists(them):
         os.mkdir(them)
      self.messages = message_file["messages"]

      for message in self.messages:
         self.total_message_count += 1

         if message["sender_name"] == me:
            self.me_message_count += 1
         else:
            self.them_message_count += 1

         if "content" in message:
            sentence: str = message["content"]
            sentence = sentence.lower()

            word_list: list = re.findall("([a-zA-Z'-]+)", sentence)

            for word in word_list:
               if word not in self.total:
                  self.total[word] = 1
               else:
                  self.total[word] += 1
               if message["sender_name"] == me:
                  self. me_word_count += 1
                  if word not in self.my_val:
                     self.my_val[word] = 1
                  else:
                     self.my_val[word] += 1
               elif message["sender_name"] == them:
                  self.them_word_count += 1

   # Parses the whatsapp format of the file: txt
   def parse_whatsapp(self, name: str):

      with open(name) as txt_file:
         self.messages = txt_file.readlines()

      me: str = ""
      them: str = ""

      # Get the names
      for m in self.messages:
         message: str = m[20:]
         find: int = message.find(":")
         if find != -1:
            if len(them) == 0:
               them = message[:find]
            elif len(me) == 0:
               if message[:find] != them:
                  me = message[:find]
            else:
               break

      self.their_name = them
      message_copy = self.messages

      # Get the filtered messages
      for i in range(len(message_copy)):
         message: str = message_copy[i][20:]
         find: int = message.find(":")
         if find != -1:
            self.messages[i] = message[find:]
         else:
            self.messages[i] = ""

      if not os.path.exists(them):
         os.mkdir(them)

      for message in self.messages:
         self.total_message_count += 1

         sentence: str = message.lower()
         word_list: list = re.findall("([a-zA-Z'-]+)", sentence)

         for word in word_list:
            if word not in self.total:
               self.total[word] = 1
            else:
               self.total[word] += 1
