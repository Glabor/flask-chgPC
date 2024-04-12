const socket = io(`${window.location.href}`);
console.log(`${window.location.href}`)

var start = Date.now();

function testMess() {
    socket.emit("wifi", "")
}

socket.on('response', function (msg) {
    console.log('Received message:', msg);
});

socket.on('wifi', function (msg) {
    var response = JSON.parse(msg);
    console.log('Received message:', response);

    var keys = Object.keys(response);
    console.log(keys);

    for (var i = 0; i < keys.length; i++) {
        var key = keys[i];
        console.log(key);
        if (key === "wifi") {
            document.getElementById("wifiState").innerHTML = `${response[key] ? 'on' : 'off'} `;
            const wifiState = response[key];
            console.log(`wifi: ${wifiState} `);
            document.getElementById("wifiButton").dataset.status = wifiState;
            document.getElementById("wifiButton").innerHTML = `Turn ${wifiState ? 'off' : 'on'} `
            if (wifiState) {
                const ctrlField = document.getElementById("ctrlField");
                ctrlField.style.visibility = "visible";
                const ctrlBtn = document.getElementById("ctrlBtn");
                ctrlBtn.setAttribute("href", `http://${response["ip"]}`);

            } else {
                const ctrlField = document.getElementById("ctrlField");
                ctrlField.style.visibility = "hidden";
            }
        }
    }
});

socket.on("last", function (msg) {
    // const last = Date.now();
    console.log(`last ${Math.round(parseFloat(msg) * 100)}`)
    document.getElementById("liveField").innerHTML = Math.round(parseFloat(msg) * 100) / 100;
})

function setLast() {
    // document.getElementById("liveField").innerHTML = Date.now() - start;
    socket.emit("last", "")
}

window.addEventListener('load', function () {
    console.log("It's loaded!")
    const ctrlField = document.getElementById("ctrlField");
    ctrlField.style.visibility = "hidden";
    setInterval(setLast, 50);
})

