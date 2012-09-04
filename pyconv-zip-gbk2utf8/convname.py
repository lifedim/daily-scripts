#!/usr/bin/python
#
# Version 0.1
# http://torfy.thatsbaby.net

import zipfile
import sys
import os
import shutil

if len(sys.argv) < 3:
  print sys.argv[0]+" <zip_file> <dest_dir>"
  sys.exit()

zip_file = sys.argv[1]
dir_path = sys.argv[2]
tmp_dir_path = '__tmp__'
zip = zipfile.ZipFile(zip_file)

if not os.path.exists(dir_path):
  os.mkdir(dir_path)
if not os.path.exists(tmp_dir_path):
  os.mkdir(tmp_dir_path)

print "Extracting files..."
for old_file in zip.namelist():
  zip.extract(old_file, tmp_dir_path)

  # Copy the old file to the new dest.
  new_file = unicode(old_file, 'gbk')

  old_file_full = tmp_dir_path + '/' + old_file
  new_file_full = dir_path + '/' + new_file
  if os.path.isdir(old_file_full):
    if not os.path.exists(new_file_full):
      os.mkdir(new_file_full)
  else:
    shutil.copy2(old_file_full, new_file_full)

# Remove the temporary directory.
shutil.rmtree(tmp_dir_path)

print "Done."

