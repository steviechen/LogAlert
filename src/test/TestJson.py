# def replaceComma( string):
#    res = ""
#    for i, ch in enumerate(string):
#       # if (ch == ','):
#       #    if string.find(']',i + 1) != -1 and string.find(']', i + 1) < string.find('[', i + 1):
#       #       res += ch
#       #    elif string[0:i].count("'") % 2 != 0:
#       #       res += ch
#       #    else:
#       #       res += '^'
#       # else:
#       #    res += ch
#       #
#       #
#       # if  (ch == ',' and (string.find('[', i + 1) != -1 and string.find(']', i + 1) > string.find('[', i + 1) or string.find(']',i + 1) == -1)) or (ch == ',' and string[0:i].count("'") % 2 == 0):
#       #
#       # if (ch == ',' and string[0:i].count("'") % 2 == 0):
#       #    print(i)
#       #    res += '^'
#       # else:
#       #    res += ch
#       if (ch == ',' and string[0: i].count("'") % 2 == 0):
#          res += '^'
#       else:
#          res += ch
#    return res
# if __name__ == '__main__':
#    a = """'------> GET https'"""
#    print(replaceComma("'native ,,, socket [139,866,617,503,200] with wrapper,','aaaa,a'"))
keyWords1 =  [
            "'message': '[2019-10-14 19:15:39,900] [ INFO] 690 [http-apr-8081-exec-8] c.c.w.n.s.c.i.NGCsrfInterceptor - 68C3D4054A2D49E3AF7CCB8248B331E8_1571080539632 - The csrf token cannot be got from Cookie. Generate new random csrf token: c2f63082-48e5-42fb-af52-ec6cb0f03967, method: POST, cookie count: 0, cookie size: 0'",
            "'message': '[2019-10-14 19:15:39,900] [ INFO] 690 [http-apr-8081-exec-8] c.c.w.n.s.c.i.NGCsrfInterceptor - 68C3D4054A2D49E3AF7CCB8248B331E8_1571080539632 - The csrf token in post header or param is not valid, so reject it, headerValue=ac5b9dc3-8d82-467c-ab9d-a930fc68647f, cookieValue=c2f63082-48e5-42fb-af52-ec6cb0f03967'",
            "'message': '[2019-10-14 19:15:39,901] [ERROR] 690 [http-apr-8081-exec-8] c.c.w.s.c.e.ExceptionTrace - 68C3D4054A2D49E3AF7CCB8248B331E8_1571080539632 - Exception occured, please refer to following detail at bottom",
            "'message': '10.152.21.133 10.252.16.112 - - [14/Oct/2019:19:15:39 +0000] POST /webappng/api/v1/cdnhoststatus?siteurl=cisco HTTP/1.1 500 57 https://cisco.webex.com/webappng/sites/cisco/recording/playback/75F4D4960D724679E053D107FC0A3A83 68C3D4054A2D49E3AF7CCB8248B331E8_1571080539632 Mozilla/5.0 (Macintosh",
            "'message': '10.152.21.133, 10.252.16.112 - - [14/Oct/2019:19:15:39 +0000] POST /webappng/api/v1/cdnhoststatus?siteurl=cisco HTTP/1.0 500 57 https://cisco.webex.com/webappng/sites/cisco/recording/playback/75F4D4960D724679E053D107FC0A3A83 68C3D4054A2D49E3AF7CCB8248B331E8_1571080539632 Mozilla/5.0 (Macintosh",
            "Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.2 Safari/605.1.15 [alivereqs:3] [pid:27310] 54037 52540'",
            "'message': '[2019-10-14 19:15:39,939] [ERROR] 690 [http-apr-8081-exec-8] c.c.w.s.c.e.ExceptionTrace - 68C3D4054A2D49E3AF7CCB8248B331E8_1571080539632 - Header Key : user-agent",
            "Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.2 Safari/605.1.15 41 40 cisco.webex.com'",
            "Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.2 Safari/605.1.15'",
            "'m_ip': '10.152.21.133 10.252.16.112 - - '",
            "'m_ip': '10.152.21.133, 10.252.16.112 - - '"
        ]
keyWords2 = [
                "'message': '[2019-10-14 19:15:40:227] [INFO] [http-apr-8081-exec-178] - 33FD77E416F748DD982BF096302B55B8_1571080539983 - com.webex.webapp.common.util.security.AppTokenUtil.generateTicketWithKMSystem(AppTokenUtil.java:310) - generate token with KM system success: APP_CenterApp, true, false, keyVersion is 4'",
                "'message': '[2019-10-14 19:15:40,433] [ERROR] 19138 [http-apr-8081-exec-178] c.c.w.s.c.e.ExceptionTrace - 33FD77E416F748DD982BF096302B55B8_1571080539983 - Exception occured, please refer to following detail at bottom",
                "'message': '[2019-10-14 19:15:40,417] [ERROR] 19138 [http-apr-8081-exec-44] c.c.w.s.c.e.ExceptionTrace - 33FD77E416F748DD982BF096302B55B8_1571080539983 - Exception occured, please refer to following detail at bottom",
                "'message': '10.240.8.86, 10.240.49.9 10.252.16.112 - - [14/Oct/2019:19:15:40 +0000] POST /webappng/api/v1/meetings/simple?siteurl=broadpeak-1.my HTTP/1.0 500 57 https://broadpeak-1.my.webex.com/webappng/sites/broadpeak-1.my/meeting/scheduler 33FD77E416F748DD982BF096302B55B8_1571080539983 Mozilla/5.0 (Macintosh",
                "'message': '10.240.8.86, 10.240.49.9, 10.252.16.112 - - [14/Oct/2019:19:15:40 +0000] POST /webappng/api/v1/meetings/simple?siteurl=broadpeak-1.my HTTP/1.0 500 57 https://broadpeak-1.my.webex.com/webappng/sites/broadpeak-1.my/meeting/scheduler 33FD77E416F748DD982BF096302B55B8_1571080539983 Mozilla/5.0 (Macintosh",
                "Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36 [alivereqs:33] [pid:9893] 284816 281262'",
                "'message': '[2019-10-14 19:15:40,417] [ERROR] 19138 [http-apr-8081-exec-44] c.c.w.s.c.e.ExceptionTrace - 33FD77E416F748DD982BF096302B55B8_1571080539983 - Header Key : useragent",
                "'message': '[2019-10-14 19:15:40,501] [ERROR] 19138 [http-apr-8081-exec-178] c.c.w.s.c.e.ExceptionTrace - 33FD77E416F748DD982BF096302B55B8_1571080539983 - Header Key : user-agent",
                "Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36 282 280 broadpeak-1.my.webex.com'",
                "Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'",
                "'m_ip': '10.240.8.86, 10.240.49.9 10.252.16.112 - - '",
                "'m_ip': '10.240.8.86, 10.240.49.9, 10.252.16.112 - - '",
                "Caused by: feign.FeignException: status 500 reading RawMeetingClient#createSimpleMeeting(String,SchedulerDTO)"
            ]
keyWords3 = [
                "'message': '[2019-10-15 02:42:39,639] [ INFO] 21128 [http-apr-8081-exec-170] c.c.w.n.s.c.i.NGCsrfInterceptor - AFC4E209B1454E4AA7AABCEC4DDC4C94_1571107359371 - The csrf token cannot be got from Cookie. Generate new random csrf token: 6e4c61d0-9b92-4746-9aa5-b697c91d777c, method: POST, cookie count: 0, cookie size: 0'",
                "'message': '[2019-10-15 02:42:39,639] [ INFO] 21128 [http-apr-8081-exec-170] c.c.w.n.s.c.i.NGCsrfInterceptor - AFC4E209B1454E4AA7AABCEC4DDC4C94_1571107359371 - The csrf token in post header or param is not valid, so reject it, headerValue=4f257ed0-aa14-4a7e-b541-368184c7c95b, cookieValue=6e4c61d0-9b92-4746-9aa5-b697c91d777c'",
                "'message': '[2019-10-15 02:42:39,641] [ERROR] 21128 [http-apr-8081-exec-170] c.c.w.s.c.e.ExceptionTrace - AFC4E209B1454E4AA7AABCEC4DDC4C94_1571107359371 - Exception occured, please refer to following detail at bottom",
                "'message': '10.252.52.41 10.252.16.30 - - [15/Oct/2019:02:42:39 +0000] POST /webappng/api/v1/cdnhoststatus?siteurl=svtestt33l-r HTTP/1.1 500 57 https://nebularv.webex.com/webappng/sites/svtestt33l-r/dashboard/landing?siteurl=svtestt33l-r&type=Host AFC4E209B1454E4AA7AABCEC4DDC4C94_1571107359371 Mozilla/5.0 (Windows NT 10.0",
                "'message': '10.252.52.41, 10.252.16.30 - - [15/Oct/2019:02:42:39 +0000] POST /webappng/api/v1/cdnhoststatus?siteurl=svtestt33l-r HTTP/1.0 500 57 https://nebularv.webex.com/webappng/sites/svtestt33l-r/dashboard/landing?siteurl=svtestt33l-r&type=Host AFC4E209B1454E4AA7AABCEC4DDC4C94_1571107359371 Mozilla/5.0 (Windows NT 10.0",
                "'message': '[2019-10-15 02:42:39,702] [ERROR] 21128 [http-apr-8081-exec-170] c.c.w.s.c.e.ExceptionTrace - AFC4E209B1454E4AA7AABCEC4DDC4C94_1571107359371 - Header Key : user-agent",
                "rv:66.0) Gecko/20100101 Firefox/66.0 [alivereqs:0] [pid:21451] 80956 77885'",
                "'m_ip': '10.252.52.41 10.252.16.30 - - '",
                "'m_ip': '10.252.52.41, 10.252.16.30 - - '",
                "Value : Mozilla/5.0 (Windows NT 10.0",
                "rv:66.0) Gecko/20100101 Firefox/66.0 77 76 nebularv.webex.com'",
                "'m_agent': 'Mozilla/5.0 (Windows NT 10.0"
            ]

import numpy as np
import scipy
import re
import pandas as pd

def simlarityCal(seq1,seq2,weight = 0.2):
   if len(seq2)>len(seq1):
            tmp = seq1
            seq1 = seq2
            seq2 = tmp
   num = 0
   for i in sorted(seq1,key=str.lower):
      allLDist = []
      for j in sorted(seq2,key=str.lower):
         split1 = splitWordSentenceForLevenshtein(i)
         split2 = splitWordSentenceForLevenshtein(j)
         allLDist.append(int(levenshtein(split1,split2)))
      minDist = min(allLDist)
      if minDist <  0.5 * max(len(split1),len(split2)):
          num = num +1
   print('all similarity res is:'+str(num))
   return -scipy.log(num/(len(seq1) + len(seq2))) * weight

def levenshtein(seq1, seq2):
   size_x = len(seq1) + 1
   size_y = len(seq2) + 1
   matrix = np.zeros((size_x, size_y))
   for x in range(size_x):
      matrix[x, 0] = x
   for y in range(size_y):
      matrix[0, y] = y
   for x in range(1, size_x):
      for y in range(1, size_y):
         if seq1[x - 1] == seq2[y - 1]:
            matrix[x, y] = min(
               matrix[x - 1, y] + 1,
               matrix[x - 1, y - 1],
               matrix[x, y - 1] + 1
            )
         else:
            matrix[x, y] = min(
               matrix[x - 1, y] + 1,
               matrix[x - 1, y - 1] + 1,
               matrix[x, y - 1] + 1
            )
   return matrix[size_x - 1, size_y - 1]

def splitWordSentenceForLevenshtein(x):
   replacements = {
      "\'": " ",
      ",": " ",
      '"': ' ',
      "{": " ",
      "}": " ",
      "[": " ",
      "]": " ",
      "(": " ",
      ")": " ",
      "?": " ",
      ":": " ",
      "~": " ",
      "!": " ",
      "$": " ",
      ";": " ",
   }
   stn = x.translate(str.maketrans(replacements))
   temp_stn = re.sub('\\s+', ' ', stn.strip())
   ll = pd.Series(temp_stn.split(" "))
   return [s for s in ll if not s.isdigit()]

if __name__ == '__main__':
    print(simlarityCal(keyWords1,keyWords2))
    print(simlarityCal(keyWords1,keyWords3))