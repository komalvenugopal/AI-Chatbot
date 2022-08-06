<!DOCTYPE html>
<html>
<head>
	<title>About page</title>
</head>
<body>
<?php
session_start();

if(isset($_SESSION['user_id'])){
	include_once('dbclass.php');
	$db=new db;

	$res=$db->getUserData();
	$row=mysqli_fetch_array($res,MYSQLI_ASSOC);
}
else{
	header("location:index.php");
	exit;
}
?>
	<table align="center" border="2">
		<tr>
			<th colspan=2>User Details</th>
		</tr>
		<tr>
			<td>Name:</td>
			<td><?php echo $row['name'];?></td>
		</tr>
		<tr>
			<td>Phone:</td>
			<td><?php echo $row['phone'];?></td>
		</tr>
		<tr>
			<td>Email:</td>
			<td><?php echo $row['email'];?></td>
		</tr>
	</table>
</body>
</html>