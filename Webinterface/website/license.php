<?php
// Initialize the session
session_start();
 
// Check if the user is logged in, otherwise redirect to login page
if(!isset($_SESSION["loggedin"]) || $_SESSION["loggedin"] !== true){
    header("location: index.php");
    exit;
}
 
// Include config file
require_once "config.php";
 
// Define variables and initialize with empty values
$license = $license_err = "";
$achternaam = $achternaam_err = "";
$voornaam = $voornaam_err = "";
$straat_huis = $straat_huis_err = "";
$gemeente_post = $gemeente_post_err = "";
$bank = $bank_err = "";
$username = ($_SESSION["username"]);

 
// Check connection
if($link === false){
    die("ERROR: Could not connect. " . mysqli_connect_error());
}

// header("location: welcome.php");
if($_SERVER["REQUEST_METHOD"] == "POST"){

    // Validate password
    if(empty(trim($_POST["license"]))){
        $license_err = "Please enter a password.";     
    } elseif(strlen(trim($_POST["license"])) < 6){
        $license_err = "Password must have atleast 6 characters.";
    } else{
        $license = trim($_POST["license"]);
    }

        // Validate password
    if(empty(trim($_POST["achternaam"]))){
        $achternaam_err = "Please enter a password.";     
    } elseif(strlen(trim($_POST["achternaam"])) < 6){
        $achternaam_err = "Password must have atleast 6 characters.";
    } else{
        $achternaam = trim($_POST["achternaam"]);
    }

    // Validate password
    if(empty(trim($_POST["voornaam"]))){
        $voornaam_err = "Please enter a password.";     
    } elseif(strlen(trim($_POST["voornaam"])) < 6){
        $voornaam_err = "Password must have atleast 6 characters.";
    } else{
        $voornaam = trim($_POST["voornaam"]);
    }
    
    // Validate password
    if(empty(trim($_POST["straat_huis"]))){
        $straat_huis_err = "Please enter a password.";     
    } elseif(strlen(trim($_POST["straat_huis"])) < 6){
        $straat_huis_err = "Password must have atleast 6 characters.";
    } else{
        $straat_huis = trim($_POST["straat_huis"]);
    }

    // Validate password
    if(empty(trim($_POST["gemeente_post"]))){
        $gemeente_post_err = "Please enter a password.";     
    } elseif(strlen(trim($_POST["gemeente_post"])) < 6){
        $gemeente_post_err = "Password must have atleast 6 characters.";
    } else{
        $gemeente_post = trim($_POST["gemeente_post"]);
    }
    
    // Validate password
    if(empty(trim($_POST["bank"]))){
        $bank_err = "Please enter a password.";     
    } elseif(strlen(trim($_POST["bank"])) < 6){
        $bank_err = "Password must have atleast 6 characters.";
    } else{
        $bank = trim($_POST["bank"]);
    } 

    // Check input errors before inserting in database
    if(empty($license_err) && empty($achternaam_err) && empty($voornaam_err) && empty($straat_huis_err) && empty($gemeente_post_err) && empty($bank_err)){
        
        // Prepare an insert statement
        $sql = "UPDATE nrplaat SET username='$username', achternaam='$achternaam', voornaam='$voornaam', straat_huisnummer='$straat_huis', gemeente_postcode='$gemeente_post', bank='$bank'  WHERE nummerplaat='$license'";
         
        if($stmt = mysqli_prepare($link, $sql)){
            // Bind variables to the prepared statement as parameters
            mysqli_stmt_bind_param($stmt, "ss");
        
            
            // Attempt to execute the prepared statement
            if(mysqli_stmt_execute($stmt)){
                // Redirect to login page
                header("location: welcome.php");
            } else{
                echo "Oops! Something went wrong. Please try again later.";
                echo "ERROR: Could not able to execute $sql. " . mysqli_error($link);
            }

            // Close statement
            mysqli_stmt_close($stmt);
        }
    }

// Close connection
mysqli_close($link);

}
?>
 
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Reset Password</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>
        body{ font: 14px sans-serif; }
        .wrapper{ width: 360px; padding: 20px; }
    </style>
</head>
<body>
    <div class="wrapper">
        <h2>Create your license plate</h2>
        <p>Please fill out this form to insert your license plate into our database, with additional information.</p>
        <form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>" method="post"> 
            <div class="form-group">
                <label>License plate</label>
                <input type="license" name="license" class="form-control <?php echo (!empty($license_err)) ? 'is-invalid' : ''; ?>" value="<?php echo $license; ?>">
                <span class="invalid-feedback"><?php echo $license_err; ?></span>
            </div>
            <div class="form-group">
                <label>Achternaam</label>
                <input type="text" name="achternaam" class="form-control <?php echo (!empty($achternaam_err)) ? 'is-invalid' : ''; ?>" value="<?php echo $achternaam; ?>">
                <span class="invalid-feedback"><?php echo $achternaam_err; ?></span>
            </div>
            <div class="form-group">
                <label>Voornaam</label>
                <input type="text" name="voornaam" class="form-control <?php echo (!empty($voornaam_err)) ? 'is-invalid' : ''; ?>" value="<?php echo $voornaam; ?>">
                <span class="invalid-feedback"><?php echo $voornaam_err; ?></span>
            </div>
            <div class="form-group">
                <label>Straat + huisnummer</label>
                <input type="text" name="straat_huis" class="form-control <?php echo (!empty($straat_huis_err)) ? 'is-invalid' : ''; ?>" value="<?php echo $straat_huis; ?>">
                <span class="invalid-feedback"><?php echo $straat_huis_err; ?></span>
            </div>
            <div class="form-group">
                <label>Gemeente + postcode</label>
                <input type="text" name="gemeente_post" class="form-control <?php echo (!empty($gemeente_post_err)) ? 'is-invalid' : ''; ?>" value="<?php echo $gemeente_post; ?>">
                <span class="invalid-feedback"><?php echo $gemeente_post_err; ?></span>
            </div>
            <div class="form-group">
                <label>Bankrekeningnummer</label>
                <input type="text" name="bank" class="form-control <?php echo (!empty($bank_err)) ? 'is-invalid' : ''; ?>" value="<?php echo $bank; ?>">
                <span class="invalid-feedback"><?php echo $bank_err; ?></span>
            </div>
                <input type="submit" class="btn btn-primary" value="Submit">
                <a class="btn btn-link ml-2" href="welcome.php">Cancel</a>
            </div>
        </form>
    </div>    
</body>
</html>