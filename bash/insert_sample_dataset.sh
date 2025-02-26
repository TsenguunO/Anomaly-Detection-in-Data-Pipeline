#!/bin/sh
curl -LX POST http://127.0.0.1:8000/api/dataset?email=user1 \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@./model/data/user_sample_data1.csv;type=text/csv"

curl -LX POST http://127.0.0.1:8000/api/dataset?email=user1 \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@./model/data/user_sample_data2.csv;type=text/csv"