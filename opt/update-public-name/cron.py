#!/usr/bin/python3
import signal
import time
import os
import json
from subprocess import call
from systemd import journal

class GracefulKiller:
  kill_now = False
  def __init__(self):
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)

  def exit_gracefully(self,signum, frame):
    self.kill_now = True

def WritePidFile():
    ownpid = os.getpid()
    try:
        PidFile = open(Configuration['TemporaryPath'] + Configuration['Application'] + ".pid","w")
        PidFile.write(str(ownpid))
        PidFile.close()
    except Exception as e:
        return 1
    else:
          return 0

if __name__ == '__main__':
  ConfigurationFile = open(os.getcwd()+'/inc/configuration.json', "r")
  Configuration = json.loads(ConfigurationFile.read())
  ConfigurationFile.close()
  killer = GracefulKiller()
  ownpid = os.getpid()
  stream = journal.stream('cron.py')
  result = WritePidFile()
  timekeeper = 0
  while True:
    time.sleep(Configuration['RefreshTime'])
    result = call("python3 " + Configuration['WorkingPath'] + Configuration['Application'] +".py", shell=True )
    timekeeper = timekeeper + 1
    if timekeeper >= 360:
      ownpid = os.getpid()
      result = WritePidFile()
      timekeeper = 0
    if killer.kill_now:
      break
