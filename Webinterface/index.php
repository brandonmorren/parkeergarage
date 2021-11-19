<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<body>
<?php

$hostname = "localhost";
$username = "pi";
$password = "raspberry";
$db = "mydb";

$dbconnect=mysqli_connect($hostname,$username,$password,$db);

if ($dbconnect->connect_error) {
  die("Database connection failed: " . $dbconnect->connect_error);
}

?>

<table border="1" align="center">
<tr>
  <td>Temperature</td>
  <td>Humidity</td>
  <td>Light (%)</td>
</tr>

<?php

$query = mysqli_query($dbconnect, "SELECT * FROM Licht_temp")
   or die (mysqli_error($dbconnect));

while ($row = mysqli_fetch_array($query)) {
  echo
   "<tr>
    <td>{$row['Temperature']}</td>
    <td>{$row['Humidity']}</td>
    <td>{$row['Light']}</td>
   </tr>\n";

}

?>
</table>
</body>
</html>