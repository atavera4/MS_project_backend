<?php
$responseObject = new stdClass();
$responseObject->success = 0;
$responseObject->msg = '';

//exec("sudo rm /var/www/html/FIRST.txt");
exec("python /var/www/html/py/open.py 2>&1", $output);
//exec("python /var/www/html/p.py");
if (count($output) > 0 && strpos($output[0], 'Errno') !== false) {
	$responseObject->msg = $output[0];
} else {
	$responseObject->success = 1;
}

$jsonResponseObject = json_encode($responseObject);
echo $jsonResponseObject;
exit;
?>
