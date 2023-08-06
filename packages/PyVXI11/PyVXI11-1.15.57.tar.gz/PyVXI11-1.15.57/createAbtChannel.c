//
// 
//
#include <stdio.h> //for perror()
#include <string.h>
#include <sys/types.h>
#include <rpc/rpc.h>
#include "VXI11.h"
#include <netinet/in.h>
#include <arpa/inet.h>
#include <rpc/svc.h>
#include <rpc/clnt.h>
#include <rpc/xdr.h>
#include <netdb.h>

CLIENT *createAbtChannel(char *clnt, u_short abortPort,
			 int *sockp, /* return value */
			 u_int prog, u_int version, 
			 u_int sendsz, u_int recvsz)
{
        /* struct sockaddr_in addr; */
        /* struct hostent *he; */
	
	int ret;
	struct addrinfo *aip, hints;
        CLIENT *retv;
        int     sock = RPC_ANYSOCK;

        /* bzero( &addr, sizeof(addr)); */
        /* addr.sin_family=AF_INET; */
        /* addr.sin_port = htons(abortPort); */
	
	bzero( &hints, sizeof(hints));
	hints.ai_family=PF_INET;
	// ((struct sockaddr_in *) hints.ai_addr)->sin_port=htons(abortPort);
	
	ret=getaddrinfo(clnt, NULL, NULL, &aip);
	if (ret != 0) {
		perror(__FILE__ "failed to get address info.");
		*sockp=-1;
		return  NULL;
	}
	else if (aip->ai_addrlen < sizeof(struct sockaddr_in)){
		*sockp=-1;
		return NULL;
	}
	((struct sockaddr_in *)aip->ai_addr)->sin_port=htons(abortPort);
	
        /* follow http://www-cms.phys.s.u-tokyo.ac.jp/~naoki/CIPINTRO/NETWORK/struct.html to setup addr*/
		
	/* he=gethostbyname(clnt);/\* may(should?) be replaced with getaddrinfo() *\/ */
	
        /* inet_aton(he->h_addr_list[0], &addr.sin_addr); */

        /* retv=clnttcp_create(&addr, */
        /*                     prog, version, */
        /*                     &sock, */
        /*                     sendsz, recvsz); */

	
        retv=clnttcp_create((struct sockaddr_in *) aip->ai_addr,
                            prog, version,
                            &sock,
                            sendsz, recvsz);
        if (retv == NULL){
		clnt_pcreateerror(__FILE__ "failed to create RPC client.");
                *sockp=-1;
        }
        else{
                *sockp=sock;
	}
	freeaddrinfo(aip);
        return retv;
}
