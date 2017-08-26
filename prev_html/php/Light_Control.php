<?php
$responseObject = new stdClass();
$responseObject->success = 0;
$responseObject->msg = '';

DEFINE ('DB_USER', 'website');
DEFINE ('DB_PASSWORD', 'turtledove');
DEFINE ('DB_HOST', 'localhost');
DEFINE ('DB_NAME', 'device_manager');

// CONNECT TO SQL Database.
$dbc = @mysqli_connect(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
OR die('Could not connect to MySQL ' . mysqli_connect_error() );
if($dbc) { echo 'works dbc'; }

// Get info from SQL Table
$query = "SELECT id, name, state, status FROM device_status"; 
$response = @mysqli_query($dbc, $query);
if($response) { echo 'response done!!'; }
$row = mysqli_fetch_array($response);
if($response){
	echo  $row[name];
} else {
	echo 'DID NOT WORK';
}   

// INSERT NEW ITEM INTO SQL TABLE
$query = "INSERT INTO device_status (name, state, status) VALUES(?, ?, ?)";
$stmt = mysqli_prepare($dbc, $query);
$name = 'test button';
$state = 'NONE';
$status = 'on state';
mysqli_stmt_bind_param($stmt, "sss", $name, $state, $status); // 
mysqli_stmt_execute($stmt);

// UPDATE Value in SQL Table. Make string in parts for security purposes. Input validation.
if ($_POST["state"] == 0) {
	$update_cmd = "UPDATE device_status SET state='OFF' WHERE id=1";
} 
else {
	$update_cmd = "UPDATE device_status SET state='ON' WHERE id=1";
}

$stmt = mysqli_prepare($dbc, $update_cmd);
mysqli_stmt_execute($stmt);

if (count($output) > 0 && strpos($output[0], 'Errno') !== false) {
	$responseObject->msg = $output[0];
} else {
	$responseObject->success = 1;
}


$responseObject->msg = $_POST["state"];
$jsonResponseObject = json_encode($responseObject); 
echo $jsonResponseObject;
exit;
?>
