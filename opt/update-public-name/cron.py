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

if __name__ == '__main__':
  ConfigurationFile = open(os.getcwd()+'/inc/configuration.json', "r")
  Configuration = json.loads(ConfigurationFile.read())
  ConfigurationFile.close()
  killer = GracefulKiller()
  ownpid = os.getpid()
  stream = journal.stream('cron.py')
  result = call("echo " + str(ownpid) + " > " + Configuration['TemporaryPath'] + Configuration['Application'] + ".pid", shell=True, stdout=stream )
  timekeeper = 0
  while True:
    time.sleep(Configuration['RefreshTime'])
    result = call("python3 " + Configuration['WorkingPath'] + Configuration['Application'] +".py", shell=True, stdout=stream )
    timekeeper = timekeeper + 1
    if timekeeper >= 360:
      ownpid = os.getpid()
      result = call("echo " + str(ownpid) + " > " + Configuration['TemporaryPath'] + Configuration['Application'] + ".pid", shell=True, stdout=stream )
      timekeeper = 0
    if killer.kill_now:
      break
