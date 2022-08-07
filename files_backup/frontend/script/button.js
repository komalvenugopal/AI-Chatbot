var p=["init"];
function start_the_service() {
  // console.log(p);
  if (p[0] ==="init") {
    p[0]="started";
    var t  = document.createElement("div");
    var t2  = document.createElement("script");
    t.id = "chat";
    if (window.innerWidth > window.innerHeight) {
      t.style.width="29.6%";
      t.style.left="68%";
      t.style.top="30vh";
    } else {
      t.style.width = "92.8%";
    }
    t2.src="script/chat.js";
    document.body.appendChild(t);
    document.body.appendChild(t2);
    document.getElementById("mn-btn").style.borderRadius = "0px 0px 20px 20px";
  } 
  else if(p[0]=="started"){
    p[0]="closed"
    document.getElementById('chat').style.display="none";
    // document.getElementById('chat').remove();
    // p[0] ="o";
    // document.getElementById("mn-btn").style.borderRadius = "20px 20px 0px 0px";
  }
  else if(p[0]=="closed"){
    p[0]="started"
    document.getElementById('chat').style.display="block";
  }

}
document.body.onload = function () {
if (window.innerWidth < window.innerHeight) {
  var t = document.getElementById("mn-btn");
  t.style.width="94%";
  t.style.left="2vh";
  t.style.top="75vh";
}
console.log("Chatbot Loaded");
}