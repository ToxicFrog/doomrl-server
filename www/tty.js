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

function osc666handler(params) {
  console.log("osc 666:");
  params.map(console.log);
}

// OSC handling
/*
                case 666:
                  // DoomRL-specific extension
                  // OSC 666 ; 1 ; Snd ST
                  // Load and play the sound /sfx/<Snd>.flac
                  let [cmd,arg] = this.params[1].split(";");
                  if (cmd == "1") {
                    // console.log("PLAY SOUND:", arg);
                    let audio = document.createElement("audio");
                    audio.controls = false;
                    audio.style.display = "none";
                    audio.volume = document.getElementById("vol:sfx").value / 100.0;
                    audio.src = "/static/sfx/" + arg + ".flac";
                    audio.play();
                  } else if (cmd == "2") {
                    console.log("PLAY MUSIC", arg);
                    let music = document.getElementById("music");
                    if (arg) {
                      music.src = "/static/music/" + arg;
                      music.play();
                    } else {
                      music.pause();
                    }
                  }
                  break;
*/

const TTY_OPTIONS = {
  altClickMovesCursor: false,
  bellStyle: 'none',
  cursorBlink: 'false',
  cursorStyle: 'block',
  // drawBoldTextInBrightColors: false,
  theme: {
    foreground: '#FFFFFF',
    background: '#000000',
    black: '#000000',
    // brightBlack: '#000000',
  },
  windowOptions: {
    getWinSizeChars: true,
    getScreenSizeChars: true,
  },
};

function createTerminal() {
  var term = new Terminal(TTY_OPTIONS);
  var terminalContainer = $('#terminal-div');

  term.parser.registerOscHandler(666, osc666handler);

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
  var screen = $("div.xterm-screen");
  screen.style.left = Math.max(0,Math.floor((terminalContainer.offsetWidth - screen.offsetWidth)*position)) + "px";
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
