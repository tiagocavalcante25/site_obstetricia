# -*- coding: utf-8 -*-
"""
Perfect, Flawless Portuguese Recreation of the Rh Isoimmunization Diagram
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
# STEP 1: PRECISE INPAINTING OF TEXT INSIDE ANATOMICAL ART
# -------------------------------------------------------------------------
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

# 1. Inpaint inside fetus body in Q2 (ONLY the exact text regions)
# Upper text: "Hemolysis of FETAL RBCs"
mask_f1 = np.zeros((h, w), dtype=np.uint8)
mask_f1[250:278, 835:935] = (gray[250:278, 835:935] < 120).astype(np.uint8) * 255
mask_f1 = cv2.dilate(mask_f1, kernel, iterations=1)
clean = cv2.inpaint(clean, mask_f1, 4, cv2.INPAINT_TELEA)

# Lower text: "FETAL ANEMIA"
mask_f2 = np.zeros((h, w), dtype=np.uint8)
mask_f2[330:365, 840:915] = (gray[330:365, 840:915] < 120).astype(np.uint8) * 255
mask_f2 = cv2.dilate(mask_f2, kernel, iterations=1)
clean = cv2.inpaint(clean, mask_f2, 4, cv2.INPAINT_TELEA)

# Also smooth any residual text artifacts in that small pocket
mask_f3 = np.zeros((h, w), dtype=np.uint8)
mask_f3[275:325, 865:935] = (gray[275:325, 865:935] < 110).astype(np.uint8) * 255
mask_f3 = cv2.dilate(mask_f3, kernel, iterations=1)
clean = cv2.inpaint(clean, mask_f3, 4, cv2.INPAINT_TELEA)

# 2. Inpaint text on mother's back in Q3: "Rh-negative mother"
mask_m = np.zeros((h, w), dtype=np.uint8)
mask_m[565:605, 260:350] = (gray[565:605, 260:350] < 140).astype(np.uint8) * 255
mask_m = cv2.dilate(mask_m, kernel, iterations=1)
clean = cv2.inpaint(clean, mask_m, 4, cv2.INPAINT_TELEA)

# 3. Inpaint MCA label on fetal brain in Q4
mask_mca = np.zeros((h, w), dtype=np.uint8)
mask_mca[625:655, 770:845] = (gray[625:655, 770:845] < 85).astype(np.uint8) * 255
mask_mca = cv2.dilate(mask_mca, kernel, iterations=1)
clean = cv2.inpaint(clean, mask_mca, 4, cv2.INPAINT_TELEA)

# 4. Inpaint B-lymphocyte text in Q1
mask_b = np.zeros((h, w), dtype=np.uint8)
for (y1, y2, x1, x2) in [(180, 235, 485, 630), (240, 280, 485, 605)]:
    mask_b[y1:y2, x1:x2] = (gray[y1:y2, x1:x2] < 220).astype(np.uint8) * 255
mask_b = cv2.dilate(mask_b, kernel, iterations=1)
clean = cv2.inpaint(clean, mask_b, 5, cv2.INPAINT_TELEA)


# -------------------------------------------------------------------------
# STEP 2: COMPLETE ERASURE & SEAMLESS RECONSTRUCTION OF BACKGROUNDS & BOXES
# -------------------------------------------------------------------------
# Top main banner: pure white
clean[0:68, :] = BG_WHITE

# 4 Header Pills
clean[68:108, 12:620] = PILL_Q1
clean[68:108, 630:1365] = PILL_Q2
clean[485:545, 12:675] = PILL_Q3
clean[485:545, 685:1365] = PILL_Q4

# --- Quadrant 1 (Top Left) ---
clean[108:175, 12:370] = BG_Q1      # Circle 1, Mother text, FMH text
clean[108:175, 380:625] = BG_Q1     # Circle 2, Maternal immune response text
clean[235:300, 230:375] = BG_Q1     # Fetal RBCs text
clean[315:375, 230:375] = BG_Q1     # Maternal circulation text
clean[290:325, 415:495] = BG_Q1     # Speck between columns
clean[335:385, 390:615] = BG_Q1     # Anti-D antibody text
clean[395:475, 12:375] = BG_Q1      # Mother & First Fetus bottom text
clean[395:472, 422:575] = BG_WHITE  # Sensitized mother card interior
cv2.rectangle(clean, (422, 395), (575, 472), (120, 140, 120), 1)

# Redraw step circles (1) and (2) and divider line in Q1
cv2.circle(clean, (32, 126), 15, (0, 0, 0), -1)
cv2.circle(clean, (400, 126), 16, (0, 0, 0), -1)
cv2.line(clean, (375, 110), (375, 465), (200, 220, 200), 1)

# --- Quadrant 2 (Top Right) ---
clean[108:210, 630:770] = BG_Q2     # Interface & top Anti-D antibodies text
clean[345:410, 630:760] = BG_Q2     # Lower Anti-D antibodies text
clean[410:468, 630:770] = BG_Q2     # Crossing placenta text
clean[108:160, 770:950] = BG_Q2     # Subsequent fetus top text
clean[410:468, 745:960] = BG_Q2     # Subsequent fetus bottom text

# Q2 Flowchart Boxes (exact coordinates mapped from original grid)
clean[312:352, 948:1065] = FLOW_PINK
cv2.rectangle(clean, (948, 312), (1065, 352), (70, 70, 160), 2)

clean[114:186, 1048:1270] = FLOW_PINK
cv2.rectangle(clean, (1048, 114), (1270, 186), (70, 70, 160), 2)

clean[236:296, 1080:1248] = FLOW_PINK
cv2.rectangle(clean, (1080, 236), (1248, 296), (70, 70, 160), 2)

clean[368:442, 1076:1244] = FLOW_YELLOW
cv2.rectangle(clean, (1076, 368), (1244, 442), (60, 140, 160), 2)

clean[410:452, 1244:1365] = FLOW_YELLOW
cv2.rectangle(clean, (1244, 410), (1365, 452), (60, 140, 160), 2)

# Hydrops Fetal card text area (preserve card border and hydrops fetus baby)
clean[108:195, 1285:1365] = BG_Q2
cv2.rectangle(clean, (1285, 106), (1365, 430), (160, 140, 140), 1)

# Arrow text above Kernicterus
clean[365:395, 1190:1300] = BG_Q2

# --- Quadrant 3 (Bottom Left) ---
clean[550:600, 30:245] = BG_Q3      # Mechanism title
clean[550:660, 380:675] = BG_Q3     # Text right of mother
clean[665:755, 15:240] = BG_WHITE   # Card Left
cv2.rectangle(clean, (15, 665), (240, 755), (120, 140, 120), 1)
clean[665:755, 395:670] = BG_WHITE  # Card Right
cv2.rectangle(clean, (395, 665), (670, 755), (120, 140, 120), 1)

# --- Quadrant 4 (Bottom Right) ---
clean[548:615, 690:1025] = BG_Q4    # Title above fetus head
clean[698:755, 875:1025] = BG_Q4    # Sonogram waveform text under spectrum

# Waveform Card: ONLY clean inside the card, PRESERVING the bracket at x=1025..1055
clean[548:568, 1065:1350] = BG_WHITE  # Card header
clean[568:602, 1065:1195] = BG_WHITE  # Normal text area
clean[568:602, 1200:1350] = BG_WHITE  # Fetal anemia text area
cv2.rectangle(clean, (1060, 548), (1355, 646), (100, 100, 100), 1)

# Output text area right of bracket arrows (x > 1065)
clean[665:760, 1065:1370] = BG_Q4


# -------------------------------------------------------------------------
# STEP 3: PIL HIGH-RESOLUTION TYPOGRAPHY (BRAZILIAN PORTUGUESE)
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
draw.text((30, 78), "1. PATOGÊNESE DA ALOIMUNIZAÇÃO Rh (SENSIBILIZAÇÃO MATERNA)", fill=C_DARK_GREEN, font=f_pill)

# Step Numbers in Circles:
f_num = get_font(18, bold=True)
draw.text((27, 115), "1", fill=C_WHITE, font=f_num)
draw.text((395, 115), "2", fill=C_WHITE, font=f_num)

# Next to (1):
draw.text((55, 112), "MÃE Rh-NEGATIVA", fill=C_DARK, font=get_font(12, True))
draw.text((55, 130), "(d/d)", fill=C_DARK_GREEN, font=get_font(12, True))

# Hemorragia Fetomaterna (HFM):
draw.text((185, 110), "HEMORRAGIA", fill=C_DARK_RED, font=get_font(12, True))
draw.text((165, 128), "FETOMATERNA (HFM)", fill=C_DARK_RED, font=get_font(12, True))
draw.text((185, 146), "no parto / DPP", fill=C_MUTED, font=get_font(10, False))

# Next to (2):
draw.text((425, 112), "RESPOSTA IMUNE", fill=C_NAVY, font=get_font(12, True))
draw.text((425, 130), "MATERNA", fill=C_NAVY, font=get_font(12, True))

# Next to B-cell:
draw.text((505, 185), "Linfócito B", fill=C_DARK, font=get_font(12, True))
draw.text((505, 203), "reconhece Ag D", fill=C_DARK, font=get_font(11, False))

# Sensitization arrow:
draw.text((495, 248), "SENSIBILIZAÇÃO", fill=C_BRIGHT_GREEN, font=get_font(12, True))

# Anti-D production:
draw.text((395, 342), "PRODUÇÃO DE ANTICORPOS", fill=C_DARK_GREEN, font=get_font(12, True))
draw.text((405, 360), "IgG ANTI-D MATERNOS", fill=C_DARK_GREEN, font=get_font(12, True))

# Mother Sensitized Card:
draw.text((435, 402), "Mãe Sensibilizada", fill=C_DARK_RED, font=get_font(13, True))
draw.text((440, 424), "ao Antígeno D", fill=C_DARK, font=get_font(12, True))
draw.text((435, 446), "• Coombs Indireto (+)", fill=C_DARK_GREEN, font=get_font(11, True))

# Middle/Bottom Q1 Labels:
draw.text((235, 246), "HEMÁCIAS FETAIS Rh(+)", fill=C_RED, font=get_font(11, True))
draw.text((235, 266), "Portadoras de Antígeno D", fill=C_DARK, font=get_font(10, False))

draw.text((235, 325), "CIRCULAÇÃO MATERNA", fill=C_DARK_RED, font=get_font(11, True))
draw.text((235, 345), "Entrada das hemácias fetais", fill=C_DARK, font=get_font(10, False))

draw.text((35, 415), "MÃE Rh-NEGATIVA (d/d)", fill=C_DARK_GREEN, font=get_font(11, True))
draw.text((35, 435), "Sem anticorpos no início", fill=C_MUTED, font=get_font(10, False))

draw.text((195, 415), "1ª GESTAÇÃO: FETO Rh(+) (D/d)", fill=C_RED, font=get_font(11, True))
draw.text((195, 435), "Feto hígido (sensibilização tardia)", fill=C_MUTED, font=get_font(10, False))


# --- 3. QUADRANT 2 (TOP RIGHT) ---
# Pill Q2:
draw.text((645, 78), "2. GESTAÇÃO SUBSEQUENTE Rh(+) (FISIOPATOLOGIA DA DHPN)", fill=C_DARK_RED, font=f_pill)

# Placental Interface & Antibodies:
draw.text((635, 112), "INTERFACE FETOMATERNAL", fill=C_DARK_RED, font=get_font(11, True))

draw.text((635, 165), "ANTICORPOS IgG", fill=C_DARK_GREEN, font=get_font(11, True))
draw.text((635, 182), "ANTI-D MATERNOS", fill=C_DARK_GREEN, font=get_font(11, True))

draw.text((635, 350), "ANTICORPOS IgG", fill=C_DARK_GREEN, font=get_font(11, True))
draw.text((635, 367), "ANTI-D MATERNOS", fill=C_DARK_GREEN, font=get_font(11, True))

draw.text((635, 415), "TRANSPORTE PLACENTÁRIO", fill=C_DARK_RED, font=get_font(11, True))
draw.text((635, 433), "Passagem ativa via receptor FcRn", fill=C_DARK, font=get_font(10, False))

# Fetus labels:
draw.text((775, 112), "FETO Rh-POSITIVO", fill=C_DARK_RED, font=get_font(12, True))
draw.text((790, 130), "SUBSEQUENTE", fill=C_DARK_RED, font=get_font(12, True))

draw.text((750, 415), "FETO Rh-POSITIVO SUBSEQUENTE (D/d)", fill=C_RED, font=get_font(11, True))
draw.text((750, 435), "Acometimento fetal progressivo (DHPN)", fill=C_MUTED, font=get_font(10, False))

# Inside Fetus Body (clean text next to red blood cells):
draw.text((838, 252), "HEMÓLISE DE", fill=C_DARK_RED, font=get_font(10, True))
draw.text((838, 268), "HEMÁCIAS FETAIS", fill=C_DARK_RED, font=get_font(10, True))

draw.text((845, 335), "ANEMIA", fill=C_RED, font=get_font(11, True))
draw.text((845, 350), "FETAL", fill=C_RED, font=get_font(11, True))

# Flowchart Box 1 (Hemólise):
draw.text((962, 323), "HEMÓLISE", fill=C_NAVY, font=get_font(14, True))

# Flowchart Box 2 (Reticulocitose & Eritroblastose):
draw.text((1062, 122), "RETICULOCITOSE &", fill=C_NAVY, font=get_font(13, True))
draw.text((1052, 142), "ERITROBLASTOSE FETAL", fill=C_NAVY, font=get_font(13, True))
draw.text((1052, 164), "(Liberação de hemácias imaturas)", fill=C_DARK, font=get_font(10, False))

# Flowchart Box 3 (Insuficiência Cardíaca):
draw.text((1095, 248), "INSUFICIÊNCIA CARDÍACA", fill=C_DARK_RED, font=get_font(12, True))
draw.text((1115, 268), "DE ALTO DÉBITO", fill=C_DARK_RED, font=get_font(12, True))

# Flowchart Box 4 (Icterícia Neonatal):
draw.text((1095, 378), "ICTERÍCIA NEONATAL", fill=C_DARK_RED, font=get_font(12, True))
draw.text((1135, 398), "GRAVE", fill=C_DARK_RED, font=get_font(12, True))
draw.text((1085, 420), "(Hiperbilirrubinemia Indireta)", fill=C_DARK, font=get_font(10, False))

# Flowchart Box 5 (Kernicterus):
draw.text((1262, 415), "KERNICTERUS", fill=C_DARK_RED, font=get_font(12, True))
draw.text((1246, 433), "(Encefalopatia Bilirrubínica)", fill=C_DARK, font=get_font(9, False))

# Card Hidropisia Fetal (Far right):
draw.text((1296, 114), "HIDROPISIA", fill=C_DARK_RED, font=get_font(12, True))
draw.text((1308, 132), "FETAL", fill=C_DARK_RED, font=get_font(12, True))
draw.text((1292, 152), "• Ascite", fill=C_DARK, font=get_font(10, False))
draw.text((1292, 168), "• Derrame pleural", fill=C_DARK, font=get_font(10, False))
draw.text((1292, 184), "• Edema (anasarca)", fill=C_DARK, font=get_font(10, False))

# Arrow text above Kernicterus:
draw.text((1215, 368), "PÓS-PARTO", fill=C_DARK, font=get_font(11, True))


# --- 4. QUADRANT 3 (BOTTOM LEFT) ---
# Pill Q3:
draw.text((30, 498), "3. MANEJO: BLOQUEIO PROFILÁTICO COM RhoGAM (Imunoglobulina Anti-D)", fill=C_DARK_GREEN, font=f_pill)

# Mechanism title:
draw.text((40, 555), "MECANISMO DE AÇÃO DO RhoGAM", fill=C_DARK_GREEN, font=get_font(12, True))
draw.text((40, 575), "(Imunoprofilaxia Passiva com Anti-D)", fill=C_MUTED, font=get_font(10, False))

# On mother:
draw.text((265, 580), "Mãe Rh(-)", fill=C_DARK_GREEN, font=get_font(12, True))

# Right of mother:
draw.text((385, 560), "LIGAÇÃO E CLAREAMENTO:", fill=C_DARK_GREEN, font=get_font(11, True))
draw.text((385, 578), "Os anticorpos exógenos (RhoGAM) ligam-se", fill=C_DARK, font=get_font(10, False))
draw.text((385, 595), "às hemácias fetais Rh(+) na circulação", fill=C_DARK, font=get_font(10, False))
draw.text((385, 612), "materna, promovendo sua remoção esplênica", fill=C_DARK, font=get_font(10, False))
draw.text((385, 629), "antes da sensibilização dos linfócitos B.", fill=C_DARK, font=get_font(10, False))

# Card Bottom-Left (Bloqueio):
draw.text((25, 675), "BLOQUEIO DA SENSIBILIZAÇÃO", fill=C_DARK_GREEN, font=get_font(11, True))
draw.text((25, 698), "• Neutralização antigênica imediata", fill=C_DARK, font=get_font(10, False))
draw.text((25, 715), "• Impede interação com linfócitos B", fill=C_DARK, font=get_font(10, False))
draw.text((25, 732), "• Previne a formação de memória imune", fill=C_MUTED, font=get_font(10, False))

# Card Bottom-Right (Posologia):
draw.text((405, 675), "CRONOGRAMA & POSOLOGIA (300 µg / 1500 UI):", fill=C_DARK_GREEN, font=get_font(11, True))
draw.text((405, 698), "• Rotina: 28 semanas de gestação se Coombs Indireto (-)", fill=C_DARK, font=get_font(10, False))
draw.text((405, 715), "• Pós-parto: até 72h se recém-nascido Rh(+) e CD (-)", fill=C_DARK, font=get_font(10, False))
draw.text((405, 732), "• Eventos: aborto, DPP, sangramento, trauma, cordocentese", fill=C_MUTED, font=get_font(10, False))


# --- 5. QUADRANT 4 (BOTTOM RIGHT) ---
# Pill Q4:
draw.text((700, 498), "4. VIGILÂNCIA NÃO INVASIVA DA ANEMIA FETAL & CONDUTA", fill=C_NAVY, font=f_pill)

# Title above fetus head:
draw.text((695, 550), "VIGILÂNCIA DA ANEMIA FETAL", fill=C_NAVY, font=get_font(13, True))
draw.text((695, 570), "DOPPLER DA ARTÉRIA CEREBRAL MÉDIA", fill=C_RED, font=get_font(12, True))
draw.text((695, 590), "Pico de Velocidade Sistólica (ACM-PVS)", fill=C_MUTED, font=get_font(11, False))

# Inside Brain:
draw.text((795, 638), "ACM", fill=C_RED, font=get_font(13, True))

# Spectrum text:
draw.text((885, 705), "ONDA ESPECTRAL", fill=C_NAVY, font=get_font(11, True))
draw.text((898, 725), "DO DOPPLER", fill=C_NAVY, font=get_font(11, True))

# Card Doppler Analysis Header & Curves:
draw.text((1095, 552), "Análise das Ondas Doppler (ACM-PVS)", fill=C_NAVY, font=get_font(12, True))

draw.text((1105, 570), "FLUXO NORMAL", fill=C_BRIGHT_GREEN, font=get_font(11, True))
draw.text((1095, 588), "(Baixa vel. < 1,5 MoM)", fill=C_DARK, font=get_font(9, False))

draw.text((1220, 570), "ANEMIA FETAL GRAVE", fill=C_RED, font=get_font(11, True))
draw.text((1210, 588), "(Alta vel. > 1,5 MoM)", fill=C_DARK, font=get_font(9, False))

# Output text from bracket arrows:
draw.text((1070, 672), "• Pico > 1,5 MoM indica anemia fetal moderada a grave", fill=C_DARK_RED, font=get_font(11, True))
draw.text((1070, 690), "  (Hiperdinamismo por menor viscosidade sanguínea)", fill=C_MUTED, font=get_font(10, False))

draw.text((1070, 712), "Conduta: Cordocentese diagnóstica imediata + Transfusão", fill=C_NAVY, font=get_font(11, True))
draw.text((1070, 730), "Intrauterina (TIU) guiada se IG < 34-35 semanas.", fill=C_NAVY, font=get_font(11, True))
draw.text((1070, 748), "Se IG ≥ 35 semanas: Corticoterapia + Interrupção programada.", fill=C_MUTED, font=get_font(10, False))


# -------------------------------------------------------------------------
# STEP 4: SAVE FINAL IMAGE AND CROPS
# -------------------------------------------------------------------------
final_bgr = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

# Write to target
cv2.imwrite(target_file, final_bgr, [cv2.IMWRITE_JPEG_QUALITY, 98])
print(f"Successfully written final recreation to {target_file}")

# Save verification crops
cv2.imwrite("verify_v2_top.jpg", final_bgr[0:220, 0:1376])
cv2.imwrite("verify_v2_q1.jpg", final_bgr[70:480, 0:660])
cv2.imwrite("verify_v2_q2.jpg", final_bgr[70:480, 630:1376])
cv2.imwrite("verify_v2_q3.jpg", final_bgr[480:768, 0:680])
cv2.imwrite("verify_v2_q4.jpg", final_bgr[480:768, 680:1376])
cv2.imwrite("verify_v2_full.jpg", final_bgr)
print("Saved all v2 verification crops.")
