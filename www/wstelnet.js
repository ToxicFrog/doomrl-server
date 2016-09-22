/*
 * WebSockets telnet client
 * Copyright (C) 2011 Joel Martin
 * Licensed under LGPL-3 (see licenses/wstelnet.txt)
 *
 * Telnet protocol:
 *   http://www.networksorcery.com/enp/protocol/telnet.htm
 *   http://www.networksorcery.com/enp/rfc/rfc1091.txt
 *
 * ANSI escape sequeneces:
 *   http://en.wikipedia.org/wiki/ANSI_escape_code
 *   http://ascii-table.com/ansi-escape-sequences-vt-100.php
 *   http://www.termsys.demon.co.uk/vtansi.htm
 *   http://invisible-island.net/xterm/ctlseqs/ctlseqs.html
 *
 * ASCII codes:
 *   http://en.wikipedia.org/wiki/ASCII
 *   http://www.hobbyprojects.com/ascii-table/ascii-table.html
 *
 * Other web consoles:
 *   http://stackoverflow.com/questions/244750/ajax-console-window-with-ansi-vt100-support
 */




function Telnet(tty, connect_callback, disconnect_callback) {

var that = {},  // Public API interface
    termType = "VT220",
    ws, sQ = [];


Array.prototype.pushStr = function (str) {
    var n = str.length;
    for (var i=0; i < n; i++) {
        this.push(str.charCodeAt(i));
    }
}

function do_send() {
    if (sQ.length > 0) {
        Util.Debug("Sending " + sQ);
        ws.send(sQ);
        sQ = [];
    }
}

function do_recv() {
    //console.log(">> do_recv");
    var arr = ws.rQshiftBytes(ws.rQlen()), str = "",
        chr, cmd, code, value;

    //Util.Debug("Received array '" + arr + "'");
    while (arr.length > 0) {
        chr = arr.shift();
        switch (chr) {
        case 255:   // IAC
            cmd = chr;
            code = arr.shift();
            value = arr.shift();
            switch (code) {
            case 254: // DONT
                Util.Debug("Got Cmd DONT '" + value + "', ignoring");
                break;
            case 253: // DO
                Util.Debug("Got Cmd DO '" + value + "'");
                if (value === 24) {
                    // Terminal type
                    Util.Info("Send WILL '" + value + "' (TERM-TYPE)");
                    sQ.push(255, 251, value);
                } else {
                    // Refuse other DO requests with a WONT
                    Util.Debug("Send WONT '" + value + "'");
                    sQ.push(255, 252, value);
                }
                break;
            case 252: // WONT
                Util.Debug("Got Cmd WONT '" + value + "', ignoring");
                break;
            case 251: // WILL
                Util.Debug("Got Cmd WILL '" + value + "'");
                if (value === 1) {
                    // Server will echo, turn off local echo
                    // FIXME: disable echoing in the terminal
                    // tty.noecho()
                    // Affirm echo with DO
                    Util.Info("Send Cmd DO '" + value + "' (echo)");
                    sQ.push(255, 253, value);
                } else {
                    // Reject other WILL offers with a DONT
                    Util.Debug("Send Cmd DONT '" + value + "'");
                    sQ.push(255, 254, value);
                }
                break;
            case 250: // SB (subnegotiation)
                if (value === 24) {
                    Util.Info("Got IAC SB TERM-TYPE SEND(1) IAC SE");
                    // TERM-TYPE subnegotiation
                    if (arr[0] === 1 &&
                        arr[1] === 255 &&
                        arr[2] === 240) {
                        arr.shift(); arr.shift(); arr.shift();
                        Util.Info("Send IAC SB TERM-TYPE IS(0) '" +
                                  termType + "' IAC SE");
                        sQ.push(255, 250, 24, 0);
                        sQ.pushStr(termType);
                        sQ.push(255, 240);
                    } else {
                        Util.Info("Invalid subnegotiation received" + arr);
                    }
                } else {
                    Util.Info("Ignoring SB " + value);
                }
                break;
            default:
                Util.Info("Got Cmd " + cmd + " " + value + ", ignoring"); }
            continue;
        case 242:   // Data Mark (Synch)
            cmd = chr;
            code = arr.shift();
            value = arr.shift();
            Util.Info("Ignoring Data Mark (Synch)");
            break;
        default:   // everything else
            str += String.fromCharCode(chr);
        }
    }

    if (sQ) {
        do_send();
    }

    if (str) {
        tty.write(str);
    }

    //console.log("<< do_recv");
}



that.connect = function(host, port, encrypt) {
    var host = host,
        port = port,
        scheme = "ws://", uri;

    Util.Debug(">> connect");
    if ((!host) || (!port)) {
        console.log("must set host and port");
        return;
    }

    if (ws) {
        ws.close();
    }

    if (encrypt) {
        scheme = "wss://";
    }
    uri = scheme + host + ":" + port;
    Util.Info("connecting to " + uri);

    ws.open(uri);

    Util.Debug("<< connect");
}

that.disconnect = function() {
    Util.Debug(">> disconnect");
    if (ws) {
        ws.close();
    }
    //vt100.curs_set(true, false);

    disconnect_callback(this, tty);
    Util.Debug("<< disconnect");
}


function constructor() {
    /* Initialize Websock object */
    ws = new Websock();

    ws.on('message', do_recv);
    ws.on('open', function(e) {
        Util.Info(">> WebSockets.onopen");
        //vt100.curs_set(true, true);
        connect_callback(this, tty);
        Util.Info("<< WebSockets.onopen");
    });
    ws.on('close', function(e) {
        Util.Info(">> WebSockets.onclose");
        that.disconnect();
        Util.Info("<< WebSockets.onclose");
    });
    ws.on('error', function(e) {
        Util.Info(">> WebSockets.onerror");
        that.disconnect();
        Util.Info("<< WebSockets.onerror");
    });

    // Set handler for sending characters
    tty.on('data', function(data) {
      sQ.pushStr(data);
      do_send();
    })

    return that;
}

return constructor(); // Return the public API interface

} // End of Telnet()
