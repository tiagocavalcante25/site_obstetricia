# -*- coding: utf-8 -*-
import os

base_dir = r"c:\Users\Admin\Downloads\INTERNATO GO\site_obstetricia"
comp_file = os.path.join(base_dir, "components", "modulo-5-dmg-preeclampsia.html")

with open(comp_file, "r", encoding="utf-8") as f:
    orig_content = f.read()

pos_52 = orig_content.find('<!-- 5.2 PREECLAMPSIA, ECLAMPSIA & HELLP -->')
if pos_52 == -1:
    pos_52 = orig_content.find('<div id="modulo-5-has"')

prefix = orig_content[:pos_52]

# Now let's extract the existing MgSO4 block from orig_content so we keep its exact tested DOM structure
mg_start = orig_content.find('<!-- CENTRAL COMPLETA DE SULFATO DE MAGNÉSIO (MgSO4)')
mg_end = orig_content.find('<!-- 5.3 HELLP SYNDROME -->')
existing_mg_block = orig_content[mg_start:mg_end].strip()

# In existing_mg_block, let's inject the renal adjustment switch into the parameter bar (section 2)
# and add the serum reference thresholds card right under the toxicity simulator
renal_switch_html = '''
              <!-- Ajuste de Função Renal (RBEHG 2025) -->
              <div class="col-span-1 md:col-span-3 p-3 rounded-xl bg-amber-500/10 border border-amber-500/30 flex flex-wrap items-center justify-between gap-3">
                <div class="flex items-center gap-2">
                  <i class="fa-solid fa-triangle-exclamation text-amber-600 text-sm"></i>
                  <div>
                    <span class="text-xs font-bold text-amber-900 dark:text-amber-200">Ajuste de Dose na Insuficiência Renal (Creatinina ≥ 1,2 mg/dL ou Oligúria &lt; 25 mL/h)</span>
                    <span class="block text-[11px] text-amber-800 dark:text-amber-300">RBEHG 2025: Manter ataque pleno (4-6g IV), porém <strong>REDUZIR taxa de manutenção em 50%</strong> (0,5 a 1,0 g/h).</span>
                  </div>
                </div>
                <label class="relative inline-flex items-center cursor-pointer">
                  <input type="checkbox" id="mg-renal-adjust" onchange="toggleMgRenalAdjustment(this.checked)" class="sr-only peer">
                  <div class="w-11 h-6 bg-slate-300 peer-focus:outline-none rounded-full peer dark:bg-slate-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-slate-600 peer-checked:bg-amber-600"></div>
                  <span class="ml-2 text-xs font-bold text-amber-900 dark:text-amber-200">Ativar 50% BIC</span>
                </label>
              </div>
'''

# We inject the renal switch right after the H0 start time input div
if '<!-- Horário de Início (H0) -->' in existing_mg_block:
    idx_h0_end = existing_mg_block.find('</div>\n            </div>\n\n            <!-- 3. PROTOCOLO ATIVO')
    if idx_h0_end != -1:
        existing_mg_block = existing_mg_block[:idx_h0_end] + '</div>\n' + renal_switch_html + existing_mg_block[idx_h0_end:]

# Add RBEHG 2025 serum monitoring card right after section 7 (Simulador de Magnesemia)
serum_guideline_card = '''
            <!-- 8. NÍVEIS SÉRICOS DE MAGNÉSIO & CONDUTA LABORATORIAL (RBEHG 2025) -->
            <div class="p-4 rounded-xl bg-teal-50 dark:bg-teal-950/30 border border-teal-200 dark:border-teal-800 space-y-2">
              <h5 class="text-xs font-black uppercase tracking-wider text-teal-800 dark:text-teal-200 flex items-center gap-2">
                <i class="fa-solid fa-vial-virus text-teal-600"></i> Diretriz RBEHG 2025: Monitorização Sérica de Magnésio & Resgate
              </h5>
              <div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5 text-xs">
                <div class="p-2.5 rounded-lg bg-white dark:bg-slate-900 border border-teal-200 dark:border-teal-900">
                  <span class="font-bold text-teal-700 dark:text-teal-300 block mb-0.5">🎯 Faixa Alvo Terapêutica:</span>
                  <span class="font-mono text-sm font-bold text-slate-800 dark:text-slate-100">5,0 a 9,0 mg/dL</span>
                  <span class="block text-[10px] text-slate-500 mt-0.5">(ou 4,0 a 7,0 mEq/L / 2,0 a 3,5 mmol/L).</span>
                </div>
                <div class="p-2.5 rounded-lg bg-white dark:bg-slate-900 border border-rose-200 dark:border-rose-900">
                  <span class="font-bold text-rose-700 dark:text-rose-300 block mb-0.5">🛑 Critério de Interrupção:</span>
                  <span class="font-mono text-sm font-bold text-rose-600 dark:text-rose-400">&gt; 9,6 mg/dL</span>
                  <span class="block text-[10px] text-slate-500 mt-0.5">Suspender imediatamente a infusão e dosar magnesemia a cada 2 horas.</span>
                </div>
                <div class="p-2.5 rounded-lg bg-white dark:bg-slate-900 border border-emerald-200 dark:border-emerald-900">
                  <span class="font-bold text-emerald-700 dark:text-emerald-300 block mb-0.5">🔄 Critério de Reinício:</span>
                  <span class="font-mono text-sm font-bold text-emerald-600 dark:text-emerald-400">&lt; 8,4 mg/dL</span>
                  <span class="block text-[10px] text-slate-500 mt-0.5">Reiniciar infusão com dose reduzida em 50% após retorno dos reflexos patelares.</span>
                </div>
              </div>
            </div>
'''

existing_mg_block = existing_mg_block + "\n\n" + serum_guideline_card

new_section_5_2_top = '''<!-- 5.2 PREECLAMPSIA, ECLAMPSIA & HELLP -->
        <div id="modulo-5-has" class="space-y-6 pt-6 border-t border-slate-200 dark:border-slate-800">
          <div class="flex items-center gap-2 text-xl font-bold text-slate-900 dark:text-white">
            <span class="w-8 h-8 rounded-lg bg-teal-500/10 text-teal-600 flex items-center justify-center text-sm font-black">5.2</span>
            <h3>Síndromes Hipertensivas na Gravidez, Pré-Eclâmpsia & Cuidados Críticos</h3>
          </div>

          <!-- EPIDEMIOLOGIA & IMPACTO EM SAÚDE PÚBLICA (SLIDE 2) -->
          <div class="p-5 rounded-2xl bg-gradient-to-r from-rose-900/10 via-slate-900/5 to-teal-900/10 dark:from-rose-950/30 dark:via-slate-900/50 dark:to-teal-950/30 border border-rose-500/30 space-y-3">
            <div class="flex flex-wrap items-center justify-between gap-2 border-b border-rose-200/40 dark:border-rose-900/40 pb-2">
              <span class="text-xs font-black uppercase tracking-wider text-rose-700 dark:text-rose-300 flex items-center gap-2">
                <i class="fa-solid fa-chart-line"></i> Epidemiologia, Carga de Doença & Mortalidade Materna (RBEHG / FEBRASGO)
              </span>
              <span class="px-2.5 py-0.5 rounded text-[11px] font-black bg-rose-600 text-white">#1 Causa no Brasil</span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 text-xs">
              <div class="p-3 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm">
                <span class="text-2xl font-black text-rose-600 dark:text-rose-400 block mb-1">~14%</span>
                <span class="font-bold text-slate-800 dark:text-slate-200 block">Das Mortes Maternas no Mundo</span>
                <p class="text-[11px] text-slate-500 dark:text-slate-400 mt-1">
                  Respondem por cerca de uma em cada sete mortes maternas no planeta. No mundo desenvolvido, é a 2ª causa de óbito.
                </p>
              </div>
              <div class="p-3 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm">
                <span class="text-2xl font-black text-rose-600 dark:text-rose-400 block mb-1">1ª Causa</span>
                <span class="font-bold text-slate-800 dark:text-slate-200 block">De Morte Materna no Brasil</span>
                <p class="text-[11px] text-slate-500 dark:text-slate-400 mt-1">
                  Líder absoluta de mortalidade materna direta em território brasileiro, superando hemorragia pós-parto e infecções.
                </p>
              </div>
              <div class="p-3 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm">
                <span class="text-2xl font-black text-amber-600 dark:text-amber-400 block mb-1">Morbidade Severa</span>
                <span class="font-bold text-slate-800 dark:text-slate-200 block">Desfechos Perinatais Graves</span>
                <p class="text-[11px] text-slate-500 dark:text-slate-400 mt-1">
                  Causa primária de AVC materno, eclâmpsia, DPP, rotura hepática, prematuridade iatrogênica extrema e óbito fetal.
                </p>
              </div>
              <div class="p-3 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm">
                <span class="text-2xl font-black text-teal-600 dark:text-teal-400 block mb-1">Risco Futuro</span>
                <span class="font-bold text-slate-800 dark:text-slate-200 block">Doença Cardiovascular Tardia</span>
                <p class="text-[11px] text-slate-500 dark:text-slate-400 mt-1">
                  Aumenta em 2 a 4 vezes o risco ao longo da vida de infarto (IAM), AVC, insuficiência renal crônica e HAS prematura.
                </p>
              </div>
            </div>
          </div>

          <!-- 🎈 5-Year-Old Analogy Card -->
          <div class="analogy-balloon p-5 rounded-2xl bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-800/50 transition-all">
            <div class="flex items-start gap-3">
              <span class="text-2xl">🎈</span>
              <div>
                <h4 class="font-bold text-amber-900 dark:text-amber-200 text-sm">Como explicar para uma criança de 5 anos:</h4>
                <p class="text-sm text-amber-800/90 dark:text-amber-300/90 mt-1 leading-relaxed">
                  "Pense que os canos de sangue da mamãe são como mangueiras de jardim. Na gravidez, as mangueiras têm que ficar bem gordinhas e macias para o sangue correr suave. Na pré-eclâmpsia, os caninhos ficaram apertados e rígidos, aí a água passa com tanta força (pressão alta) que começa a vazar buraquinhos nas paredes da mangueira, inchando o corpo da mamãe e machucando os rins."
                </p>
              </div>
            </div>
          </div>

          <!-- AS 4 CATEGORIAS CLÍNICAS DAS SÍNDROMES HIPERTENSIVAS (SLIDE 3) -->
          <div class="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 space-y-4">
            <div class="flex flex-wrap items-center justify-between gap-2 border-b border-slate-200 dark:border-slate-800 pb-3">
              <h4 class="text-sm font-bold uppercase tracking-wider text-slate-900 dark:text-white flex items-center gap-2">
                <i class="fa-solid fa-layer-group text-teal-600"></i> Classificação em 4 Grupos Clínicos (RBEHG / ISSHP / FEBRASGO)
              </h4>
              <span class="text-xs text-slate-500">Definições cronológicas e prognósticas oficiais</span>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
              <!-- 1. Hipertensão Gestacional -->
              <div class="p-4 rounded-xl bg-blue-50/60 dark:bg-blue-950/20 border border-blue-200 dark:border-blue-900/50 space-y-1.5">
                <div class="flex items-center justify-between">
                  <span class="font-black text-blue-800 dark:text-blue-300 text-sm">1. Hipertensão Gestacional (HAG)</span>
                  <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200">&gt; 20 semanas</span>
                </div>
                <p class="text-slate-700 dark:text-slate-300 leading-relaxed">
                  Hipertensão (PAS ≥ 140 ou PAD ≥ 90 mmHg) que surge <strong>após a 20ª semana de gestação</strong> em paciente previamente normotensa, <strong>SEM proteinúria significativa e SEM disfunção de órgão-alvo materno</strong>.
                </p>
                <div class="p-2 rounded bg-white/80 dark:bg-slate-900/80 text-[11px] text-slate-600 dark:text-slate-400 border border-blue-100 dark:border-blue-950">
                  ⏱️ <strong>Evolução Pós-parto:</strong> Os níveis pressóricos normalizam tipicamente em até <strong>12 semanas pós-parto</strong>. Se persistir, reclassifica-se como Hipertensão Crônica.
                </div>
              </div>

              <!-- 2. Hipertensão Arterial Crônica -->
              <div class="p-4 rounded-xl bg-emerald-50/60 dark:bg-emerald-950/20 border border-emerald-200 dark:border-emerald-900/50 space-y-1.5">
                <div class="flex items-center justify-between">
                  <span class="font-black text-emerald-800 dark:text-emerald-300 text-sm">2. Hipertensão Arterial Crônica (HAC)</span>
                  <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 dark:bg-emerald-900 text-emerald-800 dark:text-emerald-200">&lt; 20 semanas ou Prévia</span>
                </div>
                <p class="text-slate-700 dark:text-slate-300 leading-relaxed">
                  Hipertensão arterial diagnosticada <strong>antes da gestação</strong> ou identificada <strong>antes da 20ª semana</strong> de gravidez. Também abrange a hipertensão diagnosticada na gestação que <strong>persiste além de 12 semanas pós-parto</strong>.
                </p>
                <div class="p-2 rounded bg-white/80 dark:bg-slate-900/80 text-[11px] text-slate-600 dark:text-slate-400 border border-emerald-100 dark:border-emerald-950">
                  🎯 <strong>Atenção Pré-Natal:</strong> Necessita investigação basal de órgãos-alvo no 1º trimestre e monitoramento para sobreposição.
                </div>
              </div>

              <!-- 3. Pré-Eclâmpsia Sobreposta à HAC -->
              <div class="p-4 rounded-xl bg-amber-50/60 dark:bg-amber-950/20 border border-amber-200 dark:border-amber-900/50 space-y-1.5">
                <div class="flex items-center justify-between">
                  <span class="font-black text-amber-800 dark:text-amber-300 text-sm">3. Pré-Eclâmpsia Sobreposta à HAC</span>
                  <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-100 dark:bg-amber-900 text-amber-800 dark:text-amber-200">Sobreposição &gt; 20 sem</span>
                </div>
                <p class="text-slate-700 dark:text-slate-300 leading-relaxed">
                  Gestante com HAC conhecida que após 20 semanas apresenta: <strong>piora súbita da PA</strong> necessitando escalonamento de doses, <strong>surgimento de proteinúria nova</strong> (ou aumento repentino de 2 a 3x da proteinúria basal), ou <strong>qualquer disfunção de órgão-alvo</strong>.
                </p>
                <div class="p-2 rounded bg-white/80 dark:bg-slate-900/80 text-[11px] text-slate-600 dark:text-slate-400 border border-amber-100 dark:border-amber-950">
                  ⚠️ <strong>Prognóstico:</strong> Apresenta risco materno-fetal substancialmente maior que a HAC isolada.
                </div>
              </div>

              <!-- 4. Pré-Eclâmpsia / Eclâmpsia -->
              <div class="p-4 rounded-xl bg-rose-50/60 dark:bg-rose-950/20 border border-rose-200 dark:border-rose-900/50 space-y-1.5">
                <div class="flex items-center justify-between">
                  <span class="font-black text-rose-800 dark:text-rose-300 text-sm">4. Pré-Eclâmpsia / Eclâmpsia</span>
                  <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-rose-100 dark:bg-rose-900 text-rose-800 dark:text-rose-200">&gt; 20 semanas + Órgão-Alvo</span>
                </div>
                <p class="text-slate-700 dark:text-slate-300 leading-relaxed">
                  PA ≥ 140/90 após 20 semanas com <strong>proteinúria significativa</strong> OU <strong>disfunção orgânica materna / disfunção útero-placentária</strong>. <strong>Eclâmpsia:</strong> ocorrência de convulsões tônico-clônicas generalizadas na vigência de pré-eclâmpsia.
                </p>
                <div class="p-2 rounded bg-white/80 dark:bg-slate-900/80 text-[11px] text-slate-600 dark:text-slate-400 border border-rose-100 dark:border-rose-950">
                  🚨 <strong>Emergência Obstétrica:</strong> Indicação mandante de internação, sulfatação profilática e planejamento de parto.
                </div>
              </div>
            </div>
          </div>

          <!-- TABELA COMPARATIVA: PRÉ-ECLÂMPSIA VS. HIPERTENSÃO ARTERIAL CRÔNICA (SLIDE 9) -->
          <div class="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 space-y-3">
            <div class="flex flex-wrap items-center justify-between gap-2 border-b border-slate-200 dark:border-slate-800 pb-3">
              <h4 class="text-sm font-bold uppercase tracking-wider text-teal-700 dark:text-teal-400 flex items-center gap-2">
                <i class="fa-solid fa-code-compare"></i> Diagnóstico Diferencial: Pré-Eclâmpsia vs. Hipertensão Arterial Crônica (Slide 9)
              </h4>
              <span class="px-2.5 py-0.5 rounded text-xs font-mono font-bold bg-teal-500/10 text-teal-700 dark:text-teal-300">Tabela de Diferenciação RBEHG</span>
            </div>
            <div class="overflow-x-auto">
              <table class="w-full text-left text-xs text-slate-700 dark:text-slate-300 border-collapse">
                <thead>
                  <tr class="bg-slate-100 dark:bg-slate-800/80 border-b border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white">
                    <th class="p-3 font-black">Critério / Parâmetro Clínico</th>
                    <th class="p-3 font-black text-rose-600 dark:text-rose-400">Pré-Eclâmpsia (PE)</th>
                    <th class="p-3 font-black text-blue-600 dark:text-blue-400">Hipertensão Arterial Crônica (HAC)</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-200 dark:divide-slate-800">
                  <tr class="hover:bg-slate-50 dark:hover:bg-slate-800/40">
                    <td class="p-3 font-bold text-slate-900 dark:text-white">Faixa Etária Materna</td>
                    <td class="p-3 text-rose-700 dark:text-rose-300 font-semibold">Extremos da vida fértil (&lt; 18 ou &gt; 35 anos)</td>
                    <td class="p-3 text-slate-600 dark:text-slate-400">Mais frequente em mulheres &gt; 35 anos</td>
                  </tr>
                  <tr class="hover:bg-slate-50 dark:hover:bg-slate-800/40">
                    <td class="p-3 font-bold text-slate-900 dark:text-white">Paridade</td>
                    <td class="p-3 text-rose-700 dark:text-rose-300 font-semibold">Tipicamente Primigesta / Nulípara</td>
                    <td class="p-3 text-slate-600 dark:text-slate-400">Mais comumente Multíparas</td>
                  </tr>
                  <tr class="hover:bg-slate-50 dark:hover:bg-slate-800/40">
                    <td class="p-3 font-bold text-slate-900 dark:text-white">Início das Manifestações</td>
                    <td class="p-3 text-rose-700 dark:text-rose-300 font-semibold">Após 20 semanas (3º trimestre / intraparto / puerpério)</td>
                    <td class="p-3 text-slate-600 dark:text-slate-400">Antes de 20 semanas de IG ou pré-gestacional</td>
                  </tr>
                  <tr class="hover:bg-slate-50 dark:hover:bg-slate-800/40">
                    <td class="p-3 font-bold text-slate-900 dark:text-white">Comportamento Pressórico</td>
                    <td class="p-3 text-rose-700 dark:text-rose-300 font-semibold">Altamente lábil, flutuações rápidas e picos súbitos</td>
                    <td class="p-3 text-slate-600 dark:text-slate-400">Níveis mais estáveis e contínuos</td>
                  </tr>
                  <tr class="hover:bg-slate-50 dark:hover:bg-slate-800/40">
                    <td class="p-3 font-bold text-slate-900 dark:text-white">Evolução no Pós-Parto</td>
                    <td class="p-3 text-rose-700 dark:text-rose-300 font-semibold">Normaliza completamente em 6 a 12 semanas pós-parto</td>
                    <td class="p-3 text-slate-600 dark:text-slate-400">Persiste indefinidamente após 12 semanas pós-parto</td>
                  </tr>
                  <tr class="hover:bg-slate-50 dark:hover:bg-slate-800/40">
                    <td class="p-3 font-bold text-slate-900 dark:text-white">Proteinúria</td>
                    <td class="p-3 text-rose-700 dark:text-rose-300 font-semibold">Presente, marcante, de início rápido e progressivo</td>
                    <td class="p-3 text-slate-600 dark:text-slate-400">Habitualmente ausente (ou estável se nefropatia basal)</td>
                  </tr>
                  <tr class="hover:bg-slate-50 dark:hover:bg-slate-800/40">
                    <td class="p-3 font-bold text-slate-900 dark:text-white">Ácido Úrico Sérico</td>
                    <td class="p-3 text-rose-700 dark:text-rose-300 font-semibold">
                      <strong>Elevado precocemente (&gt; 4,5 a 6,0 mg/dL)</strong><br>
                      <span class="text-[11px] font-normal text-slate-500">Primeiro marcador laboratorial a subir na PE!</span>
                    </td>
                    <td class="p-3 text-slate-600 dark:text-slate-400">Normal (exceto se uso prévio de diuréticos ou DRC)</td>
                  </tr>
                  <tr class="hover:bg-slate-50 dark:hover:bg-slate-800/40">
                    <td class="p-3 font-bold text-slate-900 dark:text-white">Fundoscopia (Fundo de Olho)</td>
                    <td class="p-3 text-rose-700 dark:text-rose-300 font-semibold">Espasmo arteriolar agudo segmentar, edema de retina</td>
                    <td class="p-3 text-slate-600 dark:text-slate-400">Cruzamento AV patológico, esclerose vascular, fio de prata/cobre</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- ULTRA-REALISTIC IMAGE: PREECLAMPSIA PATHOLOGY & FISIOPATOLOGIA EM 2 ESTÁGIOS (SLIDE 4) -->
          <div class="p-5 rounded-3xl bg-slate-900 text-white shadow-xl overflow-hidden">
            <div class="flex flex-wrap items-center justify-between gap-3 mb-4">
              <div>
                <span class="text-[10px] font-black uppercase tracking-widest text-teal-400">Figura Médica 04 • Fisiopatologia Vascular & Molecular</span>
                <h4 class="text-lg font-bold">Fisiopatologia da Pré-Eclâmpsia: Invasão Trofoblástica Rasa & Cascata Antiangiogênica</h4>
              </div>
              <button onclick="openLightbox('assets/img/preeclampsia_pathology.jpg', 'Fisiopatologia da Pré-Eclâmpsia', 'Comparação lado a lado: Gravidez normal com invasão trofoblástica profunda e artérias espiraladas dilatadas de baixa resistência versus Pré-eclâmpsia com invasão rasa, artérias musculares rígidas, isquemia placentária, liberação de fatores antiangiogênicos (sFlt-1 e Endoglina) e disfunção endotelial sistêmica materna.')" class="px-3 py-1.5 rounded-xl bg-teal-500/20 hover:bg-teal-500/30 text-teal-300 text-xs font-bold border border-teal-500/30 transition-all flex items-center gap-2">
                <i class="fa-solid fa-expand"></i> Ver em Alta Resolução
              </button>
            </div>
            
            <div class="relative rounded-2xl overflow-hidden border border-slate-800 group cursor-pointer" onclick="openLightbox('assets/img/preeclampsia_pathology.jpg', 'Fisiopatologia da Pré-Eclâmpsia', 'Invasão trofoblástica profunda vs rasa.')">
              <img src="assets/img/preeclampsia_pathology.jpg" alt="Fisiopatologia da Pré-Eclâmpsia em Alta Resolução" class="w-full h-auto object-cover transform group-hover:scale-[1.01] transition-transform duration-300">
              <div class="absolute bottom-0 inset-x-0 bg-gradient-to-t from-slate-950/95 via-slate-950/70 to-transparent p-4 text-xs text-slate-300">
                <strong>Estágio 1:</strong> Falha na 2ª onda de invasão trofoblástica (16–20 semanas) → artérias espiraladas permanecem estreitas e reativas → hipóxia placentária. <strong>Estágio 2:</strong> Síndrome endotelial sistêmica materna mediada por excesso de <strong>sFlt-1</strong> (que sequestra VEGF livre e PlGF) e <strong>Endoglina solúvel (sEng)</strong>.
              </div>
            </div>

            <!-- Mecanismo em 2 Estágios Expandido -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3 mt-4 text-xs">
              <div class="p-3 rounded-xl bg-slate-800/80 border border-slate-700">
                <span class="text-teal-400 font-bold block mb-1">🔬 Estágio 1: Defeito de Placentação (Precoce)</span>
                <p class="text-slate-300 leading-relaxed text-[11px]">
                  O trofoblasto extraviloso falha em remodelar as porções miometriais das artérias espiraladas. Os vasos mantêm túnica média muscular íntegra e alta sensibilidade a agentes vasoconstritores, provocando fluxo sanguíneo pulsátil de alta velocidade e estresse de cisalhamento.
                </p>
              </div>
              <div class="p-3 rounded-xl bg-slate-800/80 border border-slate-700">
                <span class="text-rose-400 font-bold block mb-1">⚡ Estágio 2: Desbalanço Angiogênico Materno (Sistêmico)</span>
                <p class="text-slate-300 leading-relaxed text-[11px]">
                  A placenta isquêmica hiperproduz <strong>sFlt-1</strong> e <strong>sEng</strong>, bloqueando a sinalização de sobrevivência endotelial de VEGF e PlGF. O resultado é dano endotelial difuso, vasoconstrição multiorgânica, perda de barreira capilar (edema/proteinúria) e microangiopatia trombótica.
                </p>
              </div>
            </div>
          </div>

          <!-- MANEJO DA HIPERTENSÃO ARTERIAL CRÔNICA (HAC) NO PRÉ-NATAL (SLIDES 10-14) -->
          <div class="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 space-y-4">
            <div class="flex flex-wrap items-center justify-between gap-2 border-b border-slate-200 dark:border-slate-800 pb-3">
              <h4 class="text-sm font-bold uppercase tracking-wider text-slate-900 dark:text-white flex items-center gap-2">
                <i class="fa-solid fa-stethoscope text-teal-600"></i> Manejo Pré-Natal da Hipertensa Crônica (Slides 10–14)
              </h4>
              <span class="px-2.5 py-0.5 rounded text-xs font-mono font-bold bg-teal-500/10 text-teal-700 dark:text-teal-300">CHAP Study & Diretrizes 2025</span>
            </div>

            <!-- Investigação Laboratorial Inicial e Metas Pressóricas -->
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-3 text-xs">
              <div class="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700 space-y-2">
                <span class="font-bold text-slate-900 dark:text-white block flex items-center gap-1.5">
                  <i class="fa-solid fa-vials text-teal-600"></i> Triagem Basal de 1ª Consulta:
                </span>
                <ul class="text-[11px] text-slate-600 dark:text-slate-300 space-y-1 list-disc list-inside">
                  <li><strong>Hematológico:</strong> Hemograma completo e plaquetas.</li>
                  <li><strong>Renal:</strong> Creatinina sérica, Ureia, Ácido úrico, Eletrólitos (Na/K).</li>
                  <li><strong>Urina:</strong> Relação P/C ou Proteinúria 24h basal (crucial para diferenciar sobreposição).</li>
                  <li><strong>Hepático:</strong> AST, ALT, Bilirrubinas, LDH.</li>
                  <li><strong>Órgãos-alvo:</strong> Fundo de olho, ECG, Ecocardiograma (se HAS crônica de longa data).</li>
                  <li><strong>Metabólico:</strong> Glicemia jejum / TOTG 75g (DM2 associado), TSH.</li>
                </ul>
              </div>

              <div class="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700 space-y-2">
                <span class="font-bold text-slate-900 dark:text-white block flex items-center gap-1.5">
                  <i class="fa-solid fa-bullseye text-blue-600"></i> Metas de Controle Pressórico:
                </span>
                <div class="p-2.5 rounded-lg bg-blue-50 dark:bg-blue-950/40 border border-blue-200 dark:border-blue-900 text-blue-900 dark:text-blue-200 font-semibold text-center">
                  PAS: 120 a 150 mmHg<br>
                  PAD: 80 a 100 mmHg
                </div>
                <p class="text-[11px] text-slate-600 dark:text-slate-400 leading-relaxed">
                  📌 <strong>Evitar PAD &lt; 80 mmHg:</strong> Quedas excessivas da PAD reduzem a perfusão intervilositária e causam restrição de crescimento fetal.<br>
                  📌 <strong>Indicação de Tratamento (CHAP Study):</strong> Iniciar farmacoterapia oral sempre que PA persistir <strong>≥ 140/90 mmHg</strong>.
                </p>
              </div>

              <div class="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700 space-y-2">
                <span class="font-bold text-slate-900 dark:text-white block flex items-center gap-1.5">
                  <i class="fa-solid fa-pills text-emerald-600"></i> Anti-Hipertensivos Orais Seguros:
                </span>
                <div class="space-y-1.5 text-[11px]">
                  <div class="p-2 rounded bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800">
                    <strong class="text-emerald-700 dark:text-emerald-400">1ª Linha: Metildopa</strong><br>
                    750 a 2000 mg/dia (máx 3000 mg/dia) dividido em 3 a 4 tomadas. Efeitos: sedação, boca seca, depressão, Coombs direto +.
                  </div>
                  <div class="p-2 rounded bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800">
                    <strong class="text-emerald-700 dark:text-emerald-400">2ª Linha: Nifedipino Retard</strong><br>
                    20 a 60 mg/dia (máx 120 mg/dia) em 1 a 2 tomadas. Excelente eficácia. Evitar na ICC.
                  </div>
                  <div class="p-2 rounded bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800">
                    <strong class="text-slate-700 dark:text-slate-300">Outras: Labetalol oral / Hidralazina VO</strong>
                  </div>
                </div>
              </div>
            </div>

            <!-- MEDICAMENTOS FORMALMENTE CONTRAINDICADOS NA GESTAÇÃO (CARD DE ALERTA VERMELHO) -->
            <div class="p-4 rounded-xl bg-rose-50 dark:bg-rose-950/30 border border-rose-300 dark:border-rose-900 space-y-2">
              <span class="text-xs font-black uppercase tracking-wider text-rose-800 dark:text-rose-200 flex items-center gap-2">
                <i class="fa-solid fa-ban text-rose-600"></i> Fármacos Anti-Hipertensivos Contraindicados na Gestação (Risco Fetal Crítico)
              </span>
              <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2 text-[11px]">
                <div class="p-2 rounded-lg bg-white dark:bg-slate-900 border border-rose-200 dark:border-rose-900/60">
                  <strong class="text-rose-600 block">IECA e BRA</strong>
                  Enalapril, Captopril, Losartana. Teratogênicos (2º e 3º tri): causam disgenesia renal fetal, anúria neonatal, oligoidrâmnio, hipoplasia pulmonar e óbito fetal.
                </div>
                <div class="p-2 rounded-lg bg-white dark:bg-slate-900 border border-rose-200 dark:border-rose-900/60">
                  <strong class="text-rose-600 block">Atenolol</strong>
                  Associado de forma consistente a restrição de crescimento intrauterino (CIUR grave) e bradicardia fetal.
                </div>
                <div class="p-2 rounded-lg bg-white dark:bg-slate-900 border border-rose-200 dark:border-rose-900/60">
                  <strong class="text-rose-600 block">Diuréticos de Rotina</strong>
                  HCTZ e Furosemida: Espoliação do volume plasmático materno, redução do débito cardíaco materno e piora da perfusão placentária (usar apenas se EAP).
                </div>
                <div class="p-2 rounded-lg bg-white dark:bg-slate-900 border border-rose-200 dark:border-rose-900/60">
                  <strong class="text-rose-600 block">Espironolactona</strong>
                  Efeito antiandrogênico com feminização do feto do sexo masculino.
                </div>
              </div>
            </div>
          </div>

          <!-- CRITÉRIOS DIAGNÓSTICOS MODERNOS & CHECKLIST INTERATIVO DE DISFUNÇÃO DE ÓRGÃO-ALVO (ISSHP 2022 / FEBRASGO) -->
          <div class="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-teal-500/30 shadow-md space-y-4">
            <div class="flex flex-wrap items-center justify-between gap-2 border-b border-slate-200 dark:border-slate-800 pb-3">
              <div>
                <h4 class="text-sm font-bold uppercase tracking-wider text-teal-700 dark:text-teal-400 flex items-center gap-2">
                  <i class="fa-solid fa-list-check"></i> Critérios Diagnósticos de Pré-Eclâmpsia & Disfunção Orgânica (ISSHP 2022)
                </h4>
                <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                  A proteinúria <strong>NÃO É MAIS OBRIGATÓRIA</strong> para o diagnóstico quando houver disfunção de órgão-alvo materno ou fetal!
                </p>
              </div>
              <span class="px-2.5 py-0.5 rounded text-xs font-bold bg-teal-500/10 text-teal-700 dark:text-teal-300">ISSHP / FEBRASGO</span>
            </div>

            <!-- Bloco 1: Critério Pressórico Obrigatório + Proteinúria Clássica -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
              <div class="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700">
                <span class="font-bold text-slate-900 dark:text-white block mb-1">1. Critério Pressórico Obrigatório:</span>
                <p class="text-slate-600 dark:text-slate-300 text-[11px] leading-relaxed">
                  PA sistólica <strong>≥ 140 mmHg</strong> e/ou diastólica <strong>≥ 90 mmHg</strong> em 2 aferições com intervalo mínimo de 4 horas, após a 20ª semana de gestação em mulher previamente normotensa.
                </p>
              </div>
              <div class="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700">
                <span class="font-bold text-slate-900 dark:text-white block mb-1">2. Proteinúria Significativa (Clássica):</span>
                <p class="text-slate-600 dark:text-slate-300 text-[11px] leading-relaxed">
                  Proteinúria de 24h <strong>≥ 300 mg</strong>, ou Relação Proteína/Creatinina urinária (P/C) <strong>≥ 0,3 mg/mg</strong> (ou ≥ 30 mg/mmol), ou fita reagente <strong>≥ 1+</strong> (se métodos quantitativos indisponíveis).
                </p>
              </div>
            </div>

            <!-- Bloco 2: Checklist Interativo de Disfunção Orgânica -->
            <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/40 border border-slate-200 dark:border-slate-700 space-y-3">
              <span class="text-xs font-bold uppercase tracking-wider text-slate-800 dark:text-slate-200 block">
                OU na Ausência de Proteinúria: Selecione os Critérios de Disfunção de Órgão-Alvo / Fetal:
              </span>
              <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2.5 text-xs">
                <label class="flex items-start gap-2 p-2.5 rounded-lg bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 hover:border-teal-500 cursor-pointer transition-all">
                  <input type="checkbox" id="org-dys-hemo" onchange="checkPreeclampsiaOrganDysfunction()" class="mt-0.5 rounded text-teal-600 accent-teal-600 cursor-pointer">
                  <span><strong>Hematológico:</strong> Plaquetas ≤ 150.000/μL, coagulopatia ou hemólise microangiopática.</span>
                </label>
                <label class="flex items-start gap-2 p-2.5 rounded-lg bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 hover:border-teal-500 cursor-pointer transition-all">
                  <input type="checkbox" id="org-dys-hep" onchange="checkPreeclampsiaOrganDysfunction()" class="mt-0.5 rounded text-teal-600 accent-teal-600 cursor-pointer">
                  <span><strong>Hepático:</strong> AST ou ALT ≥ 40 UI/L (ou &gt; 2x normal) ou dor epigástrica / HCD persistente.</span>
                </label>
                <label class="flex items-start gap-2 p-2.5 rounded-lg bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 hover:border-teal-500 cursor-pointer transition-all">
                  <input type="checkbox" id="org-dys-ren" onchange="checkPreeclampsiaOrganDysfunction()" class="mt-0.5 rounded text-teal-600 accent-teal-600 cursor-pointer">
                  <span><strong>Renal:</strong> Creatinina sérica ≥ 1,0 mg/dL ou duplicação do basal na ausência de nefropatia prévia.</span>
                </label>
                <label class="flex items-start gap-2 p-2.5 rounded-lg bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 hover:border-teal-500 cursor-pointer transition-all">
                  <input type="checkbox" id="org-dys-pulm" onchange="checkPreeclampsiaOrganDysfunction()" class="mt-0.5 rounded text-teal-600 accent-teal-600 cursor-pointer">
                  <span><strong>Pulmonar:</strong> Edema agudo de pulmão (dispneia, estertores crepitantes, hipoxemia).</span>
                </label>
                <label class="flex items-start gap-2 p-2.5 rounded-lg bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 hover:border-teal-500 cursor-pointer transition-all">
                  <input type="checkbox" id="org-dys-neuro" onchange="checkPreeclampsiaOrganDysfunction()" class="mt-0.5 rounded text-teal-600 accent-teal-600 cursor-pointer">
                  <span><strong>Neurológico:</strong> Eclâmpsia, sineclâmpsia, cefaleia refratária, escotomas, amaurose, clônus.</span>
                </label>
                <label class="flex items-start gap-2 p-2.5 rounded-lg bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 hover:border-teal-500 cursor-pointer transition-all">
                  <input type="checkbox" id="org-dys-plac" onchange="checkPreeclampsiaOrganDysfunction()" class="mt-0.5 rounded text-teal-600 accent-teal-600 cursor-pointer">
                  <span><strong>Útero-Placentário:</strong> CIUR, Doppler de artéria umbilical alterado, DPP ou óbito fetal.</span>
                </label>
              </div>

              <!-- Resultado do Diagnóstico por Disfunção Orgânica -->
              <div id="org-dys-result" class="hidden"></div>
            </div>
          </div>

          <!-- CALCULADORA DE ESTRATIFICAÇÃO DE RISCO & PROFILAXIA COM AAS E CÁLCIO (QUADRO 6 RBEHG) (SLIDES 15-19) -->
          <div class="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 space-y-4">
            <div class="flex flex-wrap items-center justify-between gap-2 border-b border-slate-200 dark:border-slate-800 pb-3">
              <div>
                <h4 class="text-sm font-bold uppercase tracking-wider text-slate-900 dark:text-white flex items-center gap-2">
                  <i class="fa-solid fa-calculator text-teal-600"></i> Calculadora de Risco de Pré-Eclâmpsia & Profilaxia com AAS / Cálcio
                </h4>
                <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                  Diretriz RBEHG 2025 / FEBRASGO (Quadro 6): <strong>1 fator de alto risco</strong> OU <strong>≥ 2 fatores moderados</strong> indicam profilaxia!
                </p>
              </div>
              <button type="button" onclick="calcPreeclampsiaRisk()" class="px-3 py-1.5 rounded-lg bg-teal-600 hover:bg-teal-700 text-white font-bold text-xs transition-all cursor-pointer">
                Calcular Indicação
              </button>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
              <!-- Alto Risco (Basta 1) -->
              <div class="p-3.5 rounded-xl bg-rose-50/50 dark:bg-rose-950/20 border border-rose-200 dark:border-rose-900/50 space-y-2">
                <span class="font-bold text-rose-800 dark:text-rose-300 block flex items-center justify-between">
                  <span>🔴 Fatores de Alto Risco (Basta 1 fator presente):</span>
                  <span class="text-[10px] bg-rose-200 dark:bg-rose-900 px-1.5 py-0.5 rounded font-black text-rose-900 dark:text-rose-100">Alto Risco</span>
                </span>
                <div class="space-y-1.5 text-[11px]">
                  <label class="flex items-center gap-2 cursor-pointer hover:text-rose-700 dark:hover:text-rose-300">
                    <input type="checkbox" id="pe-risk-prev" onchange="calcPreeclampsiaRisk()" class="rounded text-rose-600 accent-rose-600">
                    <span>Pré-eclâmpsia em gestação anterior (esp. precoce ou complicada)</span>
                  </label>
                  <label class="flex items-center gap-2 cursor-pointer hover:text-rose-700 dark:hover:text-rose-300">
                    <input type="checkbox" id="pe-risk-multi" onchange="calcPreeclampsiaRisk()" class="rounded text-rose-600 accent-rose-600">
                    <span>Gestação múltipla (gemelaridade)</span>
                  </label>
                  <label class="flex items-center gap-2 cursor-pointer hover:text-rose-700 dark:hover:text-rose-300">
                    <input type="checkbox" id="pe-risk-obese" onchange="calcPreeclampsiaRisk()" class="rounded text-rose-600 accent-rose-600">
                    <span>Obesidade pré-gestacional (IMC ≥ 30 kg/m²)</span>
                  </label>
                  <label class="flex items-center gap-2 cursor-pointer hover:text-rose-700 dark:hover:text-rose-300">
                    <input type="checkbox" id="pe-risk-hac" onchange="calcPreeclampsiaRisk()" class="rounded text-rose-600 accent-rose-600">
                    <span>Hipertensão Arterial Crônica preexistente</span>
                  </label>
                  <label class="flex items-center gap-2 cursor-pointer hover:text-rose-700 dark:hover:text-rose-300">
                    <input type="checkbox" id="pe-risk-dm" onchange="calcPreeclampsiaRisk()" class="rounded text-rose-600 accent-rose-600">
                    <span>Diabetes Mellitus pré-gestacional (DM1 ou DM2)</span>
                  </label>
                  <label class="flex items-center gap-2 cursor-pointer hover:text-rose-700 dark:hover:text-rose-300">
                    <input type="checkbox" id="pe-risk-ckd" onchange="calcPreeclampsiaRisk()" class="rounded text-rose-600 accent-rose-600">
                    <span>Doença Renal Crônica (DRC)</span>
                  </label>
                  <label class="flex items-center gap-2 cursor-pointer hover:text-rose-700 dark:hover:text-rose-300">
                    <input type="checkbox" id="pe-risk-auto" onchange="calcPreeclampsiaRisk()" class="rounded text-rose-600 accent-rose-600">
                    <span>Doença autoimune (Lúpus Eritematoso Sistêmico ou SAF)</span>
                  </label>
                  <label class="flex items-center gap-2 cursor-pointer hover:text-rose-700 dark:hover:text-rose-300">
                    <input type="checkbox" id="pe-risk-fiv" onchange="calcPreeclampsiaRisk()" class="rounded text-rose-600 accent-rose-600">
                    <span>Reprodução assistida (Fertilização in vitro)</span>
                  </label>
                </div>
              </div>

              <!-- Risco Moderado (Necessário >= 2) -->
              <div class="p-3.5 rounded-xl bg-amber-50/50 dark:bg-amber-950/20 border border-amber-200 dark:border-amber-900/50 space-y-2">
                <span class="font-bold text-amber-800 dark:text-amber-300 block flex items-center justify-between">
                  <span>🟡 Fatores de Risco Moderado (Necessário ≥ 2 fatores):</span>
                  <span class="text-[10px] bg-amber-200 dark:bg-amber-900 px-1.5 py-0.5 rounded font-black text-amber-900 dark:text-amber-100">Risco Moderado</span>
                </span>
                <div class="space-y-1.5 text-[11px]">
                  <label class="flex items-center gap-2 cursor-pointer hover:text-amber-700 dark:hover:text-amber-300">
                    <input type="checkbox" id="pe-risk-nuli" onchange="calcPreeclampsiaRisk()" class="rounded text-amber-600 accent-amber-600">
                    <span>Nuliparidade (primeira gestação)</span>
                  </label>
                  <label class="flex items-center gap-2 cursor-pointer hover:text-amber-700 dark:hover:text-amber-300">
                    <input type="checkbox" id="pe-risk-fam" onchange="calcPreeclampsiaRisk()" class="rounded text-amber-600 accent-amber-600">
                    <span>História familiar de pré-eclâmpsia em parentes de 1º grau (mãe ou irmã)</span>
                  </label>
                  <label class="flex items-center gap-2 cursor-pointer hover:text-amber-700 dark:hover:text-amber-300">
                    <input type="checkbox" id="pe-risk-age" onchange="calcPreeclampsiaRisk()" class="rounded text-amber-600 accent-amber-600">
                    <span>Idade materna avançada (≥ 35 anos)</span>
                  </label>
                  <label class="flex items-center gap-2 cursor-pointer hover:text-amber-700 dark:hover:text-amber-300">
                    <input type="checkbox" id="pe-risk-interv" onchange="calcPreeclampsiaRisk()" class="rounded text-amber-600 accent-amber-600">
                    <span>Intervalo interpartal prolongado (&gt; 10 anos)</span>
                  </label>
                  <label class="flex items-center gap-2 cursor-pointer hover:text-amber-700 dark:hover:text-amber-300">
                    <input type="checkbox" id="pe-risk-socio" onchange="calcPreeclampsiaRisk()" class="rounded text-amber-600 accent-amber-600">
                    <span>Condição socioeconômica desfavorável</span>
                  </label>
                  <label class="flex items-center gap-2 cursor-pointer hover:text-amber-700 dark:hover:text-amber-300">
                    <input type="checkbox" id="pe-risk-race" onchange="calcPreeclampsiaRisk()" class="rounded text-amber-600 accent-amber-600">
                    <span>Etnia / Raça negra ou parda</span>
                  </label>
                  <label class="flex items-center gap-2 cursor-pointer hover:text-amber-700 dark:hover:text-amber-300">
                    <input type="checkbox" id="pe-risk-adverse" onchange="calcPreeclampsiaRisk()" class="rounded text-amber-600 accent-amber-600">
                    <span>Histórico prévio de desfecho perinatal adverso (baixo peso, CIUR, óbito fetal)</span>
                  </label>
                </div>
              </div>
            </div>

            <!-- Resultado da Calculadora de Risco -->
            <div id="pe-risk-result" class="hidden"></div>
          </div>

          <!-- CONDUTA NA PRÉ-ECLÂMPSIA SEM GRAVIDADE VS. GRAVE (SLIDES 20-25) -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            <!-- PE Sem Critérios de Gravidade -->
            <div class="p-4 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 space-y-2">
              <span class="font-bold text-slate-900 dark:text-white text-sm flex items-center justify-between">
                <span>Pré-Eclâmpsia Sem Sinais de Gravidade</span>
                <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200">Expectante até 37 sem</span>
              </span>
              <ul class="text-[11px] text-slate-600 dark:text-slate-300 space-y-1.5 list-disc list-inside">
                <li><strong>Internação ou Ambulatório de Alto Risco:</strong> Vigilância clínica rigorosa com repouso relativo no leito.</li>
                <li><strong>Anti-hipertensivo oral:</strong> Iniciar apenas se PA ≥ 140/90 mmHg, mantendo meta entre 130-145 / 80-95 mmHg.</li>
                <li><strong>NÃO USAR Sulfato de Magnésio:</strong> A profilaxia de convulsões com MgSO4 <em>NÃO é indicada</em> na ausência de critérios de gravidade!</li>
                <li><strong>Laboratório Seriado:</strong> Hemograma, plaquetas, TGO/TGP, creatinina e ácido úrico 1 a 2 vezes por semana.</li>
                <li><strong>Vigilância Fetal:</strong> Cardiotocografia basal semanal, PBF e Doppler de artéria umbilical a cada 1-2 semanas.</li>
                <li><strong>Resolução Eletiva:</strong> Interrupção indicada com <strong>37 semanas completas</strong>.</li>
              </ul>
            </div>

            <!-- PE com Critérios de Gravidade -->
            <div class="p-4 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 space-y-2">
              <span class="font-bold text-slate-900 dark:text-white text-sm flex items-center justify-between">
                <span>Pré-Eclâmpsia com Critérios de Gravidade</span>
                <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-rose-100 dark:bg-rose-900 text-rose-800 dark:text-rose-200">Internação + MgSO4</span>
              </span>
              <ul class="text-[11px] text-slate-600 dark:text-slate-300 space-y-1.5 list-disc list-inside">
                <li><strong>Internação Imediata:</strong> Transferência para Centro Obstétrico / UTI Materna em centro terciário.</li>
                <li><strong>Sulfato de Magnésio Obrigatório:</strong> Ataque + manutenção imediata para prevenção de convulsões eclâmpticas.</li>
                <li><strong>Crise Hipertensiva (PA ≥ 160×110):</strong> Tratamento agudo imediato com Hidralazina IV, Labetalol IV ou Nifedipino oral.</li>
                <li><strong>Corticoterapia Antenatal (24 a 34 semanas):</strong> Betametasona 12 mg IM q24h por 2 doses se estabilidade clínica para ganho pulmonar.</li>
                <li><strong>Conduta Expectante (24 a 34 sem):</strong> Permitida SOMENTE sob estabilidade absoluta materno-fetal em centro terciário.</li>
                <li><strong>Resolução Mandatória:</strong> Interrupção com <strong>34 semanas completas</strong> ou imediatamente se critérios de emergência.</li>
              </ul>
            </div>
          </div>

          <!-- Preeclampsia Severe Features & Acute Crisis Management (SLIDES 22-25) -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Critérios de Gravidade -->
            <div class="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800">
              <h4 class="text-sm font-bold uppercase tracking-wider text-rose-600 dark:text-rose-400 mb-3 flex items-center gap-2">
                <i class="fa-solid fa-triangle-exclamation"></i> Critérios de Gravidade da Pré-Eclâmpsia (ACOG / RBEHG)
              </h4>
              <ul class="text-xs space-y-2 text-slate-700 dark:text-slate-300">
                <li class="p-2 rounded-lg bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-900">
                  <strong>PA Crítica:</strong> PAS ≥ 160 mmHg ou PAD ≥ 110 mmHg em duas ocasiões com intervalo de 15 min.
                </li>
                <li class="p-2 rounded-lg bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-900">
                  <strong>Plaquetopenia:</strong> Plaquetas &lt; 100.000 / μL.
                </li>
                <li class="p-2 rounded-lg bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-900">
                  <strong>Disfunção Hepática:</strong> Transaminases (AST/ALT) &gt; 2x o limite superior do normal ou dor em hipocôndrio direito persistente.
                </li>
                <li class="p-2 rounded-lg bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-900">
                  <strong>Insuficiência Renal:</strong> Creatinina sérica &gt; 1,1 mg/dL ou duplicação do valor basal.
                </li>
                <li class="p-2 rounded-lg bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-900">
                  <strong>Edema Agudo de Pulmão & Sintomas Cerebrais:</strong> Cefaleia intensa refratária a analgésicos, escotomas cintilantes, turvação visual ou amaurose.
                </li>
              </ul>
            </div>

            <!-- Anti-Hipertensivos de Urgência na Crise Hipertensiva -->
            <div class="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 flex flex-col justify-between">
              <div>
                <h4 class="text-sm font-bold uppercase tracking-wider text-amber-600 dark:text-amber-400 mb-3 flex items-center gap-2">
                  <i class="fa-solid fa-pills"></i> Tratamento Agudo da Crise Hipertensiva (PA ≥ 160×110)
                </h4>
                <div class="space-y-2 text-xs">
                  <div class="p-2.5 rounded-xl bg-amber-50/60 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-900">
                    <div class="flex justify-between items-center">
                      <span class="font-bold text-slate-900 dark:text-white">1. Hidralazina IV (1ª Linha Brasil)</span>
                      <span class="font-mono font-bold text-amber-700 dark:text-amber-300">5 mg IV lento</span>
                    </div>
                    <p class="text-[11px] text-slate-600 dark:text-slate-300 mt-1">
                      Diluir 1 ampola (20 mg/mL) em 19 mL de SF (1 mg/mL). Aplicar 5 mg (5 mL). Se PA mantiver ≥ 160×110 após 20 min, repetir 5 a 10 mg (dose máx: 20-30 mg).
                    </p>
                  </div>

                  <div class="p-2.5 rounded-xl bg-blue-50/60 dark:bg-blue-950/30 border border-blue-200 dark:border-blue-900">
                    <div class="flex justify-between items-center">
                      <span class="font-bold text-slate-900 dark:text-white">2. Labetalol IV (Padrão ACOG)</span>
                      <span class="font-mono font-bold text-blue-700 dark:text-blue-300">20 mg IV</span>
                    </div>
                    <p class="text-[11px] text-slate-600 dark:text-slate-300 mt-1">
                      Infundir 20 mg em 2 min. Se necessário, dobrar a dose após 10-20 min: 40 mg, depois 80 mg a cada 10-20 min (dose máx cumulativa: 220-300 mg). Evitar na asma grave.
                    </p>
                  </div>

                  <div class="p-2.5 rounded-xl bg-purple-50/60 dark:bg-purple-950/30 border border-purple-200 dark:border-purple-900">
                    <div class="flex justify-between items-center">
                      <span class="font-bold text-slate-900 dark:text-white">3. Nifedipino Oral (Liberação Rápida)</span>
                      <span class="font-mono font-bold text-purple-700 dark:text-purple-300">10 a 20 mg VO</span>
                    </div>
                    <p class="text-[11px] text-slate-600 dark:text-slate-300 mt-1">
                      Administrar VO com deglutição (NUNCA sublingual). Repetir 10-20 mg em 30 min se necessário (dose máx: 50 mg). Excelente na indisponibilidade de acesso venoso imediato.
                    </p>
                  </div>
                </div>
              </div>

              <div class="mt-3 p-2 rounded-lg bg-slate-100 dark:bg-slate-800 text-[11px] text-slate-600 dark:text-slate-400">
                🎯 <strong>Meta Pressórica:</strong> PAS 140–150 mmHg e PAD 90–100 mmHg. Não reduzir abruptamente para não comprometer o fluxo útero-placentário!
              </div>
            </div>
          </div>

          <!-- CRITÉRIOS DE INTERRUPÇÃO IMEDIATA DA GESTAÇÃO - QUADRO 13 RBEHG 2025 (SLIDE 26) -->
          <div class="p-5 rounded-2xl bg-rose-50 dark:bg-rose-950/30 border border-rose-300 dark:border-rose-900 space-y-3">
            <div class="flex flex-wrap items-center justify-between gap-2 border-b border-rose-200 dark:border-rose-800 pb-2">
              <h4 class="text-xs font-black uppercase tracking-wider text-rose-800 dark:text-rose-200 flex items-center gap-2">
                <i class="fa-solid fa-triangle-exclamation text-rose-600"></i> Quadro 13 RBEHG 2025: Critérios para Interrupção Imediata da Gestação (Qualquer IG)
              </h4>
              <span class="px-2.5 py-0.5 rounded text-[11px] font-black bg-rose-600 text-white">Após Estabilização Materna</span>
            </div>
            <p class="text-xs text-rose-900 dark:text-rose-200">
              Na presença de qualquer um dos 10 critérios abaixo, <strong>a conduta expectante está contraindicada</strong> independentemente da idade gestacional. Proceder à estabilização hemodinâmica imediata (MgSO4 + anti-hipertensivo) e realizar o parto:
            </p>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-2 text-[11px]">
              <div class="p-2.5 rounded-lg bg-white dark:bg-slate-900 border border-rose-200 dark:border-rose-900">
                <span class="font-bold text-rose-700 dark:text-rose-300 block mb-1">1. HAS Grave Refratária</span>
                Pressão arterial descontrolada apesar do uso de 3 classes de anti-hipertensivos em doses máximas.
              </div>
              <div class="p-2.5 rounded-lg bg-white dark:bg-slate-900 border border-rose-200 dark:border-rose-900">
                <span class="font-bold text-rose-700 dark:text-rose-300 block mb-1">2. Cefaleia Intensa</span>
                Cefaleia refratária persistente e sem alívio com analgésicos usuais (risco iminente de hemorragia cerebral).
              </div>
              <div class="p-2.5 rounded-lg bg-white dark:bg-slate-900 border border-rose-200 dark:border-rose-900">
                <span class="font-bold text-rose-700 dark:text-rose-300 block mb-1">3. Epigastralgia Refratária</span>
                Dor em hipocôndrio direito persistente (sinal de distensão de Glisson e hematoma hepático iminente).
              </div>
              <div class="p-2.5 rounded-lg bg-white dark:bg-slate-900 border border-rose-200 dark:border-rose-900">
                <span class="font-bold text-rose-700 dark:text-rose-300 block mb-1">4. Distúrbios Visuais</span>
                Escotomas cintilantes persistentes, turvação visual contínua ou amaurose cortical.
              </div>
              <div class="p-2.5 rounded-lg bg-white dark:bg-slate-900 border border-rose-200 dark:border-rose-900">
                <span class="font-bold text-rose-700 dark:text-rose-300 block mb-1">5. Evento Vascular Maior</span>
                Acidente vascular cerebral (AVC isquêmico ou hemorrágico), IAM ou edema agudo de pulmão.
              </div>
              <div class="p-2.5 rounded-lg bg-white dark:bg-slate-900 border border-rose-200 dark:border-rose-900">
                <span class="font-bold text-rose-700 dark:text-rose-300 block mb-1">6. Síndrome HELLP</span>
                Hemólise microangiopática + TGO &gt; 70 + Plaquetas &lt; 100.000 / μL.
              </div>
              <div class="p-2.5 rounded-lg bg-white dark:bg-slate-900 border border-rose-200 dark:border-rose-900">
                <span class="font-bold text-rose-700 dark:text-rose-300 block mb-1">7. Falência Renal</span>
                Creatinina &gt; 1,1 mg/dL rapidamente progressiva, oligúria refratária &lt; 500 mL/24h ou anasarca.
              </div>
              <div class="p-2.5 rounded-lg bg-white dark:bg-slate-900 border border-rose-200 dark:border-rose-900">
                <span class="font-bold text-rose-700 dark:text-rose-300 block mb-1">8. Eclâmpsia / Sineclâmpsia</span>
                Crise convulsiva tônico-clônica ou pródromos neurológicos graves refratários.
              </div>
              <div class="p-2.5 rounded-lg bg-white dark:bg-slate-900 border border-rose-200 dark:border-rose-900">
                <span class="font-bold text-rose-700 dark:text-rose-300 block mb-1">9. Descolamento Prematuro</span>
                Suspeita clínica ou ultrassonográfica de DPP (hipertonia uterina, dor súbita e metrorragia).
              </div>
              <div class="p-2.5 rounded-lg bg-white dark:bg-slate-900 border border-rose-200 dark:border-rose-900">
                <span class="font-bold text-rose-700 dark:text-rose-300 block mb-1">10. Sofrimento Fetal Crítico</span>
                CTG categoria III, PBF ≤ 4/10, diástole reversa persistente na artéria umbilical ou óbito fetal.
              </div>
            </div>
          </div>

          <!-- CUIDADOS CIRÚRGICOS & ANESTÉSICOS NA PRÉ-ECLÂMPSIA / PLAQUETOPENIA (SLIDES 27-28) -->
          <div class="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 space-y-3">
            <div class="flex flex-wrap items-center justify-between gap-2 border-b border-slate-200 dark:border-slate-800 pb-2">
              <h4 class="text-xs font-black uppercase tracking-wider text-slate-900 dark:text-white flex items-center gap-2">
                <i class="fa-solid fa-syringe text-teal-600"></i> Manejo Anestésico & Plaquetopenia na Pré-Eclâmpsia (Slides 27–28)
              </h4>
              <span class="px-2.5 py-0.5 rounded text-[11px] font-bold bg-amber-500/10 text-amber-700 dark:text-amber-300 border border-amber-500/30">Protocolo de Segurança Cirúrgica</span>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
              <div class="p-3.5 rounded-xl bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-900 space-y-1">
                <span class="font-bold text-rose-800 dark:text-rose-200 block text-xs flex items-center gap-1.5">
                  <i class="fa-solid fa-ban text-rose-600"></i> Plaquetas &lt; 70.000 / μL:
                </span>
                <span class="font-black text-rose-600 dark:text-rose-400 block text-xs">ANESTESIA GERAL OBRIGATÓRIA!</span>
                <p class="text-[11px] text-rose-900 dark:text-rose-300 leading-relaxed">
                  Contraindicação absoluta de bloqueio de neuroeixo (raquianestesia ou peridural) pelo altíssimo risco de <strong>hematoma epidural compressivo e paraplegia irreversível</strong>. Realizar IOT em sequência rápida com tubo orotraqueal.
                </p>
              </div>

              <div class="p-3.5 rounded-xl bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-900 space-y-1">
                <span class="font-bold text-amber-800 dark:text-amber-200 block text-xs flex items-center gap-1.5">
                  <i class="fa-solid fa-scale-balanced text-amber-600"></i> Plaquetas 70.000 a 100.000 / μL:
                </span>
                <span class="font-black text-amber-600 dark:text-amber-400 block text-xs">Decisão Anestésica Individualizada</span>
                <p class="text-[11px] text-amber-900 dark:text-amber-300 leading-relaxed">
                  Avaliar coagulograma completo e estabilidade do declínio plaquetário. Se raquianestesia for indicada, realizar com agulha ponta-de-lápis fina (27G) e punção única sem trauma. Evitar cateter peridural.
                </p>
              </div>

              <div class="p-3.5 rounded-xl bg-blue-50 dark:bg-blue-950/30 border border-blue-200 dark:border-blue-900 space-y-1">
                <span class="font-bold text-blue-800 dark:text-blue-200 block text-xs flex items-center gap-1.5">
                  <i class="fa-solid fa-droplet text-blue-600"></i> Transfusão de Plaquetas:
                </span>
                <span class="font-black text-blue-600 dark:text-blue-400 block text-xs">1 Unidade a cada 10 kg de Peso</span>
                <p class="text-[11px] text-blue-900 dark:text-blue-300 leading-relaxed">
                  Indicada se plaquetas &lt; 50.000/μL antes de cesariana ou &lt; 20.000/μL antes de parto vaginal. Transfundir 6 a 8 unidades no intraoperatório imediatamente antes do ato cirúrgico para hemostasia efetiva.
                </p>
              </div>
            </div>
          </div>
'''

new_section_5_2_bottom = '''
          <!-- PROTOCOLO DE HIDANTALIZAÇÃO (FENITOÍNA) NA ECLÂMPSIA REFRATÁRIA (SLIDE 31) -->
          <div class="p-5 rounded-2xl bg-slate-900 text-white shadow-xl space-y-3">
            <div class="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800 pb-2">
              <h4 class="text-xs font-black uppercase tracking-wider text-rose-400 flex items-center gap-2">
                <i class="fa-solid fa-brain"></i> Eclâmpsia Refratária ao MgSO4: Protocolo de Hidantalização (Fenitoína) & UTI (Slide 31)
              </h4>
              <span class="px-2.5 py-0.5 rounded text-[10px] font-mono font-bold bg-rose-500/20 text-rose-300 border border-rose-500/30">Convulsão Recorrente</span>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-4 gap-3 text-xs">
              <div class="p-3 rounded-xl bg-slate-800/80 border border-slate-700">
                <span class="text-amber-400 font-bold block mb-1">Passo 1: Bolus de Resgate</span>
                Se a paciente apresentar nova convulsão durante a infusão contínua de MgSO4, administrar dose adicional de <strong>2g de MgSO4 IV em 3 a 5 minutos</strong>.
              </div>
              <div class="p-3 rounded-xl bg-slate-800/80 border border-slate-700">
                <span class="text-rose-400 font-bold block mb-1">Passo 2: Hidantalização IV</span>
                Se a convulsão persistir: <strong>Fenitoína (Hidantal) 15 a 20 mg/kg</strong> (dose usual: <strong>1.250 mg IV</strong> para 60-70 kg) diluída <strong>EXCLUSIVAMENTE em Soro Fisiológico 0,9%</strong> (nunca em SG5% por precipitação maciça).
              </div>
              <div class="p-3 rounded-xl bg-slate-800/80 border border-slate-700">
                <span class="text-blue-400 font-bold block mb-1">Passo 3: Velocidade & Monitorização</span>
                Infundir à velocidade máxima de <strong>50 mg/min</strong> (tempo de infusão ~25 min) com <strong>monitorização contínua de ECG e PA</strong> (risco de bradicardia severa, bloqueio AV e colapso hemodinâmico).
              </div>
              <div class="p-3 rounded-xl bg-slate-800/80 border border-slate-700">
                <span class="text-teal-400 font-bold block mb-1">Passo 4: IOT & Neuroimagem</span>
                Garantir oxigênio 100%, sequência rápida de IOT com ventilação mecânica e solicitar <strong>TC ou Ressonância de Crânio urgente</strong> para investigar AVC, hematoma intraparenquimatoso ou Síndrome PRES.
              </div>
            </div>
          </div>

          <!-- CALCULADORA DE IDADE GESTACIONAL DE INTERRUPÇÃO & ALGORITMO DE VIA DE PARTO (SLIDES 32-33) -->
          <div class="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 space-y-4">
            <div class="flex flex-wrap items-center justify-between gap-2 border-b border-slate-200 dark:border-slate-800 pb-3">
              <div>
                <h4 class="text-sm font-bold uppercase tracking-wider text-slate-900 dark:text-white flex items-center gap-2">
                  <i class="fa-solid fa-baby text-teal-600"></i> Momento da Resolução & Algoritmo de Via de Parto (RBEHG 2025 / Slides 32–33)
                </h4>
                <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                  Idades gestacionais recomendadas para cada perfil clínico e seleção criteriosa da via obstétrica.
                </p>
              </div>
              <span class="px-2.5 py-0.5 rounded text-xs font-mono font-bold bg-teal-500/10 text-teal-700 dark:text-teal-300">RBEHG 2025</span>
            </div>

            <!-- Calculadora Interativa de Idade Gestacional de Resolução -->
            <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/40 border border-slate-200 dark:border-slate-700 space-y-3">
              <label class="block text-xs font-bold uppercase tracking-wider text-slate-700 dark:text-slate-300">
                Selecione o Diagnóstico / Quadro Clínico da Paciente:
              </label>
              <div class="flex flex-col sm:flex-row gap-2">
                <select id="htn-profile-select" onchange="calcHypertensionDeliveryTiming()" class="flex-1 p-2.5 rounded-xl bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 text-xs font-bold text-slate-900 dark:text-white focus:outline-none focus:border-teal-500">
                  <option value="">-- Escolha o Perfil Hipertensivo --</option>
                  <option value="hac_no_med">Hipertensão Arterial Crônica (HAC) Sem Medicação</option>
                  <option value="hac_with_med">Hipertensão Arterial Crônica (HAC) Com Medicação Oral</option>
                  <option value="hag">Hipertensão Gestacional (HAG sem proteinúria)</option>
                  <option value="pe_super_stable">Pré-Eclâmpsia Sobreposta Estável (sem gravidade)</option>
                  <option value="pe_severe_stable">Pré-Eclâmpsia Grave Estabilizada (com corticoterapia prévia)</option>
                  <option value="pe_emergency">Eclâmpsia, Síndrome HELLP ou Sinais de Refratariedade</option>
                </select>
                <button type="button" onclick="calcHypertensionDeliveryTiming()" class="px-4 py-2.5 rounded-xl bg-teal-600 hover:bg-teal-700 text-white font-bold text-xs transition-all cursor-pointer">
                  Ver Conduta
                </button>
              </div>

              <!-- Resultado da IG de Resolução -->
              <div id="htn-delivery-result" class="hidden"></div>
            </div>

            <!-- Fluxograma de Escolha da Via de Parto (Slide 33) -->
            <div class="p-4 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 space-y-2">
              <div class="flex items-center justify-between">
                <span class="text-xs font-black uppercase tracking-wider text-slate-900 dark:text-white flex items-center gap-2">
                  <i class="fa-solid fa-route text-teal-600"></i> Via de Parto nas Síndromes Hipertensivas: Pré-Eclâmpsia NÃO é Indicação Absoluta de Cesariana!
                </span>
                <span class="text-[10px] bg-teal-100 dark:bg-teal-950 text-teal-800 dark:text-teal-300 px-2 py-0.5 rounded font-bold">Diretriz RBEHG 2025</span>
              </div>
              <div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs pt-1">
                <div class="p-3 rounded-xl bg-blue-50/60 dark:bg-blue-950/20 border border-blue-200 dark:border-blue-900/60">
                  <strong class="text-blue-800 dark:text-blue-300 block mb-1">1. Princípio Fundamental</strong>
                  A via de parto é prioritariamente <strong>OBSTÉTRICA</strong>. A indução do parto vaginal é recomendada para gestantes estáveis e com apresentação cefálica, reduzindo hemorragia e riscos cirúrgicos.
                </div>
                <div class="p-3 rounded-xl bg-amber-50/60 dark:bg-amber-950/20 border border-amber-200 dark:border-amber-900/60">
                  <strong class="text-amber-800 dark:text-amber-300 block mb-1">2. Manejo do Colo (Índice de Bishop)</strong>
                  <ul class="text-[11px] space-y-1 mt-1 list-disc list-inside text-slate-700 dark:text-slate-300">
                    <li><strong>Bishop &lt; 6 (Desfavorável):</strong> Preparo mecânico com <strong>Cateter de Foley intracervical</strong> (preferível se cesárea anterior ou CIUR) ou <strong>Misoprostol 25 mcg</strong> vaginal a cada 4-6h (apenas sem cicatriz uterina prévia).</li>
                    <li><strong>Bishop ≥ 6 (Favorável):</strong> Amniotomia precoce + <strong>Ocitocina IV em BIC</strong>.</li>
                  </ul>
                </div>
                <div class="p-3 rounded-xl bg-rose-50/60 dark:bg-rose-950/20 border border-rose-200 dark:border-rose-900/60">
                  <strong class="text-rose-800 dark:text-rose-300 block mb-1">3. Indicações Formais de Cesariana</strong>
                  Sofrimento fetal agudo refratário, apresentação anômala (pélvica / córmica), descolamento prematuro de placenta (DPP) com colo desfavorável, descompensação materna crítica refratária ou falha de indução.
                </div>
              </div>
            </div>
          </div>

          <!-- MANEJO DA HIPERTENSÃO NO PUERPÉRIO & SEGURANÇA FARMACOLÓGICA NA LACTAÇÃO (SLIDE 34) -->
          <div class="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 space-y-4">
            <div class="flex flex-wrap items-center justify-between gap-2 border-b border-slate-200 dark:border-slate-800 pb-3">
              <h4 class="text-sm font-bold uppercase tracking-wider text-slate-900 dark:text-white flex items-center gap-2">
                <i class="fa-solid fa-person-breastfeeding text-teal-600"></i> Manejo Puerperal, Pico Pressórico & Segurança na Lactação (Slide 34)
              </h4>
              <span class="px-2.5 py-0.5 rounded text-xs font-mono font-bold bg-teal-500/10 text-teal-700 dark:text-teal-300">Puerpério & Amamentação</span>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-3 gap-3 text-xs">
              <div class="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700 space-y-2">
                <span class="font-bold text-slate-900 dark:text-white block flex items-center gap-1.5">
                  <i class="fa-solid fa-water text-blue-600"></i> Fenômeno do 3º ao 5º Dia Pós-Parto:
                </span>
                <p class="text-[11px] text-slate-600 dark:text-slate-300 leading-relaxed">
                  A reabsorção maciça de líquidos do terceiro espaço de volta para o compartimento intravascular atinge o pico entre o <strong>3º e 5º dia de puerpério</strong>. Isso causa elevação fisiológica transitória da volemia, com <strong>picos hipertensivos de rebote e risco aumentado de Edema Agudo de Pulmão (EAP)</strong> puerperal.
                </p>
                <div class="p-2 rounded bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-900 text-[11px] text-amber-900 dark:text-amber-200">
                  ⚠️ <strong>Conduta:</strong> Aferir PA a cada 4 horas. Manter MgSO4 nas primeiras 24h pós-parto na PE grave. Meta: <strong>PA &lt; 140/90 mmHg</strong>.
                </div>
              </div>

              <div class="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700 space-y-2">
                <span class="font-bold text-slate-900 dark:text-white block flex items-center gap-1.5">
                  <i class="fa-solid fa-prescription-bottle-medical text-emerald-600"></i> Anti-Hipertensivos Seguros na Lactação:
                </span>
                <ul class="text-[11px] text-slate-600 dark:text-slate-300 space-y-1.5 list-disc list-inside">
                  <li><strong>Enalapril / Captopril:</strong> TOTALMENTE SEGUROS na amamentação! (Passagem mínima no leite materno. A contraindicação gestacional cessa após o parto!).</li>
                  <li><strong>Nifedipino Retard / Amlodipino:</strong> Seguros e altamente eficazes na lactação.</li>
                  <li><strong>Hidralazina:</strong> Segura no puerpério.</li>
                  <li><strong>Betabloqueadores:</strong> Propranolol ou Labetalol são preferidos (menor passagem no leite).</li>
                </ul>
              </div>

              <div class="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700 space-y-2">
                <span class="font-bold text-slate-900 dark:text-white block flex items-center gap-1.5">
                  <i class="fa-solid fa-triangle-exclamation text-rose-600"></i> Drogas a Evitar & Reclassificação:
                </span>
                <ul class="text-[11px] text-slate-600 dark:text-slate-300 space-y-1.5 list-disc list-inside">
                  <li><strong>Metildopa:</strong> Deve ser DESCONTINUADA no pós-parto devido ao risco aumentado de precipitar ou agravar <strong>Depressão Pós-Parto</strong> (efeito sedativo central e depletivo dopaminérgico).</li>
                  <li><strong>Atenolol:</strong> Evitar na lactação (concentra-se no leite materno e pode provocar bradicardia e hipotensão neonatal).</li>
                  <li><strong>Reavaliação Pós-Parto (6 a 12 semanas):</strong> Consulta obrigatória para reclassificação definitiva. Se PA persistir elevada após 12 semanas, firma-se o diagnóstico de <strong>Hipertensão Crônica</strong> prévia subjacente.</li>
                </ul>
              </div>
            </div>
          </div>

        </div>


        <!-- 5.3 HELLP SYNDROME -->
        <div id="modulo-5-hellp" class="p-5 rounded-2xl bg-rose-50 dark:bg-rose-950/20 border border-rose-500/30 space-y-4">
          <div class="flex flex-wrap items-center justify-between gap-2 border-b border-rose-200 dark:border-rose-900/60 pb-3">
            <h4 class="text-base font-black text-rose-900 dark:text-rose-200 flex items-center gap-2">
              <i class="fa-solid fa-heart-crack text-rose-500"></i> Síndrome HELLP: Critérios Diagnósticos Estritos de Tennessee & Classificação de Mississippi
            </h4>
            <span class="px-2.5 py-0.5 rounded text-xs font-black bg-rose-600 text-white">Emergência Materno-Fetal Absoluta</span>
          </div>

          <!-- Tríade Diagnóstica de Tennessee -->
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
            <div class="p-3.5 rounded-xl bg-white dark:bg-slate-900 border border-rose-200 dark:border-rose-900 space-y-1">
              <span class="font-bold text-rose-600 block text-sm">H (Hemolysis)</span>
              <p class="text-slate-700 dark:text-slate-300 text-[11px] leading-relaxed">
                Hemólise microangiopática: Esquizócitos no esfregaço de sangue periférico, Bilirrubina Total <strong>≥ 1,2 mg/dL</strong> (à custa de bilirrubina indireta), Haptoglobina sérica indetectável/baixa e <strong>LDH &gt; 600 U/L</strong>.
              </p>
            </div>
            <div class="p-3.5 rounded-xl bg-white dark:bg-slate-900 border border-rose-200 dark:border-rose-900 space-y-1">
              <span class="font-bold text-rose-600 block text-sm">EL (Elevated Liver)</span>
              <p class="text-slate-700 dark:text-slate-300 text-[11px] leading-relaxed">
                Lesão hepatocelular aguda: TGO (AST) ou TGP (ALT) <strong>≥ 70 U/L</strong> (ou mais que o dobro do limite superior da normalidade). Frequentemente acompanhada de dor persistente em hipocôndrio direito ou epigástrio.
              </p>
            </div>
            <div class="p-3.5 rounded-xl bg-white dark:bg-slate-900 border border-rose-200 dark:border-rose-900 space-y-1">
              <span class="font-bold text-rose-600 block text-sm">LP (Low Platelets)</span>
              <p class="text-slate-700 dark:text-slate-300 text-[11px] leading-relaxed">
                Trombocitopenia por consumo microvascular: Contagem de plaquetas <strong>&lt; 100.000 / μL</strong>.
              </p>
            </div>
          </div>

          <!-- Classificação de Gravidade de Mississippi -->
          <div class="p-3.5 rounded-xl bg-white dark:bg-slate-900 border border-rose-200 dark:border-rose-900/60 space-y-2">
            <span class="text-xs font-bold uppercase tracking-wider text-rose-800 dark:text-rose-300 block">
              Estratificação de Gravidade de Mississippi (Plaquetometria):
            </span>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-2 text-[11px]">
              <div class="p-2.5 rounded-lg bg-rose-50 dark:bg-rose-950/50 border border-rose-300 dark:border-rose-800">
                <strong class="text-rose-700 dark:text-rose-300 block">Classe 1 (Grave / Crítica):</strong>
                Plaquetas &lt; 50.000/μL. Altíssimo risco de CIVD, rotura hepática e óbito materno. Indicação de anestesia geral e transfusão se cirurgia.
              </div>
              <div class="p-2.5 rounded-lg bg-amber-50 dark:bg-amber-950/50 border border-amber-300 dark:border-amber-800">
                <strong class="text-amber-700 dark:text-amber-300 block">Classe 2 (Moderada):</strong>
                Plaquetas entre 50.000 e 100.000/μL. Risco elevado de progressão rápida para classe 1.
              </div>
              <div class="p-2.5 rounded-lg bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700">
                <strong class="text-slate-700 dark:text-slate-300 block">Classe 3 (Incipiente):</strong>
                Plaquetas entre 100.000 e 150.000/μL associadas a LDH &gt; 600 U/L e enzimas hepáticas moderadamente elevadas.
              </div>
            </div>
          </div>

          <!-- Conduta Obstétrica Mandatória -->
          <div class="p-3 rounded-xl bg-rose-600 text-white text-xs font-semibold flex items-center justify-between gap-3">
            <div class="flex items-center gap-2">
              <i class="fa-solid fa-truck-medical text-base"></i>
              <span><strong>Conduta Absoluta:</strong> Estabilização imediata da gestante (Sulfato de Magnésio para neuroproteção materna + Anti-hipertensivo venoso se PA crítica) e <strong>PARTO RESOLUTIVO</strong>. A resolução da gravidez é o único tratamento etiológico definitivo!</span>
            </div>
            <span class="px-2 py-1 rounded bg-white text-rose-700 font-black text-[10px] shrink-0 uppercase">Parto Imediato</span>
          </div>
        </div>

      </div>
    </section>
'''

# Combine the pieces
full_new_content = prefix + new_section_5_2_top + "\n\n          " + existing_mg_block + "\n\n" + new_section_5_2_bottom

with open(comp_file, "w", encoding="utf-8") as f:
    f.write(full_new_content)

print(f"Updated {comp_file} successfully! Total length: {len(full_new_content)} characters.")
