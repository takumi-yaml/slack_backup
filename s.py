#!/usr/bin/env python


import os

path = './zips/'

indir = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('zip')] or False
filenames = [f.split('_') for f in indir]
sorted(filenames, reverse=True, key=lambda x: ''.join(x[1:-1]))

print('_'.join(filenames[-1]))

