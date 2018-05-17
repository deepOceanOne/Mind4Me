

<?php

ignore_user_abort(true); 
set_time_limit(0); 


 $filename = 'download.zip';
 $zip = new ZipArchive; 
$res = $zip->open($filename); 
$zip->extractTo('code9'); 
 $zip->close(); 

?>




