// document.addEventListener('DOMContentLoaded', () => {
//     console.log("board.js 가 성공적으로 로드되었습니다.");

//     // 최신순, 추천순 탭 전환
//     const tabButtons = document.querySelectorAll('.tab-btn');

//     tabButtons.forEach(button => {
//         button.addEventListener('click', () => {
//             tabButtons.forEach(btn => btn.classList.remove('active'));
//             button.classList.add('active');
            
//             const filterType = button.getAttribute('data-filter');
//             console.log(`선택된 필터 탭: ${filterType}`);
//         });
//     });

//     const pageNumbers = document.querySelectorAll('.page-num');

//     pageNumbers.forEach(page => {
//         page.addEventListener('click', () => {
//             pageNumbers.forEach(p => p.classList.remove('active'));
//             page.classList.add('active');
//             console.log(`현재 페이지: ${page.innerText}`);
//         });
//     });
// });

document.addEventListener('DOMContentLoaded', () => {
    console.log("board.js 가 성공적으로 로드되었습니다.");

    // 최신순, 추천순 탭 전환
    const tabButtons = document.querySelectorAll('.tab-btn');

    /* ==========================================================
       ✨ 디폴트 설정 추가: 페이지 로드 시 '최신순' 버튼을 찾아 active 적용
       ========================================================== */
    // data-filter 속성이 'latest'인 버튼을 찾거나, 없으면 첫 번째 버튼을 기본으로 잡습니다.
    const defaultTab = document.querySelector('.tab-btn[data-filter="latest"]') || tabButtons[0];
    if (defaultTab) {
        defaultTab.classList.add('active');
    }

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            tabButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');

            const filterType = button.getAttribute('data-filter');
            console.log(`선택된 필터 탭: ${filterType}`);
        });
    });

    // 페이지네이션 번호 클릭 이벤트
    const pageNumbers = document.querySelectorAll('.page-num');

    pageNumbers.forEach(page => {
        page.addEventListener('click', () => {
            pageNumbers.forEach(p => p.classList.remove('active'));
            page.classList.add('active');
            console.log(`현재 페이지: ${page.innerText}`);
        });
    });
});