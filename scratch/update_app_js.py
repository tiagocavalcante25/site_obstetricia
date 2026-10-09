# -*- coding: utf-8 -*-
import os

js_path = r"c:\Users\Admin\Downloads\INTERNATO GO\site_obstetricia\assets\js\app.js"

with open(js_path, "r", encoding="utf-8") as f:
    js_content = f.read()

# Replace toggleDidacticMode to sync mobile toggle if present
old_didactic = """function toggleDidacticMode() {
  const isEnabled = document.getElementById('didactic-toggle').checked;
  const balloons = document.querySelectorAll('.analogy-balloon');
  
  balloons.forEach(el => {
    if (isEnabled) {
      el.classList.remove('opacity-40', 'grayscale');
      el.classList.add('ring-2', 'ring-amber-400', 'shadow-lg');
    } else {
      el.classList.remove('ring-2', 'ring-amber-400', 'shadow-lg');
      el.classList.add('opacity-40', 'grayscale');
    }
  });
}"""

new_didactic = """function toggleDidacticMode(source) {
  const desktopToggle = document.getElementById('didactic-toggle');
  const mobileToggle = document.getElementById('didactic-toggle-mobile');
  let isEnabled = true;

  if (source === 'mobile' && mobileToggle) {
    isEnabled = mobileToggle.checked;
    if (desktopToggle) desktopToggle.checked = isEnabled;
  } else if (desktopToggle) {
    isEnabled = desktopToggle.checked;
    if (mobileToggle) mobileToggle.checked = isEnabled;
  }

  const balloons = document.querySelectorAll('.analogy-balloon');
  balloons.forEach(el => {
    if (isEnabled) {
      el.classList.remove('opacity-40', 'grayscale');
      el.classList.add('ring-2', 'ring-amber-400', 'shadow-lg');
    } else {
      el.classList.remove('ring-2', 'ring-amber-400', 'shadow-lg');
      el.classList.add('opacity-40', 'grayscale');
    }
  });

  try {
    localStorage.setItem('didactic-mode', isEnabled ? 'true' : 'false');
  } catch (e) {}
}"""

if old_didactic in js_content:
    js_content = js_content.replace(old_didactic, new_didactic)
    print("Replaced toggleDidacticMode with synchronized version.")

# Replace toggleDarkMode and end of file
old_dark = """function toggleDarkMode() {
  const isDark = document.documentElement.classList.toggle('dark');
  const icon = document.getElementById('theme-icon');
  if (icon) {
    icon.className = isDark ? 'fa-solid fa-sun' : 'fa-solid fa-moon';
  }
}"""

new_mobile_and_dark = """function toggleDarkMode() {
  const isDark = document.documentElement.classList.toggle('dark');
  const icon = document.getElementById('theme-icon');
  const iconMobile = document.getElementById('theme-icon-mobile');
  const iconClass = isDark ? 'fa-solid fa-sun' : 'fa-solid fa-moon';
  
  if (icon) icon.className = iconClass;
  if (iconMobile) iconMobile.className = iconClass;

  try {
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
  } catch (e) {}
}

// --- 12. MOBILE NAVIGATION DRAWER & SCROLL UTILITIES ---
function toggleMobileMenu() {
  const drawer = document.getElementById('mobile-nav-drawer');
  const backdrop = document.getElementById('mobile-nav-backdrop');
  if (!drawer || !backdrop) return;

  const isOpen = drawer.classList.contains('drawer-open');
  if (isOpen) {
    closeMobileMenu();
  } else {
    drawer.classList.remove('drawer-closed');
    drawer.classList.add('drawer-open');
    backdrop.classList.remove('hidden');
    requestAnimationFrame(() => {
      backdrop.classList.remove('opacity-0');
    });
    document.body.style.overflow = 'hidden';
  }
}

function closeMobileMenu() {
  const drawer = document.getElementById('mobile-nav-drawer');
  const backdrop = document.getElementById('mobile-nav-backdrop');
  if (!drawer || !backdrop) return;

  drawer.classList.remove('drawer-open');
  drawer.classList.add('drawer-closed');
  backdrop.classList.add('opacity-0');
  setTimeout(() => {
    backdrop.classList.add('hidden');
    document.body.style.overflow = '';
  }, 300);
}

function scrollToTop() {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  });
}
"""

if old_dark in js_content:
    js_content = js_content.replace(old_dark, new_mobile_and_dark)
    print("Replaced toggleDarkMode and appended mobile navigation handlers.")

# Enhance DOMContentLoaded to check localStorage for dark mode and didactic mode, and attach back-to-top scroll listener
init_search_str = "document.addEventListener('DOMContentLoaded', () => {"
new_init_extra = """document.addEventListener('DOMContentLoaded', () => {
  // Restore user preferences
  try {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
      document.documentElement.classList.add('dark');
      const icon = document.getElementById('theme-icon');
      const iconMobile = document.getElementById('theme-icon-mobile');
      if (icon) icon.className = 'fa-solid fa-sun';
      if (iconMobile) iconMobile.className = 'fa-solid fa-sun';
    } else if (savedTheme === 'light') {
      document.documentElement.classList.remove('dark');
      const icon = document.getElementById('theme-icon');
      const iconMobile = document.getElementById('theme-icon-mobile');
      if (icon) icon.className = 'fa-solid fa-moon';
      if (iconMobile) iconMobile.className = 'fa-solid fa-moon';
    }

    const savedDidactic = localStorage.getItem('didactic-mode');
    if (savedDidactic !== null) {
      const isD = (savedDidactic === 'true');
      const dt = document.getElementById('didactic-toggle');
      const mt = document.getElementById('didactic-toggle-mobile');
      if (dt) dt.checked = isD;
      if (mt) mt.checked = isD;
      toggleDidacticMode();
    }
  } catch (e) {}
"""

if init_search_str in js_content and 'savedTheme' not in js_content:
    js_content = js_content.replace(init_search_str, new_init_extra, 1)
    print("Enhanced DOMContentLoaded with preference loading.")

# Enhance the scroll listener to update back-to-top button
old_scroll_block = """  // Scroll Progress Bar
  window.addEventListener('scroll', () => {
    const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrolled = (winScroll / height) * 100;
    const progressBar = document.getElementById('reading-progress');
    if (progressBar) {
      progressBar.style.width = scrolled + '%';
    }
  });"""

new_scroll_block = """  // Scroll Progress Bar & Floating Action Button
  window.addEventListener('scroll', () => {
    const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrolled = height > 0 ? (winScroll / height) * 100 : 0;
    const progressBar = document.getElementById('reading-progress');
    if (progressBar) {
      progressBar.style.width = scrolled + '%';
    }

    const fabBtn = document.getElementById('back-to-top-btn');
    if (fabBtn) {
      if (winScroll > 350) {
        fabBtn.classList.remove('fab-hidden');
        fabBtn.classList.add('fab-visible');
      } else {
        fabBtn.classList.remove('fab-visible');
        fabBtn.classList.add('fab-hidden');
      }
    }
  });"""

if old_scroll_block in js_content:
    js_content = js_content.replace(old_scroll_block, new_scroll_block)
    print("Enhanced scroll listener with Back to Top FAB.")

with open(js_path, "w", encoding="utf-8") as f:
    f.write(js_content)

print("Updated assets/js/app.js successfully!")
