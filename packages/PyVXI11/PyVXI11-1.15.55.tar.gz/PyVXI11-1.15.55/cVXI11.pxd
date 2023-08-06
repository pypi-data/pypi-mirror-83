# definition 
# distutils: language=c++
       #  """
       #  struct sockaddr_inarp .//netinet/if_ether.h
       #  struct sockaddr_un /* actual length of an initialized sockaddr_un */.//sys/un.h
       #  struct sockaddr_ctl :.//sys/kern_control.h
       #  struct sockaddr_storage .//sys/socket.h
       #  struct sockaddr_sys {.//sys/sys_domain.h
       #  struct sockaddr_in {
       #      __uint8_t       sin_len;
       #      sa_family_t     sin_family;
       #      in_port_t       sin_port;
       #      struct  in_addr sin_addr;
       #      char            sin_zero[8];
       #  };
       #  struct in_addr {
       #      in_addr_t s_addr;
       #  };
       #  typedef __uint32_t      in_addr_t;      /* base type for internet address */
       #  struct sockaddr_in6 {
       #      __uint8_t       sin6_len;       /* length of this struct(sa_family_t) */
       #      sa_family_t     sin6_family;    /* AF_INET6 (sa_family_t) */
       #      in_port_t       sin6_port;      /* Transport layer port # (in_port_t) */
       #       __uint32_t      sin6_flowinfo;  /* IP6 flow information */
       #      struct in6_addr sin6_addr;      /* IP6 address */
       #      __uint32_t      sin6_scope_id;  /* scope zone index */
       #  };
       # typedef struct in6_addr {
       #    union {
       #       __uint8_t   __u6_addr8[16];
       #       __uint16_t  __u6_addr16[8];
       #       __uint32_t  __u6_addr32[4];
       #    } __u6_addr;                    /* 128-bit IP6 address */
       #  } in6_addr_t;
       #  """

cdef extern from "sys/types.h":
  ctypedef unsigned char  __uint8_t
  ctypedef          char  __int8_t
  ctypedef unsigned short  __uint16_t
  ctypedef          short  __int16_t
  ctypedef unsigned int  __uint32_t
  ctypedef          int  __int32_t
  ctypedef unsigned long long __uint64_t
  ctypedef          long long __int64_t
  ctypedef unsigned long  u_long
  ctypedef unsigned int   u_int
  ctypedef unsigned short u_short
  ctypedef unsigned char  u_char
  ctypedef int            bool_t

cdef extern from "arpa/inet.h":
  cdef char *addr2ascii(int af, const void *addrp, int len, char *buf)

  cdef int  ascii2addr(int af, const char *ascii, void *result)

  # cdef in_addr_t inet_addr(const char *);
  # char	*inet_ntoa(struct in_addr);
  # const char	*inet_ntop(int, const void *, char *, socklen_t);
  # int		 inet_pton(int, const char *, void *);
  

cdef extern from "netinet/in.h":
    # cdef struct c_sockaddr_in "sockaddr_in":
    #    pass
    cdef struct c_sockaddr_in "sockaddr_in"
   
    cdef enum:
       IPPROTO_IP 
       IPPROTO_ICMP
       IPPROTO_IGMP
       IPPROTO_GGP
       IPPROTO_IPV4
       IPPROTO_TCP
       IPPROTO_UDP
       IPPROTO_IPV6
       IPPROTO_RAW

# for opaque data<> in VXI11.rpcl
#
cdef extern from "rpc/rpc.h":
  ctypedef struct c_CLIENT "CLIENT":
    pass

  ctypedef c_CLIENT c_CLIENT_t
  
cdef extern from "rpc/svc.h":
    cdef enum:
       RPC_ANYSOCK = -1

    ctypedef struct c_svc_req "struct svc_req":
       pass

    ctypedef struct c_SVCXPRT "SVCXPRT":
      int xp_sock
      u_short xp_port

    cdef c_SVCXPRT *svcraw_create() nogil

    cdef c_SVCXPRT *svcudp_create(int) nogil

    cdef c_SVCXPRT *svcudp_bufcreate(int, u_int, u_int) nogil

    cdef c_SVCXPRT *svcfd_create(int , u_int, u_int) nogil

    cdef c_SVCXPRT *svctcp_create(int , u_int, u_int) nogil

    # prototypes in rpc/svc.h was changed 
    IF UNAME_SYSNAME == "Darwin":
      cdef bool_t svc_register(c_SVCXPRT *, 
                               u_long,
                               u_long,
                               void (*)(),
                               int ) nogil
    ELIF UNAME_SYSNAME == "Linux": # Linux
      cdef bool_t svc_register(c_SVCXPRT *,
                               u_long,
                               u_long,
                               void (*)(c_svc_req *, c_SVCXPRT *),
                               int ) nogil
    ELSE: # Others
      cdef bool_t svc_register(c_SVCXPRT *,
                               unsigned int ,
                               unsigned int ,
                               void (*)(c_svc_req *, c_SVCXPRT *),
                               int ) nogil

    cdef void svc_unregister(u_long, u_long) nogil

    cdef void xprt_register(c_SVCXPRT *) nogil
    cdef void xprt_unregister(c_SVCXPRT *) nogil

    cdef void rpctest_service() nogil

    cdef void svc_run() nogil # never return    

    cdef void svc_getreq(int) nogil
    #cdef voit svc_getrequest(fd_set *)

ctypedef long Device_Flags

#
#//from rpc/clnt.h
cdef extern  from "rpc/clnt.h":
  cdef struct handle_type:
       u_int handle_len
       char *handle_val

  cdef c_CLIENT *clnt_create(
      char *host,
      u_long prog,
      u_long vers,
      char *prot) nogil
  # clnt_control in rpc/clnt.h is not a function but just a macro
  # cdef bool_t clnt_control(c_CLIENT *cl, u_int req, char *info)

  ctypedef struct c_timeval "timeval":
      pass

  ctypedef enum c_clnt_stat "clnt_stat":
      pass
  
  cdef c_CLIENT *clnttcp_create(
      c_sockaddr_in *raddr,
      u_long prog,
      u_long version,
      int * sockp,
      u_int sendsz,
      u_int recvsz) nogil

  cdef c_CLIENT *clntudp_create(
      c_sockaddr_in *raddr,
      u_long program,
      u_long version,
      c_timeval wait,
      int *sockp
  ) nogil

  cdef c_CLIENT *clntudp_bufcreate(
        c_sockaddr_in *raddr,
	u_long program,
	u_long version,
	c_timeval wait,
	int *sockp,
	u_int sendsz,
	u_int recvsz
        ) nogil
        
  cdef void clnt_destroy(c_CLIENT *) nogil
  cdef char *clnt_sperror(c_CLIENT * , char *) nogil
  cdef void clnt_perror(c_CLIENT * , char *)  nogil
  cdef void clnt_pcreateerror	(char *) nogil
  cdef char *clnt_spcreateerror	(char *) nogil
  cdef void clnt_perrno(c_clnt_stat stat) nogil
  cdef char *clnt_sperrno(c_clnt_stat stat) nogil


  ctypedef long Device_Link
  ctypedef long c_Device_Link

  ctypedef long Device_ErrorCode_t
  ctypedef long c_Device_ErrorCode_t

  ctypedef struct c_XDR "XDR": # typename is same as struct name in Cython
    pass

cdef extern from "rpc/xdr.h":
    ctypedef bool_t (*xdrproc_t)(c_XDR *, void *, u_int)

    IF UNAME_SYSNAME == "Darwin":
        void xdr_free(xdrproc_t, void *) nogil
        #ctypedef void *c_xdr_free_argtype
    ELIF UNAME_SYSNAME == "Linux":
        void xdr_free(xdrproc_t, char *) nogil
        #ctypedef char *c_xdr_free_argtype
# 

cdef extern from "VXI11.h":
  ctypedef  bool_t xdr_Device_Link(c_XDR *, Device_Link *) nogil

  ctypedef enum c_Device_AddrFamily "Device_AddrFamily": 
    DEVICE_TCP = 0
    DEVICE_UDP = 1
    
  cdef extern bool_t xdr_Device_AddrFamily(c_XDR *, c_Device_AddrFamily*) nogil

  ctypedef enum Device_ErrorCode:
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
      Device_ErrorCode_No_Error = 0
      Device_ErrorCode_Syntax_Error = 1
      Device_ErrorCode_not_Accessible = 3
      Device_ErrorCode_invalid_Link_Id = 4
      Device_ErrorCode_Parm_Error = 5
      Device_ErrorCode_Chan_not_Established = 6
      Device_ErrorCode_Op_not_Supported = 8
      Device_ErrorCode_Out_of_Resoruces = 9
      Device_ErrorCode_Dev_Locked_by_Another = 11
      Device_ErrorCode_No_Lock_by_this_Link = 12
      Device_ErrorCode_IO_Timeout = 15
      Device_ErrorCode_IO_Error = 17
      Device_ErrorCode_Ivalid_Addr = 21
      Device_ErrorCode_Abort = 23
      Device_ErrorCode_Already_Established = 29

  cdef cppclass c_Device_Error "Device_Error":
      Device_ErrorCode error

  cdef extern bool_t xdr_Device_ErrorCode(c_XDR *, Device_ErrorCode*) nogil
  cdef extern bool_t xdr_Device_Error(c_XDR *, c_Device_Error*) nogil

  cdef cppclass c_Create_LinkParms "Create_LinkParms": 
       int clientId
       bool_t lockDevice
       u_int lock_timeout
       char *device

  cdef bool_t xdr_Create_LinkParms(c_XDR *, c_Create_LinkParms *) nogil

  cdef cppclass c_Create_LinkResp "Create_LinkResp":
      Device_ErrorCode              error
      Device_Link                   lid
      u_short                       abortPort
      u_long                        maxRecvSize

  bool_t xdr_Create_LinkResp(c_XDR *, c_Create_LinkResp *) nogil

  ctypedef struct c_Device_WriteParms_data:
      u_int data_len
      char *data_val

  cdef cppclass c_Device_WriteParms "Device_WriteParms":
      Device_Link lid
      u_long io_timeout
      u_long lock_timeout
      Device_Flags flags
      c_Device_WriteParms_data data

  bool_t xdr_Device_WriteParms(c_XDR *, c_Device_WriteParms*) nogil

  cdef cppclass c_Device_WriteResp "Device_WriteResp":
     Device_ErrorCode error
     u_long size

  bool_t xdr_Device_WriteResp(c_XDR *, c_Device_WriteResp*) nogil

  cdef cppclass c_Device_ReadParms "Device_ReadParms":
           Device_Link lid
           u_long requestSize
           u_long io_timeout
           u_long lock_timeout
           Device_Flags flags
           char termChar

  bool_t xdr_Device_ReadParms(c_XDR *, c_Device_ReadParms*) nogil

  cdef struct c_Device_ReadResp_data:
         u_int data_len
         char *data_val
      
  cdef cppclass c_Device_ReadResp "Device_ReadResp":
       Device_ErrorCode error
       long reason
       c_Device_ReadResp_data  data
       
#  int Device_ReadResp_REQCNT=1
#  int Device_ReadResp_CHR=2
#  int Device_ReadResp_END=4

#  cdef enum:
#      DEVICE_READRESP_REQCNT=1
#      DEVICE_READRESP_CHR=2
#      DEVICE_READRESP_END=4

  bool_t xdr_Device_ReadResp(c_XDR *, c_Device_ReadResp*) nogil

  cdef cppclass c_Device_ReadStbResp "Device_ReadStbResp":
     Device_ErrorCode error
     u_char stb

  cdef bool_t xdr_Device_ReadStbResp(c_XDR *, c_Device_ReadStbResp*) nogil

  cdef cppclass c_Device_GenericParms "Device_GenericParms":
     Device_Link lid
     Device_Flags flags
     u_long lock_timeout
     u_long io_timeout

  cdef extern bool_t xdr_Device_GenericParms(c_XDR *, c_Device_GenericParms *) nogil

  cdef cppclass c_Device_RemoteFunc "Device_RemoteFunc":
       u_long hostAddr
       u_short hostPort
       u_long progNum
       u_long progVers
       c_Device_AddrFamily progFamily

  cdef bool_t xdr_Device_RemoteFunc(c_XDR *, c_Device_RemoteFunc * ) nogil

  cdef cppclass c_Device_EnableSrqParms "Device_EnableSrqParms":
     Device_Link lid
     bool_t enable
     handle_type handle

  bool_t xdr_Device_EnableSrqParms(c_XDR *, c_Device_EnableSrqParms * ) nogil

  cdef cppclass c_Device_LockParms "Device_LockParms":
     Device_Link lid
     Device_Flags flags
     u_long lock_timeout

  bool_t xdr_Device_LockParms(c_XDR *, c_Device_LockParms * ) nogil

  ctypedef struct data_in_type:
      u_int data_in_len
      char *data_in_val

  cdef cppclass c_Device_DocmdParms "Device_DocmdParms":
    Device_Link lid
    Device_Flags flags
    u_long io_timeout
    u_long lock_timeout
    int cmd
    bool_t network_order
    long datasize
    data_in_type  data_in

  bool_t xdr_Device_DocmdParms(c_XDR *, c_Device_DocmdParms * ) nogil

  cdef struct data_out_type:
      u_int data_out_len
      char *data_out_val

  cdef cppclass c_Device_DocmdResp "Device_DocmdResp":
    Device_ErrorCode error
    data_out_type data_out
  
  bool_t xdr_Device_DocmdResp(c_XDR *, c_Device_DocmdResp * ) nogil

  u_long device_abort =(<u_long> 1)
  unsigned long _device_abort=device_abort

  c_Device_Error * device_abort_1(Device_Link *, c_CLIENT * ) nogil

  u_long  create_link = (<u_long> 10)
  unsigned long _create_link=create_link

  c_Create_LinkResp * create_link_1(c_Create_LinkParms *, c_CLIENT * OClient) nogil

  u_long device_write =  (<u_long> 11)
  unsigned long _device_write=device_write

  c_Device_WriteResp * device_write_1(c_Device_WriteParms *, c_CLIENT * ) nogil

  u_long  device_read = <u_long>12
  unsigned long _device_read = device_read
  c_Device_ReadResp * device_read_1(c_Device_ReadParms *, c_CLIENT * ) nogil

  u_long device_readstb = (<u_long>13)
  unsigned long _device_readstb = device_readstb

  c_Device_ReadStbResp * device_readstb_1(c_Device_GenericParms *, c_CLIENT * ) nogil

  u_long device_trigger = (<u_long>14)
  unsigned long _device_trigger = device_trigger

  c_Device_Error * device_trigger_1(c_Device_GenericParms *, c_CLIENT * ) nogil

  u_long  device_clear =(<u_long> 15)
  unsigned long _device_clear = device_clear

  c_Device_Error * device_clear_1(c_Device_GenericParms *, c_CLIENT * ) nogil

  u_long  device_remote =(<u_long> 16)
  unsigned long _device_remote = device_remote

  c_Device_Error * device_remote_1(c_Device_GenericParms *, c_CLIENT * ) nogil

  u_long  device_local =(<u_long> 17)
  unsigned long _device_local = device_local

  c_Device_Error * device_local_1(c_Device_GenericParms *, c_CLIENT * ) nogil

  u_long  device_lock =(<u_long> 18)
  unsigned long _device_lock = device_lock

  c_Device_Error * device_lock_1(c_Device_LockParms *, c_CLIENT * ) nogil

  u_long  device_unlock =(<u_long> 19)
  unsigned long _device_unlock = device_unlock

  c_Device_Error * device_unlock_1(Device_Link *, c_CLIENT * ) nogil

  u_long  device_enable_srq =(<u_long> 20)
  unsigned long _device_enable_srq = device_enable_srq

  c_Device_Error * device_enable_srq_1(c_Device_EnableSrqParms *, c_CLIENT * ) nogil

  u_long  device_docmd =(<u_long> 22)
  unsigned long _device_docmd = device_docmd

  c_Device_DocmdResp * device_docmd_1(c_Device_DocmdParms *, c_CLIENT * ) nogil

  u_long  destroy_link =(<u_long> 23)
  unsigned long _destroy_link = destroy_link

  c_Device_Error * destroy_link_1(Device_Link *, c_CLIENT * ) nogil

  u_long  create_intr_chan =(<u_long> 25)
  unsigned long _create_intr_chan = create_intr_chan

  c_Device_Error * create_intr_chan_1(c_Device_RemoteFunc *, c_CLIENT * ) nogil

  u_long  destroy_intr_chan =(<u_long> 26)
  unsigned long _destroy_intr_chan = destroy_intr_chan

  c_Device_Error * destroy_intr_chan_1(void *, c_CLIENT * ) nogil


#
  ctypedef int Device_link 

  cdef enum:
    DEVICE_CORE
    DEVICE_CORE_VERSION
    DEVICE_ASYNC
    DEVICE_ASYNC_VERSION

cdef extern from "VXI11_intr.h":
  #//*C.2. Interrupt Protocol*/
  cdef enum:
    DEVICE_INTR
    DEVICE_INTR_VERSION

  # ctypedef struct handle_type:
  #    u_long handle_len
  #    char *handle_val

  cdef cppclass c_Device_SrqParms "Device_SrqParms":
      handle_type  handle

  bool_t xdr_Device_SrqParms(c_XDR *, c_Device_SrqParms *) nogil

  ctypedef void *svc_req_ptr

  void * device_intr_srq_1(c_Device_SrqParms *, c_CLIENT * ) nogil

# 
IF UNAME_SYSNAME == "Darwin":
    ctypedef void *c_xdr_free_argtype
ELIF UNAME_SYSNAME == "Linux":
    ctypedef char *c_xdr_free_argtype

cdef extern void device_intr_1(c_svc_req *rqstp, c_SVCXPRT *transp) nogil

cdef extern c_CLIENT *createAbtChannel( char *clnt,
                                        u_short abortPort, long *sockp,
                                        u_long prog, u_long version, 
                                        u_long sendsz, u_long recvsz) nogil
#
# for pmap_getport
cdef extern from "rpc/pmap_prot.h":
  ctypedef struct c_pmap "pmap":
     unsigned int pm_prog
     unsigned int pm_vers
     unsigned int pm_prot
     unsigned int pm_port

  ctypedef struct c_pmaplist "pmaplist" :
    c_pmap pml_map
    c_pmaplist  *pml_next

cdef extern from "cPMAP.h":
    cdef int cPMAP_getport "PMAP_getport" (char *host,
                                           unsigned int program,
                                           unsigned int version  ,
                                           unsigned int protocol ) nogil
    cdef c_pmaplist  *cPMAP_getmaps "PMAP_getmaps" (char *host) nogil

cdef extern from "rpc/pmap_clnt.h":
    cdef bool_t	cPMAP_unset "pmap_unset" (unsigned int serv, unsigned int vers) nogil
#
#

cdef class Device_GenericParms:
    cdef c_Device_GenericParms *thisptr #

cdef class Device_RemoteFunc:
    cdef c_Device_RemoteFunc *thisptr # "this" is a reserved keyword in C++

cdef class Create_LinkParms:
    cdef c_Create_LinkParms *thisptr # "this" is a reserved keyword in C++
    
