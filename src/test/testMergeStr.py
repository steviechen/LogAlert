import  re
a = """com.cisco.webex.common.exception.WBXException: csrf_token_in_post_header_is_not_valid
	at com.cisco.webex.ngapp.server.common.interceptor.NGCsrfInterceptor.preHandle(NGCsrfInterceptor.java:59) ~[classes/:1.22.2-58]
	... suppressed 5 lines
	at javax.servlet.http.HttpServlet.service(HttpServlet.java:661) [servlet-api.jar:?]
	... 
	at javax.servlet.http.HttpServlet.service(HttpServlet.java:742) [servlet-api.jar:?]
	... suppressed 5 lines
	at java.security.AccessController.doPrivileged(Native Method) [?:1.8.0_191]
	at javax.security.auth.Subject.doAsPrivileged(Subject.java:549) [?:1.8.0_191]
	... suppressed 6 lines
	at java.security.AccessController.doPrivileged(Native Method) [?:1.8.0_191]
	... 
	at org.apache.tomcat.websocket.server.WsFilter.doFilter(WsFilter.java:52) [tomcat-websocket.jar:8.5.33]
	... suppressed 5 lines
	at java.security.AccessController.doPrivileged(Native Method) [?:1.8.0_191]
	at javax.security.auth.Subject.doAsPrivileged(Subject.java:549) [?:1.8.0_191]
	... suppressed 6 lines
	at java.security.AccessController.doPrivileged(Native Method) [?:1.8.0_191]
	... 
	at org.apache.logging.log4j.web.Log4jServletFilter.doFilter(Log4jServletFilter.java:71) [log4j-web-2.10.0.jar:2.10.0]
	... suppressed 5 lines
	at java.security.AccessController.doPrivileged(Native Method) [?:1.8.0_191]
	at javax.security.auth.Subject.doAsPrivileged(Subject.java:549) [?:1.8.0_191]
	... suppressed 6 lines
	at java.security.AccessController.doPrivileged(Native Method) [?:1.8.0_191]
	... """



newtext = re.sub(r"\n\t","\\n", a, 0)

print(newtext)

print("\\n")