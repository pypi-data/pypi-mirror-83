#follow the description in
#https://cython.readthedocs.io/en/latest/src/userguide/extension_types.html#instantiation-from-existing-c-c-pointers
"""
This getifaddrs module just provides a getifaddrs function. 
It is a plain wrppere function over the getifaddrs function on Linux/Darwin(MacOS).
The function takes no argument and returns a list of interface address objects.
This module is written in Cython and works with python2/python3.

(c) Noboru Yamamoto, KEK, JAPAN, 2020
"""

cimport getifaddrs
from libc.stdlib cimport malloc, free, calloc
#
import cython
import socket, struct, os, signal
import logging
#

cdef class ifaddrs:
    cdef c_ifaddrs *thisptr
    cdef public u_long _ptr
    cdef readonly bint ptr_owner
    cdef object __weakref__  # make this class weak-referenceable
    #
    def __cinit__(self):
        self.ptr_owner = False
    #
    def __dealloc__(self):
        # De-allocate if not null and flag is set
        if (    (self.ptr_owner is True)
            and (self.thisptr is not NULL)
        ):
            free(self.thisptr)
            self.thisptr = NULL
    #
    def __init__(self):
        pass
    #
    # helper functions to wrapp c_ifaddr struct with "class ifaddrs".
    @staticmethod
    cdef ifaddrs from_ptr(c_ifaddrs *_ptr, bint owner=False):
        # Call to __new__ bypasses __init__ constructor
        cdef ifaddrs wrapper = ifaddrs.__new__(ifaddrs)
        # you cannot pass _ptr to the __init__ anyway.
        wrapper.thisptr = _ptr
        wrapper._ptr= <u_long> _ptr
        wrapper.ptr_owner = owner
        return wrapper
    #
    @staticmethod
    cdef ifaddrs new_struct():
        cdef c_ifaddrs *_ptr = <c_ifaddrs *> calloc(1,sizeof(c_ifaddrs))
        if _ptr is NULL:
            raise MemoryError
        return ifaddrs.from_ptr(_ptr, owner=True)
    #
    @property
    def ifa_name(self):
        return self.thisptr.ifa_name if self.thisptr is not NULL else None
    #
    @property
    def ifa_flags(self):
        return self.thisptr.ifa_flags if self.thisptr is not NULL else None
    #
    @property
    def ifa_addr(self):
        if self.thisptr is  NULL:return  None
        if self.thisptr.ifa_addr is NULL : return None
        return sockaddr.from_ptr(self.thisptr.ifa_addr)
    #
    @property
    def ifa_netmask(self):
        if self.thisptr is  NULL:return  None
        if self.thisptr.ifa_netmask is NULL : return None
        return sockaddr.from_ptr(self.thisptr.ifa_netmask) 
    #
    @property
    def ifa_dstaddr(self):
        if self.thisptr is  NULL:return  None
        if self.thisptr.ifa_dstaddr is NULL : return None
        return sockaddr.from_ptr(self.thisptr.ifa_dstaddr) 
    #
#
cdef class sockaddr:
    """
        __uint8_t       sa_len;         #/* total length */
        sa_family_t     sa_family;      #* [XSI] address family */
        char            sa_data[14];    #/* [XSI] addr value (actually larger) */
    """
    cdef c_sockaddr *thisptr
    cdef bint ptr_owner
    cdef object __weakref__  # make this class weak-referenceable
    #
    def __cinit__(self):
        self.ptr_owner = False
    #
    def __dealloc__(self):
        # De-allocate if not null and flag is set
        if (    (self.ptr_owner is True)
            and (self.thisptr is not NULL )
        ):
            free(self.thisptr)
            self.thisptr = NULL
    #
    def __init__(self):
        pass
    #
    # helper functions to wrapp c_ifaddr struct with "class ifaddrs".
    @staticmethod
    cdef sockaddr from_ptr(c_sockaddr *_ptr, bint owner=False):
        if _ptr is NULL: return None
        # Call to __new__ bypasses __init__ constructor
        cdef sockaddr wrapper
        if (_ptr.sa_family == c_AddressFamily.AF_INET):
            wrapper = sockaddr_in.__new__(sockaddr_in)
        elif (_ptr.sa_family == c_AddressFamily.AF_UNIX):
            wrapper = sockaddr_un.__new__(sockaddr_un)
        elif (_ptr.sa_family == c_AddressFamily.AF_INET6):
            wrapper = sockaddr_in6.__new__(sockaddr_in6)
        else:
            IF UNAME_SYSNAME== "Darwin":
                if (_ptr.sa_family == c_AddressFamily.AF_LINK):
                    wrapper = sockaddr_dl.__new__(sockaddr_dl)
                else:
                    wrapper = sockaddr.__new__(sockaddr)
            ELIF UNAME_SYSNAME == "Linux":
                if (_ptr.sa_family == c_AddressFamily.AF_PACKET):
                    wrapper = sockaddr_ll.__new__(sockaddr_ll)
                else:
                    wrapper = sockaddr.__new__(sockaddr)
            ELSE:
                wrapper = sockaddr.__new__(sockaddr)
        wrapper.thisptr = _ptr
        wrapper.ptr_owner = owner
        return wrapper
    #
    @staticmethod
    cdef sockaddr new_struct():
        cdef c_sockaddr *_ptr = <c_sockaddr *> calloc(1, sizeof(c_sockaddr))
        if _ptr is NULL:
            raise MemoryError
        return sockaddr.from_ptr(_ptr, owner=True)
    #
    # @property
    # def sa_len(self):
    #     return self.thisptr.sa_len if self.thisptr is not NULL else None
    # #
    @property
    def sa_family(self):
        if self.thisptr is NULL: return None
        return self.thisptr.sa_family
    
    @property
    def sa_data(self):
        return self.thisptr.sa_data if self.thisptr is not NULL else None
#
cdef class sockaddr_in(sockaddr):

    # @property
    # def sin_len(self):
    #     cdef c_sockaddr_in *thisptr=<c_sockaddr_in *> self.thisptr
    #     return thisptr.sin_len if thisptr is not NULL else None

    @property
    def sin_family(self):
        cdef c_sockaddr_in *thisptr=<c_sockaddr_in *> self.thisptr
        return thisptr.sin_family if thisptr is not NULL else None

    @property
    def sin_port(self):
        cdef c_sockaddr_in *thisptr=<c_sockaddr_in *> self.thisptr
        return thisptr.sin_port if thisptr is not NULL else None

    @property
    def sin_addr(self):
        cdef c_sockaddr_in *thisptr=<c_sockaddr_in *> self.thisptr
        return socket.htonl(thisptr.sin_addr.s_addr) if thisptr is not NULL else None


cdef class sockaddr_un(sockaddr):
    # @property
    # def sun_len(self):
    #     cdef c_sockaddr_un *thisptr=<c_sockaddr_un *> self.thisptr
    #     return thisptr.sun_len if thisptr is not NULL else None

    @property
    def sun_family(self):
        cdef c_sockaddr_un *thisptr=<c_sockaddr_un *> self.thisptr
        return thisptr.sun_family if thisptr is not NULL else None

    @property
    def sun_path(self):
        cdef c_sockaddr_un *thisptr=<c_sockaddr_un *> self.thisptr
        return thisptr.sun_path if thisptr is not NULL else None

cdef class sockaddr_in6(sockaddr):
    # @property
    # def sin6_len(self):
    #     cdef c_sockaddr_in6 *thisptr=<c_sockaddr_in6 *> self.thisptr
    #     return thisptr.sin6_len if thisptr is not NULL else None

    @property
    def sin6_family(self):
        cdef c_sockaddr_in6 *thisptr=<c_sockaddr_in6 *> self.thisptr
        return thisptr.sin6_family if thisptr is not NULL else None

    @property
    def sin6_port(self):
        cdef c_sockaddr_in6 *thisptr=<c_sockaddr_in6 *> self.thisptr
        return thisptr.sin6_port if thisptr is not NULL else None

    @property
    def sin6_flowinfo(self):
        cdef c_sockaddr_in6 *thisptr=<c_sockaddr_in6 *> self.thisptr
        return thisptr.sin6_flowinfo if thisptr is not NULL else None
    @property
    def sin6_scope_id(self):
        cdef c_sockaddr_in6 *thisptr=<c_sockaddr_in6 *> self.thisptr
        return thisptr.sin6_scope_id if thisptr is not NULL else None

    @property
    def sin6_addr(self):
        cdef c_sockaddr_in6 *thisptr=<c_sockaddr_in6 *> self.thisptr
        if not thisptr:
            return None
        cdef __uint16_t *paddr=<__uint16_t *> &thisptr.sin6_addr
        addr=[]
        for i in range(8):
            addr.append(socket.ntohs(paddr[i]))
        return  addr

IF UNAME_SYSNAME == "Darwin":
    cdef class sockaddr_dl(sockaddr):
        # @property
        # def sdl_len(self):
        #     cdef c_sockaddr_dl *thisptr=<c_sockaddr_dl *> self.thisptr
        #     return thisptr.sdl_len if thisptr is not NULL else None

        @property
        def sdl_family(self):
            cdef c_sockaddr_dl *thisptr=<c_sockaddr_dl *> self.thisptr
            return thisptr.sdl_family if thisptr is not NULL else None

        @property
        def sdl_index(self):
            cdef c_sockaddr_dl *thisptr=<c_sockaddr_dl *> self.thisptr
            return thisptr.sdl_index if thisptr is not NULL else None
        
        @property
        def sdl_type(self):
            cdef c_sockaddr_dl *thisptr=<c_sockaddr_dl *> self.thisptr
            return thisptr.sdl_type if thisptr is not NULL else None

        @property
        def sdl_nlen(self):
            cdef c_sockaddr_dl *thisptr=<c_sockaddr_dl *> self.thisptr
            return thisptr.sdl_nlen if thisptr is not NULL else None
        
        @property
        def sdl_alen(self):
            cdef c_sockaddr_dl *thisptr=<c_sockaddr_dl *> self.thisptr
            return thisptr.sdl_alen if thisptr is not NULL else None
        
        @property
        def sdl_slen(self):
            cdef c_sockaddr_dl *thisptr=<c_sockaddr_dl *> self.thisptr
            return thisptr.sdl_slen if thisptr is not NULL else None
        
        @property
        def sdl_data(self):
            cdef c_sockaddr_dl *thisptr=<c_sockaddr_dl *> self.thisptr
            if thisptr is NULL:
                return None
            data=[]
            for i in range(thisptr.sdl_nlen + thisptr.sdl_alen + thisptr.sdl_slen):
                data.append(thisptr.sdl_data[i])
            return data 

IF UNAME_SYSNAME == "Linux":
    cdef class sockaddr_ll(sockaddr):
        @property
        def sll_family(self):
            cdef c_sockaddr_ll *thisptr=<c_sockaddr_ll *> self.thisptr
            return thisptr.sll_family if thisptr is not NULL else None

        @property
        def sll_protocol(self):
            cdef c_sockaddr_ll *thisptr=<c_sockaddr_ll *> self.thisptr
            return thisptr.sll_protocol if thisptr is not NULL else None
        
        @property
        def sll_ifindex(self):
            cdef c_sockaddr_ll *thisptr=<c_sockaddr_ll *> self.thisptr
            return thisptr.sll_ifindex if thisptr is not NULL else None
        
        @property
        def sll_hatype(self):
            cdef c_sockaddr_ll *thisptr=<c_sockaddr_ll *> self.thisptr
            return thisptr.sll_hatype if thisptr is not NULL else None

        @property
        def sll_pkttype(self):
            cdef c_sockaddr_ll *thisptr=<c_sockaddr_ll *> self.thisptr
            return thisptr.sll_pkttype if thisptr is not NULL else None

        @property
        def sll_halen(self):
            cdef c_sockaddr_ll *thisptr=<c_sockaddr_ll *> self.thisptr
            return thisptr.sll_halen if thisptr is not NULL else None
        
        @property
        def sll_addr(self):
            cdef c_sockaddr_ll *thisptr=<c_sockaddr_ll *> self.thisptr
            if thisptr is NULL:
                return None
            data=[thisptr.sll_addr[i] 
                  for i in range(
                          thisptr.sll_halen if thisptr.sll_halen > 8 else 8
                  )]
            return data 
#    
def getifaddrs(): # you shoud use socket.if_nameindex() instead.
    cdef c_ifaddrs *ifap;
    cdef c_ifaddrs **ifapp=& ifap;
    
    py_ifaddrs=[]
    
    c_getifaddrs(<c_ifaddrs **> & ifap);

    while(ifap != NULL):
        n=ifaddrs.from_ptr(ifap,False)
        py_ifaddrs.append(n)
        ifap=ifap.ifa_next
        
    return  py_ifaddrs
