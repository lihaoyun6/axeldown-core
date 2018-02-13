#include <stdio.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <stdlib.h>
#include <netdb.h>
#include <string.h>

int http_post(char *host, int port, char *page, char *data, char *response);
char *build_post_query(char *host, char *page, char *data);
