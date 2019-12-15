$ = function(sel) { return  document.querySelector(sel) };

// Stub out the websockify Util library.
Util = {}
if (DOOMRL_DEBUG) {
  Util.Debug = console.log;
  Util.Info = console.log;
} else {
  Util.Debug = function() {};
  Util.Info = function() {};
}
Util.Warn = console.log;
Util.Error = console.log;

function createTerminal() {
  var term = new Terminal();
  var terminalContainer = $('#terminal-div');

  term.open(terminalContainer);
  term.resize(80, 26);

  return term;
}

function setMusicVolume(value) {
  document.getElementById('music').volume = value/100.0;
}

function focusTTY() {
  document.getElementById('terminal-div').firstChild.focus();
}

function centerTTY() {
  console.log("Centering terminal");
  var position = $('#position').value;
  var terminalContainer = $('#terminal-div');
  var rows = $(".xterm-rows");
  rows.style.left = Math.max(0,Math.floor((terminalContainer.offsetWidth - rows.offsetWidth)*position)) + "px";
}

function connected(telnet, tty) {
  console.log('Connected!')
  if (DOOMRL_COMMAND) {
    // Wait 250ms for initial negotiation with the server to complete.
    setTimeout(function() { telnet.sendStr(DOOMRL_COMMAND) }, 250);
  }
}

function disconnected(telnet, tty) {
  console.log('Disconnected!')
  // Clear screen and display an error message.
  tty.write("\x1B[2J<<Connection Lost>>")
}

console.log(DOOMRL_HOST)
var telnet = Telnet(createTerminal(), connected, disconnected);
telnet.connect(DOOMRL_HOST, DOOMRL_WS_PORT, true /* use ssl */)

window.addEventListener('resize', function() {
  setTimeout(centerTTY, 100);
})
setTimeout(centerTTY, 100);
