$ = function(sel) { return  document.querySelector(sel) };

// Stub out the websockify Util library.
Util = {}
Util.Debug = function() {};
Util.Info = function() {};
Util.Warn = console.log;
Util.Error = console.log;

function createTerminal() {
  var term = new Terminal();
  var terminalContainer = $('#terminal-div');

  term.open(terminalContainer);
  term.resize(80, 26);

  return term;
}

function centerTerminal() {
  var terminalContainer = $('#terminal-div');
  var rows = $(".xterm-rows");
  console.log("Container width: ", terminalContainer.offsetWidth)
  console.log("TTY width: ", rows.getBoundingClientRect().width)
  rows.style.left = Math.floor((terminalContainer.offsetWidth - rows.offsetWidth)/2) + "px";
}

function connected() {
  console.log('Connected!');
//  centerTerminal();
}

function disconnected(telnet, tty) {
  console.log('Disconnected!')
  // Clear screen and display an error message.
  tty.write("\x1B[2J<<Connection Lost>>")
}

console.log(DOOMRL_HOST)
var telnet = Telnet(createTerminal(), connected, disconnected);
telnet.connect(DOOMRL_HOST, DOOMRL_WS_PORT, false)
setTimeout(centerTerminal, 100)
