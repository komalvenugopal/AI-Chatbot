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
  inputCallbackFn: function(o) {
    var miss = function() {
      chatWindow.talk(
        {
          "i-dont-get-it": {
            says: [
              "Sorry I didn't get it, Please choose from below options"      
            ],
            reply: o.convo[o.standingAnswer].reply
          }
        },
        "i-dont-get-it"
      )
    }

    var match = function(key) {
      setTimeout(function() {
        chatWindow.talk(convo, key)
      }, 600)
    }

    // sanitize text for search function
    var strip = function(text) {
      return text.toLowerCase().replace(/[\s.,\/#!$%\^&\*;:{}=\-_'"`~()]/g, "")
    }
    // search function
    // o.convo[o.standingAnswer].reply.forEach(function(e, i) {
    //   strip(e.question).includes(strip(o.input)) && o.input.length > 0
    //     ? (found = e.answer) : found 
    // })
        
    // predict("Hi").then(val => console.log(val))
    console.log(o.convo);
    // o.convo[o.standingAnswer].says=predict()
    // match("physics")
  }
})

var convo = {
  "ice": {
    says: ["Hi", "You can ask me if you have any Questions... "],
    reply: [
      // recommended questions  
      {
        question: "How to integrate with jivox",
        answer: "physics"
      },
      {
        question: "What are the types of ads",
        answer: "chemistry"
      }
    ]
  },
  // recommended questions
  "physics": {
    says: ["The branch of science concerned with the nature and properties of matter and energy. The subject matter of physics includes mechanics, heat, light and other radiation, sound, electricity, magnetism, and the structure of atoms."],
    reply: [
      {
        question: "chemistry",
        answer: "chemistry"
      },
      {
        question: "Start Over",
        answer: "ice"
      }
    ]
  },
  "chemistry": {
    says: ["The branch of science concerned with the nature and properties of matter and energy. The subject matter of physics includes mechanics, heat, light and other radiation, sound, electricity, magnetism, and the structure of atoms."],
    reply: [
      {
        question: "physics",
        answer: "physics"
      }
    ]
  }
}

chatWindow.talk(convo);

