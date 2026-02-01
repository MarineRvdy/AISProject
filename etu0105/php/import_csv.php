<?php
$output = shell_exec('python3 ../python/insert_data.py 2>&1');
echo "<pre>$output</pre>";
?>