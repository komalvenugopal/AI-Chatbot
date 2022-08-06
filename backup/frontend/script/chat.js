function predict(message) {
  let options = {
      method: 'POST',
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ message: message }),
  }
  return fetch('http://127.0.0.1:5000/predict',options).then(r=>r.json()).then((d)=> {return d.answer})   
}
var convo = {
  ice: {
    says: ["Hi", "Would you like banana or ice cream?"],
    reply: [
      {
        question: "Banana",
        answer: "banana"
      },
      {
        question: "Ice Cream",
        answer: "ice-cream"
      }
    ]
  }
}



var chatWindow = new Bubbles(document.getElementById("chat"), "chatWindow", {
  inputCallbackFn: function(o) {
    console.log(2);
    var miss = function() {
      chatWindow.talk(
        {
          "i-dont-get-it": {
            says: [
              "Sorry, I don't get it 😕. Pls repeat? Or you can just click below 👇"
            ],
            reply:  [{
              question: "Start Over",
              answer: "ice"
            }]
          }
        },
        "i-dont-get-it"
      )
    }
    console.log(o.input);
    predict(o.input).then(function(val) {var answer=val;  document.getElementById("reply").innerHTML=answer;});
    reply=document.getElementById("reply").innerHTML;
    chatWindow.talk(
      {
        "backend": {
          says: [
            reply
          ],
          reply:  [{
            question: "Start Over",
            answer: "ice"
          }]
        }
      },
      "backend"
    )    
  }
})

chatWindow.talk(convo)