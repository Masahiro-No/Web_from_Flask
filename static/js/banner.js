let slideIndex = 1;
let slideTimer;

function showSlides(n, isManual = false) {
  let i;
  let slides = document.getElementsByClassName("mySlides");
  let dots = document.getElementsByClassName("dot");

  if (n > slides.length) { slideIndex = 1; }
  if (n < 1) { slideIndex = slides.length; }

  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }

  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }

  slides[slideIndex - 1].style.display = "block";
  dots[slideIndex - 1].className += " active";

  // รีเซ็ตตัวจับเวลาเมื่อผู้ใช้กดปุ่มเอง
  if (isManual) {
    clearTimeout(slideTimer);
    slideTimer = setTimeout(() => showSlides(slideIndex + 1), 5000);
  }
}

// ฟังก์ชันเลื่อนอัตโนมัติ
function autoSlides() {
  showSlides(slideIndex += 1);
  slideTimer = setTimeout(autoSlides, 5000);
}

// ปุ่มเปลี่ยนสไลด์
function plusSlides(n) {
  showSlides(slideIndex += n, true);
}

// เปลี่ยนสไลด์ตามจุดที่กด
function currentSlide(n) {
  showSlides(slideIndex = n, true);
}

// เริ่มแสดงผล
showSlides(slideIndex);
slideTimer = setTimeout(autoSlides, 5000);
