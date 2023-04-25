<?php

    //create connection to db
    $host = "localhost";
    $user = "root";
    $pass = "YOUR PASSWORD";
    $database = "room_IOT";
    $conn = mysqli_connect($host,$user,$pass,$database);

    if (mysqli_connect_errno())
    {
    	echo json_encode(array("error"=>"Failed to connect to mySQL:" .mysqli_connect_error()));
	exit();
    }
    //we get latest or current temp
    $sql = "SELECT value FROM temperature ORDER BY timestamp DESC LIMIT 1 ";
    $result = mysqli_query($conn,$sql);
    if(!$result || mysqli_num_rows($result)==0)
    {
	echo json_encode(array("error"=>"UPS Failure for gettin temp from database"));
    }
    $row = mysqli_fetch_assoc($result);
    $current_temperature = $row['value'];
    //we try to get min and max of the day
    $today = date('Y-m-d');
    $sql = "SELECT MIN(value) AS min, MAX(value) AS max FROM temperature WHERE DATE(timestamp)='$today'";
    $result = mysqli_query($conn,$sql);
    if(!$result || mysqli_num_rows($result)==0)
    {
    	echo json_encode(array("error"=>"Ups error to get min and max"));
	exit();
    }

    $row=mysqli_fetch_assoc($result);
    $min_temperature = $row['min'];
    $max_temperature = $row['max'];
    mysqli_close($conn);

    echo json_encode(array(
	"current_temperature"=>$current_temperature,
        "min_temperature"=>$min_temperature,
        "max_temperature"=>$max_temperature
   ));
?>
