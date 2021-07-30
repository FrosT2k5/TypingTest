
<?php
// Program to display URL of current page.
  
if(isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] === 'on')
    $link = "https";
else
    $link = "http";
  
// Here append the common URL characters.
$link .= "://";
  
// Append the host(domain name, ip) to the URL.
$link .= $_SERVER['HTTP_HOST'];
  
// Append the requested resource location to the URL
$link .= $_SERVER['REQUEST_URI'];
      
// Print the link
$link;
$string_psition = strpos($link, "?");
echo "<br>";
$final_score_append = substr($link, $string_psition+1);
echo $final_score_append;
$writer = $final_score_append;
$file = fopen("scorelog.txt","a");
fwrite($file,"$writer\n");
fclose($file);

?>
