# 🏥 Plataforma Educacional de Medicina Materno-Fetal & Obstetrícia
## Nível Ivy League & USMLE Step 2 CK / Step 3 — Guia Interativo Dinâmico

Este projeto transforma todo o conteúdo dos **Guias de Obstetrícia e Ginecologia** em uma aplicação web interativa, ultrarrealista, altamente didática e pronta para **deploy imediato no Netlify**.

---

### 📁 Estrutura de Pastas & Organização do Projeto

O projeto está organizado de forma modular, profissional e padronizada:

```text
INTERNATO GO/
│
├── 🌐 index.html                 # Ponto de entrada da aplicação web completa
├── ⚙️ netlify.toml                # Configuração de build, cache e deploy para o Netlify
├── 📄 README.md                  # Documentação completa do projeto
│
├── 🎨 assets/                    # Recursos estáticos servidos pelo site
│   ├── css/
│   │   └── custom.css            # Estilos personalizados, animações e glassmorphism
│   ├── js/
│   │   └── app.js                # Lógica interativa (calculadoras, quiz, flashcards, busca)
│   └── img/                      # Imagens médicas HD e diagramas em português
│       ├── ctg_decelerations.jpg
│       ├── doppler_fetal_iupr.jpg
│       ├── fetal_ultrasound.jpg
│       ├── gdm_art_maternal_profile.jpg
│       ├── gdm_art_neonatal_consequences.jpg
│       ├── gdm_art_placental_diffusion.jpg
│       ├── gdm_pathophysiology.jpg
│       ├── leopold_maneuvers.jpg
│       ├── preeclampsia_pathology.jpg
│       ├── rh_isoimmunization.jpg
│       └── ttts_twins.jpg
│
├── 🧩 components/                # Elementos e seções modulares do site (HTML)
│   ├── header.html               # Barra de navegação superior, controles de tema e didática
│   ├── hero.html                 # Seção principal de introdução e chamada
│   ├── modulos-index.html        # Menu rápido de navegação em cards
│   ├── modulo-1-leopold.html     # Módulo 1: Manobras de Leopold
│   ├── calculadoras.html         # Calculadoras clínicas (Naegele, IG, DPP)
│   ├── modulo-2-ultrassom.html   # Módulo 2: Ultrassonografia Fetal & Rastreamento
│   ├── modulo-4-imunizacoes.html # Módulo 4: Protocolos de Vacinação e GBS
│   ├── modulo-5-dmg-preeclampsia.html # Módulo 5: DMG, Pré-Eclâmpsia e MgSO4
│   ├── modulo-6-ctg-doppler.html # Módulo 6: Cardiotocografia e Dopplerfluxometria
│   ├── modulo-7-stff.html        # Módulo 7: Gestação Múltipla e STFF
│   ├── modulo-8-rh.html          # Módulo 8: Isoimunização Rh e Doença Hemolítica
│   ├── modulo-9-10-11-infeccoes.html # Módulos 9, 10 e 11: HIV, TORCH e Líquido Amniótico
│   ├── flashcards.html           # Seção dos flashcards 3D interativos
│   ├── quiz-simulado.html        # Simulado com vinhetas clínicas estilo USMLE
│   ├── high-yield-summary.html   # Tabelas de alto rendimento e mnemônicos
│   ├── footer.html               # Rodapé com créditos institucionais
│   └── modals.html               # Lightbox de imagens e busca rápida (Ctrl+K)
│
├── 📚 guias/                     # Documentação médica e guias de estudo
│   ├── pdf/                      # Versões formatadas em PDF para impressão e estudo
│   │   ├── Guia Obstetricia Ginecologia Parte1.pdf
│   │   ├── Guia Obstetricia Ginecologia Parte2.pdf
│   │   └── Guia Obstetricia Ginecologia Parte3.pdf
│   └── markdown/                 # Compêndios completos em Markdown (Partes 1 a 6)
│       ├── guia-obstetricia-ginecologia-parte1.md
│       ├── guia-obstetricia-ginecologia-parte2.md
│       ├── guia-obstetricia-ginecologia-parte3.md
│       ├── guia-obstetricia-ginecologia-parte4.md  (Urgências e Emergências Obstétricas)
│       ├── guia-obstetricia-ginecologia-parte5.md  (Ginecologia Geral)
│       └── guia-obstetricia-ginecologia-parte6.md  (Infecções Ginecológicas e ISTs)
│
├── 🛠️ scripts/                   # Automação, processamento de imagem e build
│   ├── build_site.py             # Verificador de integridade e montagem dos componentes
│   ├── extract_components.py     # Extrator de componentes a partir do index.html
│   ├── build_gdm_portuguese_v2.py # Gerador de alta definição da fisiopatologia de DMG
│   ├── build_gdm_portuguese.py   # Gerador legado da imagem de DMG em português
│   ├── build_rh_portuguese.py    # Gerador do diagrama de Isoimunização Rh
│   ├── build_ttts_portuguese.py  # Gerador da ilustração de STFF
│   └── ...                       # Scripts auxiliares de colorimetria e grids
│
└── 🧪 scratch/                   # Rascunhos de desenvolvimento e recortes de teste
    └── recortes_e_testes/        # Imagens temporárias de testes e inspeções
```

---

### 🚀 Como Realizar o Deploy no Netlify

Existem três maneiras super fáceis e instantâneas de publicar este site no Netlify:

#### Opção 1: Netlify Drop (Mais rápida - Sem código ou terminal)
1. Acesse **[app.netlify.com/drop](https://app.netlify.com/drop)** no seu navegador.
2. Faça login na sua conta do Netlify (ou crie uma conta gratuita).
3. Arraste e solte esta pasta inteira (`INTERNATO GO`) na área pontilhada do Netlify Drop.
4. **Pronto!** Em menos de 10 segundos o seu site estará no ar com HTTPS gratuito e um domínio público (ex: `https://meu-guia-obstetricia.netlify.app`).

#### Opção 2: Pelo Netlify CLI
Se você possui o Node.js e o Netlify CLI instalados no seu computador:
```bash
# No terminal dentro desta pasta:
npx netlify-cli deploy --prod --dir=.
```

#### Opção 3: Conectar via Repositório GitHub
1. Suba esta pasta para um repositório no seu GitHub.
2. No painel do Netlify, clique em **"Add new site" ➔ "Import an existing project" ➔ "GitHub"**.
3. Selecione o repositório. O arquivo de configuração `netlify.toml` já configurará automaticamente o diretório de publicação raiz (`publish = "."`) e as regras de cache e redirecionamento.

---

### ✨ Recursos & Funcionalidades Interativas da Plataforma

1. **🎈 Modo Didático (5 Anos) vs Modo Ivy League (Alta Complexidade)**:
   - Alternador no topo que destaca ou recolhe as analogias infantis intuitivas, permitindo transição suave entre o entendimento conceitual rápido e a profundidade de prova do USMLE.

2. **📸 8 Imagens Médicas Clínicas e Infográficos Ultra-Realistas com Textos em Português**:
   - **Manobras de Leopold**: As 4 manobras de palpação obstétrica em modelo 3D de alta definição.
   - **Ultrassonografia Fetal & Translucência Nucal**: Varredura anatômica com NT de 2,1 mm e biometria completa.
   - **Fisiopatologia da Pré-Eclâmpsia**: Comparação da invasão trofoblástica profunda vs rasa, remodelamento de artérias espiraladas e cascata antiangiogênica (sFlt-1 e Endoglina).
   - **Cardiotocografia (CTG) e Desacelerações**: Painel comparativo das desacelerações Precoce (cabeça), Tardia (insuficiência uteroplacentária) e Variável (cordão).
   - **Dopplerfluxometria em CIUR**: Sequência de deterioração hemodinâmica (Diástole Zero e Reversa na Umbilical, Brain Sparing na ACM e Onda A Reversa no Ducto Venoso).
   - **Fisiopatologia do Diabetes Gestacional (DMG)**: Hipótese de Pedersen, hiperinsulinismo fetal, macrossomia e hipoglicemia neonatal.
   - **Síndrome de Transfusão Feto-Fetal (STFF/TTTS)**: Anatomia de gêmeos monocoriônicos com feto doador vs receptor e fotocoagulação dos vasos por laser fetoscópico.
   - **Isoimunização Rh & Doença Hemolítica**: Mecanismo de aloimunização, bloqueio com RhoGAM e monitoramento de anemia fetal pela velocidade da ACM.
   - *Lightbox em Tela Cheia*: Clique em qualquer imagem para abrir em zoom com legendas clínicas e correlações anatômicas.

3. **🧮 4 Ferramentas & Calculadoras Clínicas**:
   - **Calculadora da Regra de Naegele e Idade Gestacional**: Insira a DUM e receba instantaneamente a DPP, semanas e dias atuais, trimestre e exames recomendados no momento.
   - **Calculadora do Perfil Biofísico Fetal (PBF de Manning)**: Escore automático de 0 a 10 com conduta clínica imediata e interpretação de risco de asfixia.
   - **Verificador Diagnóstico de DMG (TOTG 75g - IADPSG/OMS)**: Validação automática dos valores de glicemia de jejum, 1 hora e 2 horas.
   - **Simulador Interativo de Toxicidade do Sulfato de Magnésio (MgSO4)**: Barra de arrasto interativa com correlação dos níveis séricos (4-7 mEq/L terapêutico, 8-10 perda de reflexo patelar, 12-15 depressão respiratória e antídoto Gluconato de Cálcio 10%).

4. **⚡ 20 Flashcards Interativos com Modo Flip 3D**:
   - Sistema de repetição espaçada e treino ativo dos conceitos mais cobrados de Medicina Materno-Fetal.

5. **🎯 Simulado Interativo USMLE Step 2 CK / Step 3**:
   - Questões completas em formato de vinheta clínica realística com alternativas, feedback imediato e **High-Yield Pearls**.

6. **🔍 Busca Instantânea Inteligente (Ctrl+K)**:
   - Indexação rápida de termos e navegação instantânea para qualquer seção ou tabela.

7. **🔊 Leitor de Áudio Integrado (Web Speech API)**:
   - Narração de cada seção em voz alta com sintetizador nativo do navegador.

8. **🌙 Modo Escuro / Claro & Impressão Formatada (PDF)**:
   - Estilização completa para leitura noturna e folha de estilos limpa para exportação ou impressão.
