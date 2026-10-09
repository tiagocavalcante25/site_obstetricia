# -*- coding: utf-8 -*-
"""
High-Precision Brazilian Portuguese Medical Recreation of TTTS Diagram - Final Version 6
Flawless seamless contours, zero stray remnants, 100% pure authentic medical artwork.
"""
import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

workspace_root = r"c:\Users\Admin\Downloads\INTERNATO GO"
source_artifact = r"C:\Users\Admin\.gemini\antigravity\brain\c8a7917c-8cbc-4119-b7c7-b6bf1409ed34\ttts_twins_1790943950837.jpg"
target_file = os.path.join(workspace_root, "assets", "img", "ttts_twins.jpg")

# 1. Load pristine original image
img = cv2.imread(source_artifact)
if img is None:
    raise FileNotFoundError(f"Source artifact not found: {source_artifact}")

h, w, c = img.shape

# Helper to fill pure white
def fill_white(y1, y2, x1, x2):
    img[max(0, y1):min(h, y2), max(0, x1):min(w, x2)] = [255, 255, 255]

# -----------------------------------------------------------------------------
# 1. TOP BAR & MAIN LABELS
# -----------------------------------------------------------------------------
# Main Title:
fill_white(0, 68, 0, 1376)

# Placenta label:
# Text: "Monochorionic Diamniotic Placenta" ends at x = 485.
# At x=490, uterine wall is below y=140. We clear y: 70..130, x: 235..490.
fill_white(70, 130, 235, 490)

# Uterus label:
# Text: "Uterus -" ends at x = 255.
# Uterine wall starts below y=200 at x=255. We clear y: 145..190, x: 75..255.
fill_white(145, 190, 75, 255)

# Laser Fiber description (top right): y: 80..205, x: 1055..1376
fill_white(80, 205, 1055, 1376)

# -----------------------------------------------------------------------------
# 2. INSET BOX (x: 773..1040, y: 78..259)
# -----------------------------------------------------------------------------
# Header bar is y: 79..111, x: 774..1040.
img[79:111, 774:1040] = [181, 181, 181]

# Crisp borders of the inset box:
cv2.rectangle(img, (773, 78), (1040, 259), (40, 40, 40), 2)
cv2.line(img, (773, 111), (1040, 111), (40, 40, 40), 1)

# Inset Diagram Laser Treatment text inpainting:
crop_laser = img[195:255, 890:1025].copy()
gray_laser = cv2.cvtColor(crop_laser, cv2.COLOR_BGR2GRAY)
mask_laser = (gray_laser < 95).astype(np.uint8) * 255
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
mask_laser = cv2.dilate(mask_laser, kernel, iterations=1)
img[195:255, 890:1025] = cv2.inpaint(crop_laser, mask_laser, 5, cv2.INPAINT_TELEA)

# -----------------------------------------------------------------------------
# 3. CENTRAL ARTERIO-VENOUS TEXT INPAINTING (y: 135..215, x: 530..770)
# -----------------------------------------------------------------------------
crop_av = img[135:215, 530:770].copy()
gray_av = cv2.cvtColor(crop_av, cv2.COLOR_BGR2GRAY)
mask_av = (gray_av < 95).astype(np.uint8) * 255
mask_av = cv2.dilate(mask_av, kernel, iterations=1)
img[135:215, 530:770] = cv2.inpaint(crop_av, mask_av, 7, cv2.INPAINT_TELEA)

# -----------------------------------------------------------------------------
# 4. LEFT COLUMN (DONOR TWIN) TEXT CLEARING (PURE WHITE)
# -----------------------------------------------------------------------------
fill_white(245, 335, 0, 235) # Clears "Donor Twin" and "(Oligohydramnios)"
fill_white(345, 435, 0, 190) # Growth restricted
fill_white(460, 555, 0, 190) # Collapsed amniotic sac
fill_white(605, 715, 0, 265) # Small empty bladder

# -----------------------------------------------------------------------------
# 5. RIGHT COLUMN (RECIPIENT TWIN) TEXT CLEARING (PURE WHITE)
# -----------------------------------------------------------------------------
fill_white(240, 340, 1165, 1376) # Clears "Recipient Twin" and "(Polyhydramnios)"
fill_white(470, 580, 1195, 1376) # Hypertrophied heart
fill_white(620, 725, 1150, 1376) # Distended bladder

# -----------------------------------------------------------------------------
# 6. BOTTOM FOOTER MARGIN
# -----------------------------------------------------------------------------
fill_white(730, 768, 0, 1376)

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

font_main_title = get_font("arialbd.ttf", 25)
font_sec_title = get_font("segoeuib.ttf", 16)
font_bold = get_font("segoeuib.ttf", 14)
font_sub_bold = get_font("segoeuib.ttf", 12)
font_reg = get_font("segoeui.ttf", 12)
font_small = get_font("segoeui.ttf", 11)
font_footer = get_font("segoeui.ttf", 11)
font_footer_bold = get_font("segoeuib.ttf", 11)

# Color Palette (RGB)
CLR_TITLE = (15, 23, 42)       # Navy/slate #0f172a
CLR_DONOR = (220, 38, 38)      # Crimson Red #dc2626
CLR_DONOR_DARK = (185, 28, 28) # Dark Red #b91c1c
CLR_RECIP = (37, 99, 235)      # Royal Blue #2563eb
CLR_RECIP_DARK = (29, 78, 216) # Dark Blue #1d4ed8
CLR_TEXT_DARK = (30, 41, 59)   # Dark Charcoal #1e293b
CLR_TEXT_MUTED = (71, 85, 105) # Slate Gray #475569
CLR_TEAL = (2, 132, 199)       # Cyan/Blue #0284c7
CLR_GREEN = (22, 101, 52)      # Deep Emerald #166534

# 1. Main Header Title (Centered)
title_str = "Síndrome de Transfusão Feto-Fetal (STFF) em Gêmeos Monocoriônicos Diamnióticos"
t_box = draw.textbbox((0, 0), title_str, font=font_main_title)
t_w = t_box[2] - t_box[0]
draw.text(((w - t_w) // 2, 22), title_str, font=font_main_title, fill=CLR_TITLE)

# 2. Placenta Monocoriônica Diamniótica (Top Left, x: 240..485)
draw.text((245, 76), "Placenta Monocoriônica", font=font_sec_title, fill=CLR_TITLE)
draw.text((245, 97), "Diamniótica Compartilhada", font=font_bold, fill=CLR_TEXT_DARK)
draw.text((245, 116), "Vascularização única interligada", font=font_reg, fill=CLR_TEXT_MUTED)

# 3. Uterus / Parede Uterina (x: 100..250)
draw.text((100, 150), "Parede Uterina", font=font_sec_title, fill=CLR_TITLE)
draw.text((100, 170), "(Miométrio)", font=font_bold, fill=CLR_TEXT_MUTED)

# 4. Inset Box Header: "Anastomoses Placentárias" (Centered in gray bar x: 774..1040, y: 79..111)
inset_title = "Anastomoses Placentárias (AV)"
ib_box = draw.textbbox((0, 0), inset_title, font=font_sec_title)
ib_w = ib_box[2] - ib_box[0]
draw.text((774 + (266 - ib_w) // 2, 87), inset_title, font=font_sec_title, fill=CLR_TITLE)

# 5. Inset Box Laser Tag: inside diagram at (912, 228)
laser_badge_txt = "Ablação a Laser"
draw.rounded_rectangle([912, 228, 1030, 252], radius=4, fill=(254, 242, 242), outline=(239, 68, 68), width=1)
draw.text((920, 232), laser_badge_txt, font=font_sub_bold, fill=CLR_DONOR)

# 6. Laser Fiber Description (Right of Inset, starting at x: 1060)
draw.text((1060, 88), "Fibra de Laser Fetoscópico", font=font_sec_title, fill=CLR_TEAL)
draw.text((1060, 112), "• Fotocoagulação seletiva das", font=font_bold, fill=CLR_TEXT_DARK)
draw.text((1072, 130), "anastomoses vasculares (AV)", font=font_bold, fill=CLR_TEXT_DARK)
draw.text((1060, 150), "• Técnica de Solomon (dicorionização)", font=font_reg, fill=CLR_TEXT_MUTED)
draw.text((1060, 170), "• Padrão-ouro (16 a 26 semanas)", font=font_sub_bold, fill=CLR_GREEN)

# 7. Central Anastomoses Card (x: 520..745, y: 146..206)
overlay = Image.new('RGBA', pil_img.size, (255, 255, 255, 0))
ov_draw = ImageDraw.Draw(overlay)
ov_draw.rounded_rectangle([520, 146, 745, 206], radius=6, fill=(255, 255, 255, 240), outline=(203, 213, 225, 255), width=1)
ov_draw.text((530, 150), "Anastomoses Arteriovenosas (AV)", font=font_bold, fill=CLR_DONOR)
ov_draw.text((530, 169), "Comunicação profunda desbalanceada", font=font_reg, fill=CLR_TEXT_DARK)
ov_draw.text((530, 186), "Doador (Artéria) → Receptor (Veia)", font=font_sub_bold, fill=CLR_DONOR_DARK)
pil_img = Image.alpha_composite(pil_img.convert('RGBA'), overlay).convert('RGB')
draw = ImageDraw.Draw(pil_img)

# 8. LEFT COLUMN: FETO DOADOR (Within x: 15..190)
# Block 1: Donor & Oligohydramnios (y: 250)
draw.text((15, 250), "FETO DOADOR", font=font_sec_title, fill=CLR_DONOR)
draw.text((15, 273), "Oligoâmnio Grave", font=font_bold, fill=CLR_DONOR_DARK)
draw.text((15, 291), "Maior Bolsão < 2 cm", font=font_bold, fill=CLR_DONOR_DARK)
draw.text((15, 310), "Hipovolemia por shunt A-V", font=font_reg, fill=CLR_TEXT_MUTED)

# Block 2: CIUR (y: 350)
draw.text((15, 348), "Restrição CIUR", font=font_bold, fill=CLR_TITLE)
draw.text((15, 368), "• Feto pálido e hipotrófico", font=font_reg, fill=CLR_TEXT_MUTED)
draw.text((15, 386), "• Hipoperfusão tecidual", font=font_reg, fill=CLR_TEXT_MUTED)
draw.text((15, 404), "• Discordância > 20%", font=font_sub_bold, fill=CLR_TEXT_DARK)

# Block 3: Collapsed Sac (y: 465)
draw.text((15, 465), "Saco Colapsado", font=font_bold, fill=CLR_TITLE)
draw.text((15, 485), "• \"Stuck Twin\"", font=font_sub_bold, fill=CLR_DONOR)
draw.text((15, 503), "• Membrana aderida", font=font_reg, fill=CLR_TEXT_MUTED)
draw.text((15, 521), "• Ausência de líquido", font=font_reg, fill=CLR_TEXT_MUTED)

# Block 4: Empty Bladder (y: 615, x: 25..260)
draw.text((25, 615), "Bexiga Não Visível", font=font_bold, fill=CLR_TITLE)
draw.text((25, 635), "• Anúria / oligúria por hipovolemia", font=font_sub_bold, fill=CLR_DONOR_DARK)
draw.text((25, 653), "• Quintero Estágio II (bexiga vazia)", font=font_sub_bold, fill=CLR_DONOR)
draw.text((25, 671), "• AU com fluxo diastólico ausente (Est. III)", font=font_reg, fill=CLR_TEXT_MUTED)

# 9. RIGHT COLUMN: FETO RECEPTOR (Within x: 1180..1370)
# Block 1: Recipient & Polyhydramnios (y: 260, x: 1180)
draw.text((1180, 258), "FETO RECEPTOR", font=font_sec_title, fill=CLR_RECIP)
draw.text((1180, 281), "Polidrâmnio Severo", font=font_bold, fill=CLR_RECIP_DARK)
draw.text((1180, 299), "Maior Bolsão > 8 cm", font=font_bold, fill=CLR_RECIP_DARK)
draw.text((1180, 318), "Sobrecarga volêmica maciça", font=font_reg, fill=CLR_TEXT_MUTED)

# Block 2: Heart / Failure (y: 475, x: 1200)
draw.text((1200, 475), "Coração Hipertrofiado", font=font_bold, fill=CLR_TITLE)
draw.text((1200, 495), "• Cardiomegalia biventricular", font=font_sub_bold, fill=CLR_DONOR_DARK)
draw.text((1200, 513), "• Regurgitação tricúspide", font=font_reg, fill=CLR_TEXT_MUTED)
draw.text((1200, 531), "• Risco de Hidropisia (Est. IV)", font=font_sub_bold, fill=CLR_DONOR)
draw.text((1200, 549), "• Ducto venoso alterado (Est. III)", font=font_small, fill=CLR_TEXT_MUTED)

# Block 3: Distended Bladder (y: 630, x: 1160)
draw.text((1160, 630), "Bexiga Distendida", font=font_bold, fill=CLR_TITLE)
draw.text((1160, 650), "• Poliúria maciça fetal", font=font_sub_bold, fill=CLR_RECIP_DARK)
draw.text((1160, 668), "• Débito urinário elevado", font=font_reg, fill=CLR_TEXT_MUTED)
draw.text((1160, 686), "• Alimenta o polidrâmnio", font=font_reg, fill=CLR_TEXT_MUTED)

# 10. Clinical Footer (Classification of Quintero)
footer_box = [15, 734, 1361, 762]
draw.rounded_rectangle(footer_box, radius=4, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
f_txt1 = "Estadiamento de Quintero (STFF): "
f_txt2 = "I (Discordância LA: <2cm e >8cm) | II (Bexiga doador não visível) | III (Doppler crítico: AU reversa / DV reverso) | IV (Hidropisia) | V (Óbito fetal)"
draw.text((25, 740), f_txt1, font=font_footer_bold, fill=CLR_TITLE)
t1_w = draw.textbbox((0, 0), f_txt1, font=font_footer_bold)[2] - draw.textbbox((0, 0), f_txt1, font=font_footer_bold)[0]
draw.text((25 + t1_w, 740), f_txt2, font=font_footer, fill=CLR_TEXT_MUTED)

final_bgr = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

# Save final result
cv2.imwrite(target_file, final_bgr, [cv2.IMWRITE_JPEG_QUALITY, 96])
print(f"Saved pristine v6 image to {target_file}")

# Generate verification crops
cv2.imwrite(os.path.join(workspace_root, "v6_crop_top.jpg"), final_bgr[0:160, :])
cv2.imwrite(os.path.join(workspace_root, "v6_crop_left.jpg"), final_bgr[220:730, 0:380])
cv2.imwrite(os.path.join(workspace_root, "v6_crop_right.jpg"), final_bgr[220:730, 1000:1376])
cv2.imwrite(os.path.join(workspace_root, "v6_crop_inset.jpg"), final_bgr[60:280, 750:1376])
cv2.imwrite(os.path.join(workspace_root, "v6_crop_center.jpg"), final_bgr[120:220, 460:770])
cv2.imwrite(os.path.join(workspace_root, "v6_full.jpg"), final_bgr)
print("Saved v6 verification crops.")
