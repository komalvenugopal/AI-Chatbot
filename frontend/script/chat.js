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
  },
  banana: {
    says: ["🍌"],
    reply: [
      {
        question: "Start Over",
        answer: "ice"
      }
    ]
  },
  "ice-cream": {
    says: ["🍦"],
    reply: [
      {
        question: "Start Over",
        answer: "ice"
      }
    ]
  }
}



var chatWindow = new Bubbles(document.getElementById("chat"), "chatWindow", {
  inputCallbackFn: function(o) {
    console.log(o.input );
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
    miss()
  }
})

chatWindow.talk(convo)