#!cython
# distutils: language=c++
# distutils: sources = VXI11_clnt.c VXI11_xdr.c createAbtChannel.c

"""
cVXI11 is a reimplemented version of the VXI11 module. Previous version of VXI11 modules uses SWIG to generate 
glue code. However, cVXI11 module uses cython instead of SWIG to generate glue code between Python and C-library.
revision: $Revision: 50e51fd4f6bb $ $Date: 2020-03-02 11:47:37 +0900 $
"""

cimport PMAP

#from cVXI11 cimport device_flags_termchrset, device_flags_end, device_flags_waitlock
#from cVXI11 cimport Device_ReadResp_END,Device_ReadResp_CHR
#
import cython
import socket,struct,os,signal
import warnings,logging
#
#
#

#cdef extern from "netinet/in.h":
cdef int IPPROTO_TCP = 6              # /* tcp */
cdef int IPPROTO_UDP = 17             # /* user datagram protocol */

def getport(host, program, version=1, protocol=IPPROTO_TCP):
    return cPMAP_getport(host, program, version, protocol)

# def getmaps(host):
#     l = cPMAP_getmaps(host)
#     return cython.address(l)

