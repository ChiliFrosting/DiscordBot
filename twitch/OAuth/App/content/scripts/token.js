function getToken() {
    const hash = window.location.hash.substring(1);
    const params = new URLSearchParams(hash);
    return params.get("access_token");
}


async function sendToken(token) {
    const serverURL = "http://localhost:3000/token";

    try {
        const response = await fetch (serverURL, {
            method : "POST", 
            headers : {"Content-Type" : "application/json"},
            body : JSON.stringify({token})
        });

        if (response.ok) {
            console.log("Token sent");
        }
        else {
            console.log("Failed to send token");
        }
    }
    catch (error) {
        console.error("Error while sending token: ", error);
    }
}


window.onload = function() {
    const token = getToken();
    const tokenResponse = document.getElementById("token-response");

    if (token) {
        tokenResponse.textContent = "Token Renewed!"
        sendToken(token);
    }
    else {
        tokenResponse.textContent = "Token acquisition failed"
    }
}