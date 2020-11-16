# WoWCombatLog.txt
from datetime import datetime
import re


hc_char = "Calvin"
filelocname = "Logs\WoWCombatLogae.txt"
# filelocname = input("Enter Filename Location: ")

start_time = '11/15 08:22:0.000'
end_time = '11/15 08:34:0.000'
# runs till 23.59, doesn't include the seconds...
# so event times should be set 1m early.

########################################
start_time_object = datetime.strptime(start_time, '%m/%d %H:%M:%S.%f')
start_time_object = str(start_time_object).strip()
start_time_object = start_time_object[5:-3]
# print(start_time_object,'\n---')
# ----------------------------------------------------------- #
end_time_object = datetime.strptime(end_time, '%m/%d %H:%M:%S.%f')
end_time_object = str(end_time_object).strip()
end_time_object = end_time_object[5:-3]
# print(end_time_object,'\n--')
########################################

failed = ''
print('\n---','Parsing HC Event, from [',start_time_object, '] to [', end_time_object,']')
if start_time_object > end_time_object:
    print('Checking Setup: Failure. [start_time] > [end_time] ~ which is wrong!','\n---------------\n-F-A-I-L-U-R-E-\n---------------\n\n\n >>>>>>>>>> Fix your Start and End Times!\n\n')
    failed = False
else:
    print('---','Checking Setup: Success.')
    # print('[start_time] < [end_time] ~ which is correct!')
    # uncomment to show detailed
    print('\n-------------')
    failed = True

xp__value__list = []
xp_counted = 0

exp = "experience"
bonus = "bonus"

with open(filelocname,'r') as log_xp:
    found = False
    for line in log_xp:
        line_time = str(line).strip()
        line_time = str(line_time)[:18]

        if start_time_object <= line_time in line or end_time_object >= line_time in line:
            # print(line_time) # uncomment to show detailed
            if exp in line or bonus in line: # Key line: check if `exp` or `bonus` is in the line.
                line = line.strip()
                # print(line) # uncomment to show detailed
                xp_counted += 1

                line_xp_value = line.rpartition('experience')[0]
                line_xp_value = str(line_xp_value).strip()
                line_xp_value = line_xp_value[-6:] # confirmed 4 digits of quest xp // ahmpy: 3200
                line_xp_value = [int(i) for i in line_xp_value.split() if i.isdigit()]
                line_xp_value = str(line_xp_value)
                xp_value_int_filter  = ' '.join(re.findall(r"\[(\d+)\]",line_xp_value))
                print(xp_value_int_filter)
                xp__value__list.append(xp_value_int_filter)
                found = True
        else:
            # print('No experience messages found, bad log.') # uncomment to show error
            pass
print('-------------\n')
def tryconvert(s):
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return s

xp__int__list = [tryconvert(i) for i in xp__value__list]
# print(xp__int__list)

xp__gained = sum(xp__int__list)
print('---',hc_char,'gained: [',xp__gained,'EXP ]\n--- There were [',xp_counted,'] lines of EXP counted.')

# difference = start_time_object - end_time_object
# charname = charname," has gained: ", xp__gained, ' during a ',difference, ' event.'

# make parser for real time -> have parses send websocket-esq chat to server ->
# updates server XP values in real time, or if the player dies, effect the website in some way, real time
