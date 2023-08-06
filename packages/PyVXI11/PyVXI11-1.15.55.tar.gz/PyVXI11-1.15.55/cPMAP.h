//! cpp
// -*- coding:utf-8 -*-

#include <arpa/inet.h>
#include <rpc/rpc.h>
#include <rpc/pmap_prot.h>
#include <rpc/pmap_clnt.h>

int PMAP_getport(char *host,
		 unsigned int program,
		 unsigned int version = 1,
		 unsigned int protocol = IPPROTO_TCP);

struct pmaplist *PMAP_getmaps(char *host);
