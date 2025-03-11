# Native
import argparse
from math import ceil
import csv
from datetime import datetime

# 3rd party
from scapy.all import *
from scapy.layers.l2 import Ether

# Local
from tables import *
from pktbuilder import build_pkt

class Config():
  """
  Wrapper class for program configurations
  """
  file = None
  data_type = None
  stage = None
  build_key = None
  probe_key = None
  destiny = None
  threads = None
  

def send_chunk(cfg: Config, lines: list, index: int, chunk_size: int):
  """
  Sends the csv lines as ethernets packets over virtual interfaces

  Params
  ------
  - cfg: Config
    - Program configs
  - lines: list
    - List of strings, each one being a line from csv
  - index: int
    - The thread index (starts on 0)
  - chunk_size: int
    - How many lines this thread must send
  """
  start_i = index * chunk_size
  end_i = start_i + chunk_size

  pkts = []
  ether_frame = Ether(dst=cfg.destiny)
  for l in lines[start_i:end_i]:
    payload = build_pkt(cfg.data_type, l)

    join_ctl = JoinControl(
      table_t = cfg.data_type.value,
      stage = cfg.stage,
      build_key = payload.fields.get(cfg.build_key),
      probe_key = payload.fields.get(cfg.probe_key),
      hash_key = 0x00,
      found = 0x00,
    )

    pkt = ether_frame / join_ctl / payload
    pkts.append(pkt)

  #iface = f"veth{index}" 
  iface = "veth9" # working one
  print(f"Thread {index} sending {len(pkts)} packets on iface {iface}")
  sendp(pkts, iface = iface, verbose=False)
  print(f"Thread {index} done")


def send_close(cfg: Config):
  """
  Sends a stage 0 packet to destiny (close)

  Params
  ------
  - cfg: Config
    - Program configs
  """
  ether_frame = Ether(dst=cfg.destiny)

  join_ctl = JoinControl(
      table_t = 0x00,
      stage = 0x00,
      build_key = 0x00,
      probe_key = 0x00,
      hash_key = 0x00,
      found = 0x00,
    )
  
  sendp(ether_frame / join_ctl, iface = 'veth9', verbose=False)
  

def split_workload(cfg: Config, lines: list):
  """
  Splits the work of sending the CSV as packets, between multiple threads

  Params
  ------
  - cfg: Config
    - Program configs
  - lines: list
    - List containing the lines of the CSV
  """
  size = len(lines)
  chunk_size = ceil(size / cfg.threads)

  threads = []

  for index in range(cfg.threads):
    thrd = threading.Thread(
      target=send_chunk,
      args=(cfg, lines, index, chunk_size)
    )
    threads.append(thrd)
    thrd.start()

  for index, thrd in enumerate(threads):
    thrd.join()


def parse_csv(file: str) -> list:
  """
  Reads a CSV and returns it as lines
  
  Params
  ------
  - file: str
    - File path

  Return
  ------
  - lines: list
    - List where each element is a parsed line of the CSV
  """
  lines = []

  try:
    with open(file, mode = 'r') as file:
      csvFile = csv.reader(file, delimiter='|')
      for line in csvFile:
        lines.append(line)
  except Exception as e:
    print(f'Error while trying to read file {file}', file=sys.stderr)
    exit(1)

  return lines


def run(cfg: Config):
  if cfg.stage == 0:
    send_close(cfg)
    return

  start = datetime.now()
  print(f"Send starting on {start}")

  lines = parse_csv(cfg.file)

  split_workload(cfg, lines)

  end = datetime.now()
  print(f"Send done at {end}")
  print(f"Elapsed time {end - start}")


def get_args():
  parser = argparse.ArgumentParser(
    description="Send SSB dataset as packets via veths"
  )

  # Tables flags
  t_group = parser.add_mutually_exclusive_group(required=True)

  t_group.add_argument("-l", nargs=1, type=str, help="Use table type lineorder")
  t_group.add_argument("-c", nargs=1, type=str, help="Use table type customer")
  t_group.add_argument("-s", nargs=1, type=str, help="Use table type supplier")
  # t_group.add_argument("-d", nargs=1, type=str, help="Use table type date")
  # t_group.add_argument("-p", action="store_true", help="Use table type part")

  parser.add_argument("--stage", type=int,
                         help="Which stage to send")

  # Number of threads to use
  parser.add_argument(
    "-t", "--threads", type=int, default=1,
    help="Number of threads to use (default: 1)",
  )

  # Key field
  parser.add_argument(
    "-bk", "--build-key", type=str, required=True, help="Key to be used on build"
  )
  parser.add_argument(
    "-pk", "--probe-key", type=str, required=True, help="Key to be used on probe"
  )

  # Destiny field
  parser.add_argument(
    "--dst", type=str, default='00:00:00:00:00:03',
    help="Destiny MAC (default: '00:00:00:00:00:03')"
  )

  return parser.parse_args()


if __name__ == "__main__":
  args = get_args()

  cfg = Config()

  data_t = 0
  file = None
  if args.c:
    data_t = TableType.CUSTOMER
    file = args.c[0]
  elif args.l:
    data_t = TableType.LINEORDER
    file = args.l[0]
  elif args.s:
    data_t = TableType.SUPPLIER
    file = args.s[0]
  # elif args.d:
  #   data_t = TableType.DATE
  #   file = args.d[0]
  # elif args.p:
  #   data_t = TableType.PART

  cfg.data_type = data_t
  cfg.stage = args.stage
  cfg.file = file
  cfg.build_key = args.build_key
  cfg.probe_key = args.probe_key
  cfg.destiny = args.dst
  cfg.threads = args.threads

  run(cfg)
