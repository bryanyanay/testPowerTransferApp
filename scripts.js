
chargeBtn = document.querySelector("#transfer-form button")
chargingImg = document.querySelector("#charging-img")

function toggleCharging(e) {
    console.log("hello")

    if (chargingImg.classList.contains("on")) {
        e.target.textContent = "Start";
    } else {
        e.target.textContent = "Stop";
    }
    chargingImg.classList.toggle("on");
}

chargeBtn.addEventListener("click", toggleCharging);