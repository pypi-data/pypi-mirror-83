#!/usr/bin/env python3
import os
import signal
import sys
import time
import gzip
import argparse
import queue
import subprocess
from multiprocessing import Process, Queue

from detectr.mlmodel import MLModel
from detectr.mvcmodel import MVCModelLearn, MVCModelWatch
from detectr.mvcview import MVCViewLearn, MVCViewWatch

PROGNAME = "detectr"
GITHUB = "https://github.com/detectr"
qq = Queue()


def read_loop(mvc_model, mvc_view):
	timeout = 0.1
	last_update = 0
	while True:
		try:
			line = qq.get(timeout=timeout)
		except queue.Empty:
			pass
		else:
			if line is None:
				mvc_model.stop()
				break
			line = line.decode("latin-1", "ignore")
			if line == "RESET":
				mvc_model.reset_for_additional_trace()
			else:
				mvc_model.add_line(line)
		if time.time() - last_update >= timeout:
			mvc_view.update()
			last_update = time.time()
	mvc_view.update()


def process_reader(q, cmd):
	proc = subprocess.Popen(
		["/bin/sh", "-c", "strace -f " + cmd],
		stdout=subprocess.DEVNULL,
		stderr=subprocess.PIPE
	)
	while True:
		line = proc.stderr.readline()
		if not line:
			break
		q.put(line)
	q.put(None)


def file_reader(q, filenames, follow=False, jump_to_end=False):
	try:
		for filename in filenames:
			with open(filename, "rb") as f:
				if jump_to_end:
					f.seek(0, os.SEEK_END)
				while True:
					line = f.readline()
					if not line:
						if follow:
							time.sleep(.1)
						else:
							break
					else:
						q.put(line)
			q.put(b"RESET")
	except KeyboardInterrupt:
		pass
	q.put(None)


def subcommand_learn(args):
	mvc_model = MVCModelLearn()
	mvc_view = MVCViewLearn(mvc_model)
	proc = None
	try:
		if args.cmd is not None:
			print("\033[32m|------ Executing " + PROGNAME + " in \033[1;32mlearning mode\033[0;32m ------|\033[0m")
			print("\033[32m|------ " + GITHUB + "         ------|\033[0m")
			proc = Process(target=process_reader, args=(qq, args.cmd,))
			proc.start()
			read_loop(mvc_model, mvc_view)
		else: # --strace is given
			print("\033[32m|------ Learning " + PROGNAME + " in \033[1;32mlearning mode\033[0;32m  ------|\033[0m")
			print("\033[32m|------ " + GITHUB + "         ------|\033[0m")
			proc = Process(target=file_reader, args=(qq, args.strace, args.follow, args.end))
			proc.start()
			read_loop(mvc_model, mvc_view)
	except KeyboardInterrupt:
		os.kill(proc.pid, signal.SIGKILL)
		sys.stdout.write("\r")
	# Write model to disc
	with gzip.open(args.output, "wb") as f:
		f.write(mvc_model.model().encode("latin-1"))
	print("\033[1;35m[\033[1;34m■\033[1;35m]\033[1;34m Model written to file", args.output, "\033[0m")


def subcommand_detect(args):
	print("\033[32m|------ Executing " + PROGNAME + " in \033[1;32mdetect mode\033[0;32m -----|\033[0m")
	print("\033[32m|------ " + GITHUB + "      ------|\033[0m")
	model = MLModel.from_file(args.model)
	mvc_model = MVCModelWatch(model=model)
	mvc_view = MVCViewWatch(mvc_model)
	if args.cmd is not None:
		Process(target=process_reader, args=(qq, args.cmd,)).start()
		read_loop(mvc_model, mvc_view)
	else:
		Process(target=file_reader, args=(qq, args.strace, args.follow, args.end)).start()
		read_loop(mvc_model, mvc_view)


# ---- COMMAND LINE ARGUMENT PARSING ----
parser = argparse.ArgumentParser(prog=PROGNAME)
subparser = parser.add_subparsers(help="commands")

# Learning

parser_learn = subparser.add_parser('learn', help="Build a model.")
parser_learn.add_argument('--output', required=True, type=str, help="Filename of model.")
group = parser_learn.add_mutually_exclusive_group(required=True)
group.add_argument('--cmd', type=str, help="Command to execute.")
group.add_argument('--strace', metavar="file", nargs='+', help="Read output of strace.")
# Arguments for --strace
parser_learn.add_argument('--follow', action='store_true')
parser_learn.add_argument('--end', action='store_true')
parser_learn.set_defaults(func=subcommand_learn)

# Detection

parser_detect = subparser.add_parser('detect', help="Detection.")
parser_detect.add_argument('--model', required=True, type=str, help="Filename of model.")
group = parser_detect.add_mutually_exclusive_group(required=True)
group.add_argument('--cmd', type=str, help="Command to execute.")
group.add_argument('--strace', metavar="file", nargs='+', help="Read output of strace.")
parser_detect.add_argument('--follow', action='store_true')
parser_detect.add_argument('--end', action='store_true')
parser_detect.set_defaults(func=subcommand_detect)


def main():
	# https://stackoverflow.com/q/48648036
	args = parser.parse_args()
	try:
		args.func(args)
	except AttributeError:
		parser.print_help()
		parser.exit()

if __name__ == "__main__":
	main()
