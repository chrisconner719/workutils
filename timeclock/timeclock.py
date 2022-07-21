#!/usr/bin/env python3

import argparse
import datetime
import os

from duration import getDurationHM



parser = argparse.ArgumentParser()
parser.add_argument("-w", "--worklog", type=str, required=True, help="The worklog file to append to.")
parser.add_argument("-p", "--payrate", type=float, required=True, help="The hourly pay rate for this job.")
parser.add_argument("--lock-format", type=str, default="LOCK_%s.lock", help="A format string determining the worklog lock filename, where %s represents the worklog filename.")
args = parser.parse_args()


# Make sure we have a worklog to append to
if not os.path.exists(args.worklog):
	while True:
		_ = input("The specified worklog does not exist. Create it? y/n: ")
		if _ == "y":
			with open(args.worklog, "w") as f:
				f.write("date,start,end,payrate,hours,subtotal\n")
			break
		elif _ == "n":
			raise RuntimeError("Worklog not found!")
		else:
			print("Invalid input.\n")


# Make sure nobody else writes to the worklog
worklog_dir = os.path.dirname(args.worklog)
if worklog_dir == "":
	worklog_dir = "."
worklog_fname = os.path.basename(args.worklog)
lock_fname = worklog_dir + "/" + args.lock_format % worklog_fname
try:
	with open(lock_fname) as f:
		raise RuntimeError(f"Lock already held by PID {f.read()}!")
except FileNotFoundError:
	with open(lock_fname, "w") as f:
		f.write(str(os.getpid()))


start = datetime.datetime.now()
date = str(start.date())
start = f"{start.hour}{start.minute}"

while True:
	_ = input("Enter CLOCKOUT when you're ready to clock out: ")
	if _ == "CLOCKOUT":
		break

end = datetime.datetime.now()
end = f"{end.hour}{end.minute}"

hours, minutes = getDurationHM(start, end)
hours_worked = round(hours + (minutes / 60), 2)
subtotal = round(args.payrate * hours_worked, 2)
print(f"You worked for {hours} hours and {minutes} minutes ({hours_worked} hours) for a pay of ${subtotal}.")

with open(args.worklog, "a") as worklog:
	worklog.write(",".join([str(i) for i in [date, start, end, args.payrate, hours_worked, subtotal]]) + "\n")

os.remove(lock_fname)
