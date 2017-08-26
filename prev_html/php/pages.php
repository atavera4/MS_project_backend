<?php
$responseObject = new stdClass();
$responseObject->success = 0;
$responseObject->msg = '';

//exec("python /var/www/html/py/pages.py");
if (count($output) > 0 && strpos($output[0], 'Errno') !== false) {
	$responseObject->msg = $output[0];
} else {
	$responseObject->success = 1;
}


$responseObject->msg = $_POST["name"];
$jsonResponseObject = json_encode($responseObject);
echo $jsonResponseObject;
exit;
?>
