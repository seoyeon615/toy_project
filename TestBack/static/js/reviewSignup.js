const usernameInput = document.getElementById("username");
const nameInput = document.getElementById("name");
const passwordInput = document.getElementById("password");
const confirmPasswordInput = document.getElementById("confirm-password");
const signupBtn = document.getElementById("signup-btn");

function checkSignupConditions() {
    const isAllFilled = 
        usernameInput.value !== "" && 
        nameInput.value !== "" && 
        passwordInput.value !== "" && 
        confirmPasswordInput.value !== "";

    const isPasswordLongEnough = 
        passwordInput.value.length >= 8 && 
        confirmPasswordInput.value.length >= 8;

    if (isAllFilled && isPasswordLongEnough) {
        signupBtn.classList.add("active");
    } else {
        signupBtn.classList.remove("active");
    }
}

usernameInput.addEventListener("input", checkSignupConditions);
nameInput.addEventListener("input", checkSignupConditions);
passwordInput.addEventListener("input", checkSignupConditions);
confirmPasswordInput.addEventListener("input", checkSignupConditions);