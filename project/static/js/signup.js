// bind the form submit event to our function
$("#signupForm").bind('submit', function(e) {
    // prevent page refresh
    e.preventDefault();
    // post the data
    var formData = {};
    formData.email    =  $('input[name="email"]').val();
    formData.name     =  $('input[twitter_username="twitter_username"]').val();
    formData.name     =  $('input[name="name"]').val();
    formData.password =  $('input[name="password"]').val();
    
    

    var ajax=$.ajax({
        type: "POST",
        data: JSON.stringify(formData),
        contentType: 'application/json;charset=UTF-8',
        dataType: "json",
        url: "http://127.0.0.1:8000/users/",
        beforeSend: function() {
            $('#loading').show();
            $('#signupButton').hide();
        },
        complete: function(){
            $('#loading').hide();
            $('#signupButton').show();
        },
        success: function(responseJson){

            alert('Success: ' + responseJson.message);
        },
        error: function(response){
           alert('Error: ' + response);
        }
    });
});
