//
// -*- coding: utf-8 -*-

#include "cPMAP.h"

int PMAP_getport(char *host,unsigned int program, unsigned int version, unsigned int protocol){
	struct sockaddr_in sock_in;
	
	sock_in.sin_family=AF_INET;
	sock_in.sin_port=htons(PMAPPORT);
	sock_in.sin_addr.s_addr=inet_addr(host);
	return pmap_getport(&sock_in, program, version, protocol);
	
}

struct pmaplist *PMAP_getmaps(char *host){
	struct sockaddr_in sock_in;
	sock_in.sin_family=AF_INET;
	sock_in.sin_port=htons(PMAPPORT);
	sock_in.sin_addr.s_addr=inet_addr(host);
	return pmap_getmaps(&sock_in);
}
