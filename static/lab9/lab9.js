function openGift(id) {
    fetch(OPEN_URL, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({id: id})
    })
    .then(r => r.json())
    .then(d => {
        if (d.error) {
            alert(d.error);
            return;
        }

        document.getElementById("modal-image").src = "/static/lab9/" + d.image;
        document.getElementById("modal-text").innerText = d.message;
        document.getElementById("modal").style.display = "flex";

        document.getElementById("opened").innerText = d.opened;
        document.getElementById("remaining").innerText = d.remaining;

        document.querySelectorAll(".gift")[id].classList.add("opened");
    });
}

function closeModal() {
    document.getElementById("modal").style.display = "none";
}

function resetGifts() {
    fetch(RESET_URL, {method: "POST"})
        .then(r => r.json())
        .then(() => location.reload());
}
