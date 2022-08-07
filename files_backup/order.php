<!DOCTYPE>
<html>
<head>
	<title>My Order</title>
</head>
<body>
<?php
session_start();
	if(isset($_SESSION['user_id'])){
		include_once('dbclass.php');
		$db=new db;

		$res=$db->getOrder();
		
		echo "<h1 align='center'>My Order</h1><br/>";
		echo "<table align='center' border=1>";
		echo "<tr><th>Product name</th><th>Quantity</th><th>Amount</th></tr>";

		while($row=mysqli_fetch_array($res,MYSQLI_ASSOC)){

			echo "<tr>";
			echo "<td>".$row['product_name']."</td>";
			echo "<td>".$row['qty']."</td>";
			echo "<td>".$row['amount']."</td>";
			echo "</tr>";
		}
		echo "</table>";
	}
	else{
		header("location:index.php");
		exit;
	}	
?>	

</body>
</html>