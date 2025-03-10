
async function getRoles() {
    const response = await fetch("/get_roles");
    const roles = await response.json();

    console.log(roles)

    const adminRole = document.getElementById("adminRole");
    const verifiedRole = document.getElementById("verifiedRole");

    function createRoleSelect(selectElement, roles) {
        roles.forEach(role => {
            const option = document.createElement("option");
            option.textContent = role.name;

            selectElement.appendChild(option);
        });
    }

    createRoleSelect(adminRole, roles);
    createRoleSelect(verifiedRole, roles);

}


getRoles();