# -*- coding: utf-8 -*-
import os

css_path = r"c:\Users\Admin\Downloads\INTERNATO GO\site_obstetricia\assets\css\custom.css"

with open(css_path, "r", encoding="utf-8") as f:
    content = f.read()

responsive_css = '''
/* ==========================================================================
   RESPONSIVE & MOBILE ENGINE (OPTIMIZED FOR ANDROID, IOS & TABLETS)
   ========================================================================== */

/* 1. Viewport & Safe Area Insets (iPhone Dynamic Island, Notch, Android Gestures) */
html {
  -webkit-text-size-adjust: 100%;
  text-size-adjust: 100%;
  scroll-padding-top: 5rem; /* Prevents sticky header from obscuring anchor jumps */
}

body {
  overflow-x: hidden;
  position: relative;
  width: 100%;
  padding-left: env(safe-area-inset-left, 0px);
  padding-right: env(safe-area-inset-right, 0px);
}

/* 2. Touch Response & Elimination of 300ms iOS Tap Delay */
a, button, input, select, textarea, [role="button"], .cursor-pointer {
  touch-action: manipulation;
  -webkit-tap-highlight-color: transparent;
}

/* 3. iOS Safari Form Auto-Zoom Prevention (Elements < 16px cause zoom) */
@media (max-width: 768px) {
  input[type="text"],
  input[type="number"],
  input[type="date"],
  input[type="time"],
  input[type="email"],
  select,
  textarea {
    font-size: 16px !important;
  }
}

/* 4. Minimum Touch Target Sizing (WCAG 2.5.5) & Handheld Readability */
@media (max-width: 640px) {
  button, 
  .btn,
  .protocol-tab,
  .pw-btn,
  .pump-btn {
    min-height: 42px;
  }

  /* Make checkbox labels easier to tap on phones */
  label {
    min-height: 38px;
    display: flex;
    align-items: center;
  }
  
  /* Readability floor: prevent microscopic text on mobile OLED/Retina screens */
  .text-\\[9px\\],
  .text-\\[10px\\] {
    font-size: 0.72rem !important; /* ~11.5px */
    line-height: 1.15rem !important;
  }

  .text-\\[11px\\] {
    font-size: 0.8rem !important; /* ~12.8px */
    line-height: 1.3rem !important;
  }

  /* Ensure long medical compound words don't overflow */
  h1, h2, h3, h4, h5, .font-bold {
    overflow-wrap: break-word;
    word-break: break-word;
    hyphens: auto;
  }

  /* Compact glass panels padding for mobile */
  .glass-panel {
    padding: 1.15rem !important;
    border-radius: 1.25rem !important;
  }
}

/* 5. Fluid Responsive Tables with Momentum Touch Scroll */
.overflow-x-auto,
.table-responsive {
  -webkit-overflow-scrolling: touch;
  overscroll-behavior-x: contain;
  scrollbar-width: thin;
}

/* Table scroll visual hint on small screens */
@media (max-width: 768px) {
  .overflow-x-auto::after {
    content: '↔ deslize horizontalmente para tabela completa';
    display: block;
    font-size: 10px;
    text-align: right;
    color: #94a3b8;
    padding: 6px 4px 2px 4px;
    font-family: var(--font-mono);
  }
}

/* 6. Mobile Slide-Over Navigation Drawer */
#mobile-nav-drawer {
  transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.3s ease;
}

#mobile-nav-drawer.drawer-open {
  transform: translateX(0);
  opacity: 1;
  pointer-events: auto;
}

#mobile-nav-drawer.drawer-closed {
  transform: translateX(100%);
  opacity: 0;
  pointer-events: none;
}

#mobile-nav-backdrop {
  transition: opacity 0.3s ease;
}

/* 7. Floating Action Button (Voltar ao Topo) */
.fab-back-to-top {
  position: fixed;
  bottom: max(1.25rem, env(safe-area-inset-bottom, 1.25rem));
  right: max(1.25rem, env(safe-area-inset-right, 1.25rem));
  z-index: 45;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.fab-back-to-top.fab-hidden {
  opacity: 0;
  transform: translateY(20px) scale(0.9);
  pointer-events: none;
}

.fab-back-to-top.fab-visible {
  opacity: 1;
  transform: translateY(0) scale(1);
  pointer-events: auto;
}

/* 8. Lightbox Mobile Optimizations */
@media (max-width: 640px) {
  #image-lightbox img {
    max-height: 52vh !important;
  }

  #image-lightbox .p-4 {
    padding: 0.85rem !important;
  }
}

/* 9. Flashcards Mobile Height Flexibility */
@media (max-width: 640px) {
  .perspective-1000 {
    min-height: 22rem;
    height: auto;
  }

  .flashcard-inner {
    min-height: 22rem;
  }

  .flashcard-front,
  .flashcard-back {
    min-height: 22rem;
    overflow-y: auto;
  }
}

/* 10. High-DPI & Dark Mode Contrast Polish */
.dark body {
  background-color: #030712; /* Richer pitch black for OLED battery saving */
}

.dark .text-slate-400 {
  color: #94a3b8; /* Higher contrast on dark mode */
}
'''

if 'RESPONSIVE & MOBILE ENGINE' not in content:
    with open(css_path, "a", encoding="utf-8") as f:
        f.write("\n" + responsive_css + "\n")
    print("Appended responsive engine to custom.css successfully!")
else:
    print("Responsive engine already present in custom.css.")
