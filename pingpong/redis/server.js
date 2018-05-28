var config = require('../config/config');
var log = require("./loghelp"); 
var redis = require("redis"); 
function initialclient(param) { 
	var option={ 
		host: config.redis.host, 
		port: config.redis.port
	};

	if(param) {
	 	option=Object.assign(option,param); 
	 } 
	 redis.print 
	 let client = redis.createClient(option); 
	 client.on("error", function(err) { 
	 	log.error(err); });
	 	return client
	 }
