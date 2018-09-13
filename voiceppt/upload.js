

var url = 'http://api.xfyun.cn/v1/service/v1/iat';
var api_key = 'bac6dc43992150cc4d1248293f919454';
var param = {"engine_type": "sms16k", "aue": "raw"};
var x_appid = '5b93d247';
var x_param = base64.b64encode(json.dumps(param).replace(' ', ''));
var  x_time = int(int(round(time.time() * 1000)) / 1000);
var x_checksum = hashlib.md5(api_key + str(x_time) + x_param).hexdigest()
var  x_header = {'X-Appid': x_appid,
                'X-CurTime': x_time,
                'X-Param': x_param,
                'X-CheckSum': x_checksum};
var req = urllib2.Request(url, body, x_header);
var result = urllib2.urlopen(req);
var result = result.read()