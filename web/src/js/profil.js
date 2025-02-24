function editProfileName() {
    const nameElement = document.querySelector('.profile-name');
    const newName = prompt('Enter new name:', nameElement.textContent);
    if (newName) {
        nameElement.textContent = newName;
    }
}

function editProfileEmail() {
    const emailElement = document.querySelector('.profile-email');
    const newEmail = prompt('Enter new email:', emailElement.textContent);
    if (newEmail) {
        emailElement.textContent = newEmail;
    }
}

function editProfileDob() {
    const dobElement = document.querySelector('.profile-dob');
    const newDob = prompt('Enter new date of birth:', dobElement.textContent.replace('Date de naissance: ', ''));
    if (newDob) {
        dobElement.textContent = 'Date de naissance: ' + newDob;
    }
}

function editProfileAddress() {
    const addressElement = document.querySelector('.profile-address');
    const newAddress = prompt('Enter new address:', addressElement.textContent.replace('Adresse: ', ''));
    if (newAddress) {
        addressElement.textContent = 'Adresse: ' + newAddress;
    }
}

function changeProfileImage(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const imgElement = document.getElementById('profile-img');
            imgElement.src = e.target.result;
        }
        reader.readAsDataURL(file);
    }
}