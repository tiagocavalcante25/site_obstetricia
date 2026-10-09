import re

with open('assets/js/app.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

with open('index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Find getElementById calls
ids_in_js = set(re.findall(r"getElementById\(['\"]([^'\"]+)['\"]\)", js_content))

# IDs relevant to module 5
m5_ids = [
    'gdm-weight-gain-result', 'gdm-pre-weight', 'gdm-height',
    'insulin-calc-result', 'gdm-weight',
    'pw-card-A1', 'pw-card-A2', 'pw-card-B', 'pw-card-C', 'pw-card-D', 'pw-card-F', 'pw-card-R', 'pw-card-H', 'pw-card-T',
    'pw-details-title', 'pw-details-badge', 'pw-details-criteria', 'pw-details-prognosis', 'pw-details-management',
    'gdm-total-strategy', 'gdm-partial-strategy', 'gdm-btn-total', 'gdm-btn-partial',
    'pe-risk-prev', 'pe-risk-multi', 'pe-risk-obese', 'pe-risk-hac', 'pe-risk-dm', 'pe-risk-ckd', 'pe-risk-auto', 'pe-risk-fiv',
    'pe-risk-nuli', 'pe-risk-fam', 'pe-risk-age', 'pe-risk-interv', 'pe-risk-socio', 'pe-risk-race', 'pe-risk-adverse',
    'pe-risk-result',
    'htn-profile-select', 'htn-delivery-result',
    'org-dys-hemo', 'org-dys-hep', 'org-dys-ren', 'org-dys-neuro', 'org-dys-pulm', 'org-dys-plac',
    'org-dys-result',
    'mg-renal-adjust',
    'mg-tab-zuspan1', 'mg-tab-zuspan2', 'mg-tab-sibai', 'mg-tab-pritchard', 'mg-tab-neuro', 'mg-tab-recorrencia',
    'mg-ampoule-50', 'mg-ampoule-10', 'mg-bag-padrao', 'mg-bag-concentrada', 'mg-bag-restricao', 'mg-start-time',
    'mg-protocol-title', 'mg-protocol-subtitle', 'mg-protocol-badge', 'mg-attack-val', 'mg-attack-time',
    'mg-maint-val', 'mg-maint-time', 'mg-attack-amp-val', 'mg-attack-amp-desc', 'mg-maint-amp-val', 'mg-maint-amp-desc',
    'mg-bic-ml-h', 'mg-bic-drops-min', 'mg-bic-vol-remaining', 'mg-total-attack-g', 'mg-total-maint-g', 'mg-total-24h-g',
    'mg-total-ampoules', 'mg-copy-btn-label', 'mg-copied-feedback', 'mg-prescription-textarea',
    'mg-level-val', 'mg-level-bar', 'mg-clinical-state', 'mg-action-needed'
]

missing = []
for m_id in m5_ids:
    if f'id="{m_id}"' not in html_content and f"id='{m_id}'" not in html_content:
        missing.append(m_id)

print(f"Total checked: {len(m5_ids)}")
if missing:
    print("MISSING IDs in index.html:", missing)
else:
    print("ALL MÓDULO 5 IDs EXIST IN index.html! 100% matched!")
