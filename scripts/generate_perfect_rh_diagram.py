# -*- coding: utf-8 -*-
"""
Flawless Portuguese Recreation of the Rh Isoimmunization Diagram
Zero English remnants, crisp Brazilian Portuguese typography, pristine authentic illustrations.
"""
import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

source_artifact = r"C:\Users\Admin\.gemini\antigravity\brain\c8a7917c-8cbc-4119-b7c7-b6bf1409ed34\rh_isoimmunization_1790944009975.jpg"
target_file = r"c:\Users\Admin\Downloads\INTERNATO GO\assets\img\rh_isoimmunization.jpg"

orig = cv2.imread(source_artifact)
if orig is None:
    raise FileNotFoundError(f"Missing artifact: {source_artifact}")

h, w, c = orig.shape
gray = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
clean = orig.copy()

# Base Colors (BGR)
BG_WHITE = [255, 255, 255]
BG_Q1 = [231, 246, 229]
BG_Q2 = [234, 234, 252]
BG_Q3 = [230, 248, 229]
BG_Q4 = [250, 241, 225]

PILL_Q1 = [184, 224, 182]
PILL_Q2 = [190, 193, 248]
PILL_Q3 = [189, 229, 188]
PILL_Q4 = [245, 230, 205]

FLOW_PINK = [177, 188, 238]
FLOW_YELLOW = [153, 235, 246]

# -------------------------------------------------------------------------
# STEP 1: INPAINTING DELICATE ANATOMICAL ZONES
# -------------------------------------------------------------------------
# 1. Inpaint inside fetus body in Q2
mask_fbody = np.zeros((h, w), dtype=np.uint8)
fbody_gray = gray[280:390, 820:940]
mask_fbody[280:390, 820:940] = (fbody_gray < 110).astype(np.uint8) * 255
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
mask_fbody = cv2.dilate(mask_fbody, kernel, iterations=1)
clean = cv2.inpaint(clean, mask_fbody, 5, cv2.INPAINT_TELEA)

# 2. Inpaint Q1 B-cell text next to B-cell
mask_bcell = np.zeros((h, w), dtype=np.uint8)
for (y1, y2, x1, x2) in [(180, 235, 485, 630), (240, 280, 485, 605)]:
    m = (gray[y1:y2, x1:x2] < 220).astype(np.uint8) * 255
    mask_bcell[y1:y2, x1:x2] = m
mask_bcell = cv2.dilate(mask_bcell, kernel, iterations=1)
clean = cv2.inpaint(clean, mask_bcell, 5, cv2.INPAINT_TELEA)

# 3. Inpaint MCA label on fetal brain tissue in Q4
mask_mca = np.zeros((h, w), dtype=np.uint8)
crop_gray_brain = gray[625:665, 770:870]
mask_mca[625:665, 770:870] = (crop_gray_brain < 85).astype(np.uint8) * 255
mask_mca = cv2.dilate(mask_mca, kernel, iterations=1)
clean = cv2.inpaint(clean, mask_mca, 5, cv2.INPAINT_TELEA)

# -------------------------------------------------------------------------
# STEP 2: COMPLETE ERASURE & SEAMLESS RECONSTRUCTION OF BACKGROUNDS & CARDS
# -------------------------------------------------------------------------
# Top main banner: pure white
clean[0:68, :] = BG_WHITE

# 4 Header Pills
clean[68:110, 12:620] = PILL_Q1
clean[68:110, 630:1365] = PILL_Q2
clean[485:550, 12:675] = PILL_Q3
clean[485:550, 690:1365] = PILL_Q4

# Quadrant 1 (Top Left)
clean[110:182, 15:380] = BG_Q1     # Circle 1, Mother text, FMH text
clean[110:180, 385:625] = BG_Q1    # Circle 2, Maternal immune response text
clean[235:305, 215:375] = BG_Q1    # Fetal RBCs text
clean[320:385, 215:380] = BG_Q1    # Maternal circulation text
clean[295:315, 430:480] = BG_Q1    # Speck
clean[330:400, 390:615] = BG_Q1    # Anti-D antibody text
clean[388:468, 15:420] = BG_Q1     # Mother & First Fetus bottom text
clean[390:468, 422:580] = BG_WHITE # Sensitized mother card interior
cv2.rectangle(clean, (422, 390), (580, 468), (120, 140, 120), 1)

# Quadrant 2 (Top Right)
clean[110:270, 630:775] = BG_Q2    # Interface & Anti-D antibodies
clean[350:470, 630:780] = BG_Q2    # Crossing placenta & Anti-D bottom
clean[110:182, 745:965] = BG_Q2    # Subsequent fetus top text
clean[388:468, 735:950] = BG_Q2    # Subsequent fetus bottom text
clean[105:235, 1255:1365] = BG_Q2  # Hydrops text inside card
clean[190:215, 1255:1285] = BG_Q2  # Speck near Box 2
clean[375:412, 1180:1340] = BG_Q2  # After birth text
clean[440:465, 1225:1260] = BG_Q2  # Corner near Kernicterus

# Q2 Flowchart Boxes
clean[308:368, 945:1065] = FLOW_PINK
cv2.rectangle(clean, (945, 308), (1065, 368), (70, 70, 160), 2)

clean[112:192, 1010:1275] = FLOW_PINK
cv2.rectangle(clean, (1010, 112), (1275, 192), (70, 70, 160), 2)

clean[228:306, 1025:1275] = FLOW_PINK
cv2.rectangle(clean, (1025, 228), (1275, 306), (70, 70, 160), 2)

clean[368:444, 1045:1245] = FLOW_YELLOW
cv2.rectangle(clean, (1045, 368), (1245, 444), (60, 140, 160), 2)

clean[405:460, 1235:1365] = FLOW_YELLOW
cv2.rectangle(clean, (1235, 405), (1365, 460), (60, 140, 160), 2)

# Quadrant 3 (Bottom Left)
clean[550:620, 30:245] = BG_Q3     # Mechanism title
clean[566:610, 255:355] = [192, 215, 241] # Mother skin tone
clean[555:680, 375:685] = BG_Q3    # Text right of mother
clean[480:768, 670:695] = BG_Q3    # Border remnants
clean[665:758, 15:245] = BG_WHITE  # Card Left
cv2.rectangle(clean, (15, 665), (245, 758), (120, 140, 120), 1)
clean[665:758, 395:675] = BG_WHITE # Card Right
cv2.rectangle(clean, (395, 665), (675, 758), (120, 140, 120), 1)

# Quadrant 4 (Bottom Right)
clean[550:632, 680:1040] = BG_Q4   # Title above head
clean[698:760, 875:1020] = BG_Q4   # US waveform text under spectrum
clean[648:765, 1020:1370] = BG_Q4  # Action text
clean[480:768, 675:710] = BG_Q4    # Dividing border remnants
clean[548:606, 1030:1365] = BG_WHITE # Card header
clean[548:646, 1030:1085] = BG_WHITE # Card left area
cv2.rectangle(clean, (1080, 548), (1365, 646), (100, 100, 100), 1)

# Redraw step circles (1) and (2) in Q1
cv2.circle(clean, (32, 126), 15, (0, 0, 0), -1)
cv2.circle(clean, (400, 126), 16, (0, 0, 0), -1)

# -------------------------------------------------------------------------
# STEP 3: PIL HIGH-RESOLUTION TYPOGRAPHY
# -------------------------------------------------------------------------
pil_img = Image.fromarray(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB))
draw = ImageDraw.Draw(pil_img)

def get_font(size, bold=True):
    try:
        font_name = "arialbd.ttf" if bold else "arial.ttf"
        return ImageFont.truetype(font_name, size)
    except:
        try:
            font_name = "segoeuib.ttf" if bold else "segoeui.ttf"
            return ImageFont.truetype(font_name, size)
        except:
            return ImageFont.load_default()

# Colors (RGB)
C_DARK = (15, 23, 42)
C_NAVY = (11, 37, 69)
C_DARK_GREEN = (15, 56, 30)
C_BRIGHT_GREEN = (22, 101, 52)
C_RED = (185, 28, 28)
C_DARK_RED = (127, 29, 29)
C_WHITE = (255, 255, 255)
C_MUTED = (71, 85, 105)

# --- 1. TOP HEADER BANNER ---
f_top = get_font(26, bold=True)
top_text = "FISIOPATOLOGIA DA ALOIMUNIZAÇÃO Rh & DOENÇA HEMOLÍTICA PERINATAL (DHPN)"
bb = draw.textbbox((0, 0), top_text, font=f_top)
tx = (w - (bb[2] - bb[0])) // 2
draw.text((tx, 20), top_text, fill=C_DARK, font=f_top)

# --- 2. QUADRANT 1 (TOP LEFT) ---
# Pill Q1:
f_pill = get_font(16, bold=True)
draw.text((30, 80), "1. PATOGÊNESE DA ALOIMUNIZAÇÃO Rh (SENSIBILIZAÇÃO MATERNA)", fill=C_DARK_GREEN, font=f_pill)

# Numbers in circles:
f_num = get_font(18, bold=True)
draw.text((27, 115), "1", fill=C_WHITE, font=f_num)
draw.text((395, 115), "2", fill=C_WHITE, font=f_num)

# Text next to (1):
f_sec = get_font(11, bold=True)
f_sub = get_font(10, bold=False)
draw.text((55, 115), "MÃE Rh-NEGATIVA (d/d)", fill=C_DARK_GREEN, font=f_sec)
draw.text((55, 132), "Sem antígeno D (homozigota)", fill=C_DARK, font=f_sub)
draw.text((55, 148), "Ausência de resposta prévia", fill=C_MUTED, font=f_sub)

# FMH:
draw.text((195, 115), "HEMORRAGIA FETOMATERNA (HFM)", fill=C_DARK_RED, font=f_sec)
draw.text((195, 132), "Passagem de sangue fetal no parto ou", fill=C_DARK, font=f_sub)
draw.text((195, 148), "descolamento prematuro de placenta", fill=C_DARK, font=f_sub)

# Fetal RBCs (Step 1 left):
draw.text((225, 252), "HEMÁCIAS FETAIS Rh(+)", fill=C_RED, font=f_sec)
draw.text((225, 270), "Portadoras do Antígeno D (D/d)", fill=C_DARK, font=f_sub)

# Maternal circulation (Step 1 left):
draw.text((225, 335), "CIRCULAÇÃO MATERNA", fill=C_DARK_RED, font=f_sec)
draw.text((225, 353), "Entrada das hemácias Rh(+)", fill=C_DARK, font=f_sub)

# Step 2 Header (Step 2 right):
draw.text((425, 115), "RESPOSTA IMUNE MATERNA", fill=C_NAVY, font=f_sec)
draw.text((425, 132), "Reconhecimento antigênico primário", fill=C_DARK, font=f_sub)
draw.text((425, 148), "Sensibilização mediada por B-cells", fill=C_MUTED, font=f_sub)

# B-lymphocyte text:
draw.text((505, 185), "Linfócito B materno", fill=C_DARK, font=get_font(11, True))
draw.text((505, 202), "reconhece o antígeno D", fill=C_DARK, font=f_sub)

# Sensitizes arrow:
draw.text((495, 248), "SENSIBILIZAÇÃO", fill=C_BRIGHT_GREEN, font=get_font(12, True))

# Anti-D production:
draw.text((395, 342), "PRODUÇÃO DE ANTICORPOS", fill=C_DARK_GREEN, font=f_sec)
draw.text((395, 360), "IgG ANTI-D MATERNOS", fill=C_DARK_GREEN, font=f_sec)

# Mother Sensitized Card:
draw.text((435, 396), "MÃE SENSIBILIZADA", fill=C_DARK_RED, font=get_font(12, True))
draw.text((435, 416), "• Coombs Indireto (+)", fill=C_DARK, font=get_font(11, True))
draw.text((435, 432), "• Memória imunológica ativa", fill=C_DARK, font=f_sub)
draw.text((435, 448), "• Título de anticorpos > 1:16", fill=C_MUTED, font=f_sub)

# Bottom Labels Q1:
draw.text((35, 415), "MÃE Rh-NEGATIVA (d/d)", fill=C_DARK_GREEN, font=f_sec)
draw.text((35, 435), "Sem anticorpos no início", fill=C_MUTED, font=f_sub)

draw.text((205, 415), "1ª GESTAÇÃO: FETO Rh(+) (D/d)", fill=C_RED, font=f_sec)
draw.text((205, 435), "Feto hígido (sensibilização tardia)", fill=C_MUTED, font=f_sub)


# --- 3. QUADRANT 2 (TOP RIGHT) ---
# Pill Q2:
draw.text((645, 80), "2. GESTAÇÃO SUBSEQUENTE Rh(+) (FISIOPATOLOGIA DA DHPN)", fill=C_DARK_RED, font=f_pill)

# Placental interface:
draw.text((635, 115), "INTERFACE PLACENTÁRIA", fill=C_DARK_RED, font=f_sec)
draw.text((635, 134), "Barreira sinciciotrofoblástica", fill=C_DARK, font=f_sub)

draw.text((635, 185), "Anticorpos IgG Anti-D", fill=C_DARK_GREEN, font=get_font(11, True))
draw.text((635, 203), "Circulação materna", fill=C_MUTED, font=f_sub)

draw.text((635, 415), "TRANSPORTE PLACENTÁRIO", fill=C_DARK_RED, font=get_font(11, True))
draw.text((635, 433), "Passagem ativa via receptor FcRn", fill=C_DARK, font=f_sub)

# Fetus labels:
draw.text((815, 115), "FETO Rh(+) SUBSEQUENTE", fill=C_RED, font=f_sec)
draw.text((815, 133), "Alvo dos anticorpos maternos IgG anti-D", fill=C_DARK, font=f_sub)

draw.text((800, 415), "GESTAÇÃO SUBSEQUENTE Rh(+) (D/d)", fill=C_RED, font=f_sec)
draw.text((800, 435), "Acometimento fetal progressivo (DHPN)", fill=C_MUTED, font=f_sub)

# Inside fetus body:
draw.text((825, 292), "HEMÓLISE", fill=C_DARK_RED, font=get_font(11, True))
draw.text((825, 308), "EXTRAVASCULAR", fill=C_DARK_RED, font=get_font(10, True))
draw.text((825, 348), "ANEMIA FETAL", fill=C_RED, font=get_font(11, True))

# Flowchart Box 1 (Hemólise):
draw.text((962, 330), "HEMÓLISE", fill=C_NAVY, font=get_font(14, True))

# Flowchart Box 2 (Reticulocitose & Eritroblastose):
draw.text((1060, 122), "RETICULOCITOSE &", fill=C_NAVY, font=get_font(13, True))
draw.text((1050, 142), "ERITROBLASTOSE FETAL", fill=C_NAVY, font=get_font(13, True))
draw.text((1045, 164), "(Liberação de hemácias imaturas)", fill=C_DARK, font=get_font(11, False))

# Flowchart Box 3 (Insuficiência Cardíaca):
draw.text((1075, 250), "INSUFICIÊNCIA CARDÍACA", fill=C_DARK_RED, font=get_font(13, True))
draw.text((1100, 272), "DE ALTO DÉBITO", fill=C_DARK_RED, font=get_font(13, True))

# Card 4 (Hidropisia Fetal):
draw.text((1260, 110), "HIDROPISIA FETAL", fill=C_DARK_RED, font=get_font(12, True))
draw.text((1260, 130), "• Ascite volumosa", fill=C_DARK, font=get_font(10, False))
draw.text((1260, 146), "• Derrame pleural", fill=C_DARK, font=get_font(10, False))
draw.text((1260, 162), "• Edema (anasarca)", fill=C_DARK, font=get_font(10, False))
draw.text((1260, 178), "• Hepatoesplenomegalia", fill=C_MUTED, font=get_font(10, False))

# Box 5 (Icterícia Neonatal):
draw.text((1065, 380), "ICTERÍCIA NEONATAL GRAVE", fill=C_DARK_RED, font=get_font(12, True))
draw.text((1070, 402), "Hiperbilirrubinemia Indireta", fill=C_DARK, font=get_font(11, True))
draw.text((1070, 420), "(Fígado imaturo pós-parto)", fill=C_MUTED, font=get_font(10, False))

# Arrow text:
draw.text((1255, 375), "PÓS-PARTO", fill=C_DARK, font=get_font(11, True))

# Pill 6 (Kernicterus):
draw.text((1265, 414), "KERNICTERUS", fill=C_DARK_RED, font=get_font(12, True))
draw.text((1245, 432), "(Encefalopatia Bilirrubínica)", fill=C_DARK, font=get_font(9, False))


# --- 4. QUADRANT 3 (BOTTOM LEFT) ---
# Pill Q3:
draw.text((30, 502), "3. MANEJO: BLOQUEIO PROFILÁTICO COM RhoGAM (Imunoglobulina Anti-D)", fill=C_DARK_GREEN, font=f_pill)

# Mechanism title:
draw.text((35, 560), "MECANISMO DE AÇÃO DO RhoGAM", fill=C_DARK_GREEN, font=f_sec)
draw.text((35, 578), "Imunoprofilaxia Passiva com Anti-D", fill=C_MUTED, font=f_sub)

# Text on mother:
draw.text((260, 580), "Mãe Rh(-)", fill=C_DARK_GREEN, font=get_font(13, True))

# Text right of mother:
draw.text((395, 560), "LIGAÇÃO E CLAREAMENTO ESPLÊNICO:", fill=C_DARK_GREEN, font=f_sec)
draw.text((395, 580), "Os anticorpos anti-D exógenos (RhoGAM) ligam-se", fill=C_DARK, font=f_sub)
draw.text((395, 598), "rapidamente às hemácias fetais Rh(+) na circulação", fill=C_DARK, font=f_sub)
draw.text((395, 616), "materna, promovendo fagocitose e clareamento no baço", fill=C_DARK, font=f_sub)
draw.text((395, 634), "antes da sensibilização dos linfócitos B maternos.", fill=C_DARK, font=f_sub)

# Card Bottom-Left (Bloqueio):
draw.text((25, 675), "BLOQUEIO DA SENSIBILIZAÇÃO", fill=C_DARK_GREEN, font=get_font(11, True))
draw.text((25, 698), "• Neutralização antigênica rápida", fill=C_DARK, font=get_font(10, False))
draw.text((25, 715), "• Impede interação com linfócitos B", fill=C_DARK, font=get_font(10, False))
draw.text((25, 732), "• Previne a formação de memória imune", fill=C_MUTED, font=get_font(10, False))

# Card Bottom-Right (Posologia):
draw.text((405, 675), "CRONOGRAMA & POSOLOGIA (300 µg / 1500 UI):", fill=C_DARK_GREEN, font=get_font(11, True))
draw.text((405, 698), "• Rotina: 28 semanas de gestação se Coombs Indireto (-)", fill=C_DARK, font=get_font(10, False))
draw.text((405, 715), "• Pós-parto: até 72h se RN Rh(+) e Coombs Direto (-)", fill=C_DARK, font=get_font(10, False))
draw.text((405, 732), "• Eventos: aborto, sangramento, trauma, cordocentese", fill=C_MUTED, font=get_font(10, False))


# --- 5. QUADRANT 4 (BOTTOM RIGHT) ---
# Pill Q4:
draw.text((700, 502), "4. VIGILÂNCIA NÃO INVASIVA DA ANEMIA FETAL & CONDUTA", fill=C_NAVY, font=f_pill)

# Title above fetus head:
draw.text((695, 555), "VIGILÂNCIA NÃO INVASIVA DA ANEMIA FETAL", fill=C_NAVY, font=f_sec)
draw.text((695, 575), "DOPPLER DA ARTÉRIA CEREBRAL MÉDIA (ACM-PVS)", fill=C_RED, font=f_sec)
draw.text((695, 595), "Avaliação do pico de velocidade sistólica (PVS)", fill=C_MUTED, font=f_sub)

# Brain label:
draw.text((795, 638), "ACM", fill=C_RED, font=get_font(13, True))

# Spectrum text:
draw.text((885, 715), "ONDA ESPECTRAL", fill=C_NAVY, font=get_font(11, True))
draw.text((895, 732), "DO DOPPLER", fill=C_NAVY, font=get_font(11, True))

# Card Doppler Analysis Header:
draw.text((1100, 554), "ANÁLISE DAS ONDAS DOPPLER (ACM-PVS)", fill=C_NAVY, font=get_font(12, True))
draw.text((1100, 578), "FLUXO NORMAL", fill=C_BRIGHT_GREEN, font=get_font(11, True))
draw.text((1090, 594), "(Baixa vel. < 1,5 MoM)", fill=C_DARK, font=get_font(9, False))

draw.text((1235, 578), "ANEMIA FETAL GRAVE", fill=C_RED, font=get_font(11, True))
draw.text((1225, 594), "(Alta vel. > 1,5 MoM)", fill=C_DARK, font=get_font(9, False))

# Action text below Card:
draw.text((1045, 665), "• Pico > 1,5 MoM prediz anemia fetal moderada a grave", fill=C_DARK_RED, font=get_font(12, True))
draw.text((1045, 682), "  (Hiperdinamismo por menor viscosidade sanguínea)", fill=C_MUTED, font=get_font(10, False))

draw.text((1045, 706), "Conduta: Cordocentese diagnóstica imediata +", fill=C_NAVY, font=get_font(12, True))
draw.text((1045, 724), "Transfusão Intrauterina (TIU) guiada se IG < 34-35 semanas.", fill=C_NAVY, font=get_font(11, True))
draw.text((1045, 742), "Se IG ≥ 35 semanas: Corticoterapia + Interrupção programada.", fill=C_MUTED, font=get_font(10, False))

# -------------------------------------------------------------------------
# STEP 4: SAVE OUTPUT AND CROPS
# -------------------------------------------------------------------------
final_bgr = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

# Write to target
cv2.imwrite(target_file, final_bgr, [cv2.IMWRITE_JPEG_QUALITY, 98])
print(f"Successfully written final recreation to {target_file}")

# Save verification crops
cv2.imwrite("verify_final_top.jpg", final_bgr[0:220, 0:1376])
cv2.imwrite("verify_final_q1.jpg", final_bgr[70:480, 0:660])
cv2.imwrite("verify_final_q2.jpg", final_bgr[70:480, 630:1376])
cv2.imwrite("verify_final_q3.jpg", final_bgr[480:768, 0:680])
cv2.imwrite("verify_final_q4.jpg", final_bgr[480:768, 680:1376])
cv2.imwrite("verify_final_full.jpg", final_bgr)
print("Saved all final verification crops.")
