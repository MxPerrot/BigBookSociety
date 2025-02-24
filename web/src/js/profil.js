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

function addBook() {
    const bookList = document.querySelector('.book-list');
    const bookTitle = prompt('Enter book title:');
    if (bookTitle) {
        const listItem = document.createElement('li');
        listItem.textContent = bookTitle;
        const removeButton = document.createElement('button');
        removeButton.textContent = 'Remove';
        removeButton.onclick = () => listItem.remove();
        listItem.appendChild(removeButton);
        bookList.appendChild(listItem);
    }
}