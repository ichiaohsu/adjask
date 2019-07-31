#!/usr/bin/env python
# coding: utf-8
import psycopg2

import csv

conn = psycopg2.connect(host="localhost", dbname="adjask", user="adjask_user", password="adjask_pw")
cur = conn.cursor()

from datetime import datetime
with open('sample_data.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        date, *r = row
        date = datetime.strptime(date,'%d.%m.%Y')
        row = [date, *r]
        cur.execute("INSERT INTO metrics_metrics(date, channel, country, os, impressions, clicks, installs, spend, revenue) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", row)
        conn.commit()

