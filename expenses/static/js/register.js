
const usernameField = document.getElementById('usernameField');
const feedBackArea = document.querySelector(".invalid-feedback");


usernameField.addEventListener('keyup',(e) => {
    const usernameVal = e.target.value;
    usernameField.classList.remove("is-invalid");
    feedBackArea.style.display="none";
    if(usernameVal.length > 2){
        fetch("/authentication/validate-username", {
            body: JSON.stringify({username: usernameVal}),
            method: "POST",
        }).then((res) => res.json())
        .then((data) => {
            if(data.username_error) {
                usernameField.classList.add("is-invalid");
                feedBackArea.style.display="block";
                feedBackArea.innerHTML = `<p class="ms-4">${data.username_error}</p>`

            }
            /* if(data.username_valid){
                usernameField.classList.remove("is-invalid");
                feedBackArea.style.display="block";
                feedBackArea.innerHTML = `<p class="ms-4 text-success">Valid Username</p>`
            } */
        })
    }else{
        usernameField.classList.add("is-invalid");
        feedBackArea.style.display="block";
        feedBackArea.innerHTML = `<p class="ms-4">username can't be less than 3 </p>`
    }
});