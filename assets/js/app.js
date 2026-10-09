/**
 * Guia de Obstetrícia e Ginecologia - Parte 1
 * Interactive Engine: Calculators, USMLE Quiz, Flashcards, Modal Lightbox, Audio Reader, Search
 */

// --- 1. DUM / NAEGELE & GESTATIONAL AGE CALCULATOR ---
function calculateNaegele() {
  const dumInput = document.getElementById('dum-input').value;
  if (!dumInput) {
    alert('Por favor, selecione a Data da Última Menstruação (DUM).');
    return;
  }

  const dum = new Date(dumInput + 'T00:00:00');
  
  // Regra de Naegele: DUM + 7 dias - 3 meses + 1 ano
  const dpp = new Date(dum);
  dpp.setDate(dpp.getDate() + 7);
  dpp.setMonth(dpp.getMonth() - 3);
  dpp.setFullYear(dpp.getFullYear() + 1);

  // Idade Gestacional Atual
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const diffTime = today - dum;
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
  
  if (diffDays < 0) {
    alert('A DUM informada está no futuro. Por favor, verifique a data.');
    return;
  }

  const weeks = Math.floor(diffDays / 7);
  const remainingDays = diffDays % 7;

  // Determinar Trimestre
  let trimester = '1º Trimestre (0 - 13 sem e 6 dias)';
  let progressPct = Math.min(100, Math.round((diffDays / 280) * 100));
  let recommendations = '';

  if (weeks < 14) {
    trimester = '1º Trimestre (Desenvolvimento Embrionário e Organogênese)';
    recommendations = `
      <ul class="list-disc list-inside space-y-1 text-sm text-slate-700 dark:text-slate-300">
        <li><strong>Exames Obrigatórios:</strong> Tipagem sanguínea + fator Rh, Coombs indireto (se Rh-), Hemograma, Glicemia de jejum, VDRL/RPR, Testes rápidos HIV, HBsAg, Anti-HCV, Toxoplasmose (IgG/IgM), Rubéola, EAS + Urocultura.</li>
        <li><strong>Suplementação:</strong> Ácido Fólico 400 mcg a 5 mg/dia (prevenção de defeitos do tubo neural).</li>
        <li><strong>Ultrassonografia:</strong> USG Transvaginal precoce (6-10 sem) para datação precisa e USG Morfológica de 1º Tri (11-13 sem 6 dias) com medida da <em>Translucência Nucal</em>.</li>
      </ul>
    `;
  } else if (weeks < 28) {
    trimester = '2º Trimestre (Crescimento Fetal e Morfologia)';
    recommendations = `
      <ul class="list-disc list-inside space-y-1 text-sm text-slate-700 dark:text-slate-300">
        <li><strong>Ultrassom Morfológico:</strong> Realizar idealmente entre 20 e 24 semanas para anatomia detalhada e medida do colo uterino.</li>
        <li><strong>Rastreio DMG:</strong> TOTG 75g entre 24 e 28 semanas para todas as gestantes sem diabetes prévio.</li>
        <li><strong>Repetição Laboratorial:</strong> Hemograma e urocultura de controle.</li>
        <li><strong>Vacinação:</strong> Iniciar dTpa a partir da 20ª semana (ideal 27-36 sem).</li>
      </ul>
    `;
  } else {
    trimester = '3º Trimestre (Ganho Ponderal Fetal e Vigilância Pré-Parto)';
    recommendations = `
      <ul class="list-disc list-inside space-y-1 text-sm text-slate-700 dark:text-slate-300">
        <li><strong>Rastreio de Streptococcus agalactiae (GBS):</strong> Swab vaginal e anorretal entre 35 e 37 semanas.</li>
        <li><strong>Sorologias de 3º Tri:</strong> Repetir VDRL, HIV, HBsAg e Urocultura.</li>
        <li><strong>Vigilância de Bem-Estar:</strong> Contagem diária de movimentos fetais (mobilograma) e ausculta de BCF quinzenal/semanal.</li>
        <li><strong>Preparo do Parto:</strong> Elaboração do Plano de Parto e identificação de sinais de alarme (cefaleia, escotomas visuais, sangramento, perda de líquido).</li>
      </ul>
    `;
  }

  // Atualizar DOM
  document.getElementById('result-dpp').innerText = dpp.toLocaleDateString('pt-BR');
  document.getElementById('result-ig').innerText = `${weeks} semanas e ${remainingDays} dias`;
  document.getElementById('result-trimester').innerText = trimester;
  document.getElementById('result-progress-bar').style.width = `${progressPct}%`;
  document.getElementById('result-progress-text').innerText = `${progressPct}% da gestação completada`;
  document.getElementById('result-recommendations').innerHTML = recommendations;

  const resultContainer = document.getElementById('naegele-results');
  resultContainer.classList.remove('hidden');
  resultContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// --- 2. MANNING BIOPHYSICAL PROFILE (PBF) CALCULATOR ---
function calculatePBF() {
  const params = ['pbf-resp', 'pbf-mov', 'pbf-tonus', 'pbf-la', 'pbf-ctg'];
  let totalScore = 0;
  
  params.forEach(id => {
    const val = parseInt(document.getElementById(id).value, 10);
    totalScore += val;
  });

  const scoreEl = document.getElementById('pbf-total-score');
  const badgeEl = document.getElementById('pbf-status-badge');
  const condutaEl = document.getElementById('pbf-conduta');
  const detailEl = document.getElementById('pbf-detail-text');

  scoreEl.innerText = `${totalScore} / 10`;

  let badgeClass = '';
  let badgeText = '';
  let condutaText = '';
  let detailText = '';

  if (totalScore >= 8) {
    badgeClass = 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/30';
    badgeText = 'Normal — Feto Hígido (Sem Asfixia)';
    condutaText = 'Conduta Conservadora. Manter vigilância de rotina conforme o risco gestacional basal.';
    detailText = 'Risco de asfixia fetal ou morte perinatal nas próximas 48-72h é extremamente baixo (< 1/1000). Repetir semanalmente ou a cada 2 semanas se houver indicação clínica.';
  } else if (totalScore === 6) {
    badgeClass = 'bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/30';
    badgeText = 'Equívoco / Suspeito de Hipóxia Crônica';
    condutaText = 'Se gestação a termo (≥ 37 semanas) ou na presença de oligoâmnio (LA = 0), indicar parto. Se pré-termo com LA normal, repetir em 12-24h.';
    detailText = 'Atenção redobrada ao volume de líquido amniótico: oligoâmnio é marcador de hipóxia crônica com redistribuição hemodinâmica renal fetal.';
  } else if (totalScore === 4) {
    badgeClass = 'bg-rose-500/10 text-rose-600 dark:text-rose-400 border-rose-500/30';
    badgeText = 'Anormal — Forte Suspeita de Asfixia Fetal';
    condutaText = 'Se idade gestacional ≥ 32 semanas, resolução imediata da gestação. Se < 32 semanas, internação em UTI obstétrica, corticoterapia para maturação pulmonar e monitorização contínua/Doppler.';
    detailText = 'Elevado risco de desfecho perinatal adverso. Avaliar imediatamente Doppler de artéria umbilical e ducto venoso.';
  } else {
    badgeClass = 'bg-red-600/20 text-red-600 dark:text-red-400 border-red-600/40 animate-pulse';
    badgeText = '🚨 Iminência de Óbito Fetal (Asfixia Crítica)';
    condutaText = 'PARTO IMEDIATO por via mais rápida (geralmente cesárea de emergência), após rápida estabilização materna.';
    detailText = 'Asfixia fetal profunda. A sobrevida fetal depende da extração desimpedida e suporte avançado por neonatologia.';
  }

  badgeEl.className = `inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold border ${badgeClass}`;
  badgeEl.innerText = badgeText;
  condutaEl.innerHTML = `<strong>Conduta Recomendada:</strong> ${condutaText}`;
  detailEl.innerText = detailText;

  document.getElementById('pbf-results').classList.remove('hidden');
}

// --- 3. GDM DIAGNOSTIC TOOL (IADPSG 75g / Carpenter-Coustan) ---
function evaluateGDM() {
  const fasting = parseFloat(document.getElementById('gdm-fasting').value) || 0;
  const h1 = parseFloat(document.getElementById('gdm-1h').value) || 0;
  const h2 = parseFloat(document.getElementById('gdm-2h').value) || 0;

  if (!fasting && !h1 && !h2) {
    alert('Preencha ao menos a glicemia de jejum ou os valores do TOTG.');
    return;
  }

  const resultContainer = document.getElementById('gdm-results');
  let statusHtml = '';

  // Avaliação Inicial no 1º Trimestre (Apenas Jejum)
  if (fasting && !h1 && !h2) {
    if (fasting < 92) {
      statusHtml = `
        <div class="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-700 dark:text-emerald-400">
          <h4 class="font-bold flex items-center gap-2"><i class="fa-solid fa-circle-check"></i> Glicemia de Jejum Normal no 1º Tri (< 92 mg/dL)</h4>
          <p class="text-sm mt-1">Glicemia: <strong>${fasting} mg/dL</strong>. Prossiga com o acompanhamento pré-natal regular e realize o <strong>TOTG 75g entre 24 e 28 semanas</strong>.</p>
        </div>
      `;
    } else if (fasting >= 92 && fasting <= 125) {
      statusHtml = `
        <div class="p-4 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-700 dark:text-amber-400">
          <h4 class="font-bold flex items-center gap-2"><i class="fa-solid fa-triangle-exclamation"></i> Diagnóstico de Diabetes Mellitus Gestacional (DMG)</h4>
          <p class="text-sm mt-1">Glicemia de jejum entre <strong>92 e 125 mg/dL</strong> no 1º trimestre confirma DMG sem necessidade de realizar TOTG posteriormente! Iniciar terapia nutricional, contagem de carboidratos, monitoramento glicêmico capilar 4x/dia e atividade física.</p>
        </div>
      `;
    } else {
      statusHtml = `
        <div class="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-700 dark:text-rose-400">
          <h4 class="font-bold flex items-center gap-2"><i class="fa-solid fa-circle-exclamation"></i> Diagnóstico de Diabetes Mellitus Pré-Gestacional (Overt Diabetes)</h4>
          <p class="text-sm mt-1">Glicemia de jejum <strong>≥ 126 mg/dL</strong> indica diabetes prévio à gestação! Alto risco de malformações congênitas (cardíacas, regressão caudal). Encaminhar imediatamente ao pré-natal de alto risco, solicitar HbA1c, ecocardiograma fetal e fundo de olho.</p>
        </div>
      `;
    }
  } else {
    // Avaliação pelo TOTG 75g (Critérios IADPSG / OMS - 1 valor alterado basta)
    const fastingAlterado = fasting >= 92;
    const h1Alterado = h1 >= 180;
    const h2Alterado = h2 >= 153;
    const countAlterados = (fastingAlterado ? 1 : 0) + (h1Alterado ? 1 : 0) + (h2Alterado ? 1 : 0);

    if (countAlterados >= 1) {
      statusHtml = `
        <div class="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-700 dark:text-rose-400">
          <h4 class="font-bold flex items-center gap-2"><i class="fa-solid fa-circle-exclamation"></i> TOTG 75g Positivo para Diabetes Gestacional (DMG)</h4>
          <p class="text-sm mt-1">Pelo consenso IADPSG/OMS/ACOG, <strong>apenas 1 valor igual ou acima da linha de corte</strong> estabelece o diagnóstico de DMG:</p>
          <ul class="text-xs list-disc list-inside mt-2 space-y-1 font-mono">
            <li class="${fastingAlterado ? 'font-bold text-rose-600 dark:text-rose-300' : 'text-slate-500'}">Jejum: ${fasting} mg/dL (Corte: ≥ 92) ${fastingAlterado ? '🚨 ALTERADO' : '✅ Normal'}</li>
            <li class="${h1Alterado ? 'font-bold text-rose-600 dark:text-rose-300' : 'text-slate-500'}">1 Hora: ${h1} mg/dL (Corte: ≥ 180) ${h1Alterado ? '🚨 ALTERADO' : '✅ Normal'}</li>
            <li class="${h2Alterado ? 'font-bold text-rose-600 dark:text-rose-300' : 'text-slate-500'}">2 Horas: ${h2} mg/dL (Corte: ≥ 153) ${h2Alterado ? '🚨 ALTERADO' : '✅ Normal'}</li>
          </ul>
          <p class="text-xs mt-3 text-slate-700 dark:text-slate-300"><strong>Conduta:</strong> Dieta para DMG + exercício por 2 semanas. Se > 20-30% das medidas capilares estiverem alteradas (Jejum > 95 ou 1h pós-prandial > 140), iniciar <strong>Insulina NPH + Regular</strong>.</p>
        </div>
      `;
    } else {
      statusHtml = `
        <div class="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-700 dark:text-emerald-400">
          <h4 class="font-bold flex items-center gap-2"><i class="fa-solid fa-circle-check"></i> TOTG 75g Normal — Rastreio Negativo</h4>
          <p class="text-sm mt-1">Todos os valores estão dentro da normalidade: Jejum < 92, 1h < 180 e 2h < 153 mg/dL. Continuar acompanhamento habitual.</p>
        </div>
      `;
    }
  }

  resultContainer.innerHTML = statusHtml;
  resultContainer.classList.remove('hidden');
}

// --- 3B. GDM CALCULATOR & CLINICAL TOOLS ---
function calcGestationalWeightGain() {
  const imcInput = parseFloat(document.getElementById('gdm-weight-imc')?.value);
  const resultDiv = document.getElementById('gdm-weight-result');
  if (!imcInput || imcInput <= 0 || !resultDiv) {
    alert('Por favor, informe um valor válido de IMC pré-gestacional.');
    return;
  }

  let cat = '';
  let gain1Tri = '';
  let weeklyRate = '';
  let totalGain = '';
  let badgeColor = '';

  if (imcInput < 18.5) {
    cat = 'Baixo Peso (IMC < 18,5 kg/m²)';
    gain1Tri = '1,0 a 3,0 kg';
    weeklyRate = '0,51 kg/semana (faixa: 0,44 - 0,58 kg/sem)';
    totalGain = '12,5 a 18,0 kg';
    badgeColor = 'text-blue-700 dark:text-blue-300 bg-blue-50 dark:bg-blue-950/40 border-blue-300 dark:border-blue-800';
  } else if (imcInput <= 24.9) {
    cat = 'Eutrófica / Peso Adequado (IMC 18,5 - 24,9 kg/m²)';
    gain1Tri = '1,0 a 3,0 kg';
    weeklyRate = '0,42 kg/semana (faixa: 0,35 - 0,50 kg/sem)';
    totalGain = '11,5 a 16,0 kg';
    badgeColor = 'text-emerald-700 dark:text-emerald-300 bg-emerald-50 dark:bg-emerald-950/40 border-emerald-300 dark:border-emerald-800';
  } else if (imcInput <= 29.9) {
    cat = 'Sobrepeso (IMC 25,0 - 29,9 kg/m²)';
    gain1Tri = '1,0 a 3,0 kg';
    weeklyRate = '0,28 kg/semana (faixa: 0,23 - 0,33 kg/sem)';
    totalGain = '7,0 a 11,5 kg';
    badgeColor = 'text-amber-700 dark:text-amber-300 bg-amber-50 dark:bg-amber-950/40 border-amber-300 dark:border-amber-800';
  } else {
    cat = 'Obesidade (IMC ≥ 30,0 kg/m²)';
    gain1Tri = '0,2 a 2,0 kg';
    weeklyRate = '0,22 kg/semana (faixa: 0,17 - 0,27 kg/sem)';
    totalGain = '5,0 a 9,0 kg';
    badgeColor = 'text-rose-700 dark:text-rose-300 bg-rose-50 dark:bg-rose-950/40 border-rose-300 dark:border-rose-800';
  }

  resultDiv.innerHTML = `
    <div class="p-4 rounded-xl border ${badgeColor} space-y-2 mt-3">
      <div class="flex items-center justify-between">
        <span class="font-bold text-sm">${cat}</span>
        <span class="text-xs font-mono font-bold px-2 py-0.5 rounded bg-white dark:bg-slate-900 border border-current">Tabela 2 SBD / IOM</span>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-2 text-xs font-medium pt-1">
        <div class="p-2.5 rounded-lg bg-white/90 dark:bg-slate-900/90 border border-slate-200 dark:border-slate-800">
          <span class="text-slate-500 dark:text-slate-400 block text-[10px] uppercase font-bold">Até a 14ª semana (1º Tri)</span>
          <strong class="text-slate-800 dark:text-slate-100 text-sm">${gain1Tri}</strong>
        </div>
        <div class="p-2.5 rounded-lg bg-white/90 dark:bg-slate-900/90 border border-slate-200 dark:border-slate-800">
          <span class="text-slate-500 dark:text-slate-400 block text-[10px] uppercase font-bold">Semanal (2º e 3º Tri)</span>
          <strong class="text-slate-800 dark:text-slate-100 text-sm">${weeklyRate}</strong>
        </div>
        <div class="p-2.5 rounded-lg bg-white/90 dark:bg-slate-900/90 border border-slate-200 dark:border-slate-800">
          <span class="text-slate-500 dark:text-slate-400 block text-[10px] uppercase font-bold">Ganho Total Gestacional</span>
          <strong class="text-slate-800 dark:text-slate-100 text-sm">${totalGain}</strong>
        </div>
      </div>
      <p class="text-[11px] text-slate-600 dark:text-slate-300 pt-1 leading-relaxed">
        💡 <strong>Recomendação SBD / FEBRASGO:</strong> Dieta balanceada e atividade física regular de 150 min/semana (30 min 5x/semana de leve a moderada intensidade). 60% das gestantes mantêm-se euglicêmicas sem necessidade de farmacoterapia!
      </p>
    </div>
  `;
  resultDiv.classList.remove('hidden');
}

function calcInsulinDose() {
  const weight = parseFloat(document.getElementById('gdm-insulin-weight')?.value);
  const resultDiv = document.getElementById('gdm-insulin-result');
  if (!weight || weight <= 30 || !resultDiv) {
    alert('Por favor, informe um peso materno válido (em kg).');
    return;
  }

  // Dose inicial padrão: 0,5 UI/kg de peso atual (SBD 2024 / FEBRASGO 2019)
  const totalDose = Math.round(weight * 0.5);
  const doseMorning = Math.round(totalDose * 0.5); // 50% = 1/2 antes do café
  const doseLunch = Math.round(totalDose * 0.25);   // 25% = 1/4 antes do almoço
  const doseBedtime = Math.max(1, totalDose - doseMorning - doseLunch); // 25% = 1/4 às 22h

  resultDiv.innerHTML = `
    <div class="p-4 rounded-xl bg-teal-50 dark:bg-teal-950/40 border border-teal-300 dark:border-teal-800 space-y-3 mt-3">
      <div class="flex flex-wrap items-center justify-between gap-2 border-b border-teal-200 dark:border-teal-800 pb-2">
        <div>
          <span class="text-xs font-bold uppercase text-teal-700 dark:text-teal-300">Prescrição Inicial de Insulina NPH</span>
          <h5 class="text-base font-black text-slate-900 dark:text-white">Dose Total Calculada: ${totalDose} UI/dia (0,5 UI/kg para ${weight} kg)</h5>
        </div>
        <span class="px-2.5 py-1 rounded-md text-xs font-mono font-bold bg-teal-600 text-white">Padrão Ouro SBD 2024</span>
      </div>

      <!-- Fracionamento em 3 tomadas -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5 text-xs">
        <div class="p-3 rounded-lg bg-white dark:bg-slate-900 border border-teal-200 dark:border-teal-900">
          <span class="text-slate-500 dark:text-slate-400 block text-[10px] font-bold uppercase">1/2 Antes do Café da Manhã</span>
          <div class="text-lg font-black text-teal-600 dark:text-teal-400 font-mono">${doseMorning} UI NPH</div>
          <p class="text-[10px] text-slate-500 dark:text-slate-400 mt-0.5">30 min antes da refeição matinal.</p>
        </div>
        <div class="p-3 rounded-lg bg-white dark:bg-slate-900 border border-teal-200 dark:border-teal-900">
          <span class="text-slate-500 dark:text-slate-400 block text-[10px] font-bold uppercase">1/4 Antes do Almoço</span>
          <div class="text-lg font-black text-teal-600 dark:text-teal-400 font-mono">${doseLunch} UI NPH</div>
          <p class="text-[10px] text-slate-500 dark:text-slate-400 mt-0.5">30 min antes do almoço.</p>
        </div>
        <div class="p-3 rounded-lg bg-white dark:bg-slate-900 border border-teal-200 dark:border-teal-900">
          <span class="text-slate-500 dark:text-slate-400 block text-[10px] font-bold uppercase">1/4 às 22h00 (Ao Deitar)</span>
          <div class="text-lg font-black text-teal-600 dark:text-teal-400 font-mono">${doseBedtime} UI NPH</div>
          <p class="text-[10px] text-slate-500 dark:text-slate-400 mt-0.5">Evita hipoglicemia noturna e pico matinal.</p>
        </div>
      </div>

      <div class="p-3 rounded-lg bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-800 text-xs space-y-1 text-amber-900 dark:text-amber-200">
        <div><strong>Picos Pós-Prandiais Insatisfatórios:</strong> Se a glicemia de 1h for ≥ 140 mg/dL ou 2h ≥ 120 mg/dL, introduzir <strong>Insulina Regular</strong> antes da refeição alterada.</div>
        <div><strong>Glicemia de Jejum Inadequada:</strong> Aferir glicemia capilar às 03:00h para diferenciar <em>Fenômeno do Alvorecer</em> (aumentar NPH das 22h) de <em>Efeito Somogyi</em> (reduzir NPH noturna devido à hipoglicemia de rebote).</div>
        <div><strong>Critério USG Fetal (SBD 2024 - R3):</strong> Mesmo com glicemias normais, iniciar insulinoterapia se a Circunferência Abdominal (CA) fetal for ≥ percentil 75 em USG entre a 29ª e 33ª semana!</div>
      </div>
    </div>
  `;
  resultDiv.classList.remove('hidden');
}

// Priscilla White classification data
const priscillaWhiteData = {
  A1: {
    title: 'Classe A1 (DMG Dietético)',
    timing: 'Início na gestação atual',
    duration: 'Gestacional',
    vasculo: 'Sem vasculopatia',
    therapy: 'Não Farmacológica (MEV: Dieta + Atividade Física)',
    prognosis: 'Excelente prognóstico materno-fetal. Resolução a termo com até 40 semanas se bom controle glicêmico.',
    badge: 'DMG Leve'
  },
  A2: {
    title: 'Classe A2 (DMG Farmacológico)',
    timing: 'Início na gestação atual',
    duration: 'Gestacional',
    vasculo: 'Sem vasculopatia',
    therapy: 'Farmacológica (Insulina NPH ± Regular)',
    prognosis: 'Requer vigilância da vitalidade fetal semanal a partir de 32 semanas. Parto entre 38 e 39+6 semanas.',
    badge: 'DMG com Insulina'
  },
  B: {
    title: 'Classe B (DM Prévio Inicial)',
    timing: 'Início com idade ≥ 20 anos',
    duration: '< 10 anos de doença',
    vasculo: 'Sem vasculopatia detectável',
    therapy: 'Farmacológica (Insulina)',
    prognosis: 'Risco de malformações congênitas se descontrole periconcepcional (HbA1c > 6,5%). USG morfológica e ecocardiograma fetal.',
    badge: 'DM Prévio'
  },
  C: {
    title: 'Classe C (DM Prévio Intermediário)',
    timing: 'Início entre 10 e 19 anos',
    duration: '10 a 19 anos de doença',
    vasculo: 'Sem vasculopatia clínica estabelecida',
    therapy: 'Farmacológica (Insulina)',
    prognosis: 'Maior necessidade de insulina no 2º e 3º trimestres por resistência fisiológica aumentada.',
    badge: 'DM Prévio'
  },
  D: {
    title: 'Classe D (DM Prévio de Longa Duração)',
    timing: 'Início com < 10 anos de idade',
    duration: '> 20 anos de doença',
    vasculo: 'Retinopatia Simples (Background) ou Calcificação vascular',
    therapy: 'Farmacológica (Insulina)',
    prognosis: 'Alto risco de pré-eclâmpsia sobreposta e CIUR por vasculopatia. Dopplervelocimetria de artérias umbilicais seriada.',
    badge: 'Vasculopatia Inicial'
  },
  E: {
    title: 'Classe E (Calcificação Pélvica)',
    timing: 'DM prévio com vasculopatia',
    duration: 'Longa data',
    vasculo: 'Calcificação das artérias ilíacas e pélvicas ao RX',
    therapy: 'Farmacológica (Insulina)',
    prognosis: 'Classificação histórica, indicando aterosclerose acelerada e fluxo uteroplacentário reduzido.',
    badge: 'Histórica'
  },
  F: {
    title: 'Classe F (Nefropatia Diabética)',
    timing: 'DM prévio',
    duration: 'Variável',
    vasculo: 'Nefropatia com proteinúria > 500 mg/dia ou microalbuminúria',
    therapy: 'Farmacológica (Insulina)',
    prognosis: 'Risco de até 50% de pré-eclâmpsia sobreposta, prematuridade e CIUR grave. Prescrever AAS precoce e vigiar função renal.',
    badge: 'Alto Risco Renal'
  },
  R: {
    title: 'Classe R (Retinopatia Proliferativa)',
    timing: 'DM prévio',
    duration: 'Variável',
    vasculo: 'Retinopatia Proliferativa ou Hemorragia vítrea',
    therapy: 'Farmacológica (Insulina)',
    prognosis: 'Risco de progressão rápida e amaurose na gestação. A fotocoagulação a laser NÃO é contraindicada na gravidez.',
    badge: 'Alto Risco Oftalmo'
  },
  H: {
    title: 'Classe H (Cardiopatia Isquêmica)',
    timing: 'DM prévio',
    duration: 'Variável',
    vasculo: 'Doença arterial coronariana comprovada (Infarto / Angina prévia)',
    therapy: 'Farmacológica (Insulina)',
    prognosis: 'Mortalidade materna elevada (10 a 20%). Aconselhamento periconcepcional rigoroso e acompanhamento cardiológico conjunto.',
    badge: 'Risco Crítico'
  },
  T: {
    title: 'Classe T (Transplante Renal Prévio)',
    timing: 'DM prévio pós-transplante',
    duration: 'Variável',
    vasculo: 'Transplante renal prévio funcional',
    therapy: 'Farmacológica (Insulina + Imunossupressores)',
    prognosis: 'Gestação de altíssimo risco. Vigilância de rejeição de enxerto, toxicidade farmacológica e infecções oportunistas.',
    badge: 'Transplantada'
  }
};

function selectPriscillaWhite(key) {
  const item = priscillaWhiteData[key];
  const display = document.getElementById('pw-detail-card');
  if (!item || !display) return;

  Object.keys(priscillaWhiteData).forEach(k => {
    const btn = document.getElementById(`pw-btn-${k}`);
    if (btn) {
      if (k === key) {
        btn.className = 'pw-btn px-3 py-2 rounded-xl text-xs font-bold border transition-all bg-teal-600 text-white border-teal-600 shadow-md cursor-pointer';
      } else {
        btn.className = 'pw-btn px-3 py-2 rounded-xl text-xs font-bold border transition-all bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 border-slate-200 dark:border-slate-700 hover:border-teal-500 cursor-pointer';
      }
    }
  });

  display.innerHTML = `
    <div class="p-4 rounded-2xl bg-white dark:bg-slate-900 border border-teal-500/30 shadow-lg space-y-3">
      <div class="flex flex-wrap items-center justify-between gap-2 border-b border-slate-200 dark:border-slate-800 pb-2">
        <h5 class="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
          <i class="fa-solid fa-ribbon text-teal-600"></i> ${item.title}
        </h5>
        <span class="px-2.5 py-1 rounded-md text-xs font-bold bg-teal-100 dark:bg-teal-950 text-teal-700 dark:text-teal-300 border border-teal-300 dark:border-teal-800">
          ${item.badge}
        </span>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-2 text-xs">
        <div class="p-2.5 rounded-lg bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700">
          <span class="text-slate-400 block text-[10px] uppercase font-bold">Início da Doença</span>
          <span class="font-semibold text-slate-800 dark:text-slate-200">${item.timing}</span>
        </div>
        <div class="p-2.5 rounded-lg bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700">
          <span class="text-slate-400 block text-[10px] uppercase font-bold">Duração</span>
          <span class="font-semibold text-slate-800 dark:text-slate-200">${item.duration}</span>
        </div>
        <div class="p-2.5 rounded-lg bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700">
          <span class="text-slate-400 block text-[10px] uppercase font-bold">Vasculopatia</span>
          <span class="font-semibold text-slate-800 dark:text-slate-200">${item.vasculo}</span>
        </div>
        <div class="p-2.5 rounded-lg bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700">
          <span class="text-slate-400 block text-[10px] uppercase font-bold">Terapêutica Indicada</span>
          <span class="font-bold text-teal-600 dark:text-teal-400">${item.therapy}</span>
        </div>
      </div>
      <p class="text-xs text-slate-600 dark:text-slate-300 bg-slate-50 dark:bg-slate-800/60 p-3 rounded-xl border border-slate-200 dark:border-slate-700 leading-relaxed">
        <strong>Prognóstico & Conduta Obstétrica:</strong> ${item.prognosis}
      </p>
    </div>
  `;
}

// Switch between Total vs Partial GDM screening flowcharts
function switchGdmStrategy(strategy) {
  const totalPanel = document.getElementById('gdm-strategy-total');
  const partialPanel = document.getElementById('gdm-strategy-partial');
  const btnTotal = document.getElementById('btn-strategy-total');
  const btnPartial = document.getElementById('btn-strategy-partial');

  if (strategy === 'total') {
    if (totalPanel) totalPanel.classList.remove('hidden');
    if (partialPanel) partialPanel.classList.add('hidden');
    if (btnTotal) btnTotal.className = 'px-4 py-2 rounded-xl text-xs font-bold bg-teal-600 text-white shadow-md cursor-pointer';
    if (btnPartial) btnPartial.className = 'px-4 py-2 rounded-xl text-xs font-bold bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-300 cursor-pointer';
  } else {
    if (totalPanel) totalPanel.classList.add('hidden');
    if (partialPanel) partialPanel.classList.remove('hidden');
    if (btnPartial) btnPartial.className = 'px-4 py-2 rounded-xl text-xs font-bold bg-teal-600 text-white shadow-md cursor-pointer';
    if (btnTotal) btnTotal.className = 'px-4 py-2 rounded-xl text-xs font-bold bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-300 cursor-pointer';
  }
}

// --- 3C. HYPERTENSION RISK & DELIVERY TIMING TOOLS ---
function calcPreeclampsiaRisk() {
  const highRisks = [
    document.getElementById('pe-risk-prev')?.checked,
    document.getElementById('pe-risk-multi')?.checked,
    document.getElementById('pe-risk-obese')?.checked,
    document.getElementById('pe-risk-hac')?.checked,
    document.getElementById('pe-risk-dm')?.checked,
    document.getElementById('pe-risk-ckd')?.checked,
    document.getElementById('pe-risk-auto')?.checked,
    document.getElementById('pe-risk-fiv')?.checked
  ].filter(Boolean).length;

  const modRisks = [
    document.getElementById('pe-risk-nuli')?.checked,
    document.getElementById('pe-risk-fam')?.checked,
    document.getElementById('pe-risk-age')?.checked,
    document.getElementById('pe-risk-interv')?.checked,
    document.getElementById('pe-risk-socio')?.checked,
    document.getElementById('pe-risk-race')?.checked,
    document.getElementById('pe-risk-adverse')?.checked
  ].filter(Boolean).length;

  const resultDiv = document.getElementById('pe-risk-result');
  if (!resultDiv) return;

  const isIndicated = (highRisks >= 1) || (modRisks >= 2);

  if (isIndicated) {
    resultDiv.innerHTML = `
      <div class="p-4 rounded-xl bg-rose-50 dark:bg-rose-950/40 border border-rose-300 dark:border-rose-800 space-y-2 mt-3">
        <div class="flex flex-wrap items-center justify-between gap-2">
          <span class="font-black text-rose-700 dark:text-rose-300 text-sm flex items-center gap-2">
            <i class="fa-solid fa-triangle-exclamation"></i> Alto Risco Clínico para Pré-Eclâmpsia Identificado
          </span>
          <span class="px-2.5 py-0.5 rounded text-xs font-bold bg-rose-600 text-white">Quadro 6 RBEHG / FEBRASGO</span>
        </div>
        <p class="text-xs text-rose-900 dark:text-rose-200">
          Identificados <strong>${highRisks} fator(es) de alto risco</strong> e <strong>${modRisks} fator(es) de risco moderado</strong>. Há indicação formal de farmacoprofilaxia secundária:
        </p>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs pt-1">
          <div class="p-3 rounded-lg bg-white dark:bg-slate-900 border border-rose-200 dark:border-rose-900">
            <strong class="text-rose-600 dark:text-rose-400 block mb-1">1. Aspirina em Baixas Doses (AAS 100 a 150 mg/dia)</strong>
            Iniciar preferencialmente entre a <strong>12ª e 16ª semana</strong> de gestação (máximo 20 sem) em dose única noturna (ao deitar). Suspender com <strong>36 semanas</strong>.
          </div>
          <div class="p-3 rounded-lg bg-white dark:bg-slate-900 border border-rose-200 dark:border-rose-900">
            <strong class="text-rose-600 dark:text-rose-400 block mb-1">2. Carbonato de Cálcio (1,5 a 2,0 g/dia)</strong>
            Iniciar a partir da <strong>12ª semana</strong> em doses fracionadas até o parto para gestantes com ingesta alimentar deficiente de cálcio.
          </div>
        </div>
        <p class="text-[11px] text-slate-600 dark:text-slate-400 pt-1">
          🔍 <strong>Doppler de Artérias Uterinas:</strong> Avaliar na morfológica de 1º trimestre (11 a 14 semanas). Persistência de incisura bilateral e índice de pulsatilidade (IP) aumentado predizem alta resistência trofoblástica.
        </p>
      </div>
    `;
  } else {
    resultDiv.innerHTML = `
      <div class="p-4 rounded-xl bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-300 dark:border-emerald-800 space-y-1 mt-3">
        <h5 class="font-bold text-emerald-800 dark:text-emerald-300 text-sm flex items-center gap-2">
          <i class="fa-solid fa-circle-check"></i> Risco Habitual / Baixo Risco de Pré-Eclâmpsia
        </h5>
        <p class="text-xs text-emerald-900 dark:text-emerald-200">
          Critérios de alto risco ausentes e menos de 2 fatores moderados identificados (${modRisks} selecionado). Não há indicação rotineira de AAS preventivo. Manter pré-natal habitual, aferição pressórica em todas as consultas e orientações de hábitos saudáveis.
        </p>
      </div>
    `;
  }
  resultDiv.classList.remove('hidden');
}

function calcHypertensionDeliveryTiming() {
  const selectVal = document.getElementById('htn-profile-select')?.value;
  const resultDiv = document.getElementById('htn-delivery-result');
  if (!selectVal || !resultDiv) return;

  const data = {
    hac_no_med: {
      title: 'Hipertensão Arterial Crônica (HAC) Sem Medicação',
      weeks: '38 a 40 semanas',
      route: 'Indução do parto vaginal preferível se feto cefálico e condições favoráveis.',
      notes: 'Avaliar vitalidade fetal a termo. Cesariana apenas por indicações obstétricas.',
      color: 'emerald'
    },
    hac_with_med: {
      title: 'Hipertensão Arterial Crônica (HAC) Com Medicação Anti-Hipertensiva',
      weeks: 'A partir de 37 semanas (37 a 38 semanas)',
      route: 'Indução do parto vaginal recomendada. Se Bishop desfavorável, preparo de colo com Foley ou Misoprostol.',
      notes: 'Não ultrapassar 39 semanas devido ao risco aumentado de insuficiência placentária e óbito fetal.',
      color: 'blue'
    },
    hag: {
      title: 'Hipertensão Gestacional (HAG sem proteinúria nem gravidade)',
      weeks: 'A partir de 37 semanas completas',
      route: 'Preferível parto vaginal por indução.',
      notes: 'Expectante até 37 semanas se estável. Não utilizar Sulfato de Magnésio se não houver critérios de gravidade.',
      color: 'blue'
    },
    pe_super_stable: {
      title: 'Pré-Eclâmpsia Sobreposta Estável (Sem Sinais de Gravidade)',
      weeks: '37 semanas (ou até 34 semanas se conservadora)',
      route: 'Parto vaginal preferível.',
      notes: 'Se deterioração clínica, piora laboratorial ou alteração de vitalidade fetal, interrupção imediata.',
      color: 'amber'
    },
    pe_severe_stable: {
      title: 'Pré-Eclâmpsia Grave Estabilizada (Sem Refratariedade)',
      weeks: '34 semanas completas',
      route: 'Parto vaginal ou cesariano conforme estabilidade materna e vitalidade fetal.',
      notes: 'Internação hospitalar, corticoterapia antenatal (24-34 semanas) e sulfato de magnésio profilático.',
      color: 'rose'
    },
    pe_emergency: {
      title: 'Eclâmpsia, Síndrome HELLP ou Condições de Alto Risco Refratárias',
      weeks: 'IMEDIATAMENTE após estabilização materna (Qualquer IG)',
      route: 'Parto cesáreo rápido se sofrimento fetal / colo desfavorável / sangramento, ou vaginal se viável e rápido.',
      notes: 'Chamar ajuda, via aérea, O2, MgSO4 até 24h pós-parto, hidralazina se PA ≥ 160x110. A anestesia é GERAL se plaquetas < 70.000/mm³!',
      color: 'rose'
    }
  };

  const item = data[selectVal];
  if (!item) return;

  resultDiv.innerHTML = `
    <div class="p-4 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-md space-y-2 mt-3">
      <div class="flex flex-wrap items-center justify-between gap-2 border-b border-slate-200 dark:border-slate-800 pb-2">
        <h5 class="text-sm font-bold text-slate-900 dark:text-white">${item.title}</h5>
        <span class="px-2.5 py-1 rounded text-xs font-mono font-black bg-teal-500/10 text-teal-700 dark:text-teal-300 border border-teal-500/30">
          Parto: ${item.weeks}
        </span>
      </div>
      <p class="text-xs text-slate-700 dark:text-slate-300">
        <strong>Via de Parto Recomendada:</strong> ${item.route}
      </p>
      <p class="text-[11px] text-slate-500 dark:text-slate-400 bg-slate-50 dark:bg-slate-800 p-2.5 rounded-lg border border-slate-200 dark:border-slate-700 leading-relaxed">
        📌 <strong>Diretriz RBEHG 2025 / FEBRASGO:</strong> ${item.notes}
      </p>
    </div>
  `;
  resultDiv.classList.remove('hidden');
}

function checkPreeclampsiaOrganDysfunction() {
  const selected = [
    document.getElementById('org-dys-hemo')?.checked ? 'Hematológico (Plaquetas ≤ 150.000, CIVD, hemólise)' : null,
    document.getElementById('org-dys-hep')?.checked ? 'Hepático (TGO ou TGP ≥ 40 UI/L, dor em HCD/epigástrio)' : null,
    document.getElementById('org-dys-ren')?.checked ? 'Renal (Creatinina sérica ≥ 1,0 mg/dL)' : null,
    document.getElementById('org-dys-neuro')?.checked ? 'Neurológico (Eclâmpsia, sineclâmpsia, amaurose, cefaleia refratária, escotomas)' : null,
    document.getElementById('org-dys-pulm')?.checked ? 'Edema Pulmonar agudo' : null,
    document.getElementById('org-dys-plac')?.checked ? 'Placentário (CIUR, Doppler de artéria umbilical alterado, DPP, óbito fetal)' : null
  ].filter(Boolean);

  const resultDiv = document.getElementById('org-dys-result');
  if (!resultDiv) return;

  if (selected.length > 0) {
    resultDiv.innerHTML = `
      <div class="p-4 rounded-xl bg-rose-50 dark:bg-rose-950/40 border border-rose-300 dark:border-rose-800 space-y-2 mt-3">
        <h5 class="text-sm font-bold text-rose-800 dark:text-rose-200 flex items-center gap-2">
          <i class="fa-solid fa-triangle-exclamation"></i> Diagnóstico Confirmado de Pré-Eclâmpsia (ISSHP 2022 / FEBRASGO)
        </h5>
        <p class="text-xs text-rose-900 dark:text-rose-200">
          Na presença de hipertensão arterial após 20 semanas, <strong>a proteinúria NÃO é mais obrigatória</strong> se houver comprometimento de órgão-alvo. Foram identificados ${selected.length} critério(s):
        </p>
        <ul class="text-xs list-disc list-inside space-y-1 font-semibold text-rose-800 dark:text-rose-300">
          ${selected.map(s => `<li>${s}</li>`).join('')}
        </ul>
        <p class="text-xs font-bold text-slate-800 dark:text-slate-200 pt-1">
          🚨 <strong>Conduta:</strong> Internação hospitalar imediata, monitorização materno-fetal, exames laboratoriais seriados, sulfato de magnésio se critérios de gravidade e definição da idade gestacional para resolução!
        </p>
      </div>
    `;
  } else {
    resultDiv.innerHTML = `
      <div class="p-4 rounded-xl bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-xs text-slate-600 dark:text-slate-300 mt-3">
        Nenhum critério de disfunção orgânica selecionado. Se a paciente apresentar proteinúria significativa (≥ 300 mg/24h ou P/C > 0,3), o diagnóstico de Pré-Eclâmpsia clássica é estabelecido. Caso contrário e sem gravidade, classifica-se como <strong>Hipertensão Gestacional</strong>.
      </div>
    `;
  }
  resultDiv.classList.remove('hidden');
}

// Renal adjustment toggle for MgSO4
function toggleMgRenalAdjustment(isRenal) {
  if (isRenal) {
    const baseRate = getCurrentMgBicRate();
    currentMgState.bicRateOverride = baseRate * 0.5;
  } else {
    currentMgState.bicRateOverride = null;
  }
  updateMgAllViews();
}

// --- 4. MAGNESIUM SULFATE (MgSO4) PROTOCOLS, DILUTIONS, BIC & TOXICITY ---
const mgProtocols = {
  zuspan1: {
    id: 'zuspan1',
    name: 'Zuspan Padrão (1 g/h)',
    subtitle: 'Padrão-Ouro FEBRASGO / ACOG / OMS',
    indication: 'Prevenção e Tratamento da Eclâmpsia em Pré-Eclâmpsia com Sinais de Gravidade',
    badge: 'Padrão Ouro (1 g/h)',
    isIM: false,
    attackGrams: 4,
    attackTimeMin: 20,
    maintGramsPerHour: 1.0,
    durationHours: 24,
    notes: 'Manter infusão contínua em BIC por 24 horas após o parto ou 24 horas após a última crise convulsiva (o que ocorrer por último).'
  },
  zuspan2: {
    id: 'zuspan2',
    name: 'Zuspan Reforçado (2 g/h)',
    subtitle: 'ACOG / Obesas / Gravidade Acentuada',
    indication: 'Pacientes com IMC elevado (> 35 kg/m²), sintomas premonitórios persistentes ou refratariedade inicial',
    badge: 'ACOG Reforçado (2 g/h)',
    isIM: false,
    attackGrams: 4,
    attackTimeMin: 20,
    maintGramsPerHour: 2.0,
    durationHours: 24,
    notes: 'Requer vigilância intensificada dos reflexos tendinosos e diurese horária devido a níveis séricos mais próximos do limiar superior.'
  },
  sibai: {
    id: 'sibai',
    name: 'Protocolo de Sibai (6g + 2 g/h)',
    subtitle: 'Ataque Expandido 6g + BIC 2 g/h',
    indication: 'Eclâmpsia ativa com crises frequentes ou iminência crítica com vasoespasmo severo',
    badge: 'Sibai (6g Bolus)',
    isIM: false,
    attackGrams: 6,
    attackTimeMin: 25,
    maintGramsPerHour: 2.0,
    durationHours: 24,
    notes: 'Ataque de 6g em 20-30 min garante estabilização terapêutica ultrarrápida em situações de alto risco convulsivo.'
  },
  pritchard: {
    id: 'pritchard',
    name: 'Protocolo de Pritchard (IM / Misto)',
    subtitle: 'Ataque IV+IM + Manutenção 5g IM 4/4h (Sem BIC)',
    indication: 'Maternidades sem bomba de infusão contínua, transferências inter-hospitalares e perda de acesso venoso central',
    badge: 'Esquema IM (Sem BIC)',
    isIM: true,
    attackGrams: 14, // 4g IV + 10g IM
    attackTimeMin: 20,
    maintGramsPerHour: 1.25, // 5g a cada 4h
    durationHours: 24,
    notes: 'Injeção IM profunda em nádegas (agulha 40x12) com 1 mL de Lidocaína 2% sem vasoconstritor em cada aplicação para analgesia local intensa.'
  },
  neuro: {
    id: 'neuro',
    name: 'Neuroproteção Fetal (< 32 semanas)',
    subtitle: 'Prevenção de Paralisia Cerebral e Transtornos Motores',
    indication: 'Gestação entre 24 e 31+6 semanas com parto prematuro iminente previsto nas próximas 2 a 24 horas',
    badge: 'Neuroproteção (<32s)',
    isIM: false,
    attackGrams: 4,
    attackTimeMin: 30,
    maintGramsPerHour: 1.0,
    durationHours: 12,
    notes: 'Descontinuar se as contrações cessarem ou no nascimento do feto. Não ultrapassar o limite recomendado de 12 a 24h contínuas.'
  },
  recorrencia: {
    id: 'recorrencia',
    name: 'Recorrência de Crise Convulsiva',
    subtitle: 'Bolus de Resgate 2g IV + Ajuste de BIC',
    indication: 'Paciente em uso regular de MgSO4 que apresenta nova convulsão tônico-clônica durante a infusão',
    badge: 'Resgate de Crise (Bolus 2g)',
    isIM: false,
    attackGrams: 2,
    attackTimeMin: 5,
    maintGramsPerHour: 2.0,
    durationHours: 24,
    notes: 'Administrar 2g IV lento em 3-5 minutos. Elevar a BIC para 2 g/h. Se crises persistirem após 2 bolus, associar Diazepam ou Fenitoína e providenciar via aérea definitiva.'
  }
};

const mgDilutionBags = {
  padrao: {
    id: 'padrao',
    name: 'Bolsa Padrão (10g em 500 mL)',
    soluteGrams: 10,
    totalVolumeMl: 500,
    diluentType: 'Soro Glicosado 5% (SG 5%) ou SF 0,9%',
    concentrationMgMl: 20, // 20 mg/mL = 0.02 g/mL
    ampoules50: 2,
    ampoules10: 10,
    diluentVolume50: 480,
    diluentVolume10: 400
  },
  concentrada: {
    id: 'concentrada',
    name: 'Bolsa Concentrada (20g em 500 mL)',
    soluteGrams: 20,
    totalVolumeMl: 500,
    diluentType: 'Soro Glicosado 5% (SG 5%)',
    concentrationMgMl: 40, // 40 mg/mL = 0.04 g/mL
    ampoules50: 4,
    ampoules10: 20,
    diluentVolume50: 460,
    diluentVolume10: 300
  },
  restricao: {
    id: 'restricao',
    name: 'Restrição Hídrica (10g em 250 mL)',
    soluteGrams: 10,
    totalVolumeMl: 250,
    diluentType: 'Soro Glicosado 5% (SG 5%)',
    concentrationMgMl: 40, // 40 mg/mL = 0.04 g/mL
    ampoules50: 2,
    ampoules10: 10,
    diluentVolume50: 230,
    diluentVolume10: 150
  }
};

let currentMgState = {
  protocolKey: 'zuspan1',
  ampouleType: '50', // '50' (50% 10 mL = 5g) ou '10' (10% 10 mL = 1g)
  bagKey: 'padrao',
  bicRunning: true,
  bicRateOverride: null,
  startTime: '14:00',
  toxicityLevel: 5.0
};

function selectMgProtocol(key) {
  if (!mgProtocols[key]) return;
  currentMgState.protocolKey = key;
  currentMgState.bicRateOverride = null; // reseta ajuste manual para preset oficial
  updateMgAllViews();
}

function setMgAmpoule(type) {
  currentMgState.ampouleType = type;
  updateMgAllViews();
}

function setMgBag(key) {
  if (!mgDilutionBags[key]) return;
  currentMgState.bagKey = key;
  currentMgState.bicRateOverride = null;
  updateMgAllViews();
}

function adjustMgBicRate(delta) {
  const currentRate = getCurrentMgBicRate();
  const newRate = Math.max(5, Math.min(250, currentRate + delta));
  currentMgState.bicRateOverride = newRate;
  updateMgAllViews();
}

function setMgBicRatePreset(rate) {
  currentMgState.bicRateOverride = rate;
  updateMgAllViews();
}

function toggleMgBicRun() {
  currentMgState.bicRunning = !currentMgState.bicRunning;
  updateMgBicDisplay();
}

function onMgStartTimeChange(val) {
  if (val) {
    currentMgState.startTime = val;
    renderMgSchedule();
    updateMgPrescription();
  }
}

function setMgStartTimeNow() {
  const now = new Date();
  const hh = String(now.getHours()).padStart(2, '0');
  const mm = String(now.getMinutes()).padStart(2, '0');
  currentMgState.startTime = `${hh}:${mm}`;
  const input = document.getElementById('mg-start-time');
  if (input) input.value = currentMgState.startTime;
  renderMgSchedule();
  updateMgPrescription();
}

function getCurrentMgBicRate() {
  if (currentMgState.bicRateOverride !== null) {
    return currentMgState.bicRateOverride;
  }
  const protocol = mgProtocols[currentMgState.protocolKey];
  const bag = mgDilutionBags[currentMgState.bagKey];
  const concGPerMl = bag.soluteGrams / bag.totalVolumeMl;
  return protocol.maintGramsPerHour / concGPerMl;
}

function updateMgAllViews() {
  const protocol = mgProtocols[currentMgState.protocolKey];
  const bag = mgDilutionBags[currentMgState.bagKey];
  const isAmp50 = currentMgState.ampouleType === '50';

  // 1. Atualizar Abas de Protocolo
  Object.keys(mgProtocols).forEach(key => {
    const tab = document.getElementById(`mg-tab-${key}`);
    if (tab) {
      if (key === currentMgState.protocolKey) {
        tab.className = 'protocol-tab p-3 rounded-xl border text-left transition-all cursor-pointer bg-teal-500/10 dark:bg-teal-950/40 border-teal-500 text-teal-800 dark:text-teal-200 shadow-sm';
      } else {
        tab.className = 'protocol-tab p-3 rounded-xl border border-slate-200 dark:border-slate-800 text-left transition-all cursor-pointer hover:bg-slate-100 dark:hover:bg-slate-800/60 text-slate-700 dark:text-slate-300';
      }
    }
  });

  // 2. Atualizar Seleção de Ampola
  const btnAmp50 = document.getElementById('mg-ampoule-50');
  const btnAmp10 = document.getElementById('mg-ampoule-10');
  if (btnAmp50 && btnAmp10) {
    if (isAmp50) {
      btnAmp50.className = 'px-3 py-2 rounded-lg border text-xs font-bold transition-all text-center cursor-pointer bg-teal-500/10 dark:bg-teal-950/40 border-teal-500 text-teal-700 dark:text-teal-300';
      btnAmp10.className = 'px-3 py-2 rounded-lg border border-slate-200 dark:border-slate-700 text-xs font-bold transition-all text-center cursor-pointer text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800';
    } else {
      btnAmp10.className = 'px-3 py-2 rounded-lg border text-xs font-bold transition-all text-center cursor-pointer bg-teal-500/10 dark:bg-teal-950/40 border-teal-500 text-teal-700 dark:text-teal-300';
      btnAmp50.className = 'px-3 py-2 rounded-lg border border-slate-200 dark:border-slate-700 text-xs font-bold transition-all text-center cursor-pointer text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800';
    }
  }

  // 3. Atualizar Seleção de Bolsa
  Object.keys(mgDilutionBags).forEach(key => {
    const btn = document.getElementById(`mg-bag-${key}`);
    if (btn) {
      if (key === currentMgState.bagKey) {
        btn.className = 'px-2 py-2 rounded-lg border text-[11px] font-bold transition-all text-center cursor-pointer bg-teal-500/10 dark:bg-teal-950/40 border-teal-500 text-teal-700 dark:text-teal-300';
      } else {
        btn.className = 'px-2 py-2 rounded-lg border border-slate-200 dark:border-slate-700 text-[11px] font-bold transition-all text-center cursor-pointer text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800';
      }
    }
  });

  // 4. Detalhes da Dose de Ataque
  const attackBadge = document.getElementById('mg-attack-badge-grams');
  const attackHeadline = document.getElementById('mg-attack-headline');
  const attackIndication = document.getElementById('mg-attack-indication-text');
  const attackSolute = document.getElementById('mg-attack-solute-detail');
  const attackDiluent = document.getElementById('mg-attack-diluent-detail');
  const attackVolTotal = document.getElementById('mg-attack-vol-total');
  const attackAdminMode = document.getElementById('mg-attack-administration-mode');
  const pritchardAttackBox = document.getElementById('mg-pritchard-attack-im-box');
  const attackFooterTip = document.getElementById('mg-attack-footer-tip');

  if (attackBadge) attackBadge.innerText = `${protocol.attackGrams} g ${protocol.isIM ? 'Misto IV+IM' : 'IV'}`;
  if (attackHeadline) {
    if (protocol.id === 'recorrencia') {
      attackHeadline.innerText = 'Bolus Adicional de Resgate (2g IV Lento)';
    } else if (protocol.id === 'sibai') {
      attackHeadline.innerText = 'Bolus Inicial Expandido (6g IV em 25 min)';
    } else if (protocol.id === 'pritchard') {
      attackHeadline.innerText = 'Ataque Misto: 4g IV + 10g IM Profundo';
    } else {
      attackHeadline.innerText = 'Ataque Intravenoso Padrão (4g IV em 20 min)';
    }
  }
  if (attackIndication) attackIndication.innerText = protocol.indication;

  if (isAmp50) {
    if (protocol.id === 'recorrencia') {
      if (attackSolute) attackSolute.innerText = `4 mL de MgSO₄ 50% (0,4 ampola = 2g)`;
      if (attackDiluent) attackDiluent.innerText = `16 mL de SG 5% ou AD`;
      if (attackVolTotal) attackVolTotal.innerText = `20 mL em seringa IV lenta`;
      if (attackAdminMode) attackAdminMode.innerHTML = `Infundir <strong>IV lento em 3 a 5 minutos</strong> diretamente na via venosa sob monitorização contínua.`;
      if (attackFooterTip) attackFooterTip.innerText = `Avaliar imediatamente saturação de O2, reflexo patelar e preparar oxigênio com máscara.`;
    } else if (protocol.id === 'sibai') {
      if (attackSolute) attackSolute.innerText = `12 mL de MgSO₄ 50% (1,2 ampola = 6g)`;
      if (attackDiluent) attackDiluent.innerText = `88 mL de Soro Glicosado 5%`;
      if (attackVolTotal) attackVolTotal.innerText = `100 mL em mini-bolsa`;
      if (attackAdminMode) attackAdminMode.innerHTML = `Infundir em <strong>Bomba de Infusão a 200 a 300 mL/h em 20-30 min</strong> (ou seringa infusora).`;
      if (attackFooterTip) attackFooterTip.innerText = `Monitorar pressão arterial a cada 5 minutos durante a infusão rápida do ataque.`;
    } else if (protocol.id === 'pritchard') {
      if (attackSolute) attackSolute.innerText = `Parte IV: 8 mL de MgSO₄ 50% (4g)`;
      if (attackDiluent) attackDiluent.innerText = `12 mL de Água Destilada ou SG 5%`;
      if (attackVolTotal) attackVolTotal.innerText = `20 mL em seringa IV + 20 mL IM nas nádegas`;
      if (attackAdminMode) attackAdminMode.innerHTML = `Infundir <strong>4g IV lento em 20 min</strong> e aplicar <strong>10g IM simultâneo (5g em cada nádega)</strong>.`;
      if (attackFooterTip) attackFooterTip.innerText = `Uso estrito de agulha 40x12 mm e Lidocaína 2% 1 mL em cada seringa IM.`;
    } else {
      if (attackSolute) attackSolute.innerText = `8 mL de MgSO₄ 50% (0,8 ampola = 4g)`;
      if (attackDiluent) attackDiluent.innerText = `12 mL de Soro Glicosado 5% ou AD`;
      if (attackVolTotal) attackVolTotal.innerText = `20 mL em seringa (ou 100 mL se BIC)`;
      if (attackAdminMode) attackAdminMode.innerHTML = `Infundir <strong>IV lento em 15 a 20 minutos</strong> (ou 8 mL em 92 mL SG 5% a 300 mL/h na BIC por 20 min).`;
      if (attackFooterTip) attackFooterTip.innerText = `Sensação de calor facial e rubor transitório são comuns durante o ataque.`;
    }
  } else {
    if (protocol.id === 'recorrencia') {
      if (attackSolute) attackSolute.innerText = `20 mL de MgSO₄ 10% (2 ampolas = 2g)`;
      if (attackDiluent) attackDiluent.innerText = `Puro (sem diluente adicional)`;
      if (attackVolTotal) attackVolTotal.innerText = `20 mL em seringa`;
      if (attackAdminMode) attackAdminMode.innerHTML = `Infundir <strong>IV lento em 3 a 5 minutos</strong> diretamente na via venosa.`;
    } else if (protocol.id === 'sibai') {
      if (attackSolute) attackSolute.innerText = `60 mL de MgSO₄ 10% (6 ampolas = 6g)`;
      if (attackDiluent) attackDiluent.innerText = `40 mL de Soro Glicosado 5%`;
      if (attackVolTotal) attackVolTotal.innerText = `100 mL em mini-frasco`;
      if (attackAdminMode) attackAdminMode.innerHTML = `Infundir em <strong>Bomba de Infusão a 200 a 300 mL/h em 20-30 min</strong>.`;
    } else if (protocol.id === 'pritchard') {
      if (attackSolute) attackSolute.innerText = `Atenção: Inviável para IM com ampolas a 10%`;
      if (attackDiluent) attackDiluent.innerText = `Requer ampolas a 50% para injeção glútea profunda`;
      if (attackVolTotal) attackVolTotal.innerText = `Incompatível`;
      if (attackAdminMode) attackAdminMode.innerHTML = `<span class="text-rose-500 font-bold">ALERTA:</span> O esquema IM de Pritchard exige estritamente ampolas de 50%. A ampola de 10% exigiria 50 mL em cada glúteo!`;
    } else {
      if (attackSolute) attackSolute.innerText = `40 mL de MgSO₄ 10% (4 ampolas = 4g)`;
      if (attackDiluent) attackDiluent.innerText = `60 mL de Soro Glicosado 5%`;
      if (attackVolTotal) attackVolTotal.innerText = `100 mL em mini-frasco`;
      if (attackAdminMode) attackAdminMode.innerHTML = `Infundir na BIC a <strong>300 mL/h durante 20 minutos</strong> (Volume a infundir = 100 mL).`;
    }
  }

  if (pritchardAttackBox) {
    if (protocol.isIM) {
      pritchardAttackBox.classList.remove('hidden');
    } else {
      pritchardAttackBox.classList.add('hidden');
    }
  }

  // 5. Atualizar Manutenção (BIC ou Pritchard)
  const maintTargetBadge = document.getElementById('mg-maint-target-badge');
  const bicDeviceContainer = document.getElementById('mg-bic-device-container');
  const pritchardMaintPanel = document.getElementById('mg-pritchard-maint-panel');
  const maintBagRecipe = document.getElementById('mg-maint-bag-recipe');
  const maintBagConcFooter = document.getElementById('mg-maint-bag-conc-footer');

  if (maintTargetBadge) {
    maintTargetBadge.innerText = protocol.isIM ? 'Meta IM: 5g 4/4h' : `Meta: ${protocol.maintGramsPerHour.toFixed(1)} g/h`;
  }

  if (protocol.isIM) {
    if (bicDeviceContainer) bicDeviceContainer.classList.add('hidden');
    if (pritchardMaintPanel) pritchardMaintPanel.classList.remove('hidden');
  } else {
    if (bicDeviceContainer) bicDeviceContainer.classList.remove('hidden');
    if (pritchardMaintPanel) pritchardMaintPanel.classList.add('hidden');
    updateMgBicDisplay();
  }

  // Receita de diluição da bolsa
  if (maintBagRecipe && maintBagConcFooter) {
    const ampCount = isAmp50 ? bag.ampoules50 : bag.ampoules10;
    const mgMl = ampCount * 10;
    const diluentMl = isAmp50 ? bag.diluentVolume50 : bag.diluentVolume10;
    const ampTypeStr = isAmp50 ? '50% (10 mL = 5g)' : '10% (10 mL = 1g)';
    
    maintBagRecipe.innerHTML = `
      Diluir <strong>${ampCount} ampolas (${mgMl} mL) de MgSO₄ ${ampTypeStr}</strong> em <strong>${diluentMl} mL de ${bag.diluentType}</strong>. Volume final: <strong>${bag.totalVolumeMl} mL</strong>.
    `;
    maintBagConcFooter.innerText = `${bag.concentrationMgMl} mg/mL (${bag.soluteGrams}g em ${bag.totalVolumeMl} mL)`;
  }

  // 6. Atualizar Cronograma
  renderMgSchedule();

  // 7. Atualizar Prescrição
  updateMgPrescription();
}

function updateMgBicDisplay() {
  const rate = getCurrentMgBicRate();
  const bag = mgDilutionBags[currentMgState.bagKey];
  const concGPerMl = bag.soluteGrams / bag.totalVolumeMl;
  const deliveredGrams = (rate * concGPerMl).toFixed(1);
  const durationHours = (bag.totalVolumeMl / rate);
  const durH = Math.floor(durationHours);
  const durM = Math.round((durationHours - durH) * 60);

  const rateBig = document.getElementById('mg-bic-rate-big');
  const deliveredDose = document.getElementById('mg-bic-delivered-dose');
  const vtbiVal = document.getElementById('mg-bic-vtbi-val');
  const concVal = document.getElementById('mg-bic-conc-val');
  const durationVal = document.getElementById('mg-bic-duration-val');
  const led = document.getElementById('mg-pump-led');
  const statusLabel = document.getElementById('mg-pump-status-label');
  const toggleBtn = document.getElementById('mg-bic-toggle-btn');

  if (rateBig) rateBig.innerText = rate.toFixed(1);
  if (deliveredDose) deliveredDose.innerText = `${deliveredGrams} g/h`;
  if (vtbiVal) vtbiVal.innerText = `${bag.totalVolumeMl} mL`;
  if (concVal) concVal.innerText = `${bag.concentrationMgMl} mg/mL`;
  if (durationVal) durationVal.innerText = `~${durH}h ${durM.toString().padStart(2, '0')}m`;

  if (led && statusLabel && toggleBtn) {
    if (currentMgState.bicRunning) {
      led.className = 'w-3 h-3 rounded-full pump-led-running';
      statusLabel.className = 'font-mono font-bold text-emerald-400';
      statusLabel.innerText = 'INFUNDINDO • RUNNING';
      toggleBtn.innerHTML = '<i class="fa-solid fa-pause"></i> Pausar';
      toggleBtn.className = 'pump-btn px-2.5 py-1 rounded text-[11px] font-bold text-amber-400 hover:text-amber-300 ml-1 cursor-pointer';
    } else {
      led.className = 'w-3 h-3 rounded-full pump-led-paused';
      statusLabel.className = 'font-mono font-bold text-amber-400';
      statusLabel.innerText = 'PAUSADO • STANDBY';
      toggleBtn.innerHTML = '<i class="fa-solid fa-play"></i> Iniciar';
      toggleBtn.className = 'pump-btn px-2.5 py-1 rounded text-[11px] font-bold text-emerald-400 hover:text-emerald-300 ml-1 cursor-pointer';
    }
  }
}

function formatMgScheduleTime(baseTimeStr, addHours) {
  const parts = (baseTimeStr || '14:00').split(':');
  let h = parseInt(parts[0], 10) || 14;
  let m = parseInt(parts[1], 10) || 0;
  const totalMinutes = (h * 60 + m) + (addHours * 60);
  const endH = Math.floor((totalMinutes / 60) % 24);
  const endM = Math.floor(totalMinutes % 60);
  return `${String(endH).padStart(2, '0')}:${String(endM).padStart(2, '0')}`;
}

function renderMgSchedule() {
  const container = document.getElementById('mg-schedule-container');
  const h0Label = document.getElementById('mg-timeline-h0-label');
  if (!container) return;

  const baseTime = currentMgState.startTime || '14:00';
  if (h0Label) h0Label.innerText = `H₀: ${baseTime}`;

  const protocol = mgProtocols[currentMgState.protocolKey];
  const bag = mgDilutionBags[currentMgState.bagKey];
  const rate = getCurrentMgBicRate();
  const bagDuration = Math.round(bag.totalVolumeMl / rate);

  let milestones = [];

  if (protocol.isIM) {
    // Protocolo Pritchard (IM)
    milestones = [
      {
        hOffset: 0,
        title: 'H₀ • Dose de Ataque',
        action: '4g IV lento (20 min) + 10g IM profundo (5g Glúteo D + 5g Glúteo E com 1 mL Lidocaína 2%). Passar SVD.',
        badge: 'Ataque Misto',
        badgeColor: 'amber'
      },
      {
        hOffset: 1,
        title: 'H₁ • 1ª Checagem Enfermagem',
        action: 'Avaliar reflexo patelar (+), contar FR (≥ 16) e medir débito urinário na SVD.',
        badge: 'Checagem',
        badgeColor: 'teal'
      },
      {
        hOffset: 4,
        title: 'H₄ • 1ª Manutenção IM',
        action: '5g IM profundo no Glúteo Direito (1 ampola 50% + 1 mL Lidocaína 2%). Checar tríade.',
        badge: '5g IM Glúteo D',
        badgeColor: 'amber'
      },
      {
        hOffset: 8,
        title: 'H₈ • 2ª Manutenção IM',
        action: '5g IM profundo no Glúteo Esquerdo (1 ampola 50% + 1 mL Lidocaína 2%). Checar tríade.',
        badge: '5g IM Glúteo E',
        badgeColor: 'amber'
      },
      {
        hOffset: 12,
        title: 'H₁₂ • 3ª Manutenção IM',
        action: '5g IM profundo no Glúteo Direito. Reavaliação clínica obstétrica completa.',
        badge: '5g IM Glúteo D',
        badgeColor: 'amber'
      },
      {
        hOffset: 16,
        title: 'H₁₆ • 4ª Manutenção IM',
        action: '5g IM profundo no Glúteo Esquerdo. Monitorizar diurese acumulada.',
        badge: '5g IM Glúteo E',
        badgeColor: 'amber'
      },
      {
        hOffset: 20,
        title: 'H₂₀ • 5ª Manutenção IM',
        action: '5g IM profundo no Glúteo Direito. Checar reflexo e FR.',
        badge: '5g IM Glúteo D',
        badgeColor: 'amber'
      },
      {
        hOffset: 24,
        title: 'H₂₄ • Conclusão do Tratamento',
        action: 'Avaliar alta do protocolo (24h pós-parto ou pós-crise). Retirar SVD se estável.',
        badge: 'Término / Alta',
        badgeColor: 'emerald'
      }
    ];
  } else {
    // Protocolos Intravenosos (BIC)
    const secondBagH = bagDuration;
    const thirdBagH = bagDuration * 2;

    milestones = [
      {
        hOffset: 0,
        title: 'H₀ • Ataque & Início da BIC',
        action: `Infundir ataque (${protocol.attackGrams}g IV). Iniciar Bolsa 1 na BIC a ${rate.toFixed(1)} mL/h. Instalar SVD com urômetro.`,
        badge: 'Início BIC',
        badgeColor: 'teal'
      },
      {
        hOffset: 1,
        title: 'H₁ • Checagem de Segurança',
        action: 'Aferir Reflexo Patelar (presente), FR (≥ 16 irpm) e Diurese horária (≥ 25 mL/h).',
        badge: 'Checagem Horária',
        badgeColor: 'teal'
      },
      {
        hOffset: 2,
        title: 'H₂ • Checagem de Segurança',
        action: 'Checar reflexo, FR e volume urinário. Ajustar BIC se prescrito.',
        badge: 'Checagem Horária',
        badgeColor: 'slate'
      },
      {
        hOffset: Math.min(6, secondBagH),
        title: `H${Math.min(6, secondBagH)} • Vigilância Intensiva`,
        action: 'Checar sinais vitais, magnesemia se houver oligúria e estado de consciência.',
        badge: 'Vigilância',
        badgeColor: 'slate'
      },
      {
        hOffset: secondBagH,
        title: `H${secondBagH} • Troca para Bolsa 2`,
        action: `Fim da Bolsa 1 (~${bag.totalVolumeMl} mL). Instalar Bolsa 2 com novo preparo a ${rate.toFixed(1)} mL/h.`,
        badge: 'Troca de Bolsa BIC',
        badgeColor: 'blue'
      },
      {
        hOffset: 12,
        title: 'H₁₂ • Marco Intermediário',
        action: protocol.id === 'neuro' ? 'Avaliar suspensão se parto concluído ou contrações cessadas.' : 'Reavaliação médica, balanço hídrico das 12h e controle pressórico.',
        badge: protocol.id === 'neuro' ? 'Decisão Fetal' : 'Balanço 12h',
        badgeColor: 'purple'
      },
      {
        hOffset: Math.min(20, thirdBagH),
        title: `H${Math.min(20, thirdBagH)} • Troca Bolsa 3 / Reta Final`,
        action: 'Instalar Bolsa 3 se necessário ou checar volume restante. Manter monitorização horária.',
        badge: 'Monitorização',
        badgeColor: 'slate'
      },
      {
        hOffset: 24,
        title: 'H₂₄ • Fim do Protocolo (24h)',
        action: 'Completadas 24h de estabilidade pós-parto ou pós-crise: Desligar BIC de MgSO₄. Retirar SVD se diurese ampla.',
        badge: 'Término / Suspensão',
        badgeColor: 'emerald'
      }
    ];
  }

  container.innerHTML = milestones.map(m => {
    const timeFormatted = formatMgScheduleTime(baseTime, m.hOffset);
    return `
      <div class="p-3 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm flex flex-col justify-between">
        <div>
          <div class="flex items-center justify-between mb-1.5">
            <span class="text-xs font-mono font-black text-teal-600 dark:text-teal-400 bg-teal-50 dark:bg-teal-950/60 px-2 py-0.5 rounded border border-teal-200 dark:border-teal-900">
              ${timeFormatted}
            </span>
            <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300">
              ${m.badge}
            </span>
          </div>
          <span class="text-xs font-bold text-slate-900 dark:text-white block mb-1">${m.title}</span>
          <p class="text-[11px] text-slate-600 dark:text-slate-400 leading-snug">${m.action}</p>
        </div>
      </div>
    `;
  }).join('');
}

function updateMgPrescription() {
  const textarea = document.getElementById('mg-prescription-textarea');
  if (!textarea) return;

  const protocol = mgProtocols[currentMgState.protocolKey];
  const bag = mgDilutionBags[currentMgState.bagKey];
  const isAmp50 = currentMgState.ampouleType === '50';
  const baseTime = currentMgState.startTime || '14:00';
  const rate = getCurrentMgBicRate();

  const ampCount = isAmp50 ? bag.ampoules50 : bag.ampoules10;
  const mgMl = ampCount * 10;
  const diluentMl = isAmp50 ? bag.diluentVolume50 : bag.diluentVolume10;
  const ampLabel = isAmp50 ? '50% (10 mL = 5g)' : '10% (10 mL = 1g)';

  let prescText = `PRESCRIÇÃO MÉDICA HOSPITALAR — SULFATO DE MAGNÉSIO (MgSO4)\n`;
  prescText += `PROTOCOLO: ${protocol.name.toUpperCase()} • ${protocol.subtitle}\n`;
  prescText += `INDICAÇÃO: ${protocol.indication}\n`;
  prescText += `HORÁRIO DE INÍCIO: ${baseTime} | VIGÊNCIA PREVISTA: 24 horas pós-parto ou pós-crise\n`;
  prescText += `--------------------------------------------------------------------------\n`;

  // Ataque
  prescText += `1. DOSE DE ATAQUE:\n`;
  if (protocol.id === 'recorrencia') {
    prescText += `   - Sulfato de Magnésio 50%: 4 mL (2g) + SG 5% ou AD: 16 mL (Volume total = 20 mL em seringa).\n`;
    prescText += `   - Via: Intravenosa (IV) lenta em 3 a 5 minutos sob monitorização estrita.\n`;
  } else if (protocol.id === 'sibai') {
    prescText += `   - Sulfato de Magnésio 50%: 12 mL (6g) + SG 5%: 88 mL (Volume total = 100 mL).\n`;
    prescText += `   - Via: IV em Bomba de Infusão Contínua (BIC) a 200-300 mL/h a correr em 20-30 minutos.\n`;
  } else if (protocol.id === 'pritchard') {
    prescText += `   - PARTE IV: Sulfato de Magnésio 50% 8 mL (4g) + AD 12 mL = 20 mL IV lento em 20 min.\n`;
    prescText += `   - PARTE IM (Simultânea): Sulfato de Magnésio 50% 10 mL (5g) + Lidocaína 2% 1 mL em cada nádega (10g IM total, agulha 40x12 em técnica em Z).\n`;
  } else {
    prescText += `   - Sulfato de Magnésio 50%: 8 mL (4g) + SG 5% ou AD: 12 mL (Volume total = 20 mL em seringa).\n`;
    prescText += `   - Via: Intravenosa (IV) lenta em 15 a 20 minutos (ou 8 mL em 92 mL SG 5% a 300 mL/h na BIC em 20 min).\n`;
  }

  // Manutenção
  prescText += `\n2. DOSE DE MANUTENÇÃO:\n`;
  if (protocol.isIM) {
    prescText += `   - Sulfato de Magnésio 50%: 10 mL (1 ampola = 5g) + Lidocaína 2% sem vasoconstritor: 1 mL.\n`;
    prescText += `   - Via: Intramuscular profunda (glúteo, agulha 40x12) a cada 4 HORAS por 24 horas, alternando nádega D e nádega E.\n`;
    prescText += `   - Administrar apenas se critérios de segurança forem satisfeitos.\n`;
  } else {
    prescText += `   - Diluição: ${ampCount} ampolas (${mgMl} mL) de MgSO4 ${ampLabel} + ${diluentMl} mL de ${bag.diluentType}.\n`;
    prescText += `   - Volume Total do Frasco: ${bag.totalVolumeMl} mL (Concentração: ${bag.concentrationMgMl} mg/mL).\n`;
    prescText += `   - Via: Intravenosa contínua em Bomba de Infusão Contínua (BIC).\n`;
    prescText += `   - Programação da BIC: TAXA = ${rate.toFixed(1)} mL/h | DOSE = ${protocol.maintGramsPerHour.toFixed(1)} g/h | VTBI = ${bag.totalVolumeMl} mL.\n`;
    prescText += `   - Duração estimada: ~${Math.floor(bag.totalVolumeMl / rate)} horas por bolsa. Trocar bolsa sucessiva mantendo vazão.\n`;
  }

  // Cuidados de Enfermagem
  prescText += `\n3. CUIDADOS CRÍTICOS DE ENFERMAGEM & MONITORIZAÇÃO HORÁRIA:\n`;
  prescText += `   - Checar e registrar em prontuário a CADA 1 HORA:\n`;
  prescText += `     a) Reflexo Patelar (deve estar PRESENTE / Normoativo);\n`;
  prescText += `     b) Frequência Respiratória (deve ser ≥ 16 irpm; suspender se < 12-16 irpm);\n`;
  prescText += `     c) Diurese horária em SVD com urômetro de sistema fechado (deve ser ≥ 25 mL/h ou ≥ 100 mL/4h).\n`;
  prescText += `   - Se ausência de reflexo, FR < 16 ou diurese < 25 mL/h: SUSPENDER MgSO4 IMEDIATAMENTE e chamar plantonista.\n`;

  // Antídoto
  prescText += `\n4. PRESCRIÇÃO DE EMERGÊNCIA — ANTÍDOTO EM CASO DE INTOXICAÇÃO:\n`;
  prescText += `   - Gluconato de Cálcio a 10%: 1 ampola (10 mL = 1g) IV lento em 3 a 5 minutos.\n`;
  prescText += `   - Indicação: Perda de reflexo tendinoso, depressão respiratória ou sinais de bloqueio por MgSO4.\n`;
  prescText += `   - Manter 1 ampola de Gluconato de Cálcio 10% à beira do leito da paciente durante todo o uso de MgSO4.\n`;

  textarea.value = prescText;
}

function copyMgPrescription() {
  const textarea = document.getElementById('mg-prescription-textarea');
  if (!textarea) return;

  const textToCopy = textarea.value;

  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(textToCopy).then(() => {
      showCopyFeedback();
    }).catch(() => {
      fallbackCopy(textarea);
    });
  } else {
    fallbackCopy(textarea);
  }
}

function fallbackCopy(textarea) {
  textarea.select();
  textarea.setSelectionRange(0, 99999);
  document.execCommand('copy');
  showCopyFeedback();
}

function showCopyFeedback() {
  const feedback = document.getElementById('mg-copied-feedback');
  const btnLabel = document.getElementById('mg-copy-btn-label');
  if (feedback) {
    feedback.classList.remove('hidden');
    setTimeout(() => {
      feedback.classList.add('hidden');
    }, 3000);
  }
  if (btnLabel) {
    const orig = btnLabel.innerText;
    btnLabel.innerText = 'Copiado!';
    setTimeout(() => {
      btnLabel.innerText = orig;
    }, 2500);
  }
}

function initMgSection() {
  const timeInput = document.getElementById('mg-start-time');
  if (timeInput) {
    const now = new Date();
    const hh = String(now.getHours()).padStart(2, '0');
    const mm = String(now.getMinutes()).padStart(2, '0');
    currentMgState.startTime = `${hh}:${mm}`;
    timeInput.value = currentMgState.startTime;
  }
  updateMgAllViews();
}

// --- SIMULADOR DE TOXICIDADE SÉRICA DE MAGNÉSIO ---
function updateMgLevel(val) {
  const level = parseFloat(val);
  currentMgState.toxicityLevel = level;
  const label = document.getElementById('mg-level-val');
  if (label) label.innerText = `${level.toFixed(1)} mEq/L`;

  const bar = document.getElementById('mg-level-bar');
  const status = document.getElementById('mg-clinical-state');
  const action = document.getElementById('mg-action-needed');

  let pct = Math.min(100, Math.round((level / 30) * 100));
  if (bar) bar.style.width = `${pct}%`;

  if (!status || !action) return;

  if (level < 4.0) {
    if (bar) bar.className = 'h-full bg-slate-400 transition-all duration-300';
    status.innerHTML = '<span class="text-slate-600 dark:text-slate-400 font-semibold">Subterapêutico (< 4.0 mEq/L)</span>: Não previne convulsões eclâmpticas de forma eficaz.';
    action.innerText = 'Reajustar bomba de infusão de MgSO4 para atingir a faixa terapêutica (1 a 2 g/h).';
  } else if (level <= 7.0) {
    if (bar) bar.className = 'h-full bg-emerald-500 transition-all duration-300';
    status.innerHTML = '<span class="text-emerald-600 dark:text-emerald-400 font-bold">Faixa Terapêutica Ideal (4.0 - 7.0 mEq/L)</span>: Excelente neuroproteção e prevenção de eclâmpsia.';
    action.innerText = 'Manter infusão contínua. Checar reflexo patelar a cada 1-2h, FR (deve ser ≥ 16) e débito urinário (≥ 25 mL/h).';
  } else if (level <= 10.0) {
    if (bar) bar.className = 'h-full bg-amber-500 transition-all duration-300';
    status.innerHTML = '<span class="text-amber-600 dark:text-amber-400 font-bold">🚨 1º Sinal de Intoxicação: Perda dos Reflexos Patelar e Tendinosos Profundos (8-10 mEq/L)</span>';
    action.innerText = 'SUSPENDER IMEDIATAMENTE a infusão de Sulfato de Magnésio. Coletar magnesemia sérica. Monitorar via aérea.';
  } else if (level <= 15.0) {
    if (bar) bar.className = 'h-full bg-rose-600 transition-all duration-300 animate-pulse';
    status.innerHTML = '<span class="text-rose-600 dark:text-rose-400 font-bold">🚨 2º Sinal de Intoxicação: Depressão Respiratória Grave (< 12-16 irpm) e Sedação Profunda (12-15 mEq/L)</span>';
    action.innerText = 'EMERGÊNCIA! Suspender MgSO4 + Administrar GLUCONATO DE CÁLCIO 10% 1g (10 mL) IV lento em 3-5 minutos! Oxigenoterapia com máscara / preparar via aérea.';
  } else {
    if (bar) bar.className = 'h-full bg-red-700 transition-all duration-300 animate-pulse';
    status.innerHTML = '<span class="text-red-700 dark:text-red-400 font-black">💀 Intoxicação Letal: Parada Cardíaca em Diástole e Paralisia Muscular (> 25 mEq/L)</span>';
    action.innerText = 'PCR por MgSO4: RCP imediata + GLUCONATO DE CÁLCIO 10% 1g IV em bolus + Suporte ventilatório mecânico invasivo + Hemodiálise de urgência.';
  }
}


// --- 5. INTERACTIVE FLASHCARD SYSTEM (20 High-Yield USMLE Cards) ---
const flashcardsData = [
  {
    category: "DMG",
    q: "Qual é o mecanismo fisiopatológico exato que causa hipoglicemia no recém-nascido de mãe com diabetes gestacional?",
    a: "Hipótese de Pedersen: A glicose materna atravessa a placenta livremente (GLUT1), mas a insulina materna NÃO atravessa. O pâncreas fetal responde com hiperplasia de células-beta e hipersecreção maciça de insulina fetal. No clampeamento do cordão, o aporte de glicose é abruptamente interrompido, mas o hiperinsulinismo fetal persiste por horas, consumindo a glicose circulante e causando hipoglicemia neonatal.",
    ivyTip: "USMLE Tip: O hiperinsulinismo fetal também atrasa a produção de surfactante nos pneumócitos tipo II (antagoniza o cortisol), aumentando o risco de Síndrome do Desconforto Respiratório (RDS)!"
  },
  {
    category: "Pré-Eclâmpsia",
    q: "Quais são os 2 estágios fisiopatológicos da pré-eclâmpsia e os biomarcadores pró e antiangiogênicos envolvidos?",
    a: "Estágio 1 (Pré-clínico < 20 sem): Invasão trofoblástica rasa das artérias espiraladas maternas, mantendo alta resistência e hipoperfusão.\nEstágio 2 (Clínico > 20 sem): A placenta isquêmica secreta fatores anti-angiogênicos em excesso: sFlt-1 (receptor solúvel de VEGF) e Endoglina solúvel, diminuindo VEGF e PlGF livres. Isso desencadeia disfunção endotelial sistêmica, vasoespasmo, proteinúria e HAS.",
    ivyTip: "Relação sFlt-1/PlGF elevada tem alto valor preditivo para desenvolvimento de pré-eclâmpsia grave."
  },
  {
    category: "Doppler / Fetal",
    q: "Qual é a sequência cronológica de deterioração hemodinâmica fetal no Doppler em casos de CIUR por insuficiência placentária?",
    a: "1º ↑ Resistência na Artéria Umbilical (IP aumentado) → 2º Centralização fetal / Vasodilatação da Artéria Cerebral Média ('Brain Sparing' com IP diminuído) → 3º Diástole Zero na Artéria Umbilical (AEDV) → 4º Diástole Reversa na Artéria Umbilical (REDV) → 5º Onda 'A' reversa no Ducto Venoso (descompensação miocárdica e acidemia grave) → Iminência de óbito.",
    ivyTip: "Onda A reversa no Ducto Venoso indica resolução IMEDIATA da gestação, independentemente da idade gestacional!"
  },
  {
    category: "Isoimunização Rh",
    q: "Em uma gestante Rh-negativa já sensibilizada (Coombs indireto positivo ≥ 1:16), qual é o exame padrão-ouro não invasivo para rastrear anemia fetal grave e quando indicar transfusão intrauterina?",
    a: "Doppler do Pico de Velocidade Sistólica da Artéria Cerebral Média (ACM-PVS). Se o PVS for > 1,5 MoM (Múltiplos da Mediana) para a idade gestacional, há suspeita de anemia fetal grave (Hb < 10 g/dL), indicando cordocentese para confirmação e Transfusão Intrauterina (TIU) com hemácias O Rh-negativo.",
    ivyTip: "RhoGAM NÃO tem utilidade se a paciente já estiver sensibilizada com anticorpos anti-D circulantes!"
  },
  {
    category: "Infecções / GBS",
    q: "Qual o período ideal para coleta do swab de GBS e quais pacientes têm indicação absoluta de profilaxia intraparto mesmo sem cultura?",
    a: "Coleta: 35 a 37 semanas (swab vaginal e retal distal). Indicação absoluta sem necessidade de cultura: 1) Filho anterior com doença invasiva neonatal por GBS; 2) Bacteriúria por GBS na gestação atual (qualquer colônia); 3) Status desconhecido + parto prematuro (< 37 sem), bolsa rota ≥ 18h ou febre materna intraparto ≥ 38°C.",
    ivyTip: "Antibiótico de escolha: Penicilina G Cristalina IV (5 milhões de ataque + 2,5-3 milhões a cada 4h até o parto). Mínimo 4h antes do desprendimento!"
  },
  {
    category: "Gemelaridade",
    q: "Qual o sinal ultrassonográfico patognomônico de corionicidade no 1º trimestre e qual complicação vascular é exclusiva das gestações monocoriônicas?",
    a: "Sinal do Lambda (Twin Peak) = Gestação Dicoriônica. Sinal do 'T' = Gestação Monocoriônica. Complicação exclusiva das monocoriônicas: Síndrome de Transfusão Feto-Fetal (STFF/TTTS), decorrente de anastomoses arteriovenosas profundas desbalanceadas na placenta compartilhada. O tratamento de escolha para Estágios ≥ II de Quintero é a ablação dos vasos a laser por fetoscopia.",
    ivyTip: "O estadiamento de Quintero vai de I (oligo-polidrâmnio) a V (óbito de um ou ambos os fetos)."
  },
  {
    category: "Sífilis",
    q: "Qual é o único tratamento comprovadamente eficaz para prevenção de sífilis congênita na gestação e qual a conduta em gestante alérgica?",
    a: "Penicilina G Benzatina na dosagem correta para a fase clínica (2,4 milhões UI DU para fase primária/secundária/latente recente; 7,2 milhões em 3 doses semanais para latente tardia/indeterminada). Em caso de alergia documentada, a conduta OBRIGATÓRIA é a DESSENSIBILIZAÇÃO à penicilina em ambiente hospitalar e posterior administração da droga!",
    ivyTip: "Doxiciclina, tetraciclina e eritromicina NÃO são tratamentos adequados para sífilis na gestante segundo o CDC/ACOG e Ministério da Saúde."
  },
  {
    category: "Toxoplasmose",
    q: "Gestante no 1º trimestre apresenta sorologia IgG (+) e IgM (+). Qual é o exame para definir se a infecção é recente e qual o tratamento inicial enquanto se aguarda confirmação?",
    a: "Teste de Avidez de IgG. Alta avidez (> 60%) antes de 16 semanas exclui infecção aguda na gestação (infecção ocorreu antes da concepção). Baixa avidez (< 30%) indica infecção aguda nos últimos 3-4 meses. Conduta imediata: Iniciar Espiramicina (1g VO 8/8h) para impedir a transmissão transplacentária. Se amniocentese confirmar PCR positivo no líquido amniótico, mudar para o esquema tríplice (Sulfadiazina + Pirimetamina + Ácido Folínico) após 18 semanas.",
    ivyTip: "A espiramicina trata a placenta para evitar a transmissão, mas não trata o feto já infectado porque tem baixa passagem transplacentária."
  },
  {
    category: "HIV na Gestação",
    q: "Quais são os critérios para indicação de parto vaginal seguro em gestante vivendo com HIV e qual a recomendação sobre amamentação no Brasil?",
    a: "Parto vaginal é indicado se a Carga Viral (CV) for < 1.000 cópias/mL com 34 semanas de gestação ou indetectável. Se CV ≥ 1.000 cópias/mL ou desconhecida: Cesariana eletiva na 38ª semana (com membranas íntegras e fora de trabalho de parto) + AZT IV contínuo no periparto. No Brasil, o aleitamento materno é FORMALMENTE CONTRAINDICADO em todos os casos de PVHA (independente de CV indetectável), devendo-se inibir a lactação com Cabergolina.",
    ivyTip: "Em locais de alta renda o aleitamento pode ser discutido, mas nas provas brasileiras e Revalida, aleitamento em PVHA é contraindicação absoluta!"
  },
  {
    category: "Pré-Eclâmpsia / MgSO4",
    q: "Quais são os 3 parâmetros clínicos mandatórios que devem ser monitorados durante a infusão contínua de Sulfato de Magnésio (Protocolo Zuspan)?",
    a: "1) Presença do Reflexo Patelar (sua abolição é o 1º sinal de intoxicação, 8-10 mEq/L); 2) Frequência Respiratória (deve ser ≥ 16 irpm; se < 12-16 há risco de parada respiratória); 3) Débito Urinário (deve ser ≥ 25 mL/h ou 0,5 mL/kg/h, pois o magnésio é excretado exclusivamente pelos rins). Se intoxicação: Gluconato de Cálcio a 10% 1g IV!",
    ivyTip: "Antídoto do magnésio: 1 ampola de Gluconato de Cálcio 10% (10 mL = 1g) administrada lentamente por via intravenosa."
  }
];

let currentCardIndex = 0;
let cardFlipped = false;

function renderFlashcard() {
  const card = flashcardsData[currentCardIndex];
  document.getElementById('fc-category').innerText = card.category;
  document.getElementById('fc-index').innerText = `Card ${currentCardIndex + 1} de ${flashcardsData.length}`;
  document.getElementById('fc-question').innerText = card.q;
  document.getElementById('fc-answer').innerText = card.a;
  document.getElementById('fc-tip').innerText = card.ivyTip;

  const inner = document.getElementById('flashcard-inner');
  inner.classList.remove('flipped');
  cardFlipped = false;
}

function flipFlashcard() {
  const inner = document.getElementById('flashcard-inner');
  cardFlipped = !cardFlipped;
  if (cardFlipped) {
    inner.classList.add('flipped');
  } else {
    inner.classList.remove('flipped');
  }
}

function nextFlashcard() {
  currentCardIndex = (currentCardIndex + 1) % flashcardsData.length;
  renderFlashcard();
}

function prevFlashcard() {
  currentCardIndex = (currentCardIndex - 1 + flashcardsData.length) % flashcardsData.length;
  renderFlashcard();
}

// --- 6. INTERACTIVE USMLE STEP 2 CK / STEP 3 QUIZ (20 QUESTIONS) ---
const quizQuestions = [
  {
    q: "Uma primigesta de 32 anos com 35 semanas de gestação comparece à emergência obstétrica queixando-se de cefaleia frontal pulsátil persistente e dor epigástrica em barra há 6 horas. PA aferida em duas ocasiões com intervalo de 15 minutos: 168/112 mmHg e 172/114 mmHg. Exames laboratoriais: Plaquetas 68.000/μL, AST 180 U/L, ALT 165 U/L, LDH 820 U/L, Creatinina 1,3 mg/dL. A monitorização fetal (CTG) demonstra FCF basal de 135 bpm, variabilidade moderada e ausência de desacelerações. Qual é a conduta terapêutica inicial mais adequada?",
    options: [
      "A) Realizar cesariana de emergência imediata sem medicações prévias.",
      "B) Iniciar Sulfato de Magnésio IV + Hidralazina ou Labetalol IV, e planejar o parto após estabilização materna.",
      "C) Administrar Dexametasona para maturação pulmonar fetal e aguardar até 37 semanas.",
      "D) Prescrever Metildopa via oral e dosar proteinúria de 24 horas em ambiente ambulatorial.",
      "E) Infundir concentrado de plaquetas profilático antes de qualquer outra medida."
    ],
    answer: 1,
    explanation: "Esta paciente apresenta Pré-Eclâmpsia com Critérios de Gravidade associada à Síndrome HELLP (Hemólise com LDH > 600, Elevação de Enzimas Hepáticas com AST/ALT > 2x o limite, e Plaquetopenia < 100.000). Com 35 semanas (≥ 34 semanas), a conduta mandatória é: 1) Estabilização hemodinâmica com anti-hipertensivo de ação rápida (Hidralazina IV, Labetalol IV ou Nifedipino oral) para evitar AVC; 2) Prevenção de convulsões com Sulfato de Magnésio IV (Protocolo Zuspan); e 3) Resolução da gestação (PARTO) após estabilização materna. Aguardar até 37 semanas é erro grave e contraindicado.",
    highYieldPearl: "Em pré-eclâmpsia com critérios de gravidade com ≥ 34 semanas, o parto é a terapia curativa definitiva após estabilização clínica."
  },
  {
    q: "Uma mulher de 28 anos, G2P1 com 10 semanas de gestação, vem para sua primeira consulta de pré-natal. Sua gestação anterior foi complicada por feto com restrição de crescimento e pré-eclâmpsia precoce que necessitou de parto com 31 semanas. Ela tem IMC de 31 kg/m² e PA atual de 124/78 mmHg. Qual é a recomendação profilática mais eficaz baseada em evidências (ACOG/USPSTF) para reduzir o risco de recorrência de pré-eclâmpsia?",
    options: [
      "A) Repouso absoluto no leito a partir de 20 semanas de gestação.",
      "B) Dieta hipossódica rigorosa e restrição de ingestão de líquidos.",
      "C) Iniciar Ácido Acetilsalicílico (AAS) em baixa dose (81-150 mg/dia) antes de 16 semanas.",
      "D) Suplementação de Vitamina C e Vitamina E em altas doses.",
      "E) Heparina de baixo peso molecular profilática até o termo."
    ],
    answer: 2,
    explanation: "Pacientes com antecedente de pré-eclâmpsia precoce (parto < 34 sem) são de ALTO RISCO para desenvolvimento de pré-eclâmpsia na gestação subsequente. A intervenção de escolha comprovada por múltiplos ensaios clínicos e recomendada por ACOG, FIGO e Ministério da Saúde é o AAS em baixa dose (100 a 150 mg/dia à noite), que deve ser iniciado antes de 16 semanas (idealmente entre 12 e 16 sem) e mantido até 36 semanas. O AAS atua inibindo seletivamente o tromboxano A2 placentário sem inibir a prostaciclina endotelial, favorecendo o fluxo sanguíneo.",
    highYieldPearl: "O AAS previne pré-eclâmpsia quando iniciado ANTES da 16ª semana (antes da conclusão da segunda onda de invasão trofoblástica)."
  },
  {
    q: "Uma secundigesta de 30 anos, Rh-negativa, comparece com 28 semanas para consulta pré-natal. Seu parceiro é Rh-positivo heterozigoto. O teste de Coombs Indireto coletado nesta semana é Negativo (1:0). Qual é a conduta preconizada neste momento?",
    options: [
      "A) Não há necessidade de intervenção, pois o teste está negativo e a mãe é imune.",
      "B) Administrar Imunoglobulina Anti-D (RhoGAM) 300 μg intramuscular agora e repetir no pós-parto se o recém-nascido for Rh-positivo.",
      "C) Solicitar amniocentese para genotipagem fetal do fator Rh.",
      "D) Realizar Doppler da Artéria Cerebral Média para afastar anemia fetal oculta.",
      "E) Prescrever sulfato ferroso em dose dobrada para profilaxia de isoimunização."
    ],
    answer: 1,
    explanation: "A profilaxia sistemática de isoimunização Rh com Imunoglobulina Anti-D (300 μg IM) é indicada universalmente às 28 semanas de gestação para toda mulher Rh-negativa não sensibilizada (Coombs indireto negativo). Uma segunda dose de 300 μg deve ser administrada em até 72 horas pós-parto caso o recém-nascido seja confirmado Rh-positivo (e com Coombs direto negativo). Isso reduz a taxa de sensibilização de 16% para menos de 0,1%.",
    highYieldPearl: "O teste de Coombs indireto DEVE ser negativo para receber RhoGAM. Se for positivo (sensibilizada), a imunoglobulina não tem efeito protetor."
  },
  {
    q: "Durante a realização de um traçado de Cardiotocografia (CTG) em uma gestante em trabalho de parto ativo a termo, observa-se que após cada contração uterina há uma queda gradual da FCF que atinge seu ponto mais baixo (nadir) 30 segundos após o pico da contração, retornando à linha de base somente após o relaxamento completo do miométrio. A variabilidade basal é mínima (3 bpm). Qual é a interpretação fisiopatológica desse padrão?",
    options: [
      "A) Compressão fisiológica do polo cefálico fetal (Desaceleração Precoce / DIP I), reflexo vagal benigno.",
      "B) Compressão transitória do cordão umbilical (Desaceleração Variável).",
      "C) Insuficiência uteroplacentária e hipóxia fetal (Desaceleração Tardia / DIP II), padrão Categoria III potencialmente não tranquilizador.",
      "D) Movimento corporal fetal vigoroso associado a taquicardia supraventricular transitória.",
      "E) Estimulação mecânica simpática por toque vaginal prévio."
    ],
    answer: 2,
    explanation: "Desacelerações que iniciam APÓS o ápice da contração uterina e têm recuperação lenta após o término da contração são DESACELERAÇÕES TARDIAS (DIP II). Seu mecanismo é a insuficiência uteroplacentária: a contração uterina reduz transitoriamente a perfusão do espaço interviloso, e o feto já limítrofe em oxigenação sofre hipoxemia, ativando quimiorreceptores que disparam desaceleração reflexa mediada pelo nervo vago. Associada à variabilidade mínima ou ausente, constitui Categoria III do NICHD, indicando hipóxia/acidemia fetal.",
    highYieldPearl: "Desaceleração Precoce = Compressão da Cabeça (Benigna). Desaceleração Tardia = Insuficiência Placentária (Perigosa). Desaceleração Variável = Compressão de Cordão."
  },
  {
    q: "Uma gestante de 26 anos realiza TOTG com sobrecarga de 75g de glicose anidra na 26ª semana de gestação. Os resultados retornam: Glicemia de jejum: 88 mg/dL; Glicemia 1 hora pós-sobrecarga: 184 mg/dL; Glicemia 2 horas pós-sobrecarga: 142 mg/dL. Qual é o diagnóstico e o manejo inicial correto segundo as diretrizes IADPSG / OMS / ACOG?",
    options: [
      "A) Teste normal; manter dieta livre e repetir com 34 semanas.",
      "B) Intolerância à glicose leve; não requer acompanhamento.",
      "C) Diagnóstico de Diabetes Mellitus Gestacional (DMG); prescrever imediatamente Insulina NPH em ambiente hospitalar.",
      "D) Diagnóstico de Diabetes Mellitus Gestacional (DMG); iniciar terapia nutricional com controle de carboidratos, atividade física e automonitorização glicêmica capilar.",
      "E) Teste inconclusivo; necessário repetir teste de tolerância com 100g de glicose."
    ],
    answer: 3,
    explanation: "Pelos critérios da IADPSG/OMS/Ministério da Saúde, o TOTG 75g é diagnóstico de DMG quando QUALQUER UM dos 3 valores é atingido ou superado: Jejum ≥ 92 mg/dL; 1 hora ≥ 180 mg/dL; 2 horas ≥ 153 mg/dL. Neste caso, o valor de 1 hora foi 184 mg/dL (≥ 180 mg/dL), confirmando o diagnóstico de DMG! O tratamento de PRIMEIRA LINHA é não farmacológico: terapia nutricional médica individualizada, atividade física e perfil glicêmico capilar de 4 a 6 pontos por dia. A insulina só é indicada se após 2 semanas as metas glicêmicas não forem atingidas.",
    highYieldPearl: "No TOTG 75g, UM ÚNICO valor alterado (92 / 180 / 153) fecha diagnóstico de DMG."
  }
];

let quizCurrentIndex = 0;
let quizScore = 0;
let quizAnswered = false;

function renderQuizQuestion() {
  const qData = quizQuestions[quizCurrentIndex];
  document.getElementById('quiz-counter').innerText = `Questão ${quizCurrentIndex + 1} de ${quizQuestions.length}`;
  document.getElementById('quiz-question-text').innerText = qData.q;
  
  const optionsContainer = document.getElementById('quiz-options-container');
  optionsContainer.innerHTML = '';
  quizAnswered = false;
  document.getElementById('quiz-feedback-box').classList.add('hidden');

  qData.options.forEach((opt, idx) => {
    const btn = document.createElement('button');
    btn.className = 'w-full text-left p-4 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 hover:border-teal-500 dark:hover:border-teal-400 transition-all font-medium text-slate-800 dark:text-slate-200 text-sm flex items-start gap-3';
    btn.onclick = () => selectQuizAnswer(idx);
    btn.innerHTML = `<span class="inline-flex items-center justify-center w-6 h-6 rounded-full bg-slate-100 dark:bg-slate-700 text-xs font-bold text-slate-600 dark:text-slate-300 shrink-0">${String.fromCharCode(65 + idx)}</span> <span>${opt}</span>`;
    btn.id = `quiz-opt-${idx}`;
    optionsContainer.appendChild(btn);
  });
}

function selectQuizAnswer(selectedIndex) {
  if (quizAnswered) return;
  quizAnswered = true;

  const qData = quizQuestions[quizCurrentIndex];
  const isCorrect = selectedIndex === qData.answer;

  if (isCorrect) {
    quizScore++;
  }

  // Highlight options
  qData.options.forEach((_, idx) => {
    const btn = document.getElementById(`quiz-opt-${idx}`);
    if (idx === qData.answer) {
      btn.className = 'w-full text-left p-4 rounded-xl border-2 border-emerald-500 bg-emerald-50 dark:bg-emerald-950/40 text-emerald-900 dark:text-emerald-200 font-semibold text-sm flex items-start gap-3';
    } else if (idx === selectedIndex && !isCorrect) {
      btn.className = 'w-full text-left p-4 rounded-xl border-2 border-rose-500 bg-rose-50 dark:bg-rose-950/40 text-rose-900 dark:text-rose-200 font-medium text-sm flex items-start gap-3';
    } else {
      btn.className = 'w-full text-left p-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/30 text-slate-400 dark:text-slate-600 text-sm flex items-start gap-3 opacity-60';
    }
  });

  // Display feedback box
  const feedbackBox = document.getElementById('quiz-feedback-box');
  const title = document.getElementById('quiz-feedback-title');
  const exp = document.getElementById('quiz-feedback-explanation');
  const pearl = document.getElementById('quiz-feedback-pearl');

  if (isCorrect) {
    title.innerHTML = '<span class="text-emerald-600 dark:text-emerald-400 flex items-center gap-2"><i class="fa-solid fa-circle-check"></i> Correto! Excelente raciocínio clínico.</span>';
  } else {
    title.innerHTML = '<span class="text-rose-600 dark:text-rose-400 flex items-center gap-2"><i class="fa-solid fa-circle-xmark"></i> Incorreto. Analise os pontos-chave abaixo:</span>';
  }

  exp.innerText = qData.explanation;
  pearl.innerText = qData.highYieldPearl;
  feedbackBox.classList.remove('hidden');

  // If last question, show summary button
  const nextBtn = document.getElementById('quiz-next-btn');
  if (quizCurrentIndex === quizQuestions.length - 1) {
    nextBtn.innerText = 'Ver Resultado Final 🏆';
  } else {
    nextBtn.innerText = 'Próxima Questão ➔';
  }
}

function nextQuizQuestion() {
  if (quizCurrentIndex < quizQuestions.length - 1) {
    quizCurrentIndex++;
    renderQuizQuestion();
  } else {
    showQuizSummary();
  }
}

function showQuizSummary() {
  const container = document.getElementById('quiz-container');
  const pct = Math.round((quizScore / quizQuestions.length) * 100);
  let msg = '';
  let badgeColor = '';

  if (pct >= 80) {
    badgeColor = 'text-emerald-500';
    msg = '🏆 Nível Ivy League / USMLE 260+! Domínio exemplar dos conceitos de Medicina Materno-Fetal e Pré-Natal.';
  } else if (pct >= 60) {
    badgeColor = 'text-amber-500';
    msg = '👍 Bom desempenho! Revise os cartões de pré-eclâmpsia e rastreio de infecções congênitas para gabaritar.';
  } else {
    badgeColor = 'text-rose-500';
    msg = '📖 Continue praticando! Use o modo didático com as analogias simples para fixar as bases antes da prova.';
  }

  container.innerHTML = `
    <div class="text-center py-8">
      <div class="inline-flex items-center justify-center w-20 h-20 rounded-full bg-teal-500/10 text-teal-600 dark:text-teal-400 text-3xl font-black mb-4">
        ${pct}%
      </div>
      <h3 class="text-2xl font-bold text-slate-800 dark:text-white">Simulado Concluído!</h3>
      <p class="text-slate-600 dark:text-slate-300 mt-2">Você acertou <strong>${quizScore}</strong> de <strong>${quizQuestions.length}</strong> questões.</p>
      <p class="font-semibold mt-4 text-base ${badgeColor}">${msg}</p>
      <button onclick="restartQuiz()" class="mt-6 px-6 py-3 rounded-xl bg-teal-600 hover:bg-teal-700 text-white font-bold transition-all shadow-lg shadow-teal-500/20">
        Reiniciar Simulado
      </button>
    </div>
  `;
}

function restartQuiz() {
  quizCurrentIndex = 0;
  quizScore = 0;
  window.location.reload();
}

// --- 7. IMAGE LIGHTBOX MODAL ---
function openLightbox(src, title, caption) {
  const modal = document.getElementById('image-lightbox');
  const img = document.getElementById('lightbox-img');
  const titleEl = document.getElementById('lightbox-title');
  const captionEl = document.getElementById('lightbox-caption');

  img.src = src;
  titleEl.innerText = title;
  captionEl.innerText = caption;

  modal.classList.remove('hidden');
  modal.classList.add('flex');
}

function closeLightbox() {
  const modal = document.getElementById('image-lightbox');
  modal.classList.add('hidden');
  modal.classList.remove('flex');
}

// --- 8. AUDIO NARRATOR (Web Speech API) ---
let synth = window.speechSynthesis;
let isSpeaking = false;
let currentUtterance = null;

function toggleAudioNarration(sectionId) {
  if (synth.speaking && isSpeaking) {
    synth.cancel();
    isSpeaking = false;
    updateAudioUI(false);
    return;
  }

  const sectionEl = document.getElementById(sectionId);
  if (!sectionEl) return;

  // Clean text from icons and buttons
  const text = sectionEl.innerText
    .replace(/[^\w\sÀ-ÿ.,?!:;-]/gi, '')
    .substring(0, 3000); // limit to reasonable audio chunks

  currentUtterance = new SpeechSynthesisUtterance(text);
  currentUtterance.lang = 'pt-BR';
  currentUtterance.rate = 1.0;

  currentUtterance.onend = () => {
    isSpeaking = false;
    updateAudioUI(false);
  };

  currentUtterance.onerror = () => {
    isSpeaking = false;
    updateAudioUI(false);
  };

  synth.speak(currentUtterance);
  isSpeaking = true;
  updateAudioUI(true);
}

function updateAudioUI(playing) {
  const playBtns = document.querySelectorAll('.audio-narrate-btn');
  playBtns.forEach(btn => {
    if (playing) {
      btn.innerHTML = '<i class="fa-solid fa-pause text-amber-500 animate-pulse"></i> Pausar Leitura';
    } else {
      btn.innerHTML = '<i class="fa-solid fa-volume-high text-teal-500"></i> Ouvir Seção';
    }
  });
}

// --- 9. DIDACTIC (5 ANOS 🎈) TOGGLE ---
function toggleDidacticMode(source) {
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
}

// --- 10. QUICK SEARCH ENGINE ---
function openSearchModal() {
  const modal = document.getElementById('search-modal');
  modal.classList.remove('hidden');
  modal.classList.add('flex');
  document.getElementById('search-input').focus();
}

function closeSearchModal() {
  const modal = document.getElementById('search-modal');
  modal.classList.add('hidden');
  modal.classList.remove('flex');
}

function handleSearch(query) {
  const resultsContainer = document.getElementById('search-results');
  if (!query || query.trim().length < 2) {
    resultsContainer.innerHTML = '<p class="text-sm text-slate-400 text-center py-4">Digite ao menos 2 caracteres para buscar...</p>';
    return;
  }

  const q = query.toLowerCase();
  const searchIndex = [
    { title: "Manobras de Leopold", anchor: "#modulo-1", desc: "As 4 manobras de palpação obstétrica para identificar polo cefálico, dorso fetal e encaixamento." },
    { title: "Regra de Naegele & Idade Gestacional", anchor: "#calculadora-naegele", desc: "Cálculo da DPP: DUM + 7 dias - 3 meses + 1 ano. Datação por USG." },
    { title: "Exames Laboratoriais Pré-Natais", anchor: "#modulo-2", desc: "Rotina de 1º, 2º e 3º trimestre, sorologias, EAS, urocultura e hemograma." },
    { title: "Streptococcus agalactiae (GBS)", anchor: "#gbs-protocol", desc: "Coleta do swab 35-37 semanas e profilaxia com Penicilina G cristalina intraparto." },
    { title: "Ultrassonografia e Translucência Nucal", anchor: "#modulo-2-usg", desc: "TN ≥ 3,5mm, osso nasal e rastreio de cromossomopatias (Down, Edwards, Patau)." },
    { title: "Estratificação de Risco Gestacional", anchor: "#modulo-3", desc: "Critérios de baixo risco vs alto risco e encaminhamento oportuno." },
    { title: "Imunizações na Gestação", anchor: "#modulo-4", desc: "dTpa em CADA gestação (20-36 sem), Influenza, Hepatite B e vacinas contraindicadas." },
    { title: "Diabetes Gestacional (DMG)", anchor: "#modulo-5-dmg", desc: "Fisiopatologia (hPL e Hipótese de Pedersen), rastreio TOTG 75g e complicações fetais." },
    { title: "Pré-Eclâmpsia e Eclâmpsia", anchor: "#modulo-5-has", desc: "HAS após 20 sem + proteinúria, invasão trofoblástica rasa, sFlt-1 e disfunção endotelial." },
    { title: "Sulfato de Magnésio (Protocolo Zuspan)", anchor: "#modulo-5-mgso4", desc: "Dose de ataque 4g + 1-2g/h manutenção. Prevenção de eclâmpsia e antídoto Gluconato de Cálcio." },
    { title: "Síndrome HELLP", anchor: "#modulo-5-hellp", desc: "Hemolysis (LDH > 600), Elevated Liver enzymes (AST > 70), Low Platelets (< 100.000)." },
    { title: "Crescimento Fetal e CIUR (I vs II)", anchor: "#modulo-6-ciur", desc: "CIUR Tipo I simétrico (precoce/genético) vs Tipo II assimétrico (insuficiência placentária)." },
    { title: "Cardiotocografia (CTG) e Desacelerações", anchor: "#modulo-6-ctg", desc: "DIP I precoce (cefálica), DIP II tardia (insuficiência uteroplacentária) e DIP variável (cordão)." },
    { title: "Dopplerfluxometria Fetal", anchor: "#modulo-6-doppler", desc: "Artéria umbilical com diástole zero/reversa, ACM brain sparing e Ducto Venoso onda A reversa." },
    { title: "Perfil Biofísico Fetal (PBF)", anchor: "#calculadora-pbf", desc: "5 variáveis (MR, MC, tônus, LA, CTG), escala de 0 a 10 de Manning." },
    { title: "Gestação Múltipla & STFF", anchor: "#modulo-7", desc: "Monocoriônica vs Dicoriônica, Síndrome de Transfusão Feto-Fetal e ablação a laser." },
    { title: "Isoimunização Rh & RhoGAM", anchor: "#modulo-8", desc: "Prevenção com Imunoglobulina anti-D 28 sem + 72h pós-parto, Doppler de ACM PVS > 1,5 MoM." },
    { title: "Gestação em PVHA (HIV)", anchor: "#modulo-9", desc: "As 3 muralhas, TARV, parto pela Carga Viral (corte 1000 cópias) e contraindicação à amamentação." },
    { title: "TORCH: Sífilis e Toxoplasmose", anchor: "#modulo-10", desc: "Penicilina benzatina (única eficaz), teste de avidez de IgG, espiramicina e esquema tríplice." },
    { title: "Líquido Amniótico (Oligo vs Polidrâmnio)", anchor: "#modulo-11", desc: "ILA < 5cm (Potter, CIUR) vs ILA > 24cm (atresia esofágica, DMG)." },
    { title: "Flashcards Interativos USMLE", anchor: "#flashcards-section", desc: "20 flashcards de alta retenção com modo 3D flip." },
    { title: "Simulado USMLE Step 2 CK / Step 3", anchor: "#quiz-section", desc: "20 questões estilo vinheta clínica comentadas com pérolas da Ivy League." }
  ];

  const matches = searchIndex.filter(item => 
    item.title.toLowerCase().includes(q) || 
    item.desc.toLowerCase().includes(q)
  );

  if (matches.length === 0) {
    resultsContainer.innerHTML = '<p class="text-sm text-slate-400 text-center py-4">Nenhum resultado encontrado para o termo.</p>';
    return;
  }

  resultsContainer.innerHTML = matches.map(m => `
    <a href="${m.anchor}" onclick="closeSearchModal()" class="block p-3 rounded-lg hover:bg-teal-50 dark:hover:bg-slate-800 transition-colors border border-transparent hover:border-teal-500/20">
      <h5 class="text-sm font-bold text-teal-700 dark:text-teal-400">${m.title}</h5>
      <p class="text-xs text-slate-600 dark:text-slate-300 mt-0.5">${m.desc}</p>
    </a>
  `).join('');
}

// --- 11. INITIALIZATION ---
document.addEventListener('DOMContentLoaded', () => {
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

  renderFlashcard();
  renderQuizQuestion();
  initMgSection();
  if (typeof selectPriscillaWhite === 'function') {
    selectPriscillaWhite('A1');
  }

  // Keyboard shortcut Ctrl+K / Cmd+K for search
  window.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
      e.preventDefault();
      openSearchModal();
    }
    if (e.key === 'Escape') {
      closeSearchModal();
      closeLightbox();
    }
  });

  // Dark mode initial sync
  if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    document.documentElement.classList.add('dark');
  }

  // Scroll Progress Bar & Floating Action Button
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
  });
});

function toggleDarkMode() {
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

// --- 24. CONTROLE DINÂMICO DE TAMANHO DE FONTE (A / A+ / A++) ---
function setFontSize(size) {
  const html = document.documentElement;
  if (['normal', 'large', 'xlarge'].includes(size)) {
    html.setAttribute('data-font-size', size);
  } else {
    html.setAttribute('data-font-size', 'normal');
  }
  localStorage.setItem('fontSizePreference', size);
  
  // Atualiza estado visual dos botões de controle de fonte
  document.querySelectorAll('[data-font-btn]').forEach(btn => {
    if (btn.getAttribute('data-font-btn') === size) {
      btn.classList.add('bg-teal-600', 'text-white', 'shadow-sm');
      btn.classList.remove('text-slate-600', 'dark:text-slate-400');
    } else {
      btn.classList.remove('bg-teal-600', 'text-white', 'shadow-sm');
      btn.classList.add('text-slate-600', 'dark:text-slate-400');
    }
  });
}

// Inicializa o tamanho da fonte salvo na montagem do DOM
document.addEventListener('DOMContentLoaded', () => {
  const savedFont = localStorage.getItem('fontSizePreference') || 'normal';
  setFontSize(savedFont);
});


