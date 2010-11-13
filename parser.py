#!/usr/bin/python
import os
import sys
import subprocess

def parseCharacters(cast):
  line = cast.readline();
  chars = {}
  comps = []
  voices = []

  while(line):
    char,comp,voice = line.split(',')

    voice = voice.strip()

    chars[char] = {'computer':comp, 'voice':voice };

    if voice not in voices:
      voices.append(voice)

    if comp not in comps:
      comps.append(comp)

    line = cast.readline();

  chars["All"] = {};

  return chars,comps,voices;

def getCurrentSpeaker(line):
  current = line.strip("$");
  current = current.strip("\n");
  current = current.strip(":");
  return current

def call(command,fnull):
  result = subprocess.call(command, shell = True, stdout = fnull, stderr = fnull);
  return

def ssh(comp):
  return "ssh " + str(comp) + " -i ~/.ssh/ix_dsa"

def generateCommand(line,character,volume):
  command = "\"osascript -e \\\"set volume " + str(volume) + "\\\" > /dev/null; say \\\"" + line + "\\\" -v " + character["voice"] +"\"";
  return command

def main():
  #scene = open("temp-script.txt",'r');
  scene = open("scene-i-i.txt",'r');
  cast = open("dramatis-personae.txt",'r');
  fnull = open(os.devnull, 'w');
  debug = True;
  current = "ANNOUNCER"
  dirpath = "/home/users/ehamovit/Projects/hamlet/"
  count = 0;
  volume = 7;
  cutoff = 90;

  # CHARACTERS
  characters,computers,voices = parseCharacters(cast);

  # PRE-SCENE SETUP
  print "Setting volumes to " + str(volume) + ":"
  for comp in computers:
    command = ssh(comp) + " \"osascript -e \\\"set volume " + str(volume) + "\\\" > /dev/null \""
    print "  " + str(comp) + "...",
    call(command,fnull)
    print "done"

  # SCENE

  print("BEGINNING PLAY");

  line = scene.readline();

  while(line):
    # Ignore empty lines
    if(line == "" or line.strip() == ""):
      line = scene.readline()
      count += 1
      continue
    
    # Process real line
    if(line[0]=="$"):
      current = getCurrentSpeaker(line);

      if(debug):
        print current + "@" + characters[current]["computer"] + ":";

    else:
      line = line.strip();
      command = ssh(characters[current]["computer"]) + " " + generateCommand(line,characters[current],volume)

      print command

      if(debug):
        print "  " + line

      call(command,fnull);
      
    line = scene.readline();
    count += 1;
    sys.stdout.flush()

  scene.close()
  fnull.close()
  cast.close()

if __name__ == "__main__":
  main();
