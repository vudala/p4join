# Native
import argparse
from math import ceil
import csv
from datetime import datetime

# 3rd party
from scapy.all import *
from scapy.layers.l2 import Ether

# Local
from pkt.binds import *
from pkt.builder import build_bmark

# ifaces available
ifaces = [
  "veth8",
  "veth9",
  "veth16",
  "veth17",
  "veth32",
  "veth33"
]

class Config():
  """
  Wrapper class for program configurations
  """
  file = None
  data_type = None
  stage = None
  build_key = None
  probe_keys = None
  destiny = None
  threads = None
  algorithm = None


# Convert data into byterray
def to_bytes(data: any):
  ret = None
  side = None
  if type(data) == int:
    ret = data.to_bytes(length=4, byteorder='big')
    side = 'left'
  elif type(data) == str:
    ret = data.encode('ascii')
  elif type(data) == bytes:
    ret = data

  if ret:
    # If needed, pad the array up to fill the field
    clen = len(ret)
    if clen >= KEY_SIZE:
      return ret
    
    if side == 'left':
      return b'\x00' * (KEY_SIZE - clen) + ret

    return ret


def build_left_deep(cfg: Config, payload: any):
  return JoinControlLeftDeep(
    table_t = cfg.data_type.value,
    stage = cfg.stage,
    build_key = to_bytes(payload.fields.get(cfg.build_key)),
    probe_key = to_bytes(payload.fields.get(cfg.probe_keys[0])),
  )


def build_right_deep(cfg: Config, payload: any):
  return JoinControlRightDeep(
    table_t = cfg.data_type.value,
    stage = cfg.stage,
    build_key = to_bytes(payload.fields.get(cfg.build_key)),
    probe1_key = to_bytes(payload.fields.get(cfg.probe_keys[0])),
    probe2_key = to_bytes(payload.fields.get(cfg.probe_keys[1])),
  )


alg_args = {
  "left_deep" : build_left_deep,
  "right_deep" : build_right_deep
}


def build_alg(cfg: Config, payload: any):
  build_fn = alg_args[cfg.algorithm]

  return build_fn(cfg, payload)


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

  iface = ifaces[len(lines) % (index + 1)]
  ether_frame = Ether(dst=cfg.destiny)
  
  pkts = []

  for l in lines[start_i:end_i]:
    payload = build_bmark(cfg.data_type, l)

    join_control = build_alg(cfg, payload)

    pkt = ether_frame / join_control / payload
    pkts.append(pkt)
    pkt.show()

  print(f"Thread {index} sending {len(pkts)} packets on iface {iface}")
  # Cant increase pps because tofino2 will start dropping some pkts
  sendpfast(pkts, pps=3000, iface = iface)
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

  join_ctl = JoinControlRightDeep(
      table_t = 0x00,
      stage = 0x00,
      build_key = 0x00,
      probe1_key = 0x00,
      probe2_key = 0x00,
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
    description="Send dataset as packets via veths"
  )

  alg = parser.add_mutually_exclusive_group(required=True)
  alg.add_argument("-rd", "--right-deep",
                      action="store_true",
                      help="Use right deep algorithm")
  alg.add_argument("-ld", "--left-deep",
                      action="store_true",
                      help="Use left deep algorithm")

  bmark = parser.add_mutually_exclusive_group(required=True)
  bmark.add_argument("-ssb",
                      action="store_true",
                      help="Use SSB benchmark")
  bmark.add_argument("-tpch",
                      action="store_true",
                      help="Use TPC-H benchmark")

  parser.add_argument("-t", "--table",
                      type=str,
                      required=True,
                      help="Which table to use, check README to see options")
  
  parser.add_argument("file",
                      type=str,
                      help="Which dataset file to use")
  
  parser.add_argument("-s","--stage",
                      type=int, required=True,
                      help="Which stage to send")

  # Key field
  parser.add_argument(
    "-bk", "--build-key", type=str, required=True, help="Key to be used on build"
  )
  parser.add_argument(
    "-pks", "--probe-keys", nargs=2, required=True, help="Keys to be used on probe"
  )

  # Destiny field
  parser.add_argument(
    "--dst", type=str, default='00:00:00:00:00:03',
    help="Destiny MAC (default: '00:00:00:00:00:03')"
  )

  # Number of threads to use
  parser.add_argument(
    "--threads", type=int, default=1,
    help="Number of threads to use (default: 1)",
  )

  return parser.parse_args()


algorithms = ["left_deep", "right_deep"]

benchmarks = {
  "ssb" : {
    "lineorder" : TableType.SSB_LINEORDER,
    "supplier" :  TableType.SSB_SUPPLIER,
    "customer" :  TableType.SSB_CUSTOMER,
  },
  "tpch" : {
    "part" :      TableType.TPCH_PART,
    "supplier" :  TableType.TPCH_SUPPLIER,
    "partsupp" :  TableType.TPCH_PARTSUPP,
    "customer" :  TableType.TPCH_CUSTOMER,
    "lineitem" :  TableType.TPCH_LINEITEM,
    "order" :     TableType.TPCH_ORDER,
    "nation" :    TableType.TPCH_NATION,
    "region" :    TableType.TPCH_REGION
  }
}


if __name__ == "__main__":
  args = get_args()

  cfg = Config()

  data_t = 0
  file = None

  alg = "left_deep" if args.left_deep else "right_deep"
  bmark = "ssb" if args.ssb else "tpch"

  if not args.table in benchmarks[bmark]:
    print(f"Select valid table from {bmark} benchmark")
    exit(1)

  cfg.data_type = benchmarks[bmark][args.table]
  cfg.stage = args.stage
  cfg.file = args.file
  cfg.build_key = args.build_key
  cfg.probe_keys = args.probe_keys
  cfg.destiny = args.dst
  cfg.threads = args.threads
  cfg.algorithm = alg

  run(cfg)
