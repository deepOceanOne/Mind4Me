var Datas = {
 txt: '',
 messages: []
}

Vue.component('chatComponent', {
  props:['conversation'],
  data: function () {
    return Datas;
  },
  template:`
  <chat>
    <conversation>
      <message-line v-for="message in messages">
        <message :class="message.from">{{message.txt}}</message>
      </message-line>
    </conversation>
    <texting>
      <input v-model="txt" v-on:keyup.enter="send(txt)" placeholder="Say something" type="text">
      <input type="button" v-on:click="send(txt)"  value="Send">
    </texting>
  </chat>`,
  mounted:function(){
    this.init();
  },
  methods:{
    init:function(){
       let message = {from:'',txt:'Tell me something'};
       this.messages.push(message);
       this.ping();
    },
    send:function(txt){
      let message = {from:'me',txt:txt};
      this.messages.push(message);    
     
      setTimeout(()=>{
        let answer = {from:'',txt:'Lorem ipsum dolor sit amet...'};
        this.messages.push(answer);
      }, 1500);
    },
    ping:function(){
      // exemple of getting messages in API with conversations params
      setInterval(()=>{
       console.log('get messages');
      }, 500);
    }
  }
})

var app = new Vue({
  el: '#app',
  data:{
    conversation:[
      {
        url:'/get/conversation/123456',
        user:'exemple'
      }
    ]
  },
})

