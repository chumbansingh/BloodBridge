/*about*/
// Wait for full DOM load
document.addEventListener('DOMContentLoaded', function () {
  // Smooth scroll for nav links
  const navLinks = document.querySelectorAll('.nav-links a');

  navLinks.forEach(link => {
    link.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href');
      if (targetId.startsWith('#')) {
        e.preventDefault();
        document.querySelector(targetId).scrollIntoView({ behavior: 'smooth' });
      }
    });
  });

  // Highlight active nav link
  const currentPath = window.location.pathname;
  navLinks.forEach(link => {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
    }
  });

  // Fade-in animation for team section
  const teamMembers = document.querySelectorAll('.team-member');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  }, {
    threshold: 0.2
  });

  teamMembers.forEach(member => {
    observer.observe(member);
  });

  // Eligibility checker (Future scope idea)

  const eligibility = localStorage.getItem('lastDonationDate');
  if (eligibility) {
    const lastDonation = new Date(eligibility);
    const today = new Date();
    const diffDays = Math.floor((today - lastDonation) / (1000 * 60 * 60 * 24));
    if (diffDays < 90) {
      alert("You are currently not eligible to donate. Wait a few more days.");
    }
  }

});
/*3photos*/
document.addEventListener('DOMContentLoaded', () => {
  const cards = document.querySelectorAll('.card');

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('show');
        observer.unobserve(entry.target); // trigger only once
      }
    });
  }, {
    threshold: 0.2
  });

  cards.forEach(card => {
    observer.observe(card);
  });
});
// --- Donor Page Script ---

function showDetails(donor) {
  document.getElementById("modalName").textContent = donor.name;
  document.getElementById("modalEmail").textContent = donor.email || "N/A";
  document.getElementById("modalPhone").textContent = donor.phone;
  document.getElementById("modalBlood").textContent = donor.blood_type;
  document.getElementById("modalAddress").textContent = donor.address;
  document.getElementById("modalTimes").textContent = donor.times_donated;
  document.getElementById("modal").style.display = "flex";
}

function closeModal() {
  document.getElementById("modal").style.display = "none";
}
function filterDonors() {
  const type = document.getElementById("bloodFilter").value.toLowerCase();
  const cards = document.querySelectorAll(".donors-card");
  cards.forEach(card => {
    const blood = card.innerText.toLowerCase();
    card.style.display = blood.includes(type) ? "block" : "none";
  });
}

function searchDonors() {
  const search = document.getElementById("searchInput").value.toLowerCase();
  const cards = document.querySelectorAll(".donors-card");
  cards.forEach(card => {
    const name = card.innerText.toLowerCase();
    card.style.display = name.includes(search) ? "block" : "none";
  });
}
  
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    hamburger.addEventListener('click', () => {
      navLinks.classList.toggle('active');
    });

  document.addEventListener("DOMContentLoaded", function () {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          observer.unobserve(entry.target); // Run once
        }
      });
    });

    const animatedElements = document.querySelectorAll('.scroll-animate');
    animatedElements.forEach(el => observer.observe(el));
  });
  
//training my signup/in form
function validateForm() {
  const name = document.getElementById("username").value.trim();
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();
  const phone = document.getElementById("phone").value.trim();
  const errorMsg = document.getElementById("error-message");

  // ✅ 1. Name validation (only letters & spaces)
  const nameRegex = /^[A-Za-z\s]+$/;
  if (!nameRegex.test(name)) {
    errorMsg.textContent = "Name can only contain alphabets and spaces.";
    return false;
  }

  // ✅ 2. Email validation
const emailRegex = /^[a-zA-Z0-9._%+-]+@gmail\.com$/;
  if (!emailRegex.test(email)) {
    errorMsg.textContent = "Enter a valid email (example@gmail.com).";
    return false;
  }

  // ✅ 3. Password validation (min 8 chars, 1 uppercase, 1 special, 1 digit)
  const passwordRegex = /^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$/;
  if (!passwordRegex.test(password)) {
    errorMsg.textContent = "Password must be 8+ chars, include 1 uppercase, 1 number, and 1 special character.";
    return false;
  }

  // ✅ 4. Phone validation (10 digits only)
  const phoneRegex = /^[0-9]{10}$/;
  if (!phoneRegex.test(phone)) {
    errorMsg.textContent = "Phone number must be exactly 10 digits.";
    return false;
  }

  // ✅ All good
  errorMsg.textContent = "";
  return true;
}

function validateLogin() {
  const email = document.getElementById("login-email").value.trim();
  const password = document.getElementById("login-password").value.trim();
  const errorMsg = document.getElementById("login-error");

  // ✅ 1. Validate email format
  const emailRegex = /^[a-zA-Z0-9._%+-]+@gmail\.com$/;
  if (!emailRegex.test(email)) {
    errorMsg.textContent = "Enter a valid email (example@gmail.com).";
    return false;
  }

  // ✅ 2. Validate password format (same rule as signup)
  const passwordRegex = /^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$/;
  if (!passwordRegex.test(password)) {
    errorMsg.textContent = "Password must have 8+ chars, 1 uppercase, 1 number, and 1 special character.";
    return false;
  }

  // ✅ All good
  errorMsg.textContent = "";
  return true;
}
    // --- Modal handling ---
    function showDetails(donor) {
      document.getElementById("modal").style.display = "flex";
      document.getElementById("modalName").textContent = donor.name;
      document.getElementById("modalEmail").textContent = donor.email;
      document.getElementById("modalPhone").textContent = donor.phone;
      document.getElementById("modalBlood").textContent = donor.blood_type;
      document.getElementById("modalAddress").textContent = donor.address;
      document.getElementById("modalTimes").textContent = donor.times_donated || 0;

      // Set form action dynamically
      const form = document.getElementById("requestForm");
      form.action = `/request_blood/${donor.user_id}`;
    }

    function closeModal() {
      document.getElementById("modal").style.display = "none";
    }

    window.onclick = function(event) {
      if (event.target === document.getElementById("modal")) {
        closeModal();
      }
    };