
const usernameField = document.getElementById('usernameField');
const emailField = document.getElementById('emailField');
const usernameFeedBackArea = document.querySelector(".username-invalid-feedback");
const emailFeedBackArea = document.querySelector(".email-invalid-feedback");
const usernameSuccessOutput = document.querySelector('.usernameSuccessOutput');


emailField.addEventListener('keyup',(e)=>{
    const emailVal = e.target.value;
    emailField.classList.remove("is-invalid");
    emailFeedBackArea.style.display="none";

    if(emailVal){
        fetch("/authentication/validate-email",{
            body:JSON.stringify({email:emailVal}),
            method:"POST",
        }).then((res) => res.json())
        .then((data) => {
            if(data.email_error){
                emailField.classList.add("is-invalid");
                emailFeedBackArea.style.display="block";
                emailFeedBackArea.innerHTML = `<p class="ms-4">${data.email_error}</p>`
            }
        })
    }
})



usernameField.addEventListener('keyup',(e) => {
    const usernameVal = e.target.value;
    usernameSuccessOutput.style.display="block";
    usernameSuccessOutput.textContent = `Checking ${usernameVal}`
    usernameField.classList.remove("is-invalid");
    usernameFeedBackArea.style.display="none";
    if(usernameVal.length > 2){
        fetch("/authentication/validate-username", {
            body: JSON.stringify({username: usernameVal}),
            method: "POST",
        }).then((res) => res.json())
        .then((data) => {
            if(data.username_error) {
                usernameSuccessOutput.style.display="none";
                usernameField.classList.add("is-invalid");
                usernameFeedBackArea.style.display="block";
                usernameFeedBackArea.innerHTML = `<p class="ms-4">${data.username_error}</p>`

            }
            usernameSuccessOutput.style.display="none";
            /* if(data.username_valid){
                usernameField.classList.remove("is-invalid");
                usernameFeedBackArea.style.display="block";
                usernameFeedBackArea.innerHTML = `<p class="ms-4 text-success">Valid Username</p>`
            } */
        })
    }else{
        usernameField.classList.add("is-invalid");
        usernameFeedBackArea.style.display="block";
        usernameSuccessOutput.style.display="none";
        usernameFeedBackArea.innerHTML = `<p class="ms-4">username can't be less than 3 </p>`
    }
});