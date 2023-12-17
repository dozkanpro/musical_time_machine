const itemsPerPage = 10;
const songTable = document.getElementById('songTable');
const pagination = document.getElementById('pagination');
const songRows = songTable.getElementsByTagName('tr');
let currentPage = 1;

function showPage(page) {
    const startIndex = (page - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;

    for (let i = 0; i < songRows.length; i++) {
        if (i >= startIndex && i < endIndex) {
            songRows[i].style.display = '';
        } else {
            songRows[i].style.display = 'none';
        }
    }
}

function updatePaginationButtons() {
    pagination.innerHTML = '';
    const numPages = Math.ceil(songRows.length / itemsPerPage);
    for (let i = 1; i <= numPages; i++) {
        const li = document.createElement('li');
        const link = document.createElement('a');
        link.href = '#';
        link.textContent = i;
        li.appendChild(link);
        pagination.appendChild(li);

        link.addEventListener('click', function() {
            currentPage = i;
            showPage(currentPage);
        });
    }
}

showPage(currentPage);
updatePaginationButtons();
