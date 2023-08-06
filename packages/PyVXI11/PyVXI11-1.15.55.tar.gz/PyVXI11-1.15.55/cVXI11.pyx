#!cython
# distutils: language=c++
# distutils: sources = VXI11_clnt.c VXI11_xdr.c VXI11_intr_svc.c  VXI11_intr_xdr.c createAbtChannel.c cPMAP.cpp
#
#from __future__ import print_function

"""
cVXI11 is a reimplemented version of the VXI11 module. Previous version of VXI11 modules uses SWIG to generate 
glue code. However, cVXI11 module uses cython instead of SWIG to generate glue code between Python and C-library.
revision: $Revision: 5f5f103ac238 $ $Date: 2020-10-24 14:36:09 +0900 $
HGDate: $HGdate: Sat, 24 Oct 2020 14:36:09 +0900 $
HGTag: "$HGTag: 1.15.54-5f5f103ac238 $"
"""
cimport cVXI11
from libc.stdlib cimport malloc, free, calloc

#from cVXI11 cimport device_flags_termchrset, device_flags_end, device_flags_waitlock
#from cVXI11 cimport Device_ReadResp_END,Device_ReadResp_CHR
#
import cython
import socket, struct, os, signal
import logging
#
vxi11logger=logging.getLogger("cVXI11")
from uuid import uuid4

# you can set logging lever on application/test program side.
## for debugging
# vxi11logger.setLevel(logging.DEBUG)
## for info
#vxi11logger.setLevel(logging.INFO)
#
#

#
from cVXI11_revision import *
#
from vxi11Exceptions import *

class Device_AddrFamily:
    DEVICE_TCP = 0
    DEVICE_UDP = 1

# from VXI11.h

cdef enum:
    device_flags_termchrset = 0x80
    device_flags_end = 0x08
    device_flags_waitlock = 0x01
    DEVICE_FLAGS_TERMCHRSET = 0X80
    DEVICE_FLAGS_END = 0X08
    DEVICE_FLAGS_WAITLOCK = 0X01

cdef enum:
    DEVICE_INTR_SRQ= (<u_int>30)
    #device_intr_prog =DEVICE_INTR
    #device_intr_version =DEVICE_INTR_VERSION
    device_intr_srq = DEVICE_INTR_SRQ

# from rpc/clnt.h

cdef enum:
    Device_ReadResp_REQCNT=1
    Device_ReadResp_CHR=2
    Device_ReadResp_END=4
    DEVICE_READRESP_REQCNT=1
    DEVICE_READRESP_CHR=2
    DEVICE_READRESP_END=4
    
try:
    import threading
    _enableSRQ=True
except ImportError:
    _enableSRQ=False

class device_core:
    prog=<u_int> DEVICE_CORE
    version=<u_int> DEVICE_CORE_VERSION

class device_async:
    prog = <u_int> DEVICE_ASYNC
    version = <u_int> DEVICE_ASYNC_VERSION

class device_intr:
    prog = <u_int> DEVICE_INTR
    version = <u_int> DEVICE_INTR_VERSION
    srq = <u_int> device_intr_srq # VXI11.h does not have the definiton of DEVICE_INTR_SRQ

class device_flags:
    termchrset = <u_int> 0x80;
    end = <u_int> 0x8;
    waitlock = <u_int> 0x1;
    
class Device_ErrorCode_class:
    No_Error = 0
    Syntax_Error = 1
    not_Accessible = 3
    invalid_Link_Id = 4
    Parm_Error = 5
    Chan_not_Established = 6
    Op_not_Supported = 8
    Out_of_Resoruces = 9
    Dev_Locked_by_Another = 11
    No_Lock_by_this_Link = 12
    IO_Timeout = 15
    IO_Error = 17
    Ivalid_Addr = 21
    Abort = 23
    Already_Established = 29
    Device_ErrorCode_msg = {
        No_Error:"No Error",
        Syntax_Error:"Syntax Error",
        not_Accessible :"not accessible",
        invalid_Link_Id:"Invalid Link Id",
        Parm_Error:"Parm Error",
        Chan_not_Established:"Channel not Established",
        Op_not_Supported : "Operation not Supported",
        Out_of_Resoruces : "Out of Resources",
        Dev_Locked_by_Another : "Device Locked by Another",
        No_Lock_by_this_Link : "No Lock by this Link",
        IO_Timeout :"I/O Timeout",
        IO_Error :"I/O Error",
        Ivalid_Addr :"Invalid Address",
        Abort : "Abort",
        Already_Established : "Channele Already Established"
    }
    @classmethod
    def msg(cls, code):
        return cls.Device_ErrorCode_msg[code]
   
cdef class Device_GenericParms:
    # cdef c_Device_GenericParms *thisptr #

    def __cinit__(self, lid, flags, lock_timeout, io_timeout,*args,**kwargs):
        self.thisptr=new c_Device_GenericParms()
        if self.thisptr is NULL:
            raise MemoryError()


    def __init__(self, lid, flags, lock_timeout, io_timeout):
        self.thisptr.lid=lid
        self.thisptr.flags=flags
        self.thisptr.lock_timeout=lock_timeout
        self.thisptr.io_timeout=io_timeout

    def __dealloc__(self):
        #print "dealloc GenericParms"
        if self.thisptr is NULL:
            return 
        with nogil:
            xdr_free(<xdrproc_t> xdr_Device_GenericParms,
                     <c_xdr_free_argtype> self.thisptr)
        #del self.thisptr
    
    def getLid(self):
        return self.thisptr.lid

    def getFlags(self):
        return self.thisptr.flags

    def getLockTimeout(self):
        return self.thisptr.lock_timeout

    def getIoTimeout(self):
        return self.thisptr.io_timeout

    
    @property
    def lid(self): 
        return self.thisptr.lid if self.thisptr is not NULL else None
    
    @lid.setter
    def lid(self, lid):
        if self.thisptr is not NULL : self.thisptr.lid=lid

    @property
    def flags(self):
        return self.thisptr.flags if self.thisptr is not NULL else None
    
    @flags.setter
    def flags(self, flags): 
        if self.thisptr is not NULL : self.thisptr.flags=flags
            
cdef class Device_RemoteFunc:
    # cdef c_Device_RemoteFunc *thisptr # "this" is a reserved keyword in C++
    
    def __cinit__(self,hostAddr, hostPort, progNum, progVers, progFamily, *args, **kwargs):
        self.thisptr=new c_Device_RemoteFunc()
        if self.thisptr is NULL:
            raise MemoryError()
        
    def __init__(self,hostAddr, hostPort, progNum, progVers, progFamily, *args, **kwargs):
        self.thisptr.hostAddr=hostAddr
        self.thisptr.hostPort=hostPort
        self.thisptr.progNum=progNum
        self.thisptr.progVers=progVers
        self.thisptr.progFamily=progFamily
        
    def __dealloc__(self):
        if self.thisptr is not NULL:
            with nogil:
                xdr_free(<xdrproc_t> xdr_Device_RemoteFunc,
                         <c_xdr_free_argtype> self.thisptr)
            #del self.thisptr

    @property
    def progFamily(self): return self.thisptr.progFamily if self.thisptr is not NULL else None

    @progFamily.setter
    def progFamily(self,progFamily):
        if self.thisptr is not NULL:
            self.thisptr.progNum=progFamily

    @property
    def progNum(self):
        return self.thisptr.progNum if self.thisptr is not NULL else None

    @progNum.setter
    def progNum(self,progNum):
        if self.thisptr is not NULL: self.thisptr.progNum=progNum 

    @property
    def progVers(self):
        return self.thisptr.progVers  if self.thisptr is not NULL else None

    @progVers.setter
    def progVers(self,progVers):
        if self.thisptr is not NULL: self.thisptr.progVers=progVers

    @property
    def hostAddr(self):
        return self.thisptr.hostAddr if self.thisptr is not NULL else None

    @hostAddr.setter
    def hostAddr(self, hostAddr):
        if self.thisptr is not NULL: self.thisptr.hostAddr=hostAddr

    @property
    def progPort(self):
        return self.thisptr.hostPort if self.thisptr is not NULL else None

    @progPort.setter
    def progPort(self, hostPort):
        if self.thisptr is not NULL: self.thisptr.hostPort=hostPort

cdef class Create_LinkParms:
    # cdef c_Create_LinkParms *thisptr # "this" is a reserved keyword in C++

    def __cinit__(self, clientId, lockDevice, lock_timeout, device):
        with nogil:
            self.thisptr=new c_Create_LinkParms()
        if self.thisptr is NULL:
            raise MemoryError()
        
    def __init__(self, clientId, lockDevice, lock_timeout, device):
        self.thisptr.clientId=clientId
        self.thisptr.lockDevice=lockDevice
        self.thisptr.lock_timeout=lock_timeout
        self.thisptr.device=device 

    def __dealloc__(self):
        # temp=<long > self.thisptr
        #print "dealloc LinkParms", '0x%x'%temp
        # if self.thisptr:
        # this xdr_free crash system
        #     with nogil:
        #         xdr_free(<xdrproc_t> xdr_Create_LinkParms, self.thisptr)
        if self.thisptr is not NULL:
            del self.thisptr

    @property
    def device(self):
        return self.thisptr.device if self.thisptr is not NULL else None

    @device.setter
    def device(self,device):
        if self.thisptr is not NULL: self.thisptr.device=device
            
    
cdef class Create_LinkResp:
    cdef c_Create_LinkResp *thisptr # "this" is a reserved keyword in C++
    
    def __cinit__(self):
        self.thisptr=new c_Create_LinkResp()
        if self.thisptr is NULL:
            raise MemoryError()

    def __dealloc__(self):
        if self.thisptr is NULL: return
        with nogil:
            xdr_free(<xdrproc_t> xdr_Create_LinkResp,
                    <c_xdr_free_argtype>  self.thisptr)
        del self.thisptr

cdef class Device_WriteParms:
    cdef c_Device_WriteParms *thisptr #
   
    def __cinit__(self, lid, io_timeout, lock_timeout, flags):
        self.thisptr=new c_Device_WriteParms()
        if self.thisptr is NULL:
            raise MemoryError()
        
    def __init__(self, lid, io_timeout, lock_timeout, flags):
        self.thisptr.lid=lid
        self.thisptr.io_timeout=io_timeout
        self.thisptr.lock_timeout=lock_timeout
        self.thisptr.flags=flags

    def __dealloc__(self):
        #print "dealloc WriteParms"
        # this xdr_free crash
        #with nogil:
        #xdr_free(<xdrproc_t> xdr_Device_WriteParms, self.thisptr)
        if self.thisptr is NULL: return 
        del self.thisptr

    @property
    def data(self):
        return self.thisptr.data.data_val if self.thisptr is not NULL else None
        
    @data.setter
    def data(self,cmd):
        """
        setter for data property. 
        it set both data_val and data_len at sametime.
        """
        if self.thisptr is not NULL:
            self.thisptr.data.data_val=cmd
            self.thisptr.data.data_len=len(cmd)

    @property
    def data_len(self): 
        return (self.thisptr.data.data_len) if self.thisptr is not NULL else None
        
cdef class Device_ReadParms:
    cdef c_Device_ReadParms *thisptr #

    def __cinit__(self, lid,
                  requestSize,
                  io_timeout,
                  lock_timeout,
                  flags,
                  termChar='\n'):
        self.thisptr=new c_Device_ReadParms()
        if self.thisptr is NULL:
            raise MemoryError()
        
    def __init__(self, lid,
                  requestSize,
                  io_timeout,
                  lock_timeout,
                  flags,
                  termChar='\n'):
        self.thisptr.lid=lid
        self.thisptr.requestSize = requestSize
        self.thisptr.io_timeout = io_timeout
        self.thisptr.lock_timeout = lock_timeout
        self.thisptr.flags = int(flags)
        self.thisptr.termChar= ord(termChar)

    def __dealloc__(self):
        #print "dealloc ReadParms"
        if self.thisptr is NULL: return
        with nogil:
            xdr_free(<xdrproc_t> xdr_Device_ReadParms, <c_xdr_free_argtype> self.thisptr)
        del self.thisptr

cdef class Device_ReadResp:
    cdef c_Device_ReadResp *thisptr #

    def __cinit__(self):
        with nogil:
            self.thisptr=new c_Device_ReadResp()
        if self.thisptr == NULL:
            raise MemoryError("cannot allocate Device_ReadResp")
        

    # def __cinit__(self,c_Device_ReadResp *thisptr):
    #     self.thisptr=thisptr
    
    def __dealloc__(self):
        #print "dealloc ReadResp"
        if self.thisptr is NULL: return 
        with nogil:
            xdr_free(<xdrproc_t> xdr_Device_ReadResp, <c_xdr_free_argtype> self.thisptr)
        del self.thisptr

    def release(self):
        with nogil:
            xdr_free(<xdrproc_t> xdr_Device_ReadResp, <c_xdr_free_argtype> self.thisptr)
        self.thisptr = NULL

    def get_binary_data(self):
        if self.thisptr:
            return self.thisptr.data.data_val
        else:
            raise RuntimeError("empty response")

cdef class Device_ReadStbResp:
    cdef c_Device_ReadStbResp *thisptr#
    
    def __cinit__(self):
        with nogil:
            self.thisptr=new c_Device_ReadStbResp()
        if self.thisptr is NULL:
            raise MemoryError()

    def __dealloc__(self):
        if self.thisptr is NULL: return
        with nogil:
            xdr_free(<xdrproc_t> xdr_Device_ReadStbResp, <c_xdr_free_argtype> self.thisptr)
        del self.thisptr

cdef class Device_EnableSrqParms:
    cdef c_Device_EnableSrqParms *thisptr #

    def __cinit__(self, lid):
        with nogil:
            self.thisptr=new c_Device_EnableSrqParms()
        if self.thisptr is NULL:
            raise MemoryError()
        
        self.thisptr.lid=lid
        
    def __dealloc__(self):
        if self.thisptr is NULL: return
        #xdr_free(<xdrproc_t> xdr_Device_EnableSrqParms, self.thisptr)
        del self.thisptr

    @property
    def enable(self): 
        return self.thisptr.enable if self.thisptr is not NULL else None

    @enable.setter
    def enable(self,val):
        if self.thisptr is not NULL:
            self.thisptr.enable=val

    @property
    def handle(self): 
        return self.thisptr.handle.handle_val if self.thisptr is not NULL else None

    @handle.setter
    def handle(self,val):
        if self.thisptr is not NULL:
            self.thisptr.handle.handle_val=val
            self.thisptr.handle.handle_len=len(val)

cdef class Device_LockParms:
    cdef c_Device_LockParms *thisptr #
    
    def __cinit__(self, lid, flags, lock_timeout):
        with nogil:
            self.thisptr=new c_Device_LockParms()
        if self.thisptr is NULL:
            raise MemoryError()
        
    def __init__(self, lid, flags, lock_timeout):
        self.thisptr.lid=lid
        self.thisptr.flags=flags
        self.thisptr.lock_timeout=lock_timeout

    def __dealloc__(self):
        if self.thisptr is NULL: return
        #with nogil:
        #  xdr_free(<xdrproc_t> xdr_Device_LockParms, self.thisptr)
        del self.thisptr

cdef class Device_DocmdParms:
    cdef c_Device_DocmdParms *thisptr #

    def __cinit__(self,
                  lid,
                  flags,
                  io_timeout,
                  lock_timeout,
                  cmd,
                  network_order,
                  datasize,
    ):
        with nogil:
            self.thisptr=new c_Device_DocmdParms()
        if self.thisptr is NULL:
            raise MemoryError()
        
    def __init__(self,
                 lid,
                 flags,
                 io_timeout,
                 lock_timeout,
                 cmd,
                 network_order,
                 datasize,
    ):
        self.thisptr.lid=lid
        self.thisptr.flags=flags
        self.thisptr.io_timeout=io_timeout
        self.thisptr.lock_timeout=lock_timeout
        self.thisptr.cmd=cmd
        self.thisptr.network_order=network_order
        self.thisptr.datasize=datasize
    
    def __dealloc__(self):
        if self.thisptr is NULL: return 
        #with nogil:
        #  xdr_free(<xdrproc_t> xdr_Device_DocmdParms, self.thisptr)
        del self.thisptr

    @property
    def data_in(self):
        return self.thisptr.data_in.data_in_val if self.thisptr is not NULL else None

    @data_in.setter
    def data_in(self,cmd):
        """
        setter for data property. it set both data_val and data_len at sametime.
        """
        if self.thisptr is not NULL:
            self.thisptr.data_in.data_in_val=cmd
            self.thisptr.data_in.data_in_len=len(cmd)

    @property
    def data_in_len(self): 
        return self.thisptr.data_in.data_in_len if self.thisptr is not NULL else None
        

cdef class Device_DocmdResp:
    cdef c_Device_DocmdResp *thisptr #

    def __cinit__(self):
        with nogil:
            self.thisptr=new c_Device_DocmdResp()
        if self.thisptr is NULL:
            raise MemoryError()

    def __dealloc__(self):
        if self.thisptr is NULL: return
        with nogil:
            xdr_free(<xdrproc_t> xdr_Device_DocmdResp, <c_xdr_free_argtype> self.thisptr)
        del self.thisptr

cdef class Device_SrqParms:
    cdef c_Device_SrqParms *thisptr #

    def __cinit__(self):
        with nogil:
            self.thisptr=new c_Device_SrqParms()
        if self.thisptr is NULL:
            raise MemoryError()

    def __dealloc__(self):
        if self.thisptr is NULL: return
        with nogil:
            xdr_free(<xdrproc_t> xdr_Device_SrqParms, <c_xdr_free_argtype> self.thisptr)
        #del self.thisptr

cdef class clnt:
    cdef c_CLIENT *thisptr 

    def __cinit__(self, char *host, u_long prog,u_int vers,char *prot):
        with nogil:
            self.thisptr=clnt_create(host, prog, vers, prot)
        if self.thisptr is NULL:
            clnt_pcreateerror("clnt_create in clnt.__cinit__")
            raise MemoryError()
        
    def __dealloc__(self):
        if self.thisptr is NULL: return
        with nogil:
            clnt_destroy(self.thisptr)
        
    def perror(self,char *errmsg):
        with nogil:
            clnt_perror(self.thisptr, errmsg)   
        return errmsg

    def sperror(self,char *errmsg):
        with nogil:
            resp=clnt_sperror(self.thisptr, errmsg)
        return resp

cdef class Vxi11Device:
    cdef char *host
    cdef char *device
    cdef char *proto
    cdef int  uuid31
    cdef Device_Link lid
    cdef u_short abortPort
    cdef u_long maxRecvSize
    cdef u_long lock_timeout
    cdef u_long io_timeout
    cdef unsigned long intr_host
    cdef unsigned short intr_port
    cdef c_CLIENT *clnt
    cdef c_CLIENT *abt
    cdef long abt_socknum
    cdef c_CLIENT *intr
    cdef c_SVCXPRT *svc_xprt
    # python property
    cpdef readonly hostName
    cpdef readonly deviceName
    cpdef readonly protoName
    cpdef readonly intr_socket
    cpdef readonly svc_thread
    cpdef readonly svc_lock
    cpdef readonly srq_port
    cpdef readonly srq_sock

    @property
    def lid(self): # access properties in C object from Python.
        return self.lid

    @lid.setter
    def lid(self,lid):
        self.lid = lid

    @property
    def host(self): # strange behaviour. need debug. use hostName, instead.
        return self.host

    @property
    def device(self):
        return self.device

    @property
    def proto(self):
        return self.proto

    @property
    def abortPort(self):
            return self.abortPort

    @property
    def maxRecvSize(self):
        return self.maxRecvSize

    @property
    def uuid31(self):
        return self.uuid31

    srq_locks=dict() # thread-id:(lock object, osc)
    
    def __init__(self, char * host, char *device=b"gpib0,0",
                 char *proto=b"tcp", lock_timeout=0, lockDevice=0,
                 io_timeout=0 ):
        
        cdef u_long prog=device_core.prog
        cdef u_long vers=device_core.version
        cdef long socknum=0

        # Python propeties
        # copy string to Python object
        self.hostName=host.decode()
        self.deviceName=device.decode()
        self.protoName=proto.decode()
        self.lock_timeout=lock_timeout
        self.io_timeout=io_timeout
        self.intr_socket=None
        self.svc_thread=None
        #
        self.host=host
        self.device=device
        self.proto=proto
        self.uuid31=uuid4().int & 0x7fffffff 
        #
        with nogil:
            self.clnt=clnt_create(host, prog, vers, proto)
            if not self.clnt:
                clnt_pcreateerror("cVXI11")
        if self.clnt == NULL:
            raise RuntimeError(
                "cannot connect to host. Check output from  /usr/sbin/rpcinfo -p {host}".format(
                    host=self.hostName))

        parm=Create_LinkParms(self.uuid31,
                              lockDevice,
                              self.lock_timeout,
                              self.device
        )
        # parm.thisptr.clientId=self.uuid31
        # parm.thisptr.lockDevice=lockDevice    # boolean or 0/1?
        # parm.thisptr.lock_timeout=lock_timeout # timeout in msec
        # parm.thisptr.device=device             #device name
        
        with nogil:
            res= create_link_1(parm.thisptr, self.clnt)
        if (not res):
            raise IOError
        elif (res.error !=0):
            with nogil:
                xdr_free(<xdrproc_t> xdr_Create_LinkResp, 
                         <c_xdr_free_argtype> res)
            raise IOError("create_link failed with error:{erc}".format(erc=res.error))

        self.lid=res.lid
        self.abortPort=res.abortPort
        self.maxRecvSize=res.maxRecvSize

        self.abt=NULL
        self.abt_socknum=0
        #
        with nogil:
            xdr_free(<xdrproc_t> xdr_Create_LinkResp, <c_xdr_free_argtype> res)      

        #print "abort port:0x%dX"%res.abortPort,self.host
        #print "maxRecvSize:%ld"%res.maxRecvSize
        
        # DEVICE_ASYNC service is not registered to portmapper. 
        # So we should use clnttcp_create for abort channel.
        # Tek osc has rpc service. #395184=0X607B0 is a service number for abort channel
        #
        vxi11logger.info(
            "creating abot channel with prog:{prog} vers:{vers}".format(
                prog=DEVICE_ASYNC, vers=DEVICE_ASYNC_VERSION)
        )
        if ( device_has_async_port(host)):
            # createAbortChannel
            vxi11logger.info(" asyn service is found in mmap.")
            with nogil:
                self.abt=clnt_create(host,
                                     DEVICE_ASYNC,
                                     DEVICE_ASYNC_VERSION,
                                     "tcp")
        if ((self.abt == NULL) and (res.abortPort != 0)):
            vxi11logger.info( "No ABT channel was found. Ignore the message above.")
            with nogil:
                self.abt=createAbtChannel(host,
                                          res.abortPort, &socknum,
                                          DEVICE_ASYNC, DEVICE_ASYNC_VERSION,
                                          0, 0)
                self.abt_socknum=socknum
        if self.abt == NULL:
            vxi11logger.warn("Don't worry, rest of it should work.")
        else:
            vxi11logger.debug(
                "abort channel {port:x}:{sock:x}".format(port=res.abortPort, sock=self.abt_socknum)
            )
        vxi11logger.info( "Vxi11Device is successfully created")
        return
    
    def hasAsynService(self,host):# for consistency with 1.12.a20
        return device_has_async_port(host)
        
    def createSrqSocket(self):
        #trick to find the local ip which is connected to the device
        # connect to device's portmapper.
        # then get host name of interface connected to portmapper(= device).
        ds=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ds.connect((self.hostName, 111)) # 111 is a port number for RPC server
        host=ds.getsockname()[0] # getsockname() returns a (host,port) pair.
        vxi11logger.debug("interface to portmapper {host}".format(host=host))
        ds.close()
        
        srqBindSocket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        srqBindSocket.bind((host, 0)) # follow EPICS/drvVXI11.c. port=0 -> system pickup port number.
        return srqBindSocket

    def run_svc(self): 
        vxi11logger.info("starting rpc svc")
        xprt=self.svc_xprt

        with nogil:
            IF UNAME_SYSNAME == "Darwin":
                reg=svc_register(xprt, 
                             cVXI11.DEVICE_INTR, 
                             cVXI11.DEVICE_INTR_VERSION, 
                             <void (*)()> device_intr_1, # we need cast here.
                             0) # we don't use portmapper 
            ELIF UNAME_SYSNAME == "Linux":
                reg=svc_register(xprt,
                                 cVXI11.DEVICE_INTR, 
                                 cVXI11.DEVICE_INTR_VERSION, 
                                 # we need cast here.
                                 <void (*)(c_svc_req *, c_SVCXPRT *)> device_intr_1, 
				 0) # 0:no portmapper/IPPROTO_TCP/IPPROTO_UDP
            ELSE: # Others
                reg=svc_register(xprt, 
                                 cVXI11.DEVICE_INTR, 
                                 cVXI11.DEVICE_INTR_VERSION, 
                                 # we need cast here.
                                 <void (*)(c_svc_req *, c_SVCXPRT *)> device_intr_1, 
                                 0) # 0=IPPROTO_IP/IPPROTO_TCP()/IPPROTO_UDP
        vxi11logger.info("svc_register returns {}".format(reg))	
        if not reg: # svc_reigster returns one if it succeeds, zero otherwise.
            raise RuntimeError("cannot register RPC server")
        if self.svc_lock.locked():
                self.svc_lock.relsease()
	
        with nogil:# we must rlease Python GIL here. Otherwise main thread cannot getback GIL again.
            svc_run() # provided by rpc library. it never returns.
        vxi11logger.info("Failed to start rpc SVC")
        return

    def createSVCThread(self):
        cdef c_SVCXPRT *xprt
        cdef bool_t reg
        
        vxi11logger.info("Creating SVC thread")

        pmap_unset(cVXI11.DEVICE_INTR, 
                   cVXI11.DEVICE_INTR_VERSION)
		   
        xprt=svctcp_create(cVXI11.RPC_ANYSOCK, 0, 0)
	
        if xprt == NULL:
            raise RuntimeError("cannot create tcp service")

        self.svc_xprt=xprt
        self.srq_port=xprt.xp_port
        self.srq_sock=xprt.xp_sock
        self.svc_lock=threading.Lock()

        self.svc_thread=threading.Thread(
            name="SRQ_SVC-%s"%(self.srq_port,),
            target=self.run_svc, 
            args=(),
            kwargs=None,
        )
        
        Vxi11Device.srq_locks[self.svc_thread]=(self.svc_lock, self)
        
        #self.svc_thread.setDaemon(True) # for False, which is Thread default
        self.svc_thread.daemon=True # for False, which is Thread default

        #trick to find the local ip which is connected to the device
        ds=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        vxi11logger.info("conectiing portmapper at {host}".format(host=self.hostName))
        ds.connect((self.hostName, 111)) #111 is a port number for portmapper
        host=ds.getsockname()[0]
        # bs=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # bs.bind((ds.getsockname()[0], 0)) # follow EPICS/drvVXI11.c
        # host=bs.getsockname()[0]
        # vxi11logger.debug("bs host:{dsname} host:{host}".format(dsname=ds.getsockname()[0], host=host))
        # bs.close()
        vxi11logger.debug("ds host:{dsname} host:{host}".format(dsname=ds.getsockname()[0], host=host))
        ds.close()

        pa=socket.inet_aton(host)
        #vxi11logger.debug("ds host:{host} {ip}".format(host=host,ip=pa))
        self.intr_host=struct.unpack("!L",pa)[0]

        vxi11logger.debug("start SRQ server @ {info}".format(info=self.svc_thread))
        self.svc_thread.start()
        self.create_intr_chan(host=self.intr_host, 
                              intr_port=self.srq_port, 
                              proto=DEVICE_TCP)
        return

    def create_intr_chan(self, host=None, intr_port=None, proto=DEVICE_TCP):
        """
        notify a port number of srq socket to rpc server on device side
        """
        if(not host):
            self.intr_socket=self.createSrqSocket()
            host, self.intr_port=self.intr_socket.getsockname()
            pa=socket.inet_aton(host)
            self.intr_host=struct.unpack("!L",pa)[0]
        else:
            self.intr_host=host
            self.intr_port=intr_port

        vxi11logger.info(
            "prog: {prog}, version: {vers} prog: {prog}".format(
                prog=device_intr.prog,
                vers=device_intr.version,
            ))                     
        vxi11logger.info("intr_host/port: {host} @ {port}".format(
            host=socket.inet_ntoa(struct.pack("!L",self.intr_host)), port=self.intr_port))

        rf_parm=Device_RemoteFunc(
            self.intr_host,
            self.intr_port,
            device_intr.prog,
            device_intr.version,
            proto
        )
        
        with nogil:
            res=create_intr_chan_1(rf_parm.thisptr, self.clnt)

        if (not res) :
            raise RuntimeError("create_intr_chan failed error Empty return value")
        elif (res.error != 0):
            raise RuntimeError("create_intr_chan failed error %d"%res.error)

        if self.svc_lock.locked():
                self.svc_lock.relsease()
		
        vxi11logger.info("intr_chan was created")
	

    def destroy_intr_chan(self):
        cdef c_Device_Error *res=NULL
        vxi11logger.info("destroy intr_chan in destroy_intr_chan method")
        with nogil:
            res=destroy_intr_chan_1(NULL, self.clnt)
        if res and res.error == 0:
            return
        else:
            raise RuntimeError("destroy_intr_chan failed")

    def abort(self):
       cdef Device_Link parm
       if self.abt == NULL:
           raise RuntimeError("No abort channel")
       parm=self.lid
       with nogil:
           # for "rpcgen -N", this line should be modified accordingly.
           res=device_abort_1(cython.address(parm), self.abt)
       if res and res.error == 0:
           return
       else:
           if res :
               clnt_perror(self.abt, "abort() in Vxi11Device {}".format(res.error))
               raise RuntimeError("device_abort_1 returns {}".format(res.error))
           else:
               raise RuntimeError("Unknown Error")

    def destroy_link(self):
       cdef Device_Link parm
       cdef c_Device_Error *res=NULL
       
       parm=self.lid
       
       with  nogil:
           res=destroy_link_1(cython.address(parm),self.clnt)
       if res and res.error == 0:
           return
       else:
           if res:
               raise RuntimeError("destroy_link error:%d"%res.error)
           else:
               raise RuntimeError("destroy_link: Unknown Error")

    def __del__(self):
        cdef c_Device_Error *res=NULL
        cdef u_long prog=cVXI11.DEVICE_INTR
        cdef u_long vers=cVXI11.DEVICE_INTR_VERSION
        
        if (self.clnt != NULL) and (self.svc_thread != None):
            with nogil:
                res=destroy_intr_chan_1(NULL, self.clnt)
            vxi11logger.debug("intr_chan was destroyed")
            self.destroy_link()

        if self.svc_thread:
            vxi11logger.debug("unregister srq_svc")
            svc_unreigster(prog, vers)
            if self.svc_thread.isAlive():
                os.killpg(signal.SIGKILL, os.getpgid(os.getpid()))
                self.svc_thread.join()

        if self.clnt:
            vxi11logger.debug("destroy rpc client")
            with nogil:
                clnt_destroy (self.clnt)


    def remote(self,io_timeout=0):
        parm=Device_GenericParms(self.lid, 0, 0, io_timeout)
        with nogil:
            res = device_remote_1(parm.thisptr, self.clnt)
        if res and res.error == 0:
            return "remote"
        else:
            clnt_perror(self.clnt, "remote() failed{}".format(res.error))
            return "remote() failed with err code:%d"%res.error

    def local(self, io_timeout=0):
        parm=Device_GenericParms(self.lid, 0, 0, io_timeout)

        with nogil:
            res = device_local_1(parm.thisptr, self.clnt)
        if res and (res.error == 0):
            return "local"
        else:
            clnt_perror(self.clnt, "local failed{}".format(res.error))
            return "local() failed with error code:%d"%res.error

    def write(self,cmd=b"*IDN?;\n",
              io_timeout=0,
              lock_timeout=0,
              flags=DEVICE_FLAGS_END):
       cdef c_Device_WriteResp *res=NULL
       cdef char *cerrmsg

       if (io_timeout < 0):
           io_timeout=self.io_timeout
       if (lock_timeout < 0):
           lock_timeout= self.lock_timeout
       
       parm=Device_WriteParms(
           self.lid,
           io_timeout,
           lock_timeout,
           flags
       )
       # parm.thisptr.lid=self.lid;
       # parm.thisptr.io_timeout=10000
       # parm.thisptr.lock_timeout=10000
       # parm.thisptr.flags =DEVICE_FLAGS_END
       
       parm.data=cmd
       # parm.thisptr.data.data_val = cmd
       # parm.thisptr.data.data_len=len(cmd)
       
       try:
           with nogil:
               res = device_write_1(parm.thisptr, self.clnt)
       except:
           raise IOError("device_write Error")
       
       if (not res):
           errmsg="device_write_1"
           cerrmsg=errmsg
           with nogil:
               clnt_perror(self.clnt, cerrmsg)
           raise IOError("Null response from device_write_1")
       elif (res.error != 0):
           try:
               errmsg="device_write_1 err.:{err}".format(err=res.error)
               cerrmsg=errmsg
               with nogil:
                   clnt_perror(self.clnt, cerrmsg)
           except:
               raise IOError("clnt_perro failed in write()")
           try:
               xdr_free(<xdrproc_t> xdr_Device_WriteResp, <c_xdr_free_argtype> res)
           except:
               raise IOError("xdr_free failed in read with res.error code:{err}".format(err=res.error))
           raise IOError("device_write_1 in write() failed with error code:{err}".format(err=res.error))

       rsize=res.size
       try:
           with nogil:
               xdr_free(<xdrproc_t> xdr_Device_WriteResp, <c_xdr_free_argtype> res)
       except:
           raise IOError("xdr_free failed in write()")
       return rsize
   
    def read_one(self,
                requestSize=255, io_timeout=3000, lock_timeout=0,  # timeout in msec
                flags=device_flags_termchrset, termChar="\n"):
        r,reason=self._read_one(requestSize,
                                io_timeout,
                                lock_timeout,
                                flags, termChar)
        return r

    def _read_one(self,
                requestSize=255, io_timeout=3000, lock_timeout=0,
                flags=device_flags_termchrset, termChar="\n"):
        # read response, timeout in msec.
        parm=Device_ReadParms(
            self.lid,
            requestSize,
            io_timeout,
            lock_timeout,
            int(flags),
            termChar
         )
        # parm.thisptr.lid=self.lid
        # parm.thisptr.requestSize=requestSize
        # parm.thisptr.io_timeout=io_timeout
        # parm.thisptr.lock_timeout=lock_timeout
        # parm.thisptr.flags = int(flags)
        # parm.thisptr.termChar= ord(termChar)
        with nogil:
            res=device_read_1(parm.thisptr, self.clnt)
        if (not res):
            raise IOError
        elif (res.error != 0):
            with nogil:
                xdr_free(<xdrproc_t> xdr_Device_ReadResp, <c_xdr_free_argtype> res)
            raise IOError
        data=res.data.data_val[:res.data.data_len]
        reason=res.reason
        with nogil:
            xdr_free(<xdrproc_t> xdr_Device_ReadResp, <c_xdr_free_argtype> res)
        return (data, reason)

    def read(self, requestSize=4096,
             io_timeout=3000, lock_timeout=0,
             flags=device_flags_termchrset, termChar="\n"):
        #resp=""
        resp=[]
        r, reason=self._read_one(requestSize=requestSize,
                     io_timeout=io_timeout,
                     lock_timeout=lock_timeout,
                     flags=flags,
                     termChar=termChar)
        if r:
            #resp += r
            resp.append(r)
            #print len(r),
        #print "reason:",self.lastRes_reason,"resp:",len(r),r
        while ((reason & (DEVICE_READRESP_END|DEVICE_READRESP_CHR) == 0)):
            r=None
            try:
                r, reason = self._read_one(requestSize=requestSize,
                                           io_timeout=io_timeout,
                                           lock_timeout=lock_timeout,
                                           flags=flags,
                                           termChar=termChar)
                #print "lastRes:",reason,r,
                if r:
                    #resp +=r
                    resp.append(r)
                    #print len(r)
            except IOError as m:
                vxi11logger.warning( "IO error:read_one in read P {m}".format(m=m))
                raise 
                #break
            except TypeError as m:
                vxi11logger.warning("TypeError:read_one in read @ {m}".format(m=m))
                raise 
                #break
        resp=b"".join(resp)
        return resp

    def readResponse(self,requestSize=4096,io_timeout=30):
        return self.read(requestSize=requestSize, io_timeout=io_timeout)
    
    readResponce=readResponse # for backword compatibility
    
    def read_raw(self,requestSize=4096,io_timeout=30):
        return self.read(requestSize=requestSize, io_timeout=io_timeout)

    def ask(self, message, io_timeout=3000, termChar=b"\n", requestSize=4096):
        """ A name borrowed from PyVISA module """
        self.write(message, io_timeout=io_timeout)
        return self.read(io_timeout=io_timeout, termChar=termChar, 
                         requestSize=requestSize)

    ask_block=ask # for backword compatibility
    
    def readstb(self, flags=0, lock_timeout=0, io_timeout=5):
        parm=Device_GenericParms(self.lid, flags, lock_timeout, io_timeout)
        with nogil:
            res=device_readstb_1(parm.thisptr, self.clnt)
        if (not res):
            raise RuntimeError
        elif (res.error != 0):
            with nogil:
                xdr_free(<xdrproc_t> xdr_Device_ReadStbResp, <c_xdr_free_argtype> res)
            raise RuntimeError
        rstb=res.stb
        with nogil:
            xdr_free(<xdrproc_t> xdr_Device_ReadStbResp, <c_xdr_free_argtype> res)
        return rstb

    def trigger(self, flags=0, lock_timeout=0, io_timeout=5):
        parm=Device_GenericParms(self.lid,
                                 flags,
                                 lock_timeout,
                                 io_timeout)
        with nogil:
            res=device_trigger_1(parm.thisptr, self.clnt)
        if (not res) or (res.error != 0):
            raise RuntimeError
        return res.error
    
    def clear(self,flags=0,lock_timeout=0,io_timeout=5):
        parm=Device_GenericParms(self.lid,
                                 flags,
                                 lock_timeout,
                                 io_timeout)
        with nogil:
            res=device_clear_1(parm.thisptr, self.clnt)
        if (not res) or (res.error != 0):
            raise RuntimeError("failed to clear a device")

    def lock(self,flags=0,lock_timeout=0):
        parm=Device_LockParms(self.lid, flags, lock_timeout)
        # parm.thisptr.lid=self.lid
        # parm.thisptr.flags=flags
        # parm.thisptr.lock_timeout=lock_timeout
        with nogil:
            res=device_lock_1(parm.thisptr, self.clnt)
        if (not res) or (res.error != 0):
            clnt_perror(self.clnt, "failed to lock the device")
            raise RuntimeError("failed to lock the device")

    def unlock(self):
       # cdef Device_Link parm
       # parm=self.lid
       with nogil:
           res=device_unlock_1(cython.address(self.lid), self.clnt)
       if (not res) or (res.error != 0):
           raise RuntimeError("failed to unlock the device")

    def enable_srq(self, int enable=True):
        cdef c_Device_Error *res
        
        parm=Device_EnableSrqParms(self.lid)
        with nogil:
            if enable:
                parm.thisptr.enable=1
            else:
                parm.thisptr.enable=0
            res=device_enable_srq_1(parm.thisptr, self.clnt)
        if (not res) or (res.error != 0):
            raise RuntimeError("enable_srq_1 failed")

    def disable_srq(self):
        self.enable_srq(False)
        
    def docmd(self, cmd, data="", flags=0, io_timeout=1000,
              lock_timeout=0, network_order=1, ):
        parm=Device_DocmdParms(
            self.lid,
            flags,
            io_timeout,
            lock_timeout,
            cmd,
            network_order,
            len(data)
        )
        parm.data_in=data
        with nogil:
            res=device_docmd_1(parm.thisptr,self.clnt)
        if (not res):
            raise RuntimeError("docmd failed")
        elif (res.error != 0):
            with nogil:
                xdr_free(<xdrproc_t> xdr_Device_DocmdResp, 
                 <c_xdr_free_argtype> res)
            raise RuntimeError("docmd failed[%s]"%res.error)
        rdata=res.data_out.data_out_val[:res.data_out.data_out_len]
        with nogil:
            xdr_free(<xdrproc_t> xdr_Device_DocmdResp, 
                     <c_xdr_free_argtype> res)
        return rdata

    # Common * commsnds in IEEE488.2

    def CLS(self, io_timeout=0): # *CLS - Clear status
        return self.write(b"*CLS", io_timeout=io_timeout)

    def qESR(self): # *ESR? - Event status register query
        return self.ask(b"*ESR?")
    
    def ESE(self, io_timeout=0): # *ESE <enable_value> - Event status enable
        return self.write(b"*ESE",io_timeout=io_timeout)

    def qESE(self):
        return self.ask(b"*ESE?")

    def qIDN(self): # *IDN? - Instrument identification
        return self.ask(b"*IDN?")

    def qLRN(self, io_timeout=0):
        self.write(b"*LRN?", io_timeout=io_timeout)
        return self.readResponse(io_timeout=io_timeout)

    def qLRN_as_dict(self,io_timeout=0):
        self.write(b"*LRN?",io_timeout=io_timeout)
        s=self.readResponse(io_timeout=io_timeout)
        # it assumes ASCII mode.
        def mkpair(w):
            for e in w.split():
                if len(e) == 1:
                    return(e[0],None)
                elif len(e) > 2:
                    return (e[0]," ".join(e[1:]))
                else:
                    return e
        d=[mkpair(w) for w in s.split(";")]
        d=dict(d)
        return d
        
    def OPC(self,io_timeout=0): # *OPC - Set operation complete bit
        return self.write(b"*OPC",io_timeout=io_timeout)

    def qOPC(self): # *OPC? - Wait for current operation to complete
        return self.ask("*OPC?")
    
    def qOPT(self): # *OPT? - Show installed options
        return self.ask("*OPT?")
    
    def PSC(self, flag): # *PSC {0|1} - Power-on status clear
        if flag:
            return self.write(b"PSC 1")
        else:
            return self.write(b"PSC 0")
        
    def RCL(self,value=0, io_timeout=0): # *RCL {0|1|2|3|4} - Recall instrument state
        "<value> ::= {0 | 1 | 2 | 3 | 4 |5 | 6 | 7 | 8 | 9}"
        return self.write(b"*RCL %d"%value, io_timeout=io_timeout)

    def SAV(self,value=0, io_timeout=0): #*SAV {0|1|2|3|4} - Save instrument state
        "<value> ::= {0 | 1 | 2 | 3 | 4 |5 | 6 | 7 | 8 | 9}"
        return self.write(b"*SAV %d"%value, io_timeout=io_timeout)
 
    def RST(self,io_timeout=0): # *RST - Reset instrument to factory defaults
        return self.write(b"*RST",io_timeout=io_timeout)

    def SRE(self,mask=255,io_timeout=0): # *SRE <enable_value> - Service request enable (enable bits in enable register of Status Byte Register group
        """
        <mask> ::= sum of all bits thatare set, 0 to 255; an integer inNR1 format.
        <mask> ::= followingvalues:
        Bit Weight Name Enables
        --- ------ ---- ----------
        7 128 OPER Operation Status Reg
        6 64 ---- (Not used.)
        5 32 ESB Event Status Bit
        4 16 MAV Message Available
        3 8 ---- (Not used.)
        2 4 MSG Message
        1 2 USR User
        0 1 TRG Trigger
        quoted from "600_series_prog_refernce.pdf" by Agilent Tecnology.
        """
        return self.write(b"*SRE %d"%value, io_timeout=io_timeout)

    def qSRE(self,mask=255):
        return self.ask(b"*SRE?")

    def qSTB(self):# *STB? - Read status byte
        """
        <value> ::= 0 to 255; an integer in NR1 format, as shown in the following:
        Bit Weight Name  "1" Indicates
        --- ------ ----  ---------------
        7   128   OPER  Operation status condition occurred. 
        6   64 RQS/ MSS Instrument is requesting service.
        5   32 ESB  Enabled event status condition occurred. 
        4   16 MAV  Message available. (Not used.)
        3   8 ---- 
        2   4 MSG   Message displayed. 
        1   2 USR   User event condition occurred. 
        0   1 TRG   A trigger occurred.
        quoted from "600_series_prog_refernce.pdf" by Agilent Tecnology.
        """
        return self.ask(b"*STB?")

    def TRG(self, io_timeout=0): #*TRG - Trigger command
        return self.write(b"*TRG", io_timeout=io_timeout)

    def qTST(self,io_timeout=3000): #*TST? - Self-test
        return self.ask(b"*TST?", io_timeout=io_timeout)

    def WAI(self,io_timeout=0): #*WAI - Wait for all pending operations to complete
        return self.write(b"*WAI",io_timeout=io_timeout)

    # vxi11scan functionality as class method. 
    @classmethod
    def scan(cls, host=b"10.9.16.20", device=b"inst0,0",
             command=b"*IDN?", proto=b"tcp",
             io_timeout=0, lock_timeout=0):
        clnt=clnt_create(host,
                         device_core.prog,
                         device_core.version,
                         proto )
        if not clnt:
            vxi11logger.warning("Failed to create client {host} {device}".format(host=host,device=device))
            raise IOError

        create_link_parm=Create_LinkParms(
            0, 0, lock_timeout, device
        )
        # create_link_parm.thisptr.lockDevice=0
        # create_link_parm.thisptr.lock_timeout=0 
        # create_link_parm.thisptr.device=device 

        with nogil:
            link = create_link_1(create_link_parm.thisptr, clnt)

        if not link:
            raise IOError("failed to create link")
        vxi11logger.debug( "link created to {msg} \n".format(msg=create_link_parm.thisptr.device))
        vxi11logger.debug("\t Error code:{err}\n\t LinkID:{lid}\n\t port {port}\n\t MaxRecvSize:{maxsize}\n".format(
            err=link.error, lid=link.lid ,
            port=link.abortPort, maxsize=link.maxRecvSize))
        if link.error != 0:
            raise IOError("Link creation error {erc}".format(erc=link.error))
        
        # check remote or not
        device_remote_parm=Device_GenericParms(link.lid, 0, lock_timeout, io_timeout)

        with nogil:
            result_7 = device_remote_1(device_remote_parm.thisptr, clnt);
        
        if not result_7 :
            vxi11logger.debug("failed to make it remote")
            raise IOError("failed to make it remote")
        
        if result_7.error !=0:
            vxi11logger.debug("failed to make it remote {err}".format(err=result_7.error))
            raise IOError("failed to make it remote {err}".format(err=result_7.error))
        
        vxi11logger.info("Device is remote. RC:{rc}\n".format(rc=result_7.error))

        # send a command
        device_write_parm=Device_WriteParms(
            link.lid,
            io_timeout,
            lock_timeout,
            device_flags_end
        )
        device_write_parm.data=command
        
        # device_write_parm.thisptr.lid=link.lid
        # device_write_parm.thisptr.io_timeout=10000
        # device_write_parm.thisptr.lock_timeout=10000
        # device_write_parm.thisptr.flags = device_flags_end
        # device_write_parm.thisptr.data.data_val = command
        # device_write_parm.thisptr.data.data_len= len(command)
        
        with nogil:
            result_2 = device_write_1(device_write_parm.thisptr, clnt);
        
        vxi11logger.info("wrote {cmd} \n".format(cmd=device_write_parm.thisptr.data.data_val))

        # read response
        device_read_parm=Device_ReadParms(
            link.lid,
            255, 3000+io_timeout, lock_timeout, device_flags_termchrset, '\n'
        )

        vxi11logger.debug("Setting up Device Read parms")
        
        # device_read_parm.thisptr.lid=link.lid
        # device_read_parm.thisptr.requestSize=255
        # device_read_parm.thisptr.io_timeout=3000
        # device_read_parm.thisptr.lock_timeout=0
        # device_read_parm.thisptr.flags = int(device_flags_termchrset)
        # device_read_parm.thisptr.termChar=ord('\n')

        vxi11logger.debug("calling deviece read")
        
        with nogil:
            result_3 = device_read_1(device_read_parm.thisptr, clnt);
        if (not result_3):
            vxi11logger.debug("No response from device")
            raise IOError("No response from device")
        
        if (result_3.error !=0):
            err=result_3.error
            vxi11logger.debug("No response from device err_code:{err} ".format(err=err))
            with nogil:
                xdr_free(<xdrproc_t> xdr_Device_ReadResp, <c_xdr_free_argtype> result_3)
            raise IOError("No response from device err_code:{err} ".format(err=err))

        vxi11logger.info("{sz} bytes data read:{cmd}\n".format(
            sz=result_3.data.data_len,
            cmd=result_3.data.data_val))

        vxi11logger.debug("clear device")
        
        dev_clear_parms=Device_GenericParms(link.lid, 0, 0, io_timeout)
        with nogil:
            res=device_clear_1(dev_clear_parms.thisptr, clnt)
        if not res:
            vxi11logger.warning("device_clear call failed")
        
        vxi11logger.debug("destroy device")
        with  nogil:
            res=destroy_link_1(cython.address(link.lid), clnt)
        if res and res.error == 0:
            with nogil:
                clnt_destroy (clnt);
            return 0
        else:
            if res:
                raise RuntimeError("destroy_link error:%d"%res.error)
            else:
                raise RuntimeError("destroy_link: Unknown Error")

# from VXI11_svc.c RPC handler for intr routine

cdef extern void device_intr_1(c_svc_req *rqstp, c_SVCXPRT *transp)
cdef public long _rpcsvcdirty=0 # export _rpcsvcdirty for C-library

# SVC stubs: These entries provided just to avoid error messages. functions decleared in VXI11.h
cdef public c_Device_Error *device_abort_1_svc(Device_Link *argp, c_svc_req *rqstp) nogil:
# "rpcgen -N " generates the following fuction prototype declaration. 
#cdef public c_Device_Error *device_abort_1_svc(Device_Link argp, c_svc_req *rqstp) nogil:
    cdef c_Device_Error *result=NULL
    return result

cdef public c_Device_WriteResp *device_write_1_svc(c_Device_WriteParms *argp, c_svc_req *rqstp) nogil:
#cdef public c_Device_WriteResp *device_write_1_svc(c_Device_WriteParms argp, c_svc_req *rqstp) nogil:
    cdef c_Device_WriteResp *result=NULL
    return result

cdef public c_Device_ReadResp *device_read_1_svc(c_Device_ReadParms *argp, c_svc_req *rqstp) nogil:
#cdef public c_Device_ReadResp *device_read_1_svc(c_Device_ReadParms argp, c_svc_req *rqstp) nogil:
    cdef c_Device_ReadResp *result=NULL
    return result

cdef public c_Device_ReadStbResp * device_readstb_1_svc(c_Device_GenericParms *argp, c_svc_req *rqstp) nogil:
#cdef public c_Device_ReadStbResp * device_readstb_1_svc(c_Device_GenericParms argp, c_svc_req *rqstp) nogil:
    cdef c_Device_ReadStbResp *result=NULL
    return result

cdef public c_Device_Error *device_trigger_1_svc(c_Device_GenericParms *argp, c_svc_req *rqstp) nogil:
#cdef public c_Device_Error *device_trigger_1_svc(c_Device_GenericParms argp, c_svc_req *rqstp) nogil:
    cdef c_Device_Error *result=NULL
    return result

cdef public c_Device_Error *device_clear_1_svc(c_Device_GenericParms *argp, c_svc_req *rqstp) nogil:
#cdef public c_Device_Error *device_clear_1_svc(c_Device_GenericParms argp, c_svc_req *rqstp) nogil:
    cdef c_Device_Error *result=NULL
    return result

cdef public c_Device_Error *device_remote_1_svc(c_Device_GenericParms *argp, c_svc_req *rqstp) nogil:
#cdef public c_Device_Error *device_remote_1_svc(c_Device_GenericParms argp, c_svc_req *rqstp) nogil:
    cdef c_Device_Error *result=NULL
    return result

cdef public c_Device_Error *device_local_1_svc(c_Device_GenericParms *argp, c_svc_req *rqstp) nogil:
#cdef public c_Device_Error *device_local_1_svc(c_Device_GenericParms argp, c_svc_req *rqstp) nogil:
    cdef c_Device_Error *result=NULL
    return result

cdef public c_Device_Error *device_lock_1_svc(c_Device_LockParms *argp, c_svc_req *rqstp) nogil:
#cdef public c_Device_Error *device_lock_1_svc(c_Device_LockParms argp, c_svc_req *rqstp) nogil:
    cdef c_Device_Error *result=NULL
    return result

cdef public c_Device_Error *device_unlock_1_svc(Device_Link *argp, c_svc_req *rqstp) nogil:
#cdef public c_Device_Error *device_unlock_1_svc(Device_Link argp, c_svc_req *rqstp) nogil:
    cdef c_Device_Error *result=NULL
    return result

cdef public c_Device_Error *device_enable_srq_1_svc(c_Device_EnableSrqParms *argp, c_svc_req *rqstp) nogil:
#cdef public c_Device_Error *device_enable_srq_1_svc(c_Device_EnableSrqParms argp, c_svc_req *rqstp) nogil:
    cdef c_Device_Error *result=NULL
    return result

cdef public c_Device_DocmdResp *device_docmd_1_svc(c_Device_DocmdParms *argp, c_svc_req *rqstp) nogil:
#cdef public c_Device_DocmdResp *device_docmd_1_svc(c_Device_DocmdParms argp, c_svc_req *rqstp) nogil:
    cdef c_Device_DocmdResp *result=NULL
    return result


cdef public c_Device_Error *destroy_link_1_svc(Device_Link *argp, c_svc_req *rqstp) nogil:
#cdef public c_Device_Error *destroy_link_1_svc(Device_Link argp, c_svc_req *rqstp) nogil:
    cdef c_Device_Error *result=NULL
    return result

cdef public c_Device_Error *create_intr_chan_1_svc(c_Device_RemoteFunc *argp, c_svc_req *rqstp) nogil:
    cdef c_Device_Error *result=NULL
    return result

cdef public c_Create_LinkResp *create_link_1_svc(c_Create_LinkParms *argp, c_svc_req *rqstp) nogil:
#cdef public c_Create_LinkResp *create_link_1_svc(c_Create_LinkParms argp, c_svc_req *rqstp) nogil:
    cdef c_Create_LinkResp *result=NULL
    return result

cdef public c_Device_Error *destroy_intr_chan_1_svc(void  *argp, c_svc_req *rqstp) nogil:
    cdef c_Device_Error *result=NULL
    return result

# intr_srq handler

cdef public void *device_intr_srq_1_svc(c_Device_SrqParms *argp, c_svc_req *rqstp) nogil:
    cdef void *result=NULL
    
    with gil:
        vxi11logger.info( "SRQ received: {thread} {handle_len} {handle}".format(
            thread=threading.currentThread(),
            handle_len=argp.handle.handle_len,
            handle=argp.handle.handle_val[:argp.handle.handle_len]))
        try:
            lock, osc=Vxi11Device.srq_locks[threading.currentThread()]
        except:
            vxi11logger.warn( "Failed to get a lock in device_intr_srq_svc".format())
            raise
        osc.disable_srq()
        try:
            if lock.locked():
                lock.release()
                vxi11logger.debug( "SRQ lock released locked:{lock}".format(
                    lock=lock.locked()))
        except:
            raise
        finally:
            # osc.disable_srq()
            pass
    # end gil
    return result

# from Table B.1 "Allowed Generic Commands" in vxi-11.2 documents.

cdef enum:
    # name            cmd     data_in/data_len  datasize
    SEND_CMD      = 0x020000 # 0-128             1
    BUS_STATUS_CMD= 0x020001 # 2                 2
    ATN_CNTRL_CMD = 0x020002 # 2                 2
    REN_CNTRL_CMD = 0x020003 # 2                 2
    PASS_CNTRL_CMD= 0x020004 # 4                 4
    BUS_ADRS_CMD  = 0x02000A # 4                 4
    IFC_CNTRL_CMD = 0x020010 # 0                 X

class GenericCommands:
    SEND=         SEND_CMD
    BUS_STATUS=   BUS_STATUS_CMD
    ATN=          ATN_CNTRL_CMD
    REN=          REN_CNTRL_CMD
    PASS=         PASS_CNTRL_CMD
    BUS_ADRS=     BUS_ADRS_CMD
    IFC=          IFC_CNTRL_CMD

# from Table B.2 "Table B.2 Received and Returned Values for Bus Status" in vxi-11.2 document

class Bus_Status:
    # name = data_in  return value #Bus_status data_len is 2
    REMOTE= b"\x00\x01"          # 1 if REN 0 otherwise
    SRQ   = b"\x00\x02"          # 1 if SRQ 0 otherwise 
    NDAC  = b"\x00\0x3"          # 1 if NDAC 0 otherwise
    SYSTEM_CONTROLLER=b"\x00\x04"  # 1 or 0
    CONTROLLER_IN_CHARGE=b"\x00\x05" # 1 or 0
    TALKER= b"\x00\x06"              # 1 or 0
    LISTENER=b"\x00\x07"             # 1 or 0
    BUS_ADDRESS=b"\x00\x08"          # TCP/IP IEEE 488.1 interface device's address 0-30

class GPIBInterfaceDevice(Vxi11Device): # IEEE488_1Device?
    """
    class for TCP/IP IEEE488.1 Interface device, described in the vxi-11.2
    These methods are used to send out GPIB-Bus command to GPIB lines.
    """
    def SEND(self, data="\x00", flags=0, io_timeout=1000,
              lock_timeout=0, network_order=1,):
        """
        Send arbitrary interface dependent command to the device. 
        data_in/datasize:0-128/1
        """
        return self.docmd(GenericCommands.SEND, data=data,
                          flags=flags, io_timeout=io_timeout,lock_timeout=lock_timeout,
                          network_order=network_order)

    def BUS_STATUS(self, data="\x00\x00", flags=0, io_timeout=1000,
              lock_timeout=0, network_order=1,):
        """
        data_in_len/datasize:2
        """
        return self.docmd(GenericCommands.BUS_STATUS, data=data,
                          flags=flags, io_timeout=io_timeout,lock_timeout=lock_timeout,
                          network_order=network_order)

    def ATN(self,data="\x00\x00", flags=0, io_timeout=1000,
              lock_timeout=0, network_order=1,):
        """
        data_in_len/datasize:2
        """
        return self.docmd(GenericCommands.ATN,data=data,
                          flags=flags, io_timeout=io_timeout,lock_timeout=lock_timeout,
                          network_order=network_order)

    def REN(self,data="\x00\x00", flags=0, io_timeout=1000,
              lock_timeout=0, network_order=1,):
        """
        send remote enabel
        data_in_len/datasize:2
        """
        return self.docmd(GenericCommands.REN,data=data,
                          flags=flags, io_timeout=io_timeout,lock_timeout=lock_timeout,
                          network_order=network_order)

    def PASS(self,data="\x00\x00\x00\x00", flags=0, io_timeout=1000,
              lock_timeout=0, network_order=1,):
        """
        Pass Control 
        data_in_len/datasize:4
        """
        return self.docmd(GenericCommands.PASS,data=data,
                          flags=flags, io_timeout=io_timeout,lock_timeout=lock_timeout,
                          network_order=network_order)

    def BUSADRS(self,data="\x00\x00\x00\x00", flags=0, io_timeout=1000,
              lock_timeout=0, network_order=1,):
        """
        data_in_len/datasize:4
        """
        return self.docmd(GenericCommands.BUS_ADRS, data=data,
                          flags=flags, io_timeout=io_timeout,lock_timeout=lock_timeout,
                          network_order=network_order)

    def IFC(self, flags=0, io_timeout=1000,
              lock_timeout=0, network_order=1):
        """
        data_in_len/datasize:0/X
        """
        return self.docmd(GenericCommands.IFC, data="",
                          flags=flags, io_timeout=io_timeout,lock_timeout=lock_timeout,
                          network_order=network_order)
    
    def qREMOTE(self, flags=0, io_timeout=1000,
              lock_timeout=0, network_order=1,):
        return self.BUS_STATUS(Bus_Status.REMOTE,
                               flags=flags, io_timeout=io_timeout,lock_timeout=lock_timeout,
                               network_order=network_order)

    def qSRQ(self, flags=0, io_timeout=1000,
              lock_timeout=0, network_order=1,):
        return self.BUS_STATUS(Bus_Status.SRQ,
                               flags=flags, io_timeout=io_timeout,lock_timeout=lock_timeout,
                               network_order=network_order)
    
    def qNDAC(self, flags=0, io_timeout=1000,
              lock_timeout=0, network_order=1,):
        return self.BUS_STATUS(Bus_Status.NDAC,
                               flags=flags, io_timeout=io_timeout,lock_timeout=lock_timeout,
                               network_order=network_order)

    def qSYSTEM_CONTROLLER(self, flags=0, io_timeout=1000,
              lock_timeout=0, network_order=1,):
        return self.BUS_STATUS(Bus_Status.SYSTEM_CONTROLLER,
                               flags=flags, io_timeout=io_timeout,lock_timeout=lock_timeout,
                               network_order=network_order)

    def qCONTROLLER_IN_CHARGE(self, flags=0, io_timeout=1000,
             lock_timeout=0, network_order=1,):
        return self.BUS_STATUS(Bus_Status.CONTROLLER_IN_CHARGE,
                               flags=flags, io_timeout=io_timeout,lock_timeout=lock_timeout,
                               network_order=network_order)

    def qTALKER(self, flags=0, io_timeout=1000,
              lock_timeout=0, network_order=1,):
        return self.BUS_STATUS(Bus_Status.TALKER,
                               flags=flags, io_timeout=io_timeout,lock_timeout=lock_timeout,
                               network_order=network_order)

    def qLISTENER(self, flags=0, io_timeout=1000,
              lock_timeout=0, network_order=1,):
        return self.BUS_STATUS(Bus_Status.LISTENER,
                               flags=flags, io_timeout=io_timeout,lock_timeout=lock_timeout,
                               network_order=network_order)

    def qBUS_ADDRESS(self, flags=0, io_timeout=1000,
              lock_timeout=0, network_order=1,):
        """
        returns Buss address as 16bits integer. use struct.unpack(">H",result) ord(result[-1]) to convert it to integer
        """
        return self.BUS_STATUS(Bus_Status.BUS_ADDRESS,
                               flags=flags, io_timeout=io_timeout,lock_timeout=lock_timeout,
                               network_order=network_order)

IEEE488_1Device=GPIBInterfaceDevice

class IEEE488_2Device(Vxi11Device):
    """The TCP/IP-IEEE 488.2 Instrument Interface SHALL NOT perform any action when it receives a device_docmd RPC, 
    but SHALL terminate with error set to 8, operation not supported,.
    """
    def __init__(self, char * host, char *device=b"inst0",
                 char *proto=b"tcp",lock_timeout=0,lockDevice=0):
        GPIBInterfaceDevice.__init__(self, host, device,
                             proto, lock_timeout, lockDevice)
#
def rpcinfo(host):
    import os
    os.system("/usr/sbin/rpcinfo -p {host}".format(host=host.decode()))

def device_has_async_port(host):
    #import os
    # DEVICE_INTR_program=0x0607B1
    # DEVICE_CORE_program=0x0607AF
    # DEVICE_ASYNC_program=0x0607B0
    DEVICE_INTR_program=device_intr.prog
    DEVICE_CORE_program=device_core.prog
    DEVICE_ASYNC_program=device_async.prog
    
    #cmdargs="-t {} 395184".format(host.decode()) # 395184=0x0607B0  : VXI11 Device_ASYNC program (device_abort)
    #cmdargs="-t {} 395185".format(host.decode()) # 395185=0x0607B1 : VXI11 DEVICE_INTR program
    # search for rpcinfo in /usr/sbin or PATH.
    # for path in ["/usr/sbin"]+os.getenv("PATH").split(os.path.pathsep):
    #     cmdpath=os.path.join(path, "rpcinfo")
    #     if os.path.exists(cmdpath):
    #         if os.system("{} {}".format(cmdpath,cmdargs)):
    #             return True
    #         else:
    #             return False
    # return False
    if (cPMAP_getport(host, device_async.prog, device_async.version, IPPROTO_TCP) == 0):
        return False
    else:
        return True

# for pmap_getport
# cdef extern from "netinet/in.h":
def pmap_getport(host:str, program, version=1, protocol=IPPROTO_TCP):
    return cPMAP_getport(host.encode('utf-8'), program, version, protocol)

cdef _pmap_getmaps(char *host):
   """ 
   glue routine for pmap_getmaps. 
   """
   cdef c_pmaplist *pml
   pml = cPMAP_getmaps(host)
   l=[]
   while pml:
       l.append(pml.pml_map)
       pml=pml.pml_next
   return l

def pmap_getmaps(host:str):
    """
    pmap_getmaps(host:str)
    returns a list of portmapper map list.
    """
    return _pmap_getmaps(host.encode("utf-8"))

def pmap_unset(serv:str, vers):
    cdef  u_int  SERV=serv
    cdef  u_int  VERS=vers
    cdef  u_int RC
    
    with nogil:
        RC=cPMAP_unset(SERV, VERS)
    
    return RC		

