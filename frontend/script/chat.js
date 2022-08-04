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

var chatWindow = new Bubbles(document.getElementById("chat"), "chatWindow", {
  // the one that we care about is inputCallbackFn()
  // this function returns an object with some data that we can process from user input
  // and understand the context of it

  // this is an example function that matches the text user typed to one of the answer bubbles
  // this function does no natural language processing
  // this is where you may want to connect this script to NLC backend.
  inputCallbackFn: function(o) {
    // add error conversation block & recall it if no answer matched
    var miss = function() {
      chatWindow.talk(
        {
          "i-dont-get-it": {
            says: [
              "Sorry, I don't get it 😕. Pls repeat? Or you can just click below 👇"
            ],
            reply: o.convo[o.standingAnswer].reply
          }
        },
        "i-dont-get-it"
      )
    }

    // do this if answer found
    var match = function(key) {
      setTimeout(function() {
        chatWindow.talk(convo, key) // restart current convo from point found in the answer
      }, 600)
    }

    // sanitize text for search function
    var strip = function(text) {
      return text.toLowerCase().replace(/[\s.,\/#!$%\^&\*;:{}=\-_'"`~()]/g, "")
    }

    // search function
    var found = false
    console.log(o.convo[o.standingAnswer])
    o.convo[o.standingAnswer].reply.forEach(function(e, i) {
      strip(e.question).includes(strip(o.input)) && o.input.length > 0
        ? (found = e.answer)
        : found ? null : (found = false)
    })
    found ? match(found) : miss()
  }
}) // done setting up chat-bubble


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

// pass JSON to your function and you're done!
chatWindow.talk(convo)