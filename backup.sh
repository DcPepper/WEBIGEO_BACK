#!/bin/bash

now=`date +"%Y-%m-%d"`
sqlite3 -header -csv db.sqlite3 "select * from backend_country;" > "backup/country-${now}.csv"
sqlite3 -header -csv db.sqlite3 "select * from backend_record;" > "backup/record-${now}.csv"
sqlite3 -header -csv db.sqlite3 "select * from backend_quiz;" > "backup/quiz-${now}.csv"
