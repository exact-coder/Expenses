const searchField = document.querySelector('#searchField');
const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
const paginationContainer = document.querySelector(".pagination-container");
const tbody = document.querySelector(".table-body");

tableOutput.style.display="none"

searchField.addEventListener('keyup', (e) => {

    const searchValue = e.target.value;

    if (searchValue.trim().length > 0) {
        paginationContainer.style.display="none";
        tbody.innerHTML="";
        fetch("/search-expenses", {
            body: JSON.stringify({ searchText: searchValue}),
            method: "POST",
        }).then((res) => res.json())
        .then((data) => {
            console.log(data);
            appTable.style.display="none";
            tableOutput.style.display="block";
            if (data.length === 0) {
                tableOutput.innerHTML="No Result Found"
            }else{

                data.forEach(item => {
                    tbody.innerHTML += `
                    <tr>
                        <td>${item.amount}</td>
                        <td>${item.category}</td>
                        <td>${item.description}</td>
                        <td>${item.date}</td>
                        <td>
                            <a class="btn btn-outline-secondary btn-sm" href="expense-edit/${item.id}">Edit</a>
                            <a class="btn btn-outline-danger btn-sm fw-bolder" href="delete-expense/${item.id}">X</a>
                            </td>
                    </tr>
                
                    `;
                });
                
            }
        });
    }else{
        appTable.style.display="block";
        paginationContainer.style.display="block";
        tableOutput.style.display="none";
    }
});