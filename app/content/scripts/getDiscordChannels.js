
async function getChannels() {
    const response = await fetch("/get_channels");
    const channels = await response.json();

    const adminChannelSelect = document.getElementById("adminChannel");
    const statusChannelSelect = document.getElementById("statusChannel");
    const announceChannelSelect = document.getElementById("announceChannel");

    function createChannelSelect(selectElement, channels) {
        channels.forEach(channel => {
            const option = document.createElement("option");
            option.value = channel.id;
            option.textContent = channel.name;

            selectElement.appendChild(option);
        });
    }

    createChannelSelect(adminChannelSelect, channels);
    createChannelSelect(statusChannelSelect, channels);
    createChannelSelect(announceChannelSelect, channels);
    
}


getChannels();