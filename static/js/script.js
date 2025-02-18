document.addEventListener("DOMContentLoaded", function () {
    const buttonContainer = document.querySelector(".button-container");
    let hideTimeout;

    // ฟังก์ชันแสดงแถบปุ่ม
    function showButtons() {
        clearTimeout(hideTimeout);
        buttonContainer.style.opacity = "1";
    }

    // ฟังก์ชันซ่อนแถบปุ่มหลังจาก 5 วินาที
    function hideButtons() {
        hideTimeout = setTimeout(() => {
            buttonContainer.style.opacity = "0";
        }, 5000);
    }

    // เมื่อเมาส์เข้าไป → แสดงแถบปุ่ม
    buttonContainer.addEventListener("mouseenter", showButtons);

    // เมื่อเมาส์ออก → เริ่มนับถอยหลัง 5 วินาทีเพื่อนซ่อน
    buttonContainer.addEventListener("mouseleave", hideButtons);

    // ซ่อนแถบปุ่มหลังจาก 5 วินาทีแรกของการโหลดหน้าเว็บ
    setTimeout(() => {
        buttonContainer.style.opacity = "0";
    }, 5000);
});
