Requirements:
pyephem
pytz
egenix-mx-base
argparse
tzlocal

# phoenix
code to calculate the days and cycles in the phoenix calendar

This script is written in python and uses pyephem for the calculations

run ./phoenix -h for usage instruction

Examples:

./phoenix list now -y 1 -c 10

this will show a list of dates starting today skipping by 1 year for 10 iterations.
