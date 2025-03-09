
async function getChannels() {
    const response = await fetch("/get_channels");
    const channels = await response.json();

    const adminChannelSelect = document.getElementById("adminChannel");
    const statusChannelSelect = document.getElementById("statusChannel");
    const announceChannelSelect = document.getElementById("announceChannel");

    function createSelectMenu(selectElement, channels) {
        channels.forEach(channel => {
            const option = document.createElement("option");
            option.value = channel.id;
            option.textContent = channel.name;

            selectElement.appendChild(option);
        });
    }

    createSelectMenu(adminChannelSelect, channels);
    createSelectMenu(statusChannelSelect, channels);
    createSelectMenu(announceChannelSelect, channels);
}


document.getElementById("configForm").addEventListener("submit", async function(event) {
    event.preventDefault();
    const broadcaster = document.getElementById("broadcaster").value;
    const channel = document.getElementById("channel").value;

    const response = await fetch("/save_settings", {
        method : "POST",
        headers : {
            "Content-Type" : "application/json"
        },
        body : JSON.stringify({broadcaster, channel})
    });

    if (response.ok) {
        const settingsResponse = document.getElementById("settings_response")
        settingsResponse.textContent = "Settings saved!"
    } else {
        const settings_response = document.getElementById("settings_response")
        settings_response.textContent = "oops, something went wrong!"
    }
});

getChannels();