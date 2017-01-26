#!/usr/local/bin/python
import sys, ephem, starcalc,enoch, search

datelist = []
e = enoch.Date("-7/9/23 12:00:00")

rows = [] 
for year in range(0,100):
    row = search.Table.day_row(e)
    rows += row
    e.next_day()

list_header = search.Table.day_header()
starcalc.Columnize.cprint ( list_header + rows )

