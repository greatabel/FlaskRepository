/* If we're being iframed, let the parent know our URL */
/* Kids: don't do this at home! */
parent.postMessage(window.location.toString(), "*");

/* Override window.alert */
var originalAlert = window.alert;
window.alert = function(s) {
  parent.postMessage("success", "*");
  setTimeout(function() { 
    originalAlert("Congratulations, you executed an alert:\n\n" 
      + s + "\n\nYou can now advance to the next level.");
  }, 50);
}

