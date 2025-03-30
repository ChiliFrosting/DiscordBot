
async function getPing() {
    const response = await fetch("/ping");
    const data = await response.json();
    const ping = data.ping;
    
    document.getElementById("ping-value").textContent = ping;
}

getPing();
