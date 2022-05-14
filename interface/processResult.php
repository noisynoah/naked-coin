<?php
// echo err for debuging phase
ini_set('display_errors', '1');
ini_set('display_startup_errors', '1');
error_reporting(E_ALL);

$value_1 = "cannot get data";
$value_2 = "cannot get data";
if (isset ($_POST['value_1'])) {
    $value_1 = $_POST['value_1'];
    $value_2 = $_POST['value_2'];
}

// echo $textGenerate;
$handle = fsockopen("127.0.0.1", 10111);
$strPost =  "LKNSFWAyNLk8mjz8n91E3dBaK982y8zH1tzbuf0stfA"."--".$value_1."--".$value_2;    // string post to python file
// echo $strPost;
// check & send data
if($handle) {
    fputs($handle, $strPost);
    // get respon from python script
    while($line=fgets($handle,1024)){
        // echo $line;
        echo $line;
    }
}

fclose($handle);


?>
