#include "httppost.h" 
#define HOST "coding.debuntu.org"
#define PAGE "/"
#define PORT 80
#define USERAGENT "HTMLGET 1.0"

#define BUFSIZE 1200
char *get_ip(char *host)
{
  struct hostent *hent;
  int iplen = 15; //XXX.XXX.XXX.XXX
  char *ip = (char *)malloc(iplen+1);
  memset(ip, 0, iplen+1);
  if((hent = gethostbyname(host)) == NULL) {
      //Can't get IP
      return NULL;
    }
  if(inet_ntop(AF_INET, (void *)hent->h_addr_list[0], ip, iplen) == NULL) {
      //Can't resolve host
      return NULL;
    }
  //fprintf(stdout, "%s", ip);
  return ip;
}

int http_post(char *host, int port, char *page, char *data, char *response)
{
  struct sockaddr_in *remote;
  int sock;
  int tmpres;
  char *ip;
  char *post;
  char buf[BUFSIZE+1];
    
  if((sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)) < 0){
    return NULL;
  }
  ip = get_ip(host);//"123.125.114.14";
  remote = (struct sockaddr_in *)malloc(sizeof(struct sockaddr_in *));
  remote->sin_family = AF_INET;
  tmpres = inet_pton(AF_INET, ip, (void *)(&(remote->sin_addr.s_addr)));
  if( tmpres < 0) {
    //Can't set remote->sin_addr.s_addr
    return NULL;
  }else if(tmpres == 0) {
    return NULL;
  }
  remote->sin_port = htons(port);
    
  if(connect(sock, (struct sockaddr *)remote, sizeof(struct sockaddr)) < 0){
    //Could not connect
    return NULL;
  }
  post = build_post_query(host, page, data);

  //Send the query to the server
  int sent = 0;
  while(sent < strlen(post)) {
    tmpres = send(sock, post+sent, strlen(post)-sent, 0);
    if(tmpres == -1){
      return NULL;
      //Can't send query
    }
    sent += tmpres;
  }
  //now it is time to receive the page
  memset(buf, 0, sizeof(buf));
  int htmlstart = 0;
  char * htmlcontent;
  size_t alllen = 0;
  while((tmpres = recv(sock, buf, BUFSIZE, 0)) > 0){
    if(htmlstart == 0){
      htmlcontent = strstr(buf, "\r\n\r\n");
      if(htmlcontent != NULL){
        htmlstart = 1;
        htmlcontent += 4;
        alllen += buf + tmpres - htmlcontent;
        memcpy(response, htmlcontent, alllen);
      }
    }else{
      memcpy(response+alllen, buf, tmpres);
      alllen += tmpres;
    }
    memset(buf, 0, tmpres);
  }
  response[alllen] = '\0';
  if(htmlstart){
    free(post);
    free(remote);
    free(ip);
    close(sock);
    //fprintf(stdout, "%s", htmlcontent);
    return 1;
  }
  //Error receiving data
  return NULL;
}

char *build_post_query(char *host, char *page, char *data)
{
  char *query;
  char *postpage = page;
  char *tpl = "POST /%s HTTP/1.0\r\nHost: %s\r\nUser-Agent: %s\r\nContent-Length: %d\r\n\r\n%s";
  if(postpage[0] == '/'){
    postpage += 1;
  }
  query = (char *)malloc(strlen(host)+strlen(postpage)+strlen(USERAGENT)+strlen(data)+strlen(tpl)-9+3);
  sprintf(query, tpl, postpage, host, USERAGENT, strlen(data), data);
  return query;
}

/*
int main(int argc, char **argv)
{
  char *host = "baidu.com";
  char *page = "/";
  char *c = http_post(host, page, "");
  fprintf(stdout, "%s", c);
  return 0;
}
*/
