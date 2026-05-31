document.addEventListener("DOMContentLoaded", () => {
    checkEmptyComments();
});

function checkEmptyComments() {
    const comments = document.querySelectorAll(
        ".single-comment, .single-reply",
    );
    const emptyState = document.querySelector(".none");
    const commentCountText = document.querySelector(".comment-count");

    if (!emptyState) return;

    if (commentCountText) {
        commentCountText.innerText = comments.length;
    }

    if (comments.length == 0) {
        emptyState.classList.remove("hidden");
    } else {
        emptyState.classList.add("hidden");
    }
}

let currentDeleteType = null;
let currentDeleteId = null;

// 모달 열기
function openDeleteModal(type, id) {
    currentDeleteType = type;
    currentDeleteId = id;

    const modal = document.querySelector(".delete-modal-wrap");

    if (modal) modal.classList.add("show");
}

// 모달 닫기
function closeDeleteModal() {
    const modal = document.querySelector(".delete-modal-wrap");

    if (modal) modal.classList.remove("show");

    currentDeleteType = null;
    currentDeleteId = null;
}

function confirmDelete() {
    if (!currentDeleteType || !currentDeleteId) return;

    // HTML에서 부여한 form의 id 동적으로 찾음
    const formId = `delete-form-${currentDeleteType}-${currentDeleteId}`;
    const form = document.getElementById(formId);

    // 그 form 찾아 장고로 POST 요청 전송 (실제로 삭제 처리 여기ㅣ서)
    if (form) {
        form.submit();
    }

    // 전송 후 모달 close
    closeDeleteModal();
}

// 대댓글 작성 폼 열고 닫기
function toggleReplyForm(commentId) {
    const form = document.getElementById(`reply-form-${commentId}`);

    // display가 none(숨김)이거나 안 적혀있으면 -> flex로 바꿔서 보여줌
    if (form.style.display === "none" || form.style.display === "") {
        form.style.display = "flex";
    } else {
        form.style.display = "none";
    }
}

// 댓글 & 대댓글 삭제 시 기본 confirm 창 띄우기
document.addEventListener("DOMContentLoaded", function () {
    const deleteForms = document.querySelectorAll(".delete-comment-form");

    deleteForms.forEach((form) => {
        form.addEventListener("submit", function (event) {
            // confirm 창에서 '취소'를 누르면 폼 전송을 막음(preventDefault)
            if (!confirm("정말 삭제하시겠습니까?")) {
                event.preventDefault();
            }
        });
    });
});
