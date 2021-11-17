var main = function () {
    "use strict";
    var addCommentFromInputBox = function () {
        var $new_comment;
        if ($(".comment-input input").val() !== "") {
            $new_comment = $("<p>").text($(".comment-input input").val());
            $new_comment.hide();

        // post the data
        var formData = {};
        formData.newComment =  $(".comment-input input").val() ;

        var ajax=$.ajax({
            type: "POST",
            data: JSON.stringify(formData),
            contentType: 'application/json;charset=UTF-8',
            dataType: "json",
            url: "ajax_new_comment",
            beforeSend: function() {
                $('#loading').show();
                $('#addCommentButton').hide();
            },
            complete: function(){
                $('#loading').hide();
                $('#addCommentButton').show();
                $(".comment-input input").val("");
            },
            success: function(responseJson){
                $(".comments").append($new_comment);
                $new_comment.fadeIn();
            },
            error: function(response){
                let json = response.responseJSON;
                
               alert('Error: ' + json.message);
            }
        });
        }
    };
    $(".comment-input button").on("click", function (event) {
        addCommentFromInputBox();
    });
    $(".comment-input input").on("keypress", function (event) {
        if (event.keyCode === 13) {
            addCommentFromInputBox();
        }
    });
};
$(document).ready(main);