/*example: * 
let channel="ryan"; 
redis.pubSub.registerHandlers("ryan",msg=> console.log(msg)); 
redis.pubSub.subscribe(channel); 
redis.pubSub.publish(channel,"hello from chen");
*/
 class PubSub { 
 	constructor(){ 
 		this.sub=initialclient(); 
 		this.handlers=new Map(); 
 		this.subAction=(channle,message)=>{ 
 			let actions= this.handlers.get(channle)||new Set();
 			 for(let action of actions) {
 			  action(message); 
 			 } 
 		} 
 		this.alredyPublishs=[]; 
 		this.subConnected=false; 
 	} publish(channel,message) { 
 		let action=()=>{ 
 			let pub=initialclient();
 			 pub.publish(channel,message);
 		 }; 
 		if(this.subConnected===false) { 
 			this.alredyPublishs.push(action); 
 		}
 	    else 
 	    	action(); 
 	    } 
 	 registerHandlers(channel,action) { 
 	 	var actions=this.handlers.get(channel)||new Set(); 
		actions.add(action); 
		this.handlers.set(channel,actions); 
	} subscribe(channel) { 
		let self=this; 
		this.sub.subscribe(channel,function (err,reply) { 
			if(err) log.error(err); 
			self.subConnected=true; 
			for(let publish of self.alredyPublishs)
			 publish();
			  console.log(reply); 
			}); 
		this.sub.on("message", function (channel, message) { 
			self.subAction(channel,message); 
		}); 
	} 
	tearDown() { 
		this.sub.quit(); 
	}
}