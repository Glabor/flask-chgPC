const socket = io(`${window.location.href}`); //start socket io conection with the server

var selectedSyst = null;
var sysVariables = null;

function toggleWifi() {
    socket.emit("wifi", selectedSyst);
    sysVariables.forEach(el => {
        if (el["id"] == selectedSyst) {
            el["wifi"] = !el["wifi"];
        }
    });
}

function selectSys(e) {
    console.log(e.target.dataset.id);
    selectedSyst = e.target.dataset.id;
    const newID = document.getElementById("systID");
    newID.textContent = `Selected system #${selectedSyst}`;
}

function updateSelect() {
    // console.log(sysVariables);
    sysVariables.forEach(el => {
        if (el["id"] == selectedSyst && Number.isInteger(el["id"])) {
            const wifiState = el["wifi"];
            console.log(`wifi: ${wifiState} `);
            document.getElementById("wifiState").innerHTML = `${wifiState ? 'on' : 'off'} `;
            document.getElementById("wifiButton").dataset.status = wifiState;
            document.getElementById("wifiButton").innerHTML = `Turn ${wifiState ? 'off' : 'on'} `
            if (wifiState) {
                //activate control button if wifi is active
                const ctrlField = document.getElementById("ctrlField");
                ctrlField.style.visibility = "visible";
                const ctrlBtn = document.getElementById("ctrlBtn");
                ctrlBtn.setAttribute("href", `http://${el["ip"]}`);
            } else {
                const ctrlField = document.getElementById("ctrlField");
                ctrlField.style.visibility = "hidden";
            }
        }
    });
}

socket.on('wifi', function (msg) {
    /*handle messages from "wifi" channel
    update page depending on the content of the message    
    */
    //get keys from the json in the message 
    var response = JSON.parse(msg);
    console.log('Received message:', response);
});

function timeConverter(UNIX_timestamp) {
    var a = new Date(UNIX_timestamp * 1000);
    var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    var year = a.getFullYear();
    var month = months[a.getMonth()];
    var date = a.getDate();
    var hour = a.getHours();
    var min = a.getMinutes();
    var sec = a.getSeconds();
    var time = date + ' ' + month + ' ' + year + ' ' + hour + ':' + min + ':' + sec;
    return time;
}

socket.on("list", function (msg) {
    /*handle message in "list" channel
    update list 
    */
    var response = JSON.parse(msg);
    sysVariables = response;

    const sysList = document.getElementById("sysList");
    sysList.innerHTML = "";
    response.forEach(el => {
        if (el.hasOwnProperty("id")) {
            var li = document.createElement("li");
            li.dataset.id = el["id"];
            var t = document.createTextNode(`system #${el["id"]}, last heard ${el["last"] == 0 ? "never" : timeConverter(el["last"])}, wifi ${el["wifi"]}`);
            li.appendChild(t);
            li.addEventListener("click", selectSys);
            sysList.appendChild(li);
        }
    });
})

socket.on("last", function (msg) {
    /*handle message in "last" channel
    update time since last message 
    */
    document.getElementById("liveField").innerHTML = (Math.round(parseFloat(msg) * 10) / 10).toFixed(1);
})


function setLast() {
    socket.emit("last", selectedSyst);
    updateSelect();
}

function setList() {
    socket.emit("list", "")
}

window.addEventListener('load', function () {
    console.log("It's loaded!")
    const ctrlField = document.getElementById("ctrlField");
    ctrlField.style.visibility = "hidden";
    setInterval(setLast, 100);
    setInterval(setList, 5000);
    setList();
})

