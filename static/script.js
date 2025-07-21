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
  // Example use-case: show a message if user donated < 3 months ago
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
<!--  Mobile Nav Toggle Script -->
  
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

