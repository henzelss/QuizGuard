// $(document).ready(function(){
//     var total_questions = $(".divs div").length-1; // Get the total number of questions
//     var current_question = 1; // Initialize the current question index
    
//     $(".divs div").each(function(e) {
//         if (e != 0)
//             $(this).hide();
//     });

//     $("#next").click(function(){
//         if ($(".divs div:visible").next().length != 0) {
//             $(".divs div:visible").next().show().prev().hide();
//             current_question++;
//         } else {
//             $(".divs div:visible").hide();
//             $(".divs div:first").show();
//             current_question = 1;
//         }
        
//         // Hide the "next" button if the current question is the last one
//         if (current_question == total_questions) {
//             $("#next").hide();
//         }
        
//         // Show the "prev" button if it was hidden
//         $("#prev").show();
        
//         return false;
//     });

//     $("#prev").click(function(){
//         if ($(".divs div:visible").prev().length != 0) {
//             $(".divs div:visible").prev().show().next().hide();
//             current_question--;
//         } else {
//             $(".divs div:visible").hide();
//             $(".divs div:last").show();
//             current_question = total_questions;
//         }
        
//         // Hide the "prev" button if the current question is the first one
//         if (current_question == 1) {
//             $("#prev").hide();
//         }
        
//         // Show the "next" button if it was hidden
//         $("#next").show();
        
//         return false;
//     });
// });

$(document).ready(function(){
    var total_questions = $(".question").length; // Get the total number of questions
    var current_question = 1; // Initialize the current question index
    
    $(".question").each(function(e) {
        if (e != 0)
            $(this).hide();
    });

    $("#next").click(function(){
        if ($(".question:visible").next().length != 0) {
            $(".question:visible").next().show().prev().hide();
            current_question++;
        } else {
            $(".question:visible").hide();
            $(".question:first").show();
            current_question = 1;
        }
        
        // Hide the "next" button if the current question is the last one
        if (current_question == total_questions) {
            $("#next").hide();
        }
        
        // Show the "prev" button if it was hidden
        $("#prev").show();
        
        return false;
    });

    $("#prev").click(function(){
        if ($(".question:visible").prev().length != 0) {
            $(".question:visible").prev().show().next().hide();
            current_question--;
        } else {
            $(".question:visible").hide();
            $(".question:last").show();
            current_question = total_questions;
        }
        
        // Hide the "prev" button if the current question is the first one
        if (current_question == 1) {
            $("#prev").hide();
        }
        
        // Show the "next" button if it was hidden
        $("#next").show();
        
        return false;
    });
});