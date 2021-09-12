import time

def sleeping(seconds):
  start_time = time.time()
  sleep_time = start_time + seconds
  while time.time() < sleep_time: pass

  