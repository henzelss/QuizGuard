document.addEventListener('DOMContentLoaded', () => {
    // Get the countdown overlay element
    const countdownOverlay = document.getElementById('countdown-overlay');
  
    // Set the countdown time in seconds
    const countdownTime = 5;
    
    // Start the countdown
    let countdown = countdownTime;
    const countdownInterval = setInterval(() => {
      countdown--;
      if (countdown === 0) {
        // Clear the countdown interval, hide the overlay and show the message div
        clearInterval(countdownInterval);
        countdownOverlay.style.display = 'none';
        const showDiv = document.querySelector('.show-div');
        if (showDiv) {
          showDiv.style.display = 'block';
        }
      }
      // Update the countdown number on the overlay
      document.getElementById('countdown-number').textContent = countdown;
    }, 1000);
  });