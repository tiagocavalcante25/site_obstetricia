# -*- coding: utf-8 -*-
import os
import re

base_dir = r"c:\Users\Admin\Downloads\INTERNATO GO\site_obstetricia"
header_file = os.path.join(base_dir, "components", "header.html")
modals_file = os.path.join(base_dir, "components", "modals.html")
m5_file = os.path.join(base_dir, "components", "modulo-5-dmg-preeclampsia.html")
index_file = os.path.join(base_dir, "index.html")

# 1. NEW RESPONSIVE HEADER
new_header_html = '''<!-- NAVIGATION HEADER -->
  <header class="sticky top-0 z-40 glass-header border-b border-slate-200/80 dark:border-slate-800/80 shadow-sm" style="padding-top: env(safe-area-inset-top, 0px);">
    <div class="max-w-7xl mx-auto px-3 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-2 sm:gap-4">
      
      <!-- Brand & Title -->
      <a href="#modulo-1" class="flex items-center gap-2.5 sm:gap-3 group shrink-0">
        <div class="w-9 h-9 sm:w-10 sm:h-10 rounded-xl bg-gradient-to-tr from-teal-600 to-emerald-500 flex items-center justify-center text-white shadow-md shadow-teal-500/20 group-hover:scale-105 transition-transform shrink-0">
          <i class="fa-solid fa-baby text-base sm:text-lg"></i>
        </div>
        <div class="min-w-0">
          <span class="text-[10px] sm:text-xs font-bold uppercase tracking-wider text-teal-600 dark:text-teal-400 block leading-tight truncate">Guia Clínico</span>
          <h1 class="text-base sm:text-lg font-black tracking-tight text-slate-900 dark:text-white leading-none truncate">Obstetrícia & MFM <span class="text-[10px] sm:text-xs px-1.5 sm:px-2 py-0.5 rounded-full bg-teal-500/10 text-teal-600 dark:text-teal-400 font-bold ml-0.5">Parte 1</span></h1>
        </div>
      </a>

      <!-- Quick Nav Links (Large Screens / Landscape Tablets) -->
      <nav class="hidden lg:flex items-center gap-4 xl:gap-6 text-xs xl:text-sm font-semibold text-slate-600 dark:text-slate-300">
        <a href="#modulos-index" class="hover:text-teal-600 dark:hover:text-teal-400 transition-colors">Módulos</a>
        <a href="#calculadoras" class="hover:text-teal-600 dark:hover:text-teal-400 transition-colors">Calculadoras</a>
        <a href="#galeria-imagens" class="hover:text-teal-600 dark:hover:text-teal-400 transition-colors">Imagens Médicas</a>
        <a href="#flashcards-section" class="hover:text-teal-600 dark:hover:text-teal-400 transition-colors">Flashcards 3D</a>
        <a href="#quiz-section" class="hover:text-teal-600 dark:hover:text-teal-400 transition-colors">Simulado USMLE</a>
        <a href="#high-yield-summary" class="hover:text-teal-600 dark:hover:text-teal-400 transition-colors">High-Yield</a>
      </nav>

      <!-- Action Utilities -->
      <div class="flex items-center gap-1.5 sm:gap-2.5 shrink-0">
        <!-- Search Trigger -->
        <button onclick="openSearchModal()" title="Buscar termo (Ctrl+K)" class="p-2 sm:px-3 sm:py-1.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 text-slate-600 dark:text-slate-300 hover:border-teal-500 text-xs font-medium flex items-center gap-1.5 transition-all cursor-pointer">
          <i class="fa-solid fa-magnifying-glass text-teal-500"></i>
          <span class="hidden md:inline">Buscar...</span>
          <kbd class="hidden xl:inline-block px-1.5 py-0.5 rounded bg-slate-100 dark:bg-slate-800 text-[10px] text-slate-400">⌘K</kbd>
        </button>

        <!-- Didactic Mode Toggle (Desktop) -->
        <div class="hidden xl:flex items-center gap-2 px-3 py-1 rounded-xl bg-amber-500/10 border border-amber-500/20 text-xs font-bold text-amber-700 dark:text-amber-400" title="Ativa ou destaca as analogias simples">
          <label for="didactic-toggle" class="cursor-pointer flex items-center gap-1.5">
            <span>🎈 Modo 5 Anos</span>
            <input type="checkbox" id="didactic-toggle" checked onchange="toggleDidacticMode('desktop')" class="sr-only peer">
            <div class="w-8 h-4 bg-slate-300 peer-focus:outline-none rounded-full peer dark:bg-slate-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-3 after:w-3 after:transition-all peer-checked:bg-amber-500"></div>
          </label>
        </div>

        <!-- Dark Mode Toggle -->
        <button onclick="toggleDarkMode()" title="Alternar tema claro/escuro" class="w-9 h-9 sm:w-10 sm:h-10 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 text-slate-600 dark:text-slate-300 hover:text-teal-500 flex items-center justify-center transition-all cursor-pointer">
          <i id="theme-icon" class="fa-solid fa-moon"></i>
        </button>

        <!-- Print / PDF Export Button -->
        <button onclick="window.print()" title="Exportar ou Imprimir Resumo" class="hidden sm:flex p-2 sm:px-3 sm:py-1.5 rounded-xl bg-teal-600 hover:bg-teal-700 text-white text-xs font-bold items-center gap-1.5 transition-all shadow-md shadow-teal-500/20 cursor-pointer">
          <i class="fa-solid fa-file-pdf"></i>
          <span class="hidden md:inline">PDF</span>
        </button>

        <!-- Mobile Menu Button (Hamburger) - Visible on screens < lg -->
        <button id="mobile-menu-btn" onclick="toggleMobileMenu()" title="Abrir Menu de Navegação" class="lg:hidden w-9 h-9 sm:w-10 sm:h-10 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 text-slate-700 dark:text-slate-200 hover:border-teal-500 flex items-center justify-center transition-all cursor-pointer" aria-label="Abrir Menu">
          <i class="fa-solid fa-bars text-sm"></i>
        </button>
      </div>
    </div>
  </header>'''

# 2. NEW MODALS, LIGHTBOX, DRAWER & FLOATING ACTION BUTTON
new_modals_html = '''<!-- ==================== MODALS & LIGHTBOXES ==================== -->

  <!-- MOBILE NAVIGATION DRAWER (Slide-over for Smartphones & Tablets) -->
  <div id="mobile-nav-backdrop" onclick="closeMobileMenu()" class="fixed inset-0 bg-slate-950/60 backdrop-blur-sm z-50 hidden opacity-0 transition-opacity duration-300"></div>

  <aside id="mobile-nav-drawer" class="drawer-closed fixed top-0 right-0 bottom-0 w-80 max-w-[85vw] bg-white/95 dark:bg-slate-900/95 backdrop-blur-2xl z-50 border-l border-slate-200 dark:border-slate-800 shadow-2xl flex flex-col justify-between overflow-y-auto" style="padding-top: env(safe-area-inset-top, 1rem); padding-bottom: env(safe-area-inset-bottom, 1rem);">
    
    <!-- Drawer Header -->
    <div class="p-4 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between">
      <div class="flex items-center gap-2.5">
        <div class="w-8 h-8 rounded-lg bg-teal-600 text-white flex items-center justify-center font-bold text-sm shadow-sm">
          <i class="fa-solid fa-compass"></i>
        </div>
        <div>
          <span class="text-xs font-black text-slate-900 dark:text-white block leading-tight">Navegação Rápida</span>
          <span class="text-[10px] text-teal-600 dark:text-teal-400 font-semibold">11 Módulos & Ferramentas</span>
        </div>
      </div>
      <button onclick="closeMobileMenu()" class="w-8 h-8 rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white flex items-center justify-center cursor-pointer transition-colors" aria-label="Fechar menu">
        <i class="fa-solid fa-xmark text-sm"></i>
      </button>
    </div>

    <!-- Drawer Body: Quick Navigation Links -->
    <div class="p-4 space-y-4 flex-1 overflow-y-auto">
      
      <!-- Quick Tools Section -->
      <div>
        <span class="text-[10px] font-black uppercase tracking-wider text-slate-400 dark:text-slate-500 block mb-2">Recursos Principais</span>
        <div class="grid grid-cols-2 gap-1.5 text-xs font-bold">
          <a href="#calculadoras" onclick="closeMobileMenu()" class="p-2.5 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-200 hover:bg-teal-50 dark:hover:bg-slate-700 hover:text-teal-600 flex items-center gap-2 transition-all">
            <i class="fa-solid fa-calculator text-cyan-500"></i> Calculadoras
          </a>
          <a href="#galeria-imagens" onclick="closeMobileMenu()" class="p-2.5 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-200 hover:bg-teal-50 dark:hover:bg-slate-700 hover:text-teal-600 flex items-center gap-2 transition-all">
            <i class="fa-solid fa-image text-emerald-500"></i> Imagens 3D
          </a>
          <a href="#flashcards-section" onclick="closeMobileMenu()" class="p-2.5 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-200 hover:bg-teal-50 dark:hover:bg-slate-700 hover:text-teal-600 flex items-center gap-2 transition-all">
            <i class="fa-solid fa-layer-group text-purple-500"></i> Flashcards
          </a>
          <a href="#quiz-section" onclick="closeMobileMenu()" class="p-2.5 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-200 hover:bg-teal-50 dark:hover:bg-slate-700 hover:text-teal-600 flex items-center gap-2 transition-all">
            <i class="fa-solid fa-graduation-cap text-teal-500"></i> Simulado
          </a>
        </div>
        <a href="#high-yield-summary" onclick="closeMobileMenu()" class="mt-1.5 p-2.5 rounded-xl bg-teal-500/10 border border-teal-500/30 text-teal-800 dark:text-teal-200 hover:bg-teal-500/20 flex items-center justify-between text-xs font-bold transition-all">
          <span class="flex items-center gap-2"><i class="fa-solid fa-bolt text-teal-600"></i> High-Yield Cheat Sheet</span>
          <i class="fa-solid fa-arrow-right text-[10px]"></i>
        </a>
      </div>

      <!-- All 11 Modules List -->
      <div>
        <span class="text-[10px] font-black uppercase tracking-wider text-slate-400 dark:text-slate-500 block mb-2">Módulos Teórico-Clínicos</span>
        <nav class="space-y-1 text-xs font-bold">
          <a href="#modulo-1" onclick="closeMobileMenu()" class="flex items-center gap-2.5 p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-200 transition-all">
            <span class="w-5 h-5 rounded bg-teal-500/10 text-teal-600 flex items-center justify-center font-black text-[10px]">01</span>
            <span>Pré-Natal Baixo Risco & Leopold</span>
          </a>
          <a href="#modulo-2" onclick="closeMobileMenu()" class="flex items-center gap-2.5 p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-200 transition-all">
            <span class="w-5 h-5 rounded bg-teal-500/10 text-teal-600 flex items-center justify-center font-black text-[10px]">02</span>
            <span>Exames Laboratoriais & USG</span>
          </a>
          <a href="#modulo-4" onclick="closeMobileMenu()" class="flex items-center gap-2.5 p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-200 transition-all">
            <span class="w-5 h-5 rounded bg-teal-500/10 text-teal-600 flex items-center justify-center font-black text-[10px]">04</span>
            <span>Imunizações & Vacinas</span>
          </a>
          <a href="#modulo-5" onclick="closeMobileMenu()" class="flex items-center gap-2.5 p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-200 transition-all">
            <span class="w-5 h-5 rounded bg-rose-500/10 text-rose-600 flex items-center justify-center font-black text-[10px]">05</span>
            <span>DMG, Hipertensão & Pré-Eclâmpsia</span>
          </a>
          <a href="#modulo-6" onclick="closeMobileMenu()" class="flex items-center gap-2.5 p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-200 transition-all">
            <span class="w-5 h-5 rounded bg-blue-500/10 text-blue-600 flex items-center justify-center font-black text-[10px]">06</span>
            <span>Vitalidade Fetal, CTG & Doppler</span>
          </a>
          <a href="#modulo-7" onclick="closeMobileMenu()" class="flex items-center gap-2.5 p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-200 transition-all">
            <span class="w-5 h-5 rounded bg-indigo-500/10 text-indigo-600 flex items-center justify-center font-black text-[10px]">07</span>
            <span>Gemelaridade & Síndrome STFF</span>
          </a>
          <a href="#modulo-8" onclick="closeMobileMenu()" class="flex items-center gap-2.5 p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-200 transition-all">
            <span class="w-5 h-5 rounded bg-amber-500/10 text-amber-600 flex items-center justify-center font-black text-[10px]">08</span>
            <span>Isoimunização Rh & Coombs</span>
          </a>
          <a href="#modulo-9" onclick="closeMobileMenu()" class="flex items-center gap-2.5 p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-200 transition-all">
            <span class="w-5 h-5 rounded bg-purple-500/10 text-purple-600 flex items-center justify-center font-black text-[10px]">9+</span>
            <span>Infecções Perinatais & LA</span>
          </a>
        </nav>
      </div>

    </div>

    <!-- Drawer Footer Controls -->
    <div class="p-4 border-t border-slate-200 dark:border-slate-800 space-y-2.5 bg-slate-50/50 dark:bg-slate-900/50">
      <!-- Didactic Mode Switch in Mobile Drawer -->
      <div class="flex items-center justify-between p-2.5 rounded-xl bg-amber-500/10 border border-amber-500/20 text-xs font-bold text-amber-800 dark:text-amber-300">
        <span class="flex items-center gap-1.5">🎈 Modo Didático (5 Anos)</span>
        <label for="didactic-toggle-mobile" class="cursor-pointer relative inline-flex items-center">
          <input type="checkbox" id="didactic-toggle-mobile" checked onchange="toggleDidacticMode('mobile')" class="sr-only peer">
          <div class="w-8 h-4 bg-slate-300 peer-focus:outline-none rounded-full peer dark:bg-slate-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-3 after:w-3 after:transition-all peer-checked:bg-amber-500"></div>
        </label>
      </div>

      <!-- Action Buttons in Mobile Drawer -->
      <div class="grid grid-cols-2 gap-2 text-xs font-bold">
        <button onclick="toggleDarkMode()" class="p-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-200 flex items-center justify-center gap-2 cursor-pointer">
          <i id="theme-icon-mobile" class="fa-solid fa-moon"></i> Tema
        </button>
        <button onclick="window.print()" class="p-2.5 rounded-xl bg-teal-600 text-white flex items-center justify-center gap-2 cursor-pointer shadow-sm">
          <i class="fa-solid fa-file-pdf"></i> PDF
        </button>
      </div>
    </div>
  </aside>

  <!-- 1. IMAGE LIGHTBOX MODAL -->
  <div id="image-lightbox" class="fixed inset-0 z-50 hidden items-center justify-center bg-slate-950/90 backdrop-blur-md p-2 sm:p-4 transition-all">
    <div class="relative max-w-5xl w-full bg-slate-900 border border-slate-800 rounded-2xl sm:rounded-3xl overflow-hidden shadow-2xl flex flex-col max-h-[96vh]">
      <!-- Modal Header -->
      <div class="p-3.5 sm:px-6 border-b border-slate-800 flex items-center justify-between text-white shrink-0">
        <div class="min-w-0 pr-2">
          <span class="text-[10px] font-bold uppercase tracking-widest text-teal-400 block truncate">Visualizador Clínico em Alta Resolução</span>
          <h4 id="lightbox-title" class="text-sm sm:text-lg font-black text-white truncate">Título da Imagem</h4>
        </div>
        <button onclick="closeLightbox()" class="w-9 h-9 sm:w-10 sm:h-10 rounded-full bg-slate-800 text-slate-300 hover:text-white hover:bg-slate-700 flex items-center justify-center transition-all shrink-0 cursor-pointer" aria-label="Fechar visualizador">
          <i class="fa-solid fa-xmark text-base"></i>
        </button>
      </div>

      <!-- Modal Body (Image Container) -->
      <div class="overflow-auto p-2 sm:p-4 flex-1 flex items-center justify-center bg-black/60">
        <img id="lightbox-img" src="" alt="Imagem Médica" class="max-w-full max-h-[52vh] sm:max-h-[70vh] object-contain rounded-xl shadow-lg">
      </div>

      <!-- Modal Footer (Clinical Caption) -->
      <div class="p-3.5 sm:px-6 border-t border-slate-800 bg-slate-900/90 text-xs text-slate-300 max-h-[28vh] overflow-y-auto shrink-0">
        <p id="lightbox-caption" class="leading-relaxed"></p>
      </div>
    </div>
  </div>

  <!-- 2. QUICK SEARCH MODAL (Ctrl+K) -->
  <div id="search-modal" class="fixed inset-0 z-50 hidden items-center justify-center bg-slate-950/80 backdrop-blur-sm p-3 sm:p-4">
    <div class="relative max-w-xl w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-2xl overflow-hidden">
      <!-- Search Input Header -->
      <div class="p-3.5 sm:p-4 border-b border-slate-200 dark:border-slate-800 flex items-center gap-3">
        <i class="fa-solid fa-magnifying-glass text-teal-500 text-base"></i>
        <input type="text" id="search-input" oninput="handleSearch(this.value)" placeholder="Buscar por tema (ex: HELLP, Doppler, Zuspan, GBS, Naegele)..." class="w-full bg-transparent text-slate-900 dark:text-white font-medium text-base sm:text-sm outline-none" style="font-size: 16px;">
        <button onclick="closeSearchModal()" class="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 cursor-pointer">
          <kbd class="text-[10px] px-1.5 py-0.5 rounded bg-slate-100 dark:bg-slate-800">ESC</kbd>
        </button>
      </div>

      <!-- Search Results Box -->
      <div id="search-results" class="p-3 max-h-80 overflow-y-auto space-y-1">
        <p class="text-xs text-slate-400 text-center py-6">Digite um termo para pesquisar instantaneamente no guia...</p>
      </div>
    </div>
  </div>

  <!-- FLOATING ACTION BUTTON (Voltar ao Topo & Mobile Quick Navigation) -->
  <button id="back-to-top-btn" onclick="scrollToTop()" title="Voltar ao início da página" class="fab-back-to-top fab-hidden w-11 h-11 rounded-2xl bg-teal-600 hover:bg-teal-700 active:scale-95 text-white shadow-xl shadow-teal-600/30 flex items-center justify-center transition-all cursor-pointer border border-teal-400/30" aria-label="Voltar ao Topo">
    <i class="fa-solid fa-arrow-up text-sm"></i>
  </button>'''

# Save components/header.html
with open(header_file, "w", encoding="utf-8") as f:
    f.write(new_header_html + "\n")
print("Updated components/header.html successfully!")

# Save components/modals.html
with open(modals_file, "w", encoding="utf-8") as f:
    f.write(new_modals_html + "\n")
print("Updated components/modals.html successfully!")

# 3. Update tight grids in modulo-5-dmg-preeclampsia.html
with open(m5_file, "r", encoding="utf-8") as f:
    m5_content = f.read()

# Fix grid-cols-3 gap-1 font-mono text-[10px]
m5_content = m5_content.replace(
    'class="grid grid-cols-3 gap-1 font-mono text-[10px]"',
    'class="grid grid-cols-1 sm:grid-cols-3 gap-2 font-mono text-xs"'
)

# Fix bag options grid
m5_content = m5_content.replace(
    'class="grid grid-cols-3 gap-1.5"',
    'class="grid grid-cols-1 sm:grid-cols-3 gap-2"'
)

with open(m5_file, "w", encoding="utf-8") as f:
    f.write(m5_content)
print("Updated grid layouts in components/modulo-5-dmg-preeclampsia.html successfully!")

# 4. Update index.html
with open(index_file, "r", encoding="utf-8") as f:
    index_content = f.read()

# Update <head> meta tags
old_meta = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
new_meta = '''<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, viewport-fit=cover">
  <meta name="theme-color" content="#0d9488" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#030712" media="(prefers-color-scheme: dark)">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="format-detection" content="telephone=no">'''

if old_meta in index_content:
    index_content = index_content.replace(old_meta, new_meta, 1)
    print("Updated viewport & mobile web app meta tags in index.html.")

# Replace header in index.html
header_pattern = re.compile(r'<!-- NAVIGATION HEADER -->\s*<header.*?</header>', re.DOTALL)
index_content = header_pattern.sub(new_header_html, index_content, count=1)
print("Replaced header in index.html.")

# Replace modals/lightbox in index.html
modals_pattern = re.compile(r'<!-- ==================== MODALS & LIGHTBOXES ==================== -->.*?(?=  <!-- Main JavaScript App Logic -->|<script src="assets/js/app\.js">)', re.DOTALL)
index_content = modals_pattern.sub(new_modals_html + "\n\n  ", index_content, count=1)
print("Replaced modals/lightbox/drawer/FAB in index.html.")

# Also update the tight grids in index.html
index_content = index_content.replace(
    'class="grid grid-cols-3 gap-1 font-mono text-[10px]"',
    'class="grid grid-cols-1 sm:grid-cols-3 gap-2 font-mono text-xs"'
)
index_content = index_content.replace(
    'class="grid grid-cols-3 gap-1.5"',
    'class="grid grid-cols-1 sm:grid-cols-3 gap-2"'
)

with open(index_file, "w", encoding="utf-8") as f:
    f.write(index_content)
print("Updated index.html successfully!")
