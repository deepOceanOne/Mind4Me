 nodejs redis 发布订阅机制封装

最近项目使用redis，对publish 和 subscribe的使用进行了了解，并进行了封装。 

var config = require('../config/config'); var log = require("./loghelp"); var redis = require("redis"); function initialclient(param) { var option={ host: config.redis.host, port: config.redis.port}; if(param) { option=Object.assign(option,param); } redis.print let client = redis.createClient(option); client.on("error", function(err) { log.error(err); }); return client; }
 

/*example: * let channel="ryan"; redis.pubSub.registerHandlers("ryan",msg=> console.log(msg)); redis.pubSub.subscribe(channel); redis.pubSub.publish(channel,"hello from chen");*/ class PubSub { constructor(){ this.sub=initialclient(); this.handlers=new Map(); this.subAction=(channle,message)=>{ let actions= this.handlers.get(channle)||new Set(); for(let action of actions) { action(message); } } this.alredyPublishs=[]; this.subConnected=false; } publish(channel,message) { let action=()=>{ let pub=initialclient(); pub.publish(channel,message); }; if(this.subConnected===false) { this.alredyPublishs.push(action); } else action(); } registerHandlers(channel,action) { var actions=this.handlers.get(channel)||new Set(); actions.add(action); this.handlers.set(channel,actions); } subscribe(channel) { let self=this; this.sub.subscribe(channel,function (err,reply) { if(err) log.error(err); self.subConnected=true; for(let publish of self.alredyPublishs) publish(); console.log(reply); }); this.sub.on("message", function (channel, message) { self.subAction(channel,message); }); } tearDown() { this.sub.quit(); } }
然后通过exports.pubsub=new PubSub() 将其暴漏，可保证是单例。在程序启动时，调用

registerHandlers  注册特定通道的处理逻辑，然后调用
subscribe  订阅通道。

在合适时机调用publish，这个机制可以实现分布式下所有客户端watch 同一个数据的更改。