import csv
from datetime import datetime

def sort_scores(file_path):

  with open(file_path, 'r+') as f:
  
    reader = csv.reader(f)
    headers = next(reader)

    data = [row for row in reader if row] 
    data.sort(key=lambda x: int(x[0]), reverse=True)
    
    f.seek(0)
    f.truncate()
    
    f.write(headers[0] + ',' + headers[1] + ',' + headers[2] + ',' + headers[3] + '\n')
    
    for row in data:
      f.write(','.join(row) + '\n') 
