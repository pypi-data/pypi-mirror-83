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
            
IF UNAME_SYSNAME == "Linux":
    cdef extern from "netpacket/packet.h":
        ctypedef struct c_sockaddr_ll "sockaddr_ll":
            u_short sll_family;
            u_short  sll_protocol;
            int sll_ifindex;
            u_short sll_hatype;
            u_char sll_pkttype;
            u_char sll_halen;
            u_char sll_addr[8];

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
        AF_UNSPEC                # /* unspecified */
        AF_UNIX                # /* local to host (pipes) */
        AF_LOCAL = AF_UNIX         # /* backward compatibility */
        AF_INET                 # sockaddr_in in netinet/in.h
        # Darwin only
        AF_IMPLINK              # /* arpanet imp addresses */
        AF_PUP                # /* pup protocols: e.g. BSP */
        AF_CHAOS                # /* mit CHAOS protocols */
        AF_NS                # /* XEROX NS protocols */
        AF_ISO                # /* ISO protocols */
        AF_OSI = AF_ISO
        AF_ECMA                # /* European computer manufacturers */
        AF_DATAKIT                # /* datakit protocols */
        AF_CCITT               # /* CCITT protocols, X.25 etc */
        AF_SNA               # /* IBM SNA */
        AF_DECnet               # /* DECnet */
        AF_DLI               # /* DEC Direct data link interface */
        AF_LAT               # /* LAT */
        AF_HYLINK               # /* NSC Hyperchannel */
        AF_APPLETALK               # /* Apple Talk */
        AF_ROUTE               # /* Internal Routing Protocol */
        AF_LINK   # /* Link layer interface */ sockaddr_dl in net/if_dl.h
        pseudo_AF_XTP         # /* eXpress Transfer Protocol (no AF) */
        AF_COIP               # /* connection-oriented IP, aka ST II */
        AF_CNT               # /* Computer Network Technology */
        pseudo_AF_RTIP               # /* Help Identify RTIP packets */
        AF_IPX               # /* Novell Internet Protocol */
        AF_SIP               # /* Simple Internet Protocol */
        pseudo_AF_PIP               # /* Help Identify PIP packets */
        AF_NDRV   # /* Network Driver 'raw' access */ sockaddr_ndrv in neet/ndrv.h
        AF_ISDN          # /* Integrated Services Digital Network */
        AF_E164 = AF_ISDN    # /* CCITT E.164 recommendation */
        pseudo_AF_KEY    # /* Internal key-management function */
        AF_INET6         # /* IPv6 */ sockaddr_in6 in netinet6/in6.h
        AF_NATM           # /* native ATM access */
        AF_SYSTEM            # /* Kernel event messages */
        AF_NETBIOS               # /* NetBIOS */
        AF_PPP               # /* PPP communication protocol */
        pseudo_AF_HDRCMPLT   # /* Used by BPF to not rewrite headers
        #   *  in interface output routine */
        AF_RESERVED_36               # /* Reserved for internal usage */
        AF_IEEE80211                 # /* IEEE 802.11 protocol */
        AF_UTUN 
        AF_MAX 
        #LINUX
        PF_PACKET	# /* Packet family.  */ Linux only
        AF_PACKET = PF_PACKET	# /* Packet family.  */ Linux only
#
