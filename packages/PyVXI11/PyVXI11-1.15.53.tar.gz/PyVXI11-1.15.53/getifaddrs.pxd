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

cdef extern from "sys/un.h":
    ctypedef  __uint8_t  sa_family_t;
    
    ctypedef struct c_sockaddr "sockaddr":
        # __uint8_t     sa_len;         #/* total length */
        sa_family_t   sa_family;      #* [XSI] address family */
        char          sa_data[14];    #/* [XSI] addr value (actually larger) */
        
    ctypedef struct c_sockaddr_un "sockaddr_un":
        # __uint8_t     sun_len;         #/* total length */
        sa_family_t   sun_family;      #* [XSI] address family */
        char          sun_path[104];    #/* [XSI] addr value (actually larger

cdef extern from "arpa/inet.h":
  cdef char *addr2ascii(int af, const void *addrp, int len, char *buf)

  cdef int  ascii2addr(int af, const char *ascii, void *result)

cdef extern from "netinet/in.h":
    ctypedef struct c_in_addr "in_addr":
       __uint32_t     s_addr
        
    ctypedef __uint16_t c_in_port_t "in_port_t";

    ctypedef struct c_sockaddr_in "sockaddr_in":
        # __uint8_t     sin_len;
        sa_family_t   sin_family;
        c_in_port_t   sin_port;
        c_in_addr     sin_addr;
        char          sin_zero[8];

cdef extern from "ifaddrs.h":
    ctypedef union __u6_addr_t : # /* 128-bit IP6 address */
        __uint8_t     __u6_addr8[16]
        __uint16_t    __u6_addr16[8]
        __uint32_t    __u6_addr32[4]

    ctypedef struct c_in6_addr "in6_addr":
        __u6_addr_t   __u6_addr; # /* 128-bit IP6 address */

    ctypedef struct c_sockaddr_in6 "sockaddr_in6":        
        # __uint8_t     sin6_len; # /* length of this struct(sa_family_t) */
        sa_family_t   sin6_family; # /* AF_INET6 (sa_family_t) */
        c_in_port_t   sin6_port; # /* Transport layer port # (in_port_t) */
        __uint32_t    sin6_flowinfo; # /* IP6 flow information */
        #c_in6_addr    sin6_addr; # /* IP6 address */
        __uint16_t     sin6_addr[8]
        __uint32_t    sin6_scope_id; # /* scope zone index */

IF UNAME_SYSNAME == "Darwin":
    cdef extern from "net/if_dl.h":
        ctypedef struct c_sockaddr_dl "sockaddr_dl":
            # u_char  sdl_len;     #/* Total length of sockaddr */
            u_char  sdl_family;  #/* AF_LINK */
            u_short sdl_index;   #/* if != 0, system given index for interface */
            u_char  sdl_type;    #/* interface type */
            u_char  sdl_nlen;   #/* interface name length, no trailing 0 reqd. */
            u_char  sdl_alen;    #/* link level address length */
            u_char  sdl_slen;    #/* link layer selector length */
            char    sdl_data[12];#/* minimum work area, can be larger;
	    # *  contains both if name and ll address */
            #ifndef __APPLE__
            #/* For TokenRing */
            u_short sdl_rcf;     #/* source routing control */
            u_short sdl_route[16];#/* source routing information */
            #endif


# for getifaddrs
cdef extern from "ifaddrs.h":
    ctypedef struct c_ifaddrs "ifaddrs":
        c_ifaddrs       *ifa_next;
        char		*ifa_name;
        u_int	        ifa_flags;
        c_sockaddr	*ifa_addr;
        c_sockaddr	*ifa_netmask;
        c_sockaddr	*ifa_dstaddr;
        void		*ifa_data;

    cdef  int c_getifaddrs  "getifaddrs"  (c_ifaddrs **ifap);
    cdef  void c_freeifaddrs  "freeifaddrs" (c_ifaddrs *ifp);

    cdef enum c_AddressFamily:
        AF_UNSPEC = 0               # /* unspecified */
        AF_UNIX = 1               # /* local to host (pipes) */
        AF_LOCAL = AF_UNIX         # /* backward compatibility */
        AF_INET = 2                # sockaddr_in in netinet/in.h
        AF_IMPLINK = 3             # /* arpanet imp addresses */
        AF_PUP = 4               # /* pup protocols: e.g. BSP */
        AF_CHAOS = 5               # /* mit CHAOS protocols */
        AF_NS = 6               # /* XEROX NS protocols */
        AF_ISO = 7               # /* ISO protocols */
        AF_OSI = AF_ISO
        AF_ECMA = 8               # /* European computer manufacturers */
        AF_DATAKIT = 9               # /* datakit protocols */
        AF_CCITT = 10              # /* CCITT protocols, X.25 etc */
        AF_SNA = 11              # /* IBM SNA */
        AF_DECnet = 12              # /* DECnet */
        AF_DLI = 13              # /* DEC Direct data link interface */
        AF_LAT = 14              # /* LAT */
        AF_HYLINK = 15              # /* NSC Hyperchannel */
        AF_APPLETALK = 16              # /* Apple Talk */
        AF_ROUTE = 17              # /* Internal Routing Protocol */
        AF_LINK = 18 # /* Link layer interface */ sockaddr_dl in net/if_dl.h
        pseudo_AF_XTP = 19        # /* eXpress Transfer Protocol (no AF) */
        AF_COIP = 20              # /* connection-oriented IP, aka ST II */
        AF_CNT = 21              # /* Computer Network Technology */
        pseudo_AF_RTIP = 22              # /* Help Identify RTIP packets */
        AF_IPX = 23              # /* Novell Internet Protocol */
        AF_SIP = 24              # /* Simple Internet Protocol */
        pseudo_AF_PIP = 25              # /* Help Identify PIP packets */
        AF_NDRV = 27  # /* Network Driver 'raw' access */ sockaddr_ndrv in neet/ndrv.h
        AF_ISDN = 28         # /* Integrated Services Digital Network */
        AF_E164 = AF_ISDN    # /* CCITT E.164 recommendation */
        pseudo_AF_KEY = 29   # /* Internal key-management function */
        AF_INET6      = 30   # /* IPv6 */ sockaddr_in6 in netinet6/in6.h
        AF_NATM = 31          # /* native ATM access */
        AF_SYSTEM = 32           # /* Kernel event messages */
        AF_NETBIOS = 33              # /* NetBIOS */
        AF_PPP = 34              # /* PPP communication protocol */
        pseudo_AF_HDRCMPLT = 35  # /* Used by BPF to not rewrite headers
        #   *  in interface output routine */
        AF_RESERVED_36 = 36              # /* Reserved for internal usage */
        AF_IEEE80211   = 37              # /* IEEE 802.11 protocol */
        AF_UTUN = 38
        AF_MAX = 40
#
