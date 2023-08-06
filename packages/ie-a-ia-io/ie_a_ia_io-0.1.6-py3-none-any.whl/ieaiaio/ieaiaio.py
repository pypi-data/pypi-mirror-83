#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 15:15:29 2020

@author: ele
"""


import re
import json
import shutil
import glob
import pickle
from ieaiaio import chunkize
#import itertools

import warnings

def _rm_trailing_slash(path):
    """
    Remove ending path separator if present
    """
    if path[-1] == glob.os.sep:
        path = path[:-1]
    
    return path


def _natural_sort(items):
    """
    Correctly sort strings in list.  
    See: http://nedbatchelder.com/blog/200712/human_sorting.html
    
    >>> IOUtils.natural_sort(['test10','test1','test12','test2','test22'])
    ['test1', 'test2', 'test10', 'test12', 'test22']
    """

    def alphanum_key(s):
        """ Turn a string into a list of string and number chunks.
            "z23a" -> ["z", 23, "a"]
        """
        def tryint(s):
            try:
                return int(s)
            except ValueError:
                return s
            
        return [ tryint(c) for c in re.split('([0-9]+)', s) ] 
        
    return sorted(items, key = alphanum_key)


class IOUtils:
            
    
    @staticmethod
    def chunkize(iterable, size=10):
        """
        Split iterable into chunks of size `size`.
        
        args:
            iterable (iterable) : to be split
            size (int) : chunk size
        
        return:
            generator
        """
        
        for chunk in chunkize.chunkize(iterable, size):
            yield chunk
                
    @staticmethod
    def mkdir(path):
        """
        Create directory (with subdirectories). Equivalent to bash `mkdir -p`.
        
        args:
            path (str) : system path
        """
        
        path = glob.os.path.expanduser(path)
        
        if not glob.os.path.exists(path):
            glob.os.makedirs(path)
            
    @staticmethod
    def rm(path):
        """
        Remove directory/file. Equivalent to bash `rm -r`.
        
        args:
            path (str) : system path
        """
        
        path = glob.os.path.expanduser(path)
        
        if glob.os.path.exists(path):
            if glob.os.path.isdir(path):
                shutil.rmtree(path)
            else:
                glob.os.remove(path)
   
    
    @staticmethod
    def exists(path):
        """
        Check if directory/file exists.
        
        args:
            path (str) : system path
        
        return:
            res (bool) : response
            
        >>> IOUtils.exists('.')
        True
        """
        
        path = glob.os.path.expanduser(path)
        
        res = glob.os.path.exists(path)
        
        return res
    
    @staticmethod
    def join_paths(paths):
        """
        Create system paths from elements.
        
        args:
            paths (list) : elements to create path
        
        return:
            path (str) : system path
        
        >>> IOUtils.join_paths(['new','path','to','be','created'])
        'new/path/to/be/created'
        """
        
        path = glob.os.path.join(*paths)
        path = glob.os.path.expanduser(path)
        return path
    
    @staticmethod
    def dname(path):
        """
        Return name of main directory.
        
        args:
            path (str) : system path
        
        return:
            name (str) : directory name
        
        >>> IOUtils.dname('/path/to/file.txt')
        '/path/to'
        """
        
        name = glob.os.path.dirname(path)
        
        return name
    
    @staticmethod
    def fname(path):
        """
        Return name of file in system path.
        
        args:
            path (str) : system path
        
        return:
            name (str) : file name
        
        >>> IOUtils.fname('/path/to/file.txt')
        'file.txt'
        """
        path = _rm_trailing_slash(path)
            
        name = glob.os.path.basename(path)
        return name
    
    @staticmethod
    def load_json(path, *args, **kwargs):
        """
        Load JSON file into dict. 
        All extra arguments will be passed to `json.load`.
        
         args:
            path (str) : system path
        
        return:
            json_file (dict) : file content
        """
        
        path = glob.os.path.expanduser(path)
        
        with open(str(path)) as infile:
            json_file = json.load(infile, *args, **kwargs)
        return json_file
    
    @staticmethod
    def save_json(path,item, *args, **kwargs):
        """
        Save dict into JSON file.
        All extra arguments will be passed to `json.dump`.
        
         args:
            path (str) : system path
            item (dict) : dictionary
        
        return:
            json_file (dict) : file content
        """
        
        path = glob.os.path.expanduser(path)
        
        with open(str(path),'w') as outfile:
            json.dump(item, outfile, *args, **kwargs)
            
    @staticmethod
    def load_pickle(path, *args, **kwargs):
        """
        Load pickled python object.
        All extra arguments will be passed to `pickle.load`.
        
         args:
            path (str) : system path
        
        return:
            item (object) : python object
        """
        
        path = glob.os.path.expanduser(path)
        
        with open(str(path), mode = "rb") as infile:
            item = pickle.load(infile, *args, **kwargs)
        return item
      
    @staticmethod
    def save_pickle(item, path, *args, **kwargs):
        """
        Save python object to pickle file.
        All extra arguments will be passed to `pickle.dump`.
        
         args:
            path (str) : system path
            item (dict) : python object 
        
        return:
            json_file (dict) : file content
        """
        
        path = glob.os.path.expanduser(path)
        
        with open(str(path), mode = "wb") as outfile:
            pickle.dump(item, outfile, *args, **kwargs)        
        
    @staticmethod
    def ioglob(path, ext = None, recursive = False):
        """
        Backward compatibility.
        """
        
        warnings.DeprecationWarning("IOUtils.ioglob is deprecated. Use `IOUtils.iglob` with `ordered=True`instead")
        
        for p in IOUtils.iglob(path, ext = ext, recursive = recursive, ordered = True):
            yield p
            
    @staticmethod
    def iuglob(cls, path, ext = None, recursive = False):
        """
        Backward compatibility.
        """
        
        warnings.DeprecationWarning("IOUtils.ioglob is deprecated. Use `IOUtils.iglob` with `ordered=False`instead")
        
        for p in IOUtils.iglob(path, ext = ext, recursive = recursive):
            yield p

    
    @staticmethod
    def iglob(path, ext = None, recursive = False, ordered = False):
        """
        Iterator yielding paths matching a path pattern.
        If the extension is not provided all files are returned. 
        
        Note: if `ordered=True` all paths will be load into memory, otherwise lazy loading is used. 
        
        args:
            path (str) : system path
            ext (str) : file extension
            recursive (bool) : check subfolder
            
        >>> list(IOUtils.iglob(path = '.', ext = 'py', ordered = True))
        ['./__init__.py', './ieaiaio.py', './setup.py']
        """
        
        path = glob.os.path.expanduser(path)
        
        ext = "*.{}".format(ext) if ext is not None else "*"
        
        splits = [path,ext] 
        
        if recursive:
            splits.insert(1,"**")
        
        pregex = glob.os.path.join(*splits)
                
        path_gen = _natural_sort(glob.iglob(pregex, recursive = recursive)) if ordered else glob.iglob(pregex, recursive = recursive)
        
        for p in path_gen:
            yield p
    
if __name__ == "__main__": 
    import doctest
    doctest.testmod()


