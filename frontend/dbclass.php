<?php
$servername = "127.0.0.1";
$username = "root";
$password = "";
$db="support";

class db{
	public $conn;
	function __construct(){
		$this->conn=mysqli_connect("127.0.0.1","root","","support");
		if(mysqli_connect_errno()){
			echo "failed to connect";
			mysqli_connect_error();
			exit();
		}
		mysqli_select_db($this->conn,"support");
	}
	public function getUser($username,$password){
		$sql="SELECT user_id,username,password from user where username='$username' and password='$password' LIMIT 1";
		$result=mysqli_query($this->conn,$sql); 
		return $result;
	}
	public function getUserData(){
		//session_start();
		$sql="SELECT name,phone,email from user where user_id = ".$_SESSION['user_id']."";
		$result=mysqli_query($this->conn,$sql); 
		return $result;
	}
	public function getOrder(){
		$sql="SELECT * from order_table where user_id=".$_SESSION['user_id']."";
		$result=mysqli_query($this->conn,$sql); 
		return $result;
	}
	public function logOut(){
		
		unset($_SESSION["user_id"]);
		header("location:index.php");
		exit;
	}

	function __destruct(){
		mysqli_close($this->conn);
	}
}
?>