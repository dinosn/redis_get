# redis_get
Get redis keys from open redis, or by using a password.  This is to create a proof of concept to be used later in reports.

By default 20 keys will be displayed and this can be used as proof of concept, additionally the script will try to validate writable directories where Redis can write.  These locations can be used to achieve RCE.

Usage: ```python redis_get.py <hostname> <port> [password]``` , password is optional value in case you have a valid one or would like to test for possible values.

Requirement: `pip install redis`

I wrote this script because metasploit's redis extract module is often dying upon large redis key entries without retrieving any values.
