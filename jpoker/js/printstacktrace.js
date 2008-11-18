//
// Domain Public by Eric Wendelin http://eriwen.com/ (2008)
//                  Luke Smith http://lucassmith.name/ (2008)
//                  Loic Dachary <loic@dachary.org> (2008)
//                  Johan Euphrosine <proppy@aminche.com> (2008)
//
// Information and discussions
// http://jspoker.pokersource.info/skin/test-printstacktrace.html
// http://eriwen.com/javascript/js-stack-trace/
// http://pastie.org/253058
// http://browsershots.org/http://jspoker.pokersource.info/skin/test-printstacktrace.html
//

//
// guessFunctionNameFromLines comes from firebug
//
// Software License Agreement (BSD License)
//
// Copyright (c) 2007, Parakey Inc.
// All rights reserved.
//
// Redistribution and use of this software in source and binary forms, with or without modification,
// are permitted provided that the following conditions are met:
//
// * Redistributions of source code must retain the above
//   copyright notice, this list of conditions and the
//   following disclaimer.
//
// * Redistributions in binary form must reproduce the above
//   copyright notice, this list of conditions and the
//   following disclaimer in the documentation and/or other
//   materials provided with the distribution.
//
// * Neither the name of Parakey Inc. nor the names of its
//   contributors may be used to endorse or promote products
//   derived from this software without specific prior
//   written permission of Parakey Inc.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR
// IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
// FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
// CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
// DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
// DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
// IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
// OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


function printStackTrace(options) {
    if (options && options.guess) {
	var p = new printStackTrace.implementation();
	var result = p.run();
	return p.guessFunctions(result);
    }
    return (new printStackTrace.implementation()).run();
}

printStackTrace.implementation = function() {};

printStackTrace.implementation.prototype = {
    run: function() {
        mode = this.mode();
        if(mode != 'other') {
            try {(0)();} catch (e) {
                return this[mode](e);
            }
        } else {
            return this.other(arguments.callee);
        }
    },

    mode: function() {
        var mode;
        try {(0)();} catch (e) {
            mode = e.stack ? 'firefox' : window.opera ? 'opera' : 'other';
        }
        return mode;
    },
    
    firefox: function(e) {
        return e.stack.replace(/^.*?\n/,'').
        replace(/(?:\n@:0)?\s+$/m,'').
        replace(/^\(/gm,'{anonymous}(').
        split("\n");
    },

    opera: function(e) {
        var lines = e.message.split("\n"),
        ANON = '{anonymous}',
        lineRE = /Line\s+(\d+).*?script\s+(http\S+)(?:.*?in\s+function\s+(\S+))?/i,
        i,j,len;

        for (i=4,j=0,len=lines.length; i<len; i+=2) {
            if (lineRE.test(lines[i])) {
                lines[j++] = (RegExp.$3 ?
                              RegExp.$3 + '()@' + RegExp.$2 + RegExp.$1 :
                              ANON + '()@' + RegExp.$2 + ':' + RegExp.$1) +
                    ' -- ' + lines[i+1].replace(/^\s+/,'');
            }
        }

        lines.splice(j,lines.length-j);
        return lines;
    },

    other: function(curr) {
        var ANON = "{anonymous}",
        fnRE  = /function\s*([\w\-$]+)?\s*\(/i,
        stack = [],j=0,
        fn,args;

	var index = 1;
	var values = {};
        var replacer = function(key, value) {
            if(typeof this[key] == 'function') {
                return 'function';
            } else {
		if(values[value]) {
		    return '#' + values[values];
		} else {
		    values[value] = index++;
		}
                return value;
            }
        };

        while (curr) {
            fn    = fnRE.test(curr.toString()) ? RegExp.$1 || ANON : ANON;
            args  = Array.prototype.slice.call(curr['arguments']);
            stack[j++] = fn + '(' + JSON.stringify(args, replacer) + ')';
            curr = curr.caller;
        }

        return stack;
    },
    
    sourceCache : {},

    ajax : function(url) {
	return $.ajax({
		url: url,
		async: false
	    }).responseText;	
    },

    getSource : function(url) {
	var self = this;
	if (!(url in self.sourceCache)) {
	    self.sourceCache[url] = self.ajax(url).split("\n");
	}
	return self.sourceCache[url];
    },

    guessFunctions : function(stack) {
	for (var i = 0; i < stack.length; ++i) {
	    var reStack = /{anonymous}\(.*\)@(.*):(\d+)/;
	    var frame = stack[i];
	    var m = reStack.exec(frame);
	    if (m) {
		var file = m[1];
		var lineno = m[2];
		if (file && lineno) {
		    var functionName = this.guessFunctionName(file, lineno);
		    stack[i] = frame.replace('{anonymous}', functionName);
		}
	    }
	}
	return stack;
    },

    guessFunctionName : function(url, lineNo)
    {
	var source = this.getSource(url);
	return this.guessFunctionNameFromLines(lineNo, source);
    },

    guessFunctionNameFromLines : function(lineNo, source) {
	var reFunctionArgNames = /function ([^(]*)\(([^)]*)\)/;
	var reGuessFunction = /['"]?([0-9A-Za-z_]+)['"]?\s*[:=]\s*(function|eval|new Function)/;
	// Walk backwards from the first line in the function until we find the line which
	// matches the pattern above, which is the function definition
	var line = "";
	var maxLines = 10;
	for (var i = 0; i < maxLines; ++i)
	    {
		line = source[lineNo-i] + line;
		if (line !== undefined)
		    {
			var m = reGuessFunction.exec(line);
			if (m) {
			    return m[1];
			} else {
			    m = reFunctionArgNames.exec(line);
			} if (m && m[1]) {
			    return m[1];
			}
		    }
	    }
	return "(?)";
    }
};
