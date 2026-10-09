# -*- coding: utf-8 -*-
"""
High-Precision Brazilian Portuguese Medical Recreation of Rh Isoimmunization Diagram
100% artifact-free, zero English remnants, preserved authentic medical artwork.
"""
import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

workspace_root = r"c:\Users\Admin\Downloads\INTERNATO GO"
source_artifact = r"C:\Users\Admin\.gemini\antigravity\brain\c8a7917c-8cbc-4119-b7c7-b6bf1409ed34\rh_isoimmunization_1790944009975.jpg"
target_file = os.path.join(workspace_root, "assets", "img", "rh_isoimmunization.jpg")

# 1. Load pristine original image
img = cv2.imread(source_artifact)
if img is None:
    raise FileNotFoundError(f"Source artifact not found: {source_artifact}")

h, w, c = img.shape
print(f"Loaded pristine image: {w}x{h}")

# Background colors (BGR):
BG_WHITE = [255, 255, 255]
BG_Q1 = [226, 237, 227]       # Mint green
BG_Q2 = [232, 232, 248]       # Peach/pink
BG_Q3 = [229, 252, 224]       # Mint green
BG_Q4 = [251, 242, 228]       # Ice blue

PILL_Q1 = [184, 224, 182]     # Green pill
PILL_Q2 = [190, 193, 248]     # Pink pill
PILL_Q3 = [189, 229, 188]     # Green pill
PILL_Q4 = [245, 230, 205]     # Sky blue pill (RGB: 205, 230, 245)

FLOW_PINK = [177, 188, 238]   # Flowchart pink box
FLOW_YELLOW = [153, 235, 246] # Flowchart yellow box

def fill_box(y1, y2, x1, x2, color):
    img[max(0, y1):min(h, y2), max(0, x1):min(w, x2)] = color

# ==============================================================================
# PHASE 1: TEXT CLEARING & INPAINTING
# ==============================================================================

# 1. Main Top Header:
fill_box(0, 68, 0, 1376, BG_WHITE)

# 2. Quadrant 1 (Top Left):
# Header Pill:
cv2.rectangle(img, (15, 72), (620, 108), PILL_Q1, -1)
# Step 1 Mother:
fill_box(120, 168, 55, 225, BG_Q1)
# Delivery Hemorrhage:
fill_box(120, 175, 235, 490, BG_Q1)
# Fetal RBCs:
fill_box(245, 305, 305, 500, BG_Q1)
# Maternal circulation:
fill_box(330, 375, 295, 500, BG_Q1)
# Step 2 header:
fill_box(120, 168, 545, 625, BG_Q1)
# B-cell text:
fill_box(175, 225, 545, 625, BG_Q1)
# Sensitizes:
fill_box(235, 260, 540, 625, BG_Q1)
# Antibody production:
fill_box(335, 385, 505, 625, BG_Q1)
# Mother sensitized card (inside white box y: 395..465, x: 440..580):
fill_box(395, 465, 440, 580, BG_WHITE)
cv2.rectangle(img, (440, 395), (580, 465), (50, 50, 50), 1)
# Bottom labels Q1:
fill_box(410, 468, 15, 175, BG_Q1)
fill_box(410, 468, 195, 365, BG_Q1)

# 3. Quadrant 2 (Top Right):
# Header Pill:
cv2.rectangle(img, (630, 72), (1365, 108), PILL_Q2, -1)
# Maternal-fetal interface:
fill_box(115, 155, 640, 790, BG_Q2)
# Maternal Anti-D IgG antibodies (middle):
fill_box(160, 215, 635, 785, BG_Q2)
# Crossing the placenta (bottom):
fill_box(355, 470, 635, 790, BG_Q2)
# Subsequent Rh-positive fetus (top above fetus):
fill_box(115, 170, 800, 955, BG_Q2)
# Subsequent Rh-positive fetus (bottom below fetus):
fill_box(405, 465, 800, 955, BG_Q2)

# Inpaint text inside Fetus body ("HEMOLYSIS OF FETAL RBCS" and "FETAL ANEMIA"):
crop_fbody = img[270:385, 830:930].copy()
gray_fbody = cv2.cvtColor(crop_fbody, cv2.COLOR_BGR2GRAY)
mask_fbody = (gray_fbody < 85).astype(np.uint8) * 255
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
mask_fbody = cv2.dilate(mask_fbody, kernel, iterations=1)
img[270:385, 830:930] = cv2.inpaint(crop_fbody, mask_fbody, 5, cv2.INPAINT_TELEA)

# Flowchart Box 1 (HEMOLYSIS y: 325..365, x: 935..1065):
cv2.rectangle(img, (935, 325), (1065, 365), FLOW_PINK, -1)
cv2.rectangle(img, (935, 325), (1065, 365), (70, 70, 180), 2)

# Flowchart Box 2 (RETICULOCYTOSIS y: 120..195, x: 1040..1290):
cv2.rectangle(img, (1040, 120), (1290, 195), FLOW_PINK, -1)
cv2.rectangle(img, (1040, 120), (1290, 195), (70, 70, 180), 2)

# Flowchart Box 3 (HIGH-OUTPUT CARDIAC FAILURE y: 245..315, x: 1070..1280):
cv2.rectangle(img, (1070, 245), (1280, 315), FLOW_PINK, -1)
cv2.rectangle(img, (1070, 245), (1280, 315), (70, 70, 180), 2)

# Flowchart Box 4 (HYDROPS FETALIS y: 110..370, x: 1295..1365):
# Clear text area in card: y: 112..255, x: 1298..1363
fill_box(112, 255, 1298, 1363, BG_WHITE)

# Jaundice Box (y: 390..450, x: 1040..1220):
cv2.rectangle(img, (1040, 390), (1220, 450), FLOW_YELLOW, -1)
cv2.rectangle(img, (1040, 390), (1220, 450), (60, 160, 180), 2)
# "AFTER BIRTH" text:
fill_box(390, 415, 1230, 1340, BG_Q2)
# Kernicterus pill (y: 410..460, x: 1250..1365):
cv2.rectangle(img, (1250, 410), (1365, 460), FLOW_YELLOW, -1)
cv2.rectangle(img, (1250, 410), (1365, 460), (60, 160, 180), 2)

# 4. Quadrant 3 (Bottom Left):
# Header Pill:
cv2.rectangle(img, (15, 485), (675, 545), PILL_Q3, -1)
# Mechanism of RhoGAM:
fill_box(550, 600, 15, 230, BG_Q3)
# Mother label:
fill_box(580, 630, 255, 355, BG_Q3)
# Action text:
fill_box(560, 675, 410, 675, BG_Q3)
# Card 1 (Bottom Left y: 680..755, x: 20..250):
fill_box(680, 755, 20, 250, BG_WHITE)
cv2.rectangle(img, (20, 680), (250, 755), (50, 50, 50), 1)
# Card 2 (Bottom Right of Q3 y: 685..755, x: 410..665):
fill_box(685, 755, 410, 665, BG_WHITE)
cv2.rectangle(img, (410, 685), (665, 755), (50, 50, 50), 1)

# 5. Quadrant 4 (Bottom Right):
# Header Pill:
cv2.rectangle(img, (690, 485), (1365, 545), PILL_Q4, -1)
# Subtitle (ACM-PVS):
fill_box(550, 618, 695, 1035, BG_Q4)
# Inpaint "MCA" in brain:
crop_mca = img[630:660, 810:880].copy()
gray_mca = cv2.cvtColor(crop_mca, cv2.COLOR_BGR2GRAY)
mask_mca = (gray_mca < 75).astype(np.uint8) * 255
mask_mca = cv2.dilate(mask_mca, kernel, iterations=1)
img[630:660, 810:880] = cv2.inpaint(crop_mca, mask_mca, 5, cv2.INPAINT_TELEA)
# "DOPPLER WAVEFORM" text:
fill_box(720, 762, 885, 1020, BG_Q4)
# Graph card text:
fill_box(552, 635, 1050, 1360, BG_WHITE)
# Action & interpretation text below card:
fill_box(678, 765, 1045, 1370, BG_Q4)

# ==============================================================================
# PHASE 2: TYPOGRAPHY & ANNOTATIONS (PIL)
# ==============================================================================
pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
draw = ImageDraw.Draw(pil_img)

def get_font(font_name, size):
    fonts_dir = "C:/Windows/Fonts"
    path = os.path.join(fonts_dir, font_name)
    if os.path.exists(path):
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()

font_main_title = get_font("arialbd.ttf", 23)
font_pill_title = get_font("segoeuib.ttf", 15)
font_sec_title = get_font("segoeuib.ttf", 14)
font_bold = get_font("segoeuib.ttf", 13)
font_sub_bold = get_font("segoeuib.ttf", 11)
font_reg = get_font("segoeui.ttf", 11)
font_small = get_font("segoeui.ttf", 10)

# Colors (RGB)
CLR_TITLE = (15, 23, 42)       # Navy/dark slate
CLR_DARK_GREEN = (20, 83, 45)  # Dark emerald
CLR_DARK_RED = (153, 27, 27)   # Deep crimson/wine
CLR_CRIMSON = (220, 38, 38)    # Bright red
CLR_BLUE = (37, 99, 235)       # Royal blue
CLR_DARK_BLUE = (3, 105, 161)  # Deep cyan/blue
CLR_TEXT_DARK = (30, 41, 59)   # Charcoal
CLR_TEXT_MUTED = (71, 85, 105) # Slate

# 1. Main Header Banner:
banner_txt = "FISIOPATOLOGIA DA ALOIMUNIZAÇÃO Rh & DOENÇA HEMOLÍTICA PERINATAL (DHPN)"
b_box = draw.textbbox((0, 0), banner_txt, font=font_main_title)
b_w = b_box[2] - b_box[0]
draw.text(((w - b_w) // 2, 22), banner_txt, font=font_main_title, fill=CLR_TITLE)

# -----------------------------------------------------------------------------
# QUADRANT 1: PATOGÊNESE DA SENSIBILIZAÇÃO
# -----------------------------------------------------------------------------
# Header Pill:
q1_pill_txt = "PATOGÊNESE DA ALOIMUNIZAÇÃO Rh (SENSIBILIZAÇÃO MATERNA)"
p1_box = draw.textbbox((0, 0), q1_pill_txt, font=font_pill_title)
p1_w = p1_box[2] - p1_box[0]
draw.text((15 + (605 - p1_w) // 2, 82), q1_pill_txt, font=font_pill_title, fill=CLR_DARK_GREEN)

# Step 1 Mother:
draw.text((58, 124), "MÃE Rh-NEGATIVA", font=font_bold, fill=CLR_TEXT_DARK)
draw.text((58, 144), "Genótipo (d/d)", font=font_bold, fill=CLR_DARK_GREEN)

# Delivery Hemorrhage:
draw.text((240, 124), "HEMORRAGIA FETOMATERNA (HFM)", font=font_bold, fill=CLR_TITLE)
draw.text((240, 144), "Passagem de hemácias no parto", font=font_reg, fill=CLR_TEXT_MUTED)

# Fetal RBCs:
draw.text((315, 252), "HEMÁCIAS FETAIS Rh(+)", font=font_bold, fill=CLR_CRIMSON)
draw.text((315, 272), "Expressam antígeno D na membrana", font=font_small, fill=CLR_TEXT_DARK)

# Maternal Circulation:
draw.text((305, 335), "CIRCULAÇÃO MATERNA", font=font_bold, fill=CLR_DARK_RED)
draw.text((305, 353), "Leito vascular uteroplacentário", font=font_small, fill=CLR_TEXT_MUTED)

# Step 2 header:
draw.text((548, 124), "RESPOSTA IMUNE", font=font_bold, fill=CLR_TITLE)
draw.text((548, 142), "MATERNA", font=font_bold, fill=CLR_TITLE)

# B-cell:
draw.text((548, 180), "Linfócito B materno", font=font_sub_bold, fill=CLR_TEXT_DARK)
draw.text((548, 198), "reconhece antígeno D", font=font_reg, fill=CLR_TEXT_MUTED)

# Sensitization:
draw.text((548, 238), "SENSIBILIZAÇÃO", font=font_bold, fill=CLR_CRIMSON)

# Antibody production:
draw.text((508, 342), "PRODUÇÃO DE ANTICORPOS", font=font_bold, fill=CLR_TITLE)
draw.text((508, 360), "IgG ANTI-D MATERNOS", font=font_bold, fill=CLR_DARK_GREEN)

# Mother sensitized card:
draw.text((448, 403), "Mãe Sensibilizada", font=font_bold, fill=CLR_CRIMSON)
draw.text((448, 423), "ao antígeno D fetal", font=font_reg, fill=CLR_TEXT_DARK)
draw.text((448, 441), "Coombs Indireto (+)", font=font_bold, fill=CLR_DARK_GREEN)

# Bottom labels Q1:
draw.text((20, 415), "MÃE Rh-NEGATIVA", font=font_bold, fill=CLR_TEXT_DARK)
draw.text((20, 435), "Genótipo (d/d)", font=font_bold, fill=CLR_DARK_GREEN)

draw.text((205, 415), "1º FETO Rh-POSITIVO (D/d)", font=font_bold, fill=CLR_TITLE)
draw.text((205, 435), "Geralmente hígido (sem anticorpos)", font=font_reg, fill=CLR_TEXT_MUTED)

# -----------------------------------------------------------------------------
# QUADRANT 2: GESTAÇÃO SUBSEQUENTE & DHPN
# -----------------------------------------------------------------------------
# Header Pill:
q2_pill_txt = "GESTAÇÃO SUBSEQUENTE Rh-POSITIVA (FISIOPATOLOGIA DA DHPN)"
p2_box = draw.textbbox((0, 0), q2_pill_txt, font=font_pill_title)
p2_w = p2_box[2] - p2_box[0]
draw.text((630 + (735 - p2_w) // 2, 82), q2_pill_txt, font=font_pill_title, fill=CLR_DARK_RED)

# Interface & Antibodies:
draw.text((645, 120), "INTERFACE PLACENTÁRIA", font=font_bold, fill=CLR_TITLE)
draw.text((640, 168), "ANTICORPOS IgG ANTI-D", font=font_bold, fill=CLR_DARK_GREEN)
draw.text((640, 368), "Anticorpos IgG atravessam", font=font_bold, fill=CLR_TITLE)
draw.text((640, 388), "a barreira placentária", font=font_reg, fill=CLR_TEXT_DARK)
draw.text((640, 406), "(Transporte ativo via FcRn)", font=font_sub_bold, fill=CLR_DARK_GREEN)

# Subsequent fetus labels:
draw.text((805, 120), "2º FETO Rh-POSITIVO", font=font_bold, fill=CLR_TITLE)
draw.text((805, 138), "Sensibilização prévia ativa", font=font_reg, fill=CLR_TEXT_MUTED)

draw.text((805, 412), "2º FETO Rh-POSITIVO (D/d)", font=font_bold, fill=CLR_TITLE)
draw.text((805, 432), "Alvo da hemólise imune materna", font=font_bold, fill=CLR_CRIMSON)

# Text inside fetus:
draw.text((838, 335), "HEMÓLISE", font=font_bold, fill=CLR_CRIMSON)
draw.text((838, 355), "ANEMIA FETAL", font=font_bold, fill=CLR_DARK_RED)

# Flowchart Box 1: HEMÓLISE
draw.text((950, 336), "HEMÓLISE", font=font_bold, fill=CLR_DARK_RED)

# Flowchart Box 2: ERITROBLASTOSE
draw.text((1052, 128), "ERITROBLASTOSE FETAL &", font=font_bold, fill=CLR_TITLE)
draw.text((1052, 146), "RETICULOCITOSE COMPENSATÓRIA", font=font_bold, fill=CLR_TITLE)
draw.text((1052, 166), "(Hematopoiese extramedular hepatoesplênica)", font=font_reg, fill=CLR_TEXT_MUTED)

# Flowchart Box 3: INSUFICIÊNCIA CARDÍACA
draw.text((1080, 256), "INSUFICIÊNCIA CARDÍACA", font=font_bold, fill=CLR_DARK_RED)
draw.text((1080, 274), "DE ALTO DÉBITO", font=font_bold, fill=CLR_DARK_RED)
draw.text((1080, 294), "(Hiperdinamia e hipóxia tecidual)", font=font_reg, fill=CLR_TEXT_MUTED)

# Flowchart Box 4: HIDROPISIA FETAL
draw.text((1302, 116), "HIDROPISIA", font=font_bold, fill=CLR_CRIMSON)
draw.text((1302, 134), "FETAL", font=font_bold, fill=CLR_CRIMSON)
draw.text((1302, 155), "• Ascite fetal", font=font_sub_bold, fill=CLR_TEXT_DARK)
draw.text((1302, 175), "• Derrame pleural", font=font_sub_bold, fill=CLR_TEXT_DARK)
draw.text((1302, 195), "• Edema cutâneo", font=font_sub_bold, fill=CLR_TEXT_DARK)
draw.text((1302, 215), "• Polidrâmnio", font=font_sub_bold, fill=CLR_TEXT_DARK)

# Jaundice & Kernicterus:
draw.text((1050, 400), "HIPERBILIRRUBINEMIA &", font=font_bold, fill=CLR_TITLE)
draw.text((1050, 420), "ICTERÍCIA NEONATAL GRAVE", font=font_bold, fill=CLR_TITLE)

draw.text((1235, 395), "NO PÓS-PARTO", font=font_sub_bold, fill=CLR_DARK_RED)
draw.text((1258, 422), "KERNICTERUS", font=font_bold, fill=CLR_DARK_RED)
draw.text((1255, 438), "(Encefalopatia)", font=font_small, fill=CLR_TEXT_DARK)

# -----------------------------------------------------------------------------
# QUADRANT 3: MANEJO PROFILÁTICO COM RHOGAM
# -----------------------------------------------------------------------------
# Header Pill:
q3_pill_txt = "MANEJO: BLOQUEIO PROFILÁTICO COM RhoGAM (Imunoglobulina Anti-D)"
p3_box = draw.textbbox((0, 0), q3_pill_txt, font=font_pill_title)
p3_w = p3_box[2] - p3_box[0]
draw.text((15 + (660 - p3_w) // 2, 502), q3_pill_txt, font=font_pill_title, fill=CLR_DARK_GREEN)

# Mechanism title:
draw.text((25, 555), "MECANISMO DO RhoGAM", font=font_bold, fill=CLR_TITLE)
draw.text((25, 575), "(Imunoprofilaxia Passiva)", font=font_reg, fill=CLR_DARK_GREEN)

# Mother label:
draw.text((260, 595), "Mãe Rh(-)", font=font_bold, fill=CLR_TEXT_DARK)

# Action description:
draw.text((415, 565), "LIGAÇÃO E CLAREAMENTO ESPLÊNICO:", font=font_bold, fill=CLR_TITLE)
draw.text((415, 585), "• O RhoGAM liga-se às hemácias fetais Rh(+)", font=font_reg, fill=CLR_TEXT_DARK)
draw.text((415, 603), "  na circulação materna.", font=font_reg, fill=CLR_TEXT_DARK)
draw.text((415, 623), "• Promove fagocitose pelos macrófagos", font=font_reg, fill=CLR_TEXT_MUTED)
draw.text((415, 641), "  esplênicos antes da ativação imune.", font=font_bold, fill=CLR_DARK_GREEN)

# Card 1 (Bottom Left):
draw.text((28, 688), "Bloqueio da Sensibilização", font=font_bold, fill=CLR_DARK_GREEN)
draw.text((28, 708), "Impede que linfócitos B maternos", font=font_reg, fill=CLR_TEXT_DARK)
draw.text((28, 724), "reconheçam o epítopo D fetal,", font=font_reg, fill=CLR_TEXT_DARK)
draw.text((28, 740), "anulando a produção de IgG.", font=font_bold, fill=CLR_TITLE)

# Card 2 (Bottom Right of Q3):
draw.text((418, 690), "Posologia e Cronograma (300 µg):", font=font_bold, fill=CLR_TITLE)
draw.text((418, 708), "• Profilaxia de rotina: 28 semanas de gestação", font=font_reg, fill=CLR_TEXT_DARK)
draw.text((418, 724), "• Pós-parto: em até 72h se recém-nascido Rh(+)", font=font_bold, fill=CLR_DARK_RED)
draw.text((418, 740), "• Eventos de risco: sangramento, trauma, curetagem", font=font_small, fill=CLR_TEXT_MUTED)

# -----------------------------------------------------------------------------
# QUADRANT 4: VIGILÂNCIA NÃO INVASIVA & ACM
# -----------------------------------------------------------------------------
# Header Pill:
q4_pill_txt = "MANEJO: VIGILÂNCIA NÃO INVASIVA & TRATAMENTO DA ANEMIA FETAL"
p4_box = draw.textbbox((0, 0), q4_pill_txt, font=font_pill_title)
p4_w = p4_box[2] - p4_box[0]
draw.text((690 + (675 - p4_w) // 2, 502), q4_pill_txt, font=font_pill_title, fill=CLR_DARK_BLUE)

# Subtitle:
draw.text((705, 555), "VIGILÂNCIA DA ANEMIA FETAL", font=font_bold, fill=CLR_TITLE)
draw.text((705, 575), "DOPPLER DA ARTÉRIA CEREBRAL MÉDIA", font=font_bold, fill=CLR_DARK_BLUE)
draw.text((705, 595), "Pico de Velocidade Sistólica (ACM-PVS)", font=font_reg, fill=CLR_TEXT_MUTED)

# MCA inside brain:
draw.text((828, 638), "ACM", font=font_bold, fill=CLR_DARK_RED)

# Waveform box text:
draw.text((895, 730), "ONDA ESPECTRAL DO DOPPLER", font=font_bold, fill=CLR_TITLE)

# Graph card:
draw.text((1060, 558), "Análise Espectral das Ondas do Doppler", font=font_bold, fill=CLR_TITLE)
draw.text((1065, 580), "NORMAL", font=font_bold, fill=CLR_DARK_GREEN)
draw.text((1065, 598), "(Velocidade < 1,5 MoM)", font=font_reg, fill=CLR_TEXT_MUTED)

draw.text((1205, 580), "ANEMIA FETAL", font=font_bold, fill=CLR_CRIMSON)
draw.text((1205, 598), "(Velocidade > 1,5 MoM)", font=font_bold, fill=CLR_DARK_RED)

# Action text below card:
draw.text((1055, 680), "PVS > 1,5 MoM indica anemia fetal moderada a grave.", font=font_bold, fill=CLR_DARK_RED)
draw.text((1055, 700), "• Redução da viscosidade e hiperfluxo cardíaco compensatório.", font=font_reg, fill=CLR_TEXT_DARK)
draw.text((1055, 718), "• Conduta: Cordocentese diagnóstica imediata +", font=font_bold, fill=CLR_TITLE)
draw.text((1055, 736), "  Transfusão Intrauterina (TIU) com sangue O(-) desleucocitado.", font=font_bold, fill=CLR_DARK_GREEN)

final_bgr = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

# Save target file
cv2.imwrite(target_file, final_bgr, [cv2.IMWRITE_JPEG_QUALITY, 96])
print(f"Saved regenerated image to {target_file}")

# Generate verification crops
cv2.imwrite(os.path.join(workspace_root, "verify_rh_top.jpg"), final_bgr[0:130, :])
cv2.imwrite(os.path.join(workspace_root, "verify_rh_q1.jpg"), final_bgr[70:480, 0:650])
cv2.imwrite(os.path.join(workspace_root, "verify_rh_q2.jpg"), final_bgr[70:480, 630:1376])
cv2.imwrite(os.path.join(workspace_root, "verify_rh_q3.jpg"), final_bgr[480:768, 0:680])
cv2.imwrite(os.path.join(workspace_root, "verify_rh_q4.jpg"), final_bgr[480:768, 680:1376])
cv2.imwrite(os.path.join(workspace_root, "verify_rh_full.jpg"), final_bgr)
print("Saved all Rh verification crops.")
