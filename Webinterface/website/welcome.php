<?php
// Initialize the session
session_start();

require_once "config.php";
 
// Check if the user is logged in, if not then redirect him to login page
if(!isset($_SESSION["loggedin"]) || $_SESSION["loggedin"] !== true){
    header("location: login.php");


    exit;
}
?>
 
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Welcome</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>
        body{ font: 14px sans-serif; text-align: center; }
    </style>
</head>
<body>
    <h1 class="my-5">Hi, <b><?php echo htmlspecialchars($_SESSION["username"]); ?></b>. Welcome to our parking garage.</h1>
    <p>
        <a href="reset-password.php" class="btn btn-warning">Reset Your Password</a>
        <a href="logout.php" class="btn btn-danger ml-3">Sign Out of Your Account</a>
        <a href="license.php" class="btn btn-warning ml-3">Register your license plate</a>
        
    </p>
    <?php

if ($link->connect_error) {
  die("Database connection failed: " . $link->connect_error);
}

?>


<h3>Available parking spots: </h2>


<!-- import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="yourusername",
  password="yourpassword",
  database="mydatabase"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM customers")

myresult = mycursor.fetchall()

for x in myresult:
  print(x) -->


<?php

$query2 = mysqli_query($link, "SELECT COUNT(license) FROM users")
   or die (mysqli_error($link));

while ($row2 = mysqli_fetch_array($query2)) {
    echo "Total parking spots: " . $row2[0] . " / 4 are taken.";

}
?>

<table border="1" align="center">
    <h2>Your personal information: </h2>
<tr>
  <td>Username</td>
  <td>License plate</td>
  <td>Created at</td>
</tr>


<?php

$query = mysqli_query($link, "SELECT * FROM users WHERE username='".$_SESSION["username"]."'")
   or die (mysqli_error($link));

while ($row = mysqli_fetch_array($query)) {
  echo
   "<tr>
    <td>{$row['username']}</td>
    <td>{$row['license']}</td>
    <td>{$row['created_at']}</td>
   </tr>\n";

}

?>

</body>
</html>


