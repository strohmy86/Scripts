#!/usr/bin/env python3

import pandas as pd
import hashlib

df = pd.read_csv('AllStudents2.csv')

df['userPassword'] = df['userPassword'].apply(lambda x: hashlib.sha1(str(x).encode('utf-8')).hexdigest())

df.to_csv('AllStudents_Hashed.csv', index=False)
