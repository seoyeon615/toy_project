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




document.addEventListener("DOMContentLoaded", () => {
    const customSelectWrap = document.getElementById("grade-custom-select");
    const selectTrigger = customSelectWrap.querySelector(".custom-select-trigger");
    const selectedText = customSelectWrap.querySelector(".selected-text");
    const options = customSelectWrap.querySelectorAll(".custom-option");
    const hiddenInput = document.getElementById("grade-input");

    // 1. 드롭다운 트리거 클릭 시 드롭다운 열기/닫기
    selectTrigger.addEventListener("click", () => {
        customSelectWrap.classList.toggle("open");
    });

    // 2. 각 옵션 항목 클릭 시 동작
    options.forEach(option => {
        option.addEventListener("click", () => {
            selectedText.textContent = option.textContent; // 눈에 보이는 텍스트 업데이트
            hiddenInput.value = option.getAttribute("data-value"); // 숨겨진 input의 value 업데이트 - for 폼 제출
            customSelectWrap.classList.remove("open"); // 선택 후 드롭다운 창 닫기
        });
    });

    // 3. 드롭다운 바깥 영역(빈 화면)을 클릭 시 자동으로 닫히게
    document.addEventListener("click", (e) => {
        if (!customSelectWrap.contains(e.target)) {
            customSelectWrap.classList.remove("open");
        }
    });
});