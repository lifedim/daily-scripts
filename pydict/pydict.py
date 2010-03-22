#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
import struct
import gzip
import stat
import re
from lookup import lookup

reload(sys)
sys.setdefaultencoding('utf8')

def list_dicts(dir):
    """docstring for list_dicts"""
    dicts = []
    for item in os.listdir( dir ):
        fullpath = dir + os.sep + item
        if os.path.isdir( fullpath ):
            for subitem in os.listdir(fullpath):
                full_dict_path = fullpath + os.sep + subitem
                if os.path.isfile(full_dict_path) and full_dict_path[-4:]==".ifo":
                    #tokens = re.search(r"/(.*/)*(.*)(?=\.ifo)", full_dict_path)
                    #print tokens.group(2)
                    dicts.append(read_ifo(full_dict_path))
                    break
    return dicts
                    
def read_ifo(ifo_file):
    """docstring for read_ifo"""
    f = file(ifo_file)
    s = f.readlines()
    word_count = int(s[2].strip().split("=")[1])
    file_size = int(s[3].strip().split("=")[1])
    dict_name = s[4].strip().split("=")[1]
    f.close()
    file_prefix = ifo_file[:-4]
    return (file_prefix, word_count, file_size, dict_name)
    
def eprint(info):
    """docstring for eprint"""
    print info
     

def ui(dicts):
    """docstring for ui"""
    i=0
    for (file_prefix, word_count, file_size, dict_name) in dicts:
        i += 1        
        print "%d %s" % (i, dict_name)
    
    cur_dict_idx = 0
    cur_dict = None
    
    while 1:
        try:
            cmd_str = raw_input(">")
            cmd_str = cmd_str.strip()
            cmd = cmd_str.split(" ")
            
            if cur_dict == None:
                if cmd[0]=="use":
                    try:
                        number = int(cmd[1])
                    except Exception, e:
                        print "incorrect para #1"
                        continue
                    if number >= 1 and number <= len(dicts):
                        cur_dict_idx = number-1
                        cur_dict = StarDict(dicts[cur_dict_idx][0])
                        print "Dict used"
                    else:
                        print "number out of range"
                else:
                    print "please choose a dict first (cmd: use #)"
            else:
                if cmd[0]=="size":
                    print "word count: %d , file size: %d" % (cur_dict.word_count, cur_dict.file_size)
                elif cmd[0]=="name":
                    print "name: %s" % cur_dict.dict_name
                elif cmd[0]=="list":
                    from_word = 0
                    limit = 1
                    try:
                        if len(cmd)==2:
                            limit = int(cmd[1])
                        elif len(cmd)>=3:
                            from_word = int(cmd[1])
                            limit = int(cmd[2])
                    except Exception, e:
                        print "incorrect para. (cmd: list [from_word=0] <limit number>)"
                        continue
                    cur_dict.list(from_word, limit)
                elif cmd[0]=="s":
                    word = cmd_str[2:]
                    s = cur_dict.search_word(word)
                    print s
                    
                elif cmd[0]=="exit" or cmd[0]=="quit" or cmd[0]=="q":
                    print "exit the pydict"
                    break
                else:
                    print "invalid command."
            
        except Exception, e:
            raise e
            break
        


class StarDict(object):
    """docstring for StarDict"""
    
    def __init__(self, dict_prefix):
        super(StarDict, self).__init__()
        self.dict_prefix = dict_prefix
        ifo_file = self.dict_prefix + ".ifo"
        self.load_ifo(ifo_file)
        
    def load_ifo(self, ifo_file):
        try:
            f = file(ifo_file)
            s = f.readlines()
            self.word_count = int(s[2].strip().split("=")[1])
            self.file_size = int(s[3].strip().split("=")[1])
            self.dict_name = s[4].strip().split("=")[1]
        except Exception, e:
            raise e
        finally:
            f.close()
    
    def search_word(self, word):
        """docstring for search_word"""
        word = word.strip()
        s =  lookup(self.dict_prefix,self.file_size,self.word_count,word)
        return s
        
            
    def list(self, word_offset=0, limit=10, output=None):
        idx_file = self.dict_prefix + ".idx"
        dat_file = self.dict_prefix + ".dict.dz"
        limit = min(limit, self.word_count)
        if word_offset < 0:
            word_offset = self.word_count + word_offset;
        if word_offset >= self.word_count or word_offset < 0:
            print "offset (para #1) is out of range [0 - %d)" % self.word_count
            return
        
        print "wordoffset: %d limit: %d" % (word_offset, limit)

        #load .idx
        f_idx = file(idx_file, "rb")
        #load .dict.dz
        f_dat = gzip.open(dat_file, "rb")

        #save to file
        if output!=None:
            f_out = file("/Users/lifedim/dict_out.txt", "w")

        i = 0
        c = 0        
        while i < word_offset+limit:
            word = ""
            content = ""
            b = ''
            str_end = 1
            # find a c-style string (ended with '\0')
            while str_end!=0:
                word += b
                b = f_idx.read(1)
                str_end = ord(b)

            # find next two integers (4+4 bytes)
            offset, size = struct.unpack("!ii", f_idx.read(8))
            # find content in f_dat, offset is not used here since we don't need read randomly
            content = f_dat.read(size)

            # skip some words if word_offset > 0
            if i < word_offset :
                i += 1
                continue
                            
            if output==None:
                print word+"\n"+content+"\n"
            else:
                f_out.write(word+"\n"+content+"\n")

            if limit > 50000:
                if i%(self.word_count/100)==0:
                    c += 1
                    print "%d out of 100 " % c
            
            i += 1

        f_idx.close()
        f_dat.close()
        if output:
            f_out.close()
            
    def __print__(self):
        print "%s total:%d file_size:%d", (self.dict_name, self.word_count, self.file_size)
    
if __name__ == '__main__':
    #main()
    dicts = list_dicts("/usr/share/stardict/dic")
    ui(dicts)
    
    