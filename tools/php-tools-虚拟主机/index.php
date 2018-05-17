<?php

ignore_user_abort(true); 
set_time_limit(0); 

$myfile = fopen("download.zip", "w");
$content = file_get_contents("https://github.com/engine-go/movie/archive/master.zip");
fwrite($myfile, $content);

?>



