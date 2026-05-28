<script>
(function() {
  'use strict';

  /* ============================
     Reading Progress Bar
     ============================ */
  const progressBar = document.createElement('div');
  progressBar.id = 'reading-progress';
  progressBar.style.width = '0%';
  document.body.prepend(progressBar);

  function updateProgress() {
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const pct = docHeight > 0 ? Math.min((scrollTop / docHeight) * 100, 100) : 0;
    progressBar.style.width = pct + '%';
  }

  /* ============================
     Floating Glow Orbs
     ============================ */
  function createOrbs() {
    if (window.innerWidth < 768) return;
    const colors = ['var(--accent)', 'var(--accent-2)'];
    colors.forEach(function(color, i) {
      const orb = document.createElement('div');
      orb.className = 'glow-orb';
      orb.style.cssText = [
        'width:' + (220 + i * 60) + 'px',
        'height:' + (220 + i * 60) + 'px',
        'background:' + color,
        'top:' + (15 + i * 30) + '%',
        'left:' + (10 + i * 55) + '%',
        'animation-delay:' + (i * -7) + 's'
      ].join(';');
      document.body.appendChild(orb);
    });
  }

  /* ============================
     Scroll-triggered navbar glass
     ============================ */
  function updateNavGlass() {
    const scrollY = window.scrollY;
    if (scrollY > 30) {
      document.documentElement.classList.add('nav-scrolled');
    } else {
      document.documentElement.classList.remove('nav-scrolled');
    }
  }

  /* ============================
     Scroll Reveal (Intersection Observer)
     ============================ */
  function initScrollReveal() {
    var observerOptions = { threshold: 0.12, rootMargin: '0px 0px -40px 0px' };

    var observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, observerOptions);

    document.querySelectorAll('.reveal, .reveal-left, .reveal-right, .reveal-stagger').forEach(function(el) {
      observer.observe(el);
    });

    // Auto-wrap: add reveal classes to key page elements that don't have them
    var containers = document.querySelectorAll('#quarto-document-content .page');
    containers.forEach(function(page) {
      // Cards in themes grid
      page.querySelectorAll('.themes-grid .card').forEach(function(card) {
        card.classList.add('reveal');
      });

      // Pub entries
      page.querySelectorAll('.pub-entry').forEach(function(entry) {
        entry.classList.add('reveal');
      });

      // CV sections
      page.querySelectorAll('.cv-section').forEach(function(section) {
        section.classList.add('reveal');
      });

      // Headings (h2, h3 under .page)
      page.querySelectorAll('h2, h3').forEach(function(heading) {
        if (!heading.closest('.card') && !heading.closest('.cv-section')) {
          heading.classList.add('reveal');
        }
      });

      // Contact cards
      page.querySelectorAll(':scope > .card').forEach(function(card) {
        card.classList.add('reveal-left');
      });

      // Social links container
      page.querySelectorAll('.social-links').forEach(function(links) {
        links.classList.add('reveal');
      });

      // Horizontal rules
      page.querySelectorAll('hr').forEach(function(hr) {
        hr.classList.add('reveal');
      });
    });
  }

  /* ============================
     Card Tilt Effect
     ============================ */
  function initCardTilt() {
    document.addEventListener('mousemove', function(e) {
      var cards = document.querySelectorAll('.card:hover');
      cards.forEach(function(card) {
        var rect = card.getBoundingClientRect();
        var x = e.clientX - rect.left;
        var y = e.clientY - rect.top;
        var centerX = rect.width / 2;
        var centerY = rect.height / 2;
        var rotateX = (y - centerY) / centerY * -3;
        var rotateY = (x - centerX) / centerX * 3;
        card.style.transform = 'perspective(800px) rotateX(' + rotateX + 'deg) rotateY(' + rotateY + 'deg)';
      });
    });

    document.addEventListener('mouseleave', resetAllCards);
    document.addEventListener('mouseout', function(e) {
      var cards = document.querySelectorAll('.card');
      cards.forEach(function(card) {
        if (e.target === card || card.contains(e.target)) {
          return; // still inside a card, handled separately below
        }
      });
    });

    // Reset on card mouseleave
    document.querySelectorAll('.card').forEach(function(card) {
      card.addEventListener('mouseleave', function() {
        card.style.transform = 'perspective(800px) rotateX(0deg) rotateY(0deg)';
      });
    });
  }

  function resetAllCards() {
    document.querySelectorAll('.card').forEach(function(card) {
      card.style.transform = 'perspective(800px) rotateX(0deg) rotateY(0deg)';
    });
  }

  /* ============================
     Theme Toggle Animation
     ============================ */
  function enhanceThemeToggle() {
    var btn = document.getElementById('theme-toggle');
    if (!btn) return;
    btn.addEventListener('click', function() {
      btn.style.transform = 'rotate(180deg) scale(0.8)';
      setTimeout(function() {
        btn.style.transition = 'transform 400ms cubic-bezier(0.4, 0, 0.2, 1)';
        btn.style.transform = '';
      }, 150);
    });
    btn.style.transition = 'transform 400ms cubic-bezier(0.4, 0, 0.2, 1)';
  }

  /* ============================
     Parallax subtle scroll effect on orbs
     ============================ */
  function initOrbParallax() {
    var orbs = document.querySelectorAll('.glow-orb');
    if (orbs.length === 0) return;
    window.addEventListener('scroll', function() {
      var scrollY = window.scrollY;
      orbs.forEach(function(orb, i) {
        var speed = 0.03 + i * 0.02;
        orb.style.transform = 'translateY(' + (scrollY * speed) + 'px)';
      });
    }, { passive: true });
  }

  /* ============================
     Link hover sparkle for external links
     ============================ */
  function initLinkSparkle() {
    // Already handled by CSS underline animation
    // We skip overriding inline link styles
  }

  /* ============================
     Boot Sequence
     ============================ */
  function boot() {
    createOrbs();
    initScrollReveal();
    initCardTilt();
    initOrbParallax();
    enhanceThemeToggle();

    // Main scroll handler
    var ticking = false;
    window.addEventListener('scroll', function() {
      if (!ticking) {
        requestAnimationFrame(function() {
          updateProgress();
          updateNavGlass();
          ticking = false;
        });
        ticking = true;
      }
    }, { passive: true });

    // Initial calls
    updateProgress();
    updateNavGlass();
  }

  // Run after DOM is ready; Quarto loads via include-after-body
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
</script>