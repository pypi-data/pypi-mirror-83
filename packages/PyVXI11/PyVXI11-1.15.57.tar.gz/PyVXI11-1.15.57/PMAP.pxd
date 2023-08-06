#!cython
# definition 
# distutils: language=c++

cdef extern from "arpa/inet.h":
  pass

cdef extern from "rpc/rpc.h":
  pass

cdef extern from "rpc/pmap_prot.h":
  ctypedef struct c_pmap "pmap":
     unsigned int pm_prog
     unsigned int pm_vers
     unsigned int pm_prot
     unsigned int pm_port

  ctypedef c_pmaplist *c_pmaplist_ptr

  ctypedef struct c_pmaplist "pmaplist" :
    c_pmap pml_map
    c_pmaplist_ptr  pml_next
  
cdef extern from "sys/types.h":
  ctypedef unsigned long  u_long
  ctypedef unsigned int   u_int
  ctypedef unsigned short u_short
  ctypedef unsigned char  u_char
  ctypedef int            bool_t

cdef extern from "cPMAP.h":
    cdef int cPMAP_getport "PMAP_getport" (
        char *host,
        unsigned int program,
        unsigned int version,
        unsigned int protocol)
    
#cdef c_pmaplist_ptr cPMAP_getmaps "PMAP_getmaps" (char *host)
