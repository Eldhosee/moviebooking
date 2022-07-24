// function onLoaderFunc(booked_seats)
// {
//   $.each( booked_seats, function( index, value ){
//     $("'#"+ value+"'").prop("disabled", true);
//     console.log(value);
// });
// //   $("#B1").prop("disabled", true);
//   // $(".seatStructure *").prop("disabled", true);
//   // $(".displayerBoxes *").prop("disabled", true);
// }
function takeData()
{
  if  ( $("#Numseats").val().length == 0 )
  {
  alert("Please Enter your Name and Number of Seats");
  }
  else
  {
    $(".inputForm *").prop("disabled", true);
    $(".seatStructure *").prop("disabled", false);
    document.getElementById("notification").innerHTML = "<b style='margin-bottom:0px;background:yellow;'>Please Select your Seats NOW!</b>";
  }
}


function updateTextArea() { 
    
  if ($("input:checked").length == ($("#Numseats").val()))
    {
      $(".seatStructure *").prop("disabled", true);
      
     
     var allNumberVals = [];
     var allSeatsVals = [];
  
     //Storing in Array
     allNumberVals.push($("#Numseats").val());
     $('#seatsBlock :checked').each(function() {
       allSeatsVals.push($(this).val());
     });
    
     //Displaying 
     $('#NumberDisplay').val(allNumberVals);
     $('#seatsDisplay').val(allSeatsVals);
    }
  else
    {
      
      var allNumberVals = [];
      var allSeatsVals = [];
      //Storing in Array
     allNumberVals.push($("#Numseats").val());
     $('#seatsBlock :checked').each(function() {
       allSeatsVals.push($(this).val());
     });
    
     //Displaying 
     $('#NumberDisplay').val(allNumberVals);
     $('#seatsDisplay').val(allSeatsVals);
     $('#input').val(allSeatsVals);
     
    }
  }


function myFunction() {
  alert($("input:checked").length);
}




// $(":checkbox").click(function() {
//   if ($("input:checked").length == ($("#Numseats").val())) {
//     $(":checkbox").prop('disabled', true);
//     $(':checked').prop('disabled', false);
//   }
//   else
//     {
//       $(":checkbox").prop('disabled', false);
//     }
// });


