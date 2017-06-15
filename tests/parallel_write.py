#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This script starts {nprocess} python processes in parallel, each process runs
write.py to write a local file stream into Alluxio.

By default, each python process has an ID, starting from 0, for each process,
the local file data/5mb.txt is written to Alluxio /{root}/{ID}.txt, the log of
each python process is logs/{start time of this script}-{ID}.txt.

This script should be run directly under its parent directory.
"""

import argparse
from multiprocessing import Process
import os
import sys
import time

from write import write


script_start_time = '-'.join(time.ctime().split(' '))

parser = argparse.ArgumentParser(
    description='Start multiple python processes to write local file to Alluxio in parallel')
parser.add_argument('--nprocess', type=int, default=1,
                    help='number of python processes, each process runs write.py')
parser.add_argument('--root', default='/alluxio-py-test',
                    help='root directory for all the data written to Alluxio')
parser.add_argument('--host', default='localhost',
                    help='Alluxio proxy server hostname')
parser.add_argument('--port', type=int, default=39999,
                    help='Alluxio proxy server web port')
parser.add_argument('--src', default='data/5mb.txt',
                    help='path to the local file source')
args = parser.parse_args()

try:
    os.mkdir('logs')
except OSError:
    # logs already exists.
    pass


def run_write(process_id):
    log = 'logs/%s-%d.txt' % (script_start_time, process_id)
    dst = '%s/%d.txt' % (args.root, process_id)
    sys.stdout = open(log, 'w')
    write(args.host, args.port, args.src, dst)


start_time = time.time()
processes = []
for i in xrange(args.nprocess):
    p = Process(target=run_write, args=(i,))
    processes.append(p)
    p.start()
for p in processes:
    p.join()
elapsed_time = time.time() - start_time

print '%d seconds' % elapsed_time
