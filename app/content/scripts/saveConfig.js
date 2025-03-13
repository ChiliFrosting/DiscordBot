
document.getElementById("configForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    const broadcaster = document.getElementById("broadcaster").value.trim();
    const announceChannel = document.getElementById("announceChannel").value;
    const verifiedRole = document.getElementById("verifiedRole").value;
    const adminRole = document.getElementById("adminRole").value;
    const adminChannel = document.getElementById("adminChannel").value;
    const statusChannel = document.getElementById("statusChannel").value;

    const response = await fetch("/save_config", {
        method : "POST",
        headers : {
            "Content-Type" : "application/json"
        },
        body : JSON.stringify({
            broadcaster,
            announceChannel,
            verifiedRole,
            adminRole,
            adminChannel,
            statusChannel
        })
    });

    const settingsResponse = document.getElementById("config_response")

    if (response.ok) {
        settingsResponse.textContent = "Settings saved!"

    } else {
        settingsResponse.textContent = "oops, something went wrong!"
    }
});