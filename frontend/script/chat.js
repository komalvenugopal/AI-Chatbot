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
    chatWindow.talk(
      {
        "i-dont-get-it": {
          says: [
            "Sorry I didn't get it, Please choose from below options"      
          ],
          reply: o.convo[o.standingAnswer].reply
        }
      }
    )
  }
})
chatWindow.talk(convo);