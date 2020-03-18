import os
import shutil # For a higher level interface that is easier to use
import glob
import sys


def test_os():
    print(os.getcwd()) # Return the current working directory
    os.chdir('/root/some_codes')
    print(os.getcwd())
    os.system('mkdir today')
    # print(dir(os)) # Return a list of all module functions


def test_shutil():
    shutil.copyfile('data.db', 'archive.db')
    shutil.move('/some_codes/py_dir', 'new_dir')


def test_glob():
    print(glob.glob('*py')) # .glob() returns a list of files


def test_sys():
    print(sys.argv) # .argv returns program arguments  
    # For emitting warnings and error messages
    sys.stderr.write('Warning, log file not found starting a new one\n') 
    

test_glob()
