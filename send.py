# Native
import argparse
from math import ceil
import csv

# 3rd party
from scapy.all import *
from scapy.layers.l2 import Ether

# Local
from tables import *
from pktbuilder import build_pkt

class Config():
  file = None
  data_type = None
  ctl_type = None
  join_key = None
  destiny = None
  n_threads = None


# def flush():
#   pkts = []
#   ether_frame = Ether(dst=cfg.destiny)

#   for i in range(2 ** 16):
#     join_ctl = JoinControl(
#       table_t = 0x00,
#       ctl_type = cfg.ctl_type.value,
#       hash_key = 0x00,
#       inserted = 0x00,
#       data = i
#     )

#     pkt = ether_frame / join_ctl

#     pkts.append(pkt)

#   sendp(pkts, iface = "veth0", verbose=False)
  

def send_chunk(cfg: Config, lines: list, index: int, chunk_size: int):
  """
  Sends the csv lines as ethernets packets over virtual interfaces

  - params:
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
      ctl_type = cfg.ctl_type.value,
      hash_key = 0x00,
      inserted = 0x00,
      data = payload.fields.get(cfg.join_key)
    )

    pkt = ether_frame / join_ctl / payload

    pkts.append(pkt)

  print(f"Thread {index} sending {chunk_size} packets on iface veth{index}")

  sendp(pkts, iface = f'veth{index}', verbose=False)

  print(f"Thread {index} done")


def split_workload(cfg: Config, lines: list):
  size = len(lines)
  chunk_size = ceil(size / cfg.n_threads)

  threads = []

  for index in range(cfg.n_threads):
    thrd = threading.Thread(
      target=send_chunk,
      args=(cfg, lines, index, chunk_size)
    )
    threads.append(thrd)
    thrd.start()

  for index, thrd in enumerate(threads):
    thrd.join()


def run(cfg: Config):
  # if cfg.ctl_type == ControlType.FLUSH:
  #   flush()
  #   return

  lines = []
  try:
    with open(cfg.file, mode = 'r') as file:
      csvFile = csv.reader(file, delimiter='|')
      for line in csvFile:
        lines.append(line)
  except Exception as e:
    print(f'Error while trying to read file {cfg.file}', file=sys.stderr)
    exit(1)

  split_workload(cfg, lines)


def get_args():
  parser = argparse.ArgumentParser(
    description="Send SSB dataset as packets via veths"
  )

  # Tables flags
  t_group = parser.add_mutually_exclusive_group(required=True)

  t_group.add_argument("-l", nargs=1, type=str, help="Use table type lineorder")
  t_group.add_argument("-c", nargs=1, type=str, help="Use table type customer")
  t_group.add_argument("-s", nargs=1, type=str, help="Use table type supplier")
  t_group.add_argument("-d", nargs=1, type=str, help="Use table type date")
  # t_group.add_argument("-p", action="store_true", help="Use table type part")

  # Control type flag
  ctl_group = parser.add_mutually_exclusive_group(required=True)

  ctl_group.add_argument("--build", action="store_true",
                         help="Send table as build")
  ctl_group.add_argument("--probe", action="store_true",
                         help="Send table as probe")
  # ctl_group.add_argument("--flush", action="store_true",
  #                        help="Flush the hash tables")

  # Number of threads to use
  parser.add_argument(
    "-t", "--threads", type=int, default=1,
    help="Number of threads to use (default: 1)",
  )

  # Key field
  parser.add_argument(
    "-k", "--key", type=str, required=True, help="Which field to use as key"
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
  elif args.d:
    data_t = TableType.DATE
    file = args.d[0]
  elif args.s:
    data_t = TableType.SUPPLIER
    file = args.s[0]
  # elif args.p:
  #   data_t = TableType.PART

  ctl_t = 0
  if args.build:
    ctl_t = ControlType.BUILD
  elif args.probe:
    ctl_t = ControlType.PROBE
  elif args.flush:
    ctl_t = ControlType.FLUSH

  cfg.data_type = data_t
  cfg.ctl_type = ctl_t
  cfg.file = file
  cfg.join_key = args.key
  cfg.destiny = args.dst
  cfg.n_threads = args.threads

  run(cfg)
