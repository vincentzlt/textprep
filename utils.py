import os
import subprocess
import sys


def infix(fname, infix):
    """
    insert infix to fname path.
    
    Args:
        fname (str): input file path
        infix (str): the infix insert to the second last dir
    
    Returns:
        str: inserted path
    """

    dirname, fname = os.path.split(fname)
    dirname = os.path.join(dirname, infix)
    return os.path.join(dirname, fname)


def mkdir_if_none(fname):
    """
    make dir if the dir of a fname is not exist
    
    Args:
        fname (str): fpath
    """

    dir_name = os.path.dirname(fname)

    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def run_cmd(cmd):
    """
    run command and capture stdout
    
    Args:
        cmd (str): the command to run
    
    Raises:
        subprocess.CalledProcessError: if cmd end with non zero code, raise error.
    
    Returns:
        str: stdout in str format
    """

    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout = []

    for line in p.stdout:
        stdout.append(line.decode())
        print(line.decode().strip(), file=sys.stderr)

    if p.poll() != 0:
        raise subprocess.CalledProcessError(cmd=cmd, returncode=p.poll())

    return ''.join(stdout)


def gen_filepair(in_fnames, out_fnames, infix_str):
    """
    yield fname pairs from argument
    
    Args:
        in_fnames (list): list of in_fnames
        out_fnames (list): list of out_fnames, could be None
        infix_str (str): infix string to be inserted to path if out_fnames is None
    """

    if out_fnames is None:
        out_fnames = [infix(fname, infix_str) for fname in out_fnames]
    for fname in out_fnames:
        mkdir_if_none(fname)

    for in_file, out_file in zip(in_fnames, out_fnames):
        yield in_file, out_file
