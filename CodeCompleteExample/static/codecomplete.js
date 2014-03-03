window.onload = function() {

    // choose something random 
    var inputEntity = document.getElementById("codecomplete");
    var debugDom = document.getElementById("debug");
    var possibilities = document.getElementById("possibilities");

    var host = location.host;

    function debug( str ) {
        debugDom.innerHTML += " " + str;
    }

    function ajaxReq( obj ) {
        var xhr = new XMLHttpRequest();
        xhr.open( obj["method"] || 'GET', obj["url"]);
        if (obj["content-type"]) {
            xhr.overrideMimeType(obj["content-type"]);
        }
        if (obj["accept"]) {
            xhr.setRequestHeader('Accept', obj["accept"]);
        }
        // This is a call back
        xhr.onreadystatechange = function(){
            // readystate tells you how the transfer is going
       // 4 is done
            if( xhr.readyState === 4 ){
                // This is the HTTP Code
                if(xhr.status === 200){
                    obj["success"]( xhr.responseText );
           } else {
               alert("There was an error " + xhr.status);
           }
            }
        };
        // finally send it
        xhr.send(obj["body"] || null);
    };
    function jsonReq( obj ) {
        obj["content-type"] = "application/json";
        obj["accept"] = "application/json";
        return ajaxReq( obj );
    }
    function makeReplacer( text ) {
        return function() {
            inputEntity.value = text;
        }
    }
    function checkForUpdate() {
        if (inputEntity.oldValue !== undefined && inputEntity.value === inputEntity.oldValue) {
	    return false;
            // eh nothing is happening
        } else {
            // oh something changed
            inputEntity.oldValue = inputEntity.value;
            if (inputEntity.value !== "") {
                var uri = "http://"+host+"/words/" + encodeURI( inputEntity.value );
                jsonReq( { "url": uri,
                           "success": function(text) {
                               var list = JSON.parse(text);
                               while(possibilities.firstChild) {
                                   possibilities.removeChild( possibilities.firstChild );
                               }
                               for (var i = 0 ; i  < list.length ; i++) {
                                   var span = document.createElement("div");
                                   span.className = "suggestion";
                                   span.myText = list[i];
                                   span.appendChild( new Text( list[i] ) );
                                   span.onclick = makeReplacer( list[i] );
                                   possibilities.appendChild( span );
                               }
                           }
                         }
                       );
               return true;
            }
        }
    }
    inputEntity.onkeyup = function(e) {
        if (e.keyCode === 9 || e.keyCode === 40) {
            inputEntity.value = document.getElementsByClassName("suggestion")[0]["myText"];
            return e.preventDefault();
        }
    }

    function utime() {
	return new Date().getTime();
    }
    var lastTime = utime();
    function oncePerSecond() {
        var time = utime();
        if (time - lastTime >= 1000) {
            if (checkForUpdate()) {
                lastTime = time;
                //debug(time);
            }
        }
    }

    setInterval( function() {
        //checkForUpdate();
        oncePerSecond();
    }, 1000/30.0);
};
