<?php
// echo err for debuging phase
ini_set('display_errors', '1');
ini_set('display_startup_errors', '1');
error_reporting(E_ALL);

// $gencls -> authenticationToken();
// $gencls -> getDataClient();
// $gencls -> returnResult();

/*---------------------------END----------------------------- */
?>
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
  <link rel="stylesheet" href="resource/style.css"> 
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
  <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.bundle.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
<title></title>
</head>
<body>
<div class="container">
      <div class="baner-top">

      </div>
      <h1 class="text-center" style="color: white; margin-top: 20px;">Demo page</h1>
      <div class="form-group">
      <label style="color: white;" for="exampleInputEmail1">Full name coin</label> 
        <input class="form-control" id="input_value_1"  placeholder="Full name"> 
       <small id="emailHelp" class="form-text text-muted"></small> 
  
      <div class="form-group">
        <label style="color: white; text-" for="exampleInputPassword1">Abridgement</label>
        <input class="form-control" id="input_value_2" placeholder="abridgement">
      </div>

      <div class="text-center" style="margin-top: 30px; margin-left:-18%;">
        
        <button style="font-size: 30px;"   type="submit" class="btn btn-primary spinner-button btn btn-primary mb-2" id="btnFetch" >Submit</button>
        <button style="font-size: 30px; margin-left:20px;" onclick="putResult()"  type="submit" class="btn btn-primary spinner-button btn btn-primary mb-2" id="btnShowImg" >Sentiment analysis</button>
      </div>

      <div class="text-center" style="margin-left: 50%;">
      <!-- <h3 class = "rating-title">Rating</h3>  -->
        <fieldset class="rating">
        
            <input type="radio" id="star5" name="rating" value="5" />
            <label for="star5">5 stars</label>
            <input type="radio" id="star4" name="rating" value="4" />
            <label for="star4">4 stars</label>
            <input type="radio" id="star3" name="rating" value="3" />
            <label for="star3">3 stars</label>
            <input type="radio" id="star2" name="rating" value="2" />
            <label for="star2">2 stars</label>
            <input type="radio" id="star1" name="rating" value="1" />
            <label for="star1">1 star</label>
          </fieldset>
      </div>
     
      <br>
        <div class="text-center">
          <span style="font-size: 50px; color: white;" id="result_correct"></span>
        </div>

        <div id="imgShow"  class="text-center" style="display:none;">
          <img class="imgC" src="resource/viewChart.png" alt="">
        </div>
      </div>
</body>
</html>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script>
  var flagShow = 1;
    function putResult(){
      if(flagShow %2 == 0){
        document.getElementById("imgShow").style.display = 'none';
      }
      else if(flagShow%2 == 1){
        document.getElementById("imgShow").style.display = 'block';
      }
      flagShow = flagShow+1;
    }

$(document).ready(function() {
  $("#btnFetch").click(function() {
      // disable button
      $("#btnFetch").prop("disabled", true);
      // add spinner to button
      $("#btnFetch").html(
      '<i class="fa fa-circle-o-notch fa-spin"></i> loading...'
      );

      $("#result_correct").text("")
      var input_value_1 = $('#input_value_1').val();
        var input_value_2 = $('#input_value_2').val();
        console.log(input_value_1); 
        console.log(input_value_2); 
        $.ajax({
            url: 'processResult.php',
            type: 'post',
            data: { "value_1": input_value_1, "value_2": input_value_2},
            success: function(response) { 
                console.log("done");
                console.log(response);
                $('#result_correct').text("Naked point: ".concat(response));
                $("#btnFetch").prop("disabled", false);
                $("#btnFetch").html(
                  'Submit'
                  );
            }
        });


  });
});

</script>


