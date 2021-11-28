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




<table border="1" align="center">
  <h3>Available parking spots: </h2>
<tr>
  <td>Parkingspot</td>
  <td>Status</td>
  <td>Bezet / beschikbaar sinds</td>
</tr>



<?php

$query2 = mysqli_query($link, "SELECT * from parkingspot")
   or die (mysqli_error($link));

while ($row2 = mysqli_fetch_array($query2)) {
  echo
  "<tr>
   <td>{$row2['parkingspot']}</td>
   <td>{$row2['status']}</td>
   <td>{$row2['aankomst']}</td>
  </tr>\n";

}
?>


<div>
    <table border="1" align="center">
        <h2>Your personal information: </h2>
    <tr>
        <td>voornaam</td>
        <td>achternaa'</td>
        <td>straat_huisnummer</td>
        <td>gemeente_postcode</td>
        <td>bank</td>
        <td>nummerplaat</td>
        <td>parkingspot</td>
        <td>aankomst</td>
        <td>vertrek</td>
        <td>tebetalen</td>
    </tr>
  </div>



<?php

if ($_SESSION["username"] != "admin") {

  $query = mysqli_query($link, "SELECT * FROM nrplaat WHERE username='".$_SESSION["username"]."'")
    or die (mysqli_error($link));

  while ($row = mysqli_fetch_array($query)) {
    echo
    "<tr>
      <td>{$row['voornaam']}</td>
      <td>{$row['achternaam']}</td>
      <td>{$row['straat_huisnummer']}</td>
      <td>{$row['gemeente_postcode']}</td>
      <td>{$row['bank']}</td>
      <td>{$row['nummerplaat']}</td>
      <td>{$row['parkingspot']}</td>
      <td>{$row['aankomst']}</td>
      <td>{$row['vertrek']}</td>
      <td>{$row['tebetalen']}</td>
    </tr>\n";
  }

}



if ($_SESSION["username"] == "admin") {

  $query = mysqli_query($link, "SELECT * FROM nrplaat")
  or die (mysqli_error($link));

    while ($row = mysqli_fetch_array($query)) {
    echo
      "<tr>
      <td>{$row['voornaam']}</td>
      <td>{$row['achternaam']}</td>
      <td>{$row['straat_huisnummer']}</td>
      <td>{$row['gemeente_postcode']}</td>
      <td>{$row['bank']}</td>
      <td>{$row['nummerplaat']}</td>
      <td>{$row['parkingspot']}</td>
      <td>{$row['aankomst']}</td>
      <td>{$row['vertrek']}</td>
      <td>{$row['tebetalen']}</td>
      </tr>\n";
    }

}  

?>

<?php if ($_SESSION["username"] == "admin") { ?>

<div>
    <table border="1" align="center">
    <h2>User information</h2>
    <tr>
    <td>id</td>
    <td>username</td>
    <td>password</td>
    <td>created at</td>

    </tr>
  </div>

<?php } ?>


<?php

if ($_SESSION["username"] == "admin") {


  $query3 = mysqli_query($link, "SELECT * FROM users")
   or die (mysqli_error($link));

  while ($row3 = mysqli_fetch_array($query3)) {
    echo
    "<tr>
      <td>{$row3['id']}</td>
      <td>{$row3['username']}</td>
      <td>{$row3['password']}</td>
      <td>{$row3['created_at']}</td>
    </tr>\n";

  }
  
}


?>



</body>
</html>


