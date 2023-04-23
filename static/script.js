/*document.getElementById("run-script").addEventListener("click", function() {
  fetch("/runscript").then(function(response) {
    return response.text();
  }).then(function(text) {
    console.log(text);
  });
});
*/

var runBtn = document.getElementById('run-btn');
runBtn.addEventListener('click', runScript);

function runScript() {
  console.log('Button clicked'); // add this line
  fetch('/run_script')
  .then(function(response) {
      console.log('Script executed'); // add this line
  });
}
