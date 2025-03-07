
async function loadChannels() {
    const response = await fetch("/get_channels");
    const channels = await response.json();
    const channelSelect = document.getElementById("channel");

    channels.forEach(channel => {
        const option = document.createElement("option");
        option.value = channel.id;
        option.textContent = channel.name;
        channelSelect.appendChild(option);
    });
}

document.getElementById("configForm").addEventListener("submit", async function(event) {
    event.preventDefault();
    const broadcaster = document.getElementById("broadcaster").value;
    const channel = document.getElementById("channel").value;

    const response = await fetch("/save_config", {
        method : "POST",
        headers : {
            "Content-Type" : "application/json"
        },
        body : JSON.stringify({broadcaster, channel})
    });

    if (response.ok) {
        alert("Settings saved!");
    } else {
        alert("Failed to save settings! Please try again")
    }
});

loadChannels();