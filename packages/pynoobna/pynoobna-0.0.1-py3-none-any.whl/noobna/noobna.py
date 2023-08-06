#!/usr/bin/env python
'''
Usage:
  ./noobna.py [options]

Options:
  --help -h               This help.
  --mktest-data=D -D D    Output test-data.
'''
import numpy as np;
from struct import pack,unpack;
import os;
from io import BytesIO;

__dt = 'float64'
def _pint(i): return pack("i",i);
def _upint(f): return unpack("i",f.read(4))[0];


def serialize(P,D,dtype=__dt):
    '''
    serialize a noobna array to a bytes object.
    `P` -- iterable of dimensions, must agree in shape with D.
    `D` -- array.

    `dtype` -- optionally set the dtype if you compiled noobna differently.

    returns a bytes object of the noobna array.
    '''
    s=BytesIO();
    output(s,P,D,dtype=dtype);
    return s.getvalue();


def output(outfile,P, D, dtype=__dt):
    '''
    output to a file
    `outfile` -- either a file or a filename to be written to.
    `P` -- iterable of dimensions, must agree in shape with D.
    `D` -- array.

    `dtype` -- optionally set the dtype if you compiled noobna differently.
    '''
    if type(outfile) == str:
        with open(outfile, "wb") as f:
            output(f, P, D, dtype=dtype);
        return;
    
    D = D.astype(dtype);
    P,sz = zip(*[ (np.array(ip).astype(dtype),len(ip))
                  for ip in P ]);
    if D.shape != sz:
        raise ValueError(
            "dimensions do not agree with quantity {} != {}".format(
                D.shape, sz));
    outfile.write(_pint(len(P)));
    for i in sz:
        outfile.write(_pint(i));
    for ip in P:
        outfile.write(ip);
    outfile.write(memoryview(D));
    


def load(infile,dtype = __dt):
    '''
    load a file
    `infile` -- either a file or a filename to be read.
    `dtype` -- optionally set the dtype if you compiled noobna differently.

    returns `P`, `D`, where `P` is an array of dimensions and `D` is the array.
    '''

    if type(infile) == str:
        with open(infile, "rb") as f:
            return load(f, dtype=dtype);

    n  = _upint(infile);
    ns = [ _upint(infile) for i in range(n) ];
    P  = [  np.fromfile(infile,dtype=dtype,count=i)
            for i in ns ];
    sz = 1;
    for i in ns:
        sz*=i;        
    D = np.fromfile(infile,dtype=dtype, count=sz);
    D = D.reshape(*ns);
    return P,D;


def _mktestdata():
    x=np.array([-1.0,0.0,1.0]).astype(__dt);
    y=np.array([ 0.5,0.5,1.5]).astype(__dt);
    z=np.array([ 0.0,0.5,2.5]).astype(__dt);
    Z,Y,X = np.meshgrid(z,y,z,indexing='ij');
    D = np.sqrt(X**2+Y**2 + Z);
    return [x,y,z],D;

def _test1(fnametest):
    P,D = mktestdata();
    output(fnametest,P,D);
    Pp,Dp = load(fnametest);
    out = np.max(Dp != D );
    for x,xp in zip(P,Pp):
        out|= np.max(x  != xp);
    if out:
        raise ValueError("test failed");
    os.remove(fnametest);
    print("test passed");


if __name__ == "__main__":
    from docopt import docopt;
    opts = docopt(__doc__,help=True);
    _test1("tmp.dat");
    if opts['--mktest-data']:
        P,D=_mktestdata();
        output(opts['--mktest-data'],P,D);
    pass;
