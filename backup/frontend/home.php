<!DOCTYPE html>
<html>
<link rel="stylesheet" href="style.css">

<head>
<meta charset="UTF-8">
  <title>Chat Bot</title>
  <link rel="shortcut icon" href="image/bot.png">
  <!-- for mobile screens -->
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <!-- stylesheets are conveniently separated into components -->
  <link rel="stylesheet" media="all" href="style/setup.css">
  <link rel="stylesheet" media="all" href="style/says.css">
  <link rel="stylesheet" media="all" href="style/reply.css">
  <link rel="stylesheet" media="all" href="style/typing.css">
  <link rel="stylesheet" media="all" href="style/input.css">
  <link rel="stylesheet" media="all" href="style/button.css">
  <style>
 
  .bubble-container {
    height: 100vh;
  }
  .bubble-container .input-wrap textarea {
    width: calc(100% - 12%);
    margin-left: 5%;
    margin-right: 5%;
    margin-top: 4%;
    margin-bottom: 3%;
    resize: none;
    overflow:hidden;
}
  </style>
</head>
<body>
<?php
include_once('dbclass.php');		
$db= new db;

session_start();

if (isset($_SESSION['user_id'])) {
}
else if(isset($_POST["username"]) & isset($_POST["password"])){
	$res=$db->getUser($_POST["username"],$_POST["password"]);
	$count=mysqli_num_rows($res);
	if($count>0){
		$row=mysqli_fetch_array($res,MYSQLI_ASSOC);

		$_SESSION['user_id']=$row['user_id'];
		header("location:home.php");
		exit;
	}
	else{
		echo "<script>alert('username or password incorrect!')</script>";
		echo "<script>location.href='index.php'</script>";
	}

}
else{
	header("location:index.php");
	exit;	
}
?>	

<p id="reply" style="display:none">Default</p>

<!-- <header>Chatbot</header> -->
<button onclick="start_the_service()" id="mn-btn"><img src="image/chat.png"></button>
<!-- import the JavaScript file -->
<center>
  <img src="image/bot1.png" style="height:40vh;margin: 10vh;">
</center>
<script src="script/Bubbles.js"></script>
<script type="text/javascript" src="script/button.js"></script>

<?php
	echo "<center>";
	echo "<a href='about.php'>View User Details</a><br/><br/>";

	echo "<form method='post'><input type='submit' value='Logout' name='logout'></form>";
	echo "</center>";

	if(isset($_POST['logout'])){
		$db->logOut();
	}

?>
</body>
</html>