#!/usr/bin/python
import os
import sys
import subprocess

from parser import parseCharacters
from parser import getCurrentSpeaker

def main():
  #scene = open("full-script.txt");
  scene = open("scene-i-ii.txt");
  cast = open("dramatis-personae.txt",'r');
  fnull = open(os.devnull, 'w');
  volume = 7;

  characters = parseCharacters(cast);

  line = scene.readline()

  newChars = []

  while(line):
    
    if(line[0:4] != "    " and line.strip()):
      line = getCurrentSpeaker(line.strip())
      if line not in characters:
        print line
        if line not in newChars:
          newChars.append(line)

    line = scene.readline()

  print newChars


if __name__=="__main__":
  main();
