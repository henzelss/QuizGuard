function shareText(quizid) {
    // Get the text field
    var copyText = document.getElementById("quizcode" + quizid);
  
    // Select the text field
    copyText.select();
    copyText.setSelectionRange(0, 99999); // For mobile devices
  
     // Copy the text inside the text field
    var codeText= 'Dear User, \nWe would like to remind you that you have an upcoming quiz scheduled on quizguard, \nTo access your quiz, kindly visit quizguard.com \nand enter your quiz code: ' + copyText.value;

    navigator.clipboard.writeText(codeText);
  
    // Alert the copied text
    Swal.fire({
      title: "Code Copied",
      text: "Share this quiz to your students.",
      icon: "success",
      timer: 1000 // time in milliseconds
    });

  }
function copyText(quizid) {

  // Get the text field
  var copyText = document.getElementById("quizcode" + quizid);
  
  // Select the text field
  copyText.select();
  copyText.setSelectionRange(0, 99999); // For mobile devices

   // Copy the text inside the text field
   // var codeText= 'Dear User, \nWe would like to remind you that you have an upcoming quiz scheduled on quizguard, \nTo access your quiz, kindly visit quizguard.com \nand enter your quiz code: ' + copyText.value;

  navigator.clipboard.writeText(copyText.value);

  // Alert the copied text
  Swal.fire({
    title: "Code Copied",
    text: "The quiz code has been copied to your clipboard.",
    icon: "success",
    timer: 1000 // time in milliseconds
  });

}