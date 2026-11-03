/**
 * CampusGig Intro Wordmark Animation
 * Plays once on initial landing page load
 */
document.addEventListener('DOMContentLoaded', () => {
  const introOverlay = document.getElementById('intro-overlay');
  if (!introOverlay) return;

  // Check if intro has already been shown in this session
  const introShown = sessionStorage.getItem('campusgig_intro_shown');

  if (introShown) {
    introOverlay.style.display = 'none';
  } else {
    // Show animation, then fade out after 1.4 seconds
    setTimeout(() => {
      introOverlay.classList.add('hidden');
      sessionStorage.setItem('campusgig_intro_shown', 'true');
      setTimeout(() => {
        introOverlay.style.display = 'none';
      }, 700);
    }, 1400);
  }
});
