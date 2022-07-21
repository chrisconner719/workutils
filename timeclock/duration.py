#!/usr/bin/env python3

# Given two 24-hour time strings like "2130" and "0210", this function returns the duration in hours and minutes.
# It takes into account instances where the start time is in the evening and end time is in the morning.
def getDurationHM(start, end):
	start_hour = int(start[0:2])
	start_minute = int(start[2:4])
	end_hour = int(end[0:2])
	end_minute = int(end[2:4])
	if start_hour > end_hour:
		end_hour += 24
	duration_hour = end_hour - start_hour
	duration_minute = end_minute - start_minute
	if duration_minute < 0:
		duration_minute += 60
		duration_hour -= 1
	return duration_hour, duration_minute
