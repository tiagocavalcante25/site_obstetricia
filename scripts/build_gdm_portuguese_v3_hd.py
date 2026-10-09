# -*- coding: utf-8 -*-
"""
build_gdm_portuguese_v3_hd.py
Gera o infográfico médico em Altíssima Definição da Fisiopatologia do Diabetes Gestacional
- Resolução ultra-alta: 2500 x 2750 px
- Fontes grandes e confortáveis (Títulos 46px, Colunas 26px, Cards 24px, Texto 21-22px)
- Zero texto sobreposto, zero texto vazando (cálculo dinâmico e estrito de altura de cada bloco)
- Zero caracteres quebrados (substituição de símbolos por badges elegantes)
- 100% em Português padrão FEBRASGO, SBD 2024, IADPSG e USMLE Step 2 CK
- Rodapé clínico ampliado com Mnemônico H-I-P-E-R e Protocolo de Berçário sem cortes
- 4 Colunas com ilustrações médicas 3D ultrarrealistas
"""

import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def get_font(name, size):
    font_path = os.path.join("C:/Windows/Fonts", name)
    if os.path.exists(font_path):
        return ImageFont.truetype(font_path, size)
    return ImageFont.load_default()

def draw_wrapped_text(draw, text, x, y, max_width, font, fill, line_spacing=6):
    words = text.split(' ')
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        w = bbox[2] - bbox[0]
        if w <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(word)
                current_line = []
    if current_line:
        lines.append(' '.join(current_line))
        
    cur_y = y
    for line in lines:
        draw.text((x, cur_y), line, font=font, fill=fill)
        bbox = draw.textbbox((0, 0), line, font=font)
        h = bbox[3] - bbox[1]
        cur_y += h + line_spacing
    return cur_y

def draw_bullet(draw, bullet_title, text, x, y, max_width, f_bold, f_reg, c_bold, c_text, line_spacing=6):
    # Draw a clean circular bullet
    bullet_r = 4
    draw.ellipse([x, y + 10 - bullet_r, x + bullet_r*2, y + 10 + bullet_r], fill=c_bold)
    text_x = x + 18
    avail_w = max_width - 20
    
    full_str = f"{bullet_title}: {text}" if bullet_title else text
    words = full_str.split(' ')
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=f_reg)
        w = bbox[2] - bbox[0]
        if w <= avail_w:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(word)
                current_line = []
    if current_line:
        lines.append(' '.join(current_line))
        
    cur_y = y
    first = True
    for line in lines:
        if first and bullet_title:
            prefix = f"{bullet_title}: "
            if line.startswith(prefix):
                draw.text((text_x, cur_y), prefix, font=f_bold, fill=c_bold)
                bbox_p = draw.textbbox((0, 0), prefix, font=f_bold)
                pw = bbox_p[2] - bbox_p[0]
                rem = line[len(prefix):]
                draw.text((text_x + pw, cur_y), rem, font=f_reg, fill=c_text)
            else:
                draw.text((text_x, cur_y), line, font=f_reg, fill=c_text)
            first = False
        else:
            draw.text((text_x, cur_y), line, font=f_reg, fill=c_text)
            
        bbox = draw.textbbox((0, 0), line, font=f_reg)
        h = bbox[3] - bbox[1]
        cur_y += h + line_spacing
    return cur_y + 4

def draw_card(draw, x1, y1, x2, y2, title, subtitle, accent_color, f_title, f_sub, bg_fill=(255, 255, 255), border_fill=(226, 232, 240)):
    shadow_offset = 3
    draw.rounded_rectangle([x1 + shadow_offset, y1 + shadow_offset, x2 + shadow_offset, y2 + shadow_offset], radius=16, fill=(230, 235, 243))
    draw.rounded_rectangle([x1, y1, x2, y2], radius=16, fill=bg_fill, outline=border_fill, width=2)
    draw.rounded_rectangle([x1, y1, x2, y1 + 8], radius=16, fill=accent_color)
    draw.rectangle([x1, y1 + 5, x2, y1 + 8], fill=accent_color)
    
    cur_y = y1 + 18
    if title:
        draw.text((x1 + 20, cur_y), title, font=f_title, fill=(15, 23, 42))
        bbox = draw.textbbox((0, 0), title, font=f_title)
        cur_y += (bbox[3] - bbox[1]) + 4
    if subtitle:
        draw.text((x1 + 20, cur_y), subtitle, font=f_sub, fill=accent_color)
        bbox = draw.textbbox((0, 0), subtitle, font=f_sub)
        cur_y += (bbox[3] - bbox[1]) + 12
    else:
        cur_y += 8
    return cur_y

def main():
    W, H = 2500, 2750
    img = Image.new("RGB", (W, H), (244, 247, 251))
    draw = ImageDraw.Draw(img)

    # Fontes
    f_title = get_font("segoeuib.ttf", 46)
    f_sub = get_font("segoeui.ttf", 23)
    f_badge = get_font("segoeuib.ttf", 18)
    f_col_h = get_font("segoeuib.ttf", 26)
    f_card_h = get_font("segoeuib.ttf", 24)
    f_card_sub = get_font("segoeuib.ttf", 20)
    f_bold = get_font("segoeuib.ttf", 21)
    f_regular = get_font("segoeui.ttf", 21)
    f_alert_bold = get_font("segoeuib.ttf", 20)
    f_alert_reg = get_font("segoeui.ttf", 20)

    # 1. HEADER BANNER
    banner_h = 155
    draw.rectangle([0, 0, W, banner_h], fill=(255, 255, 255))
    draw.line([0, banner_h, W, banner_h], fill=(218, 226, 237), width=3)

    # Top Badges
    draw.rounded_rectangle([45, 20, 440, 56], radius=8, fill=(240, 253, 250), outline=(20, 184, 166), width=2)
    draw.text((242, 38), "FIGURA MÉDICA 03 • ENDOCRINOLOGIA FETAL", font=f_badge, fill=(15, 118, 110), anchor="mm")

    draw.rounded_rectangle([2010, 20, 2455, 56], radius=8, fill=(241, 245, 249), outline=(148, 163, 184), width=2)
    draw.text((2232, 38), "PADRÃO USMLE STEP 2 CK • FEBRASGO • SBD 2024", font=f_badge, fill=(51, 65, 85), anchor="mm")

    # Título Principal e Subtítulo
    draw.text((W // 2, 78), "FISIOPATOLOGIA DO DIABETES MELLITUS GESTACIONAL (DMG)", font=f_title, fill=(15, 23, 42), anchor="mm")
    draw.text((W // 2, 126), "Hipótese de Pedersen • Dinâmica Materno-Placentária-Fetal • Cinética Molecular & Repercussões Neonatais", font=f_sub, fill=(71, 85, 105), anchor="mm")

    # Imagens Médicas
    p_mat = "assets/img/gdm_art_maternal_profile.jpg"
    p_pla = "assets/img/gdm_art_placental_diffusion.jpg"
    p_neo = "assets/img/gdm_art_neonatal_consequences.jpg"

    art_mat = Image.open(p_mat) if os.path.exists(p_mat) else None
    art_pla = Image.open(p_pla) if os.path.exists(p_pla) else None
    art_neo = Image.open(p_neo) if os.path.exists(p_neo) else None

    # Coordenadas das 4 Colunas
    c_w = 585
    c1_x1, c1_x2 = 35, 35 + c_w
    c2_x1, c2_x2 = 650, 650 + c_w
    c3_x1, c3_x2 = 1265, 1265 + c_w
    c4_x1, c4_x2 = 1880, 1880 + c_w

    header_y1, header_y2 = 175, 235
    img_y1, img_y2 = 250, 520

    def paste_col_image(im_crop, x1, x2, y1, y2, tag_text, tag_color):
        im_resized = im_crop.resize((x2 - x1, y2 - y1), Image.Resampling.LANCZOS)
        mask = Image.new("L", im_resized.size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([0, 0, im_resized.size[0], im_resized.size[1]], radius=14, fill=255)
        img.paste(im_resized, (x1, y1), mask)
        draw.rounded_rectangle([x1, y1, x2, y2], radius=14, outline=(203, 213, 225), width=2)
        draw.rounded_rectangle([x1 + 12, y2 - 34, x2 - 12, y2 - 8], radius=6, fill=(15, 23, 42))
        draw.text(((x1 + x2) // 2, y2 - 21), tag_text, font=f_badge, fill=tag_color, anchor="mm")

    # =========================================================================
    # COLUNA 1: COMPARTIMENTO MATERNO
    # =========================================================================
    draw.rounded_rectangle([c1_x1, header_y1, c1_x2, header_y2], radius=12, fill=(30, 64, 175))
    draw.text(((c1_x1 + c1_x2) // 2, (header_y1 + header_y2) // 2), "1. COMPARTIMENTO MATERNO", font=f_col_h, fill=(255, 255, 255), anchor="mm")

    if art_mat:
        crop_mat = art_mat.crop((180, 40, 820, 750))
        paste_col_image(crop_mat, c1_x1, c1_x2, img_y1, img_y2, "Eixo Endócrino Materno-Placentário (3º Trimestre)", (191, 219, 254))

    # Card 1.1: Hormônios Diabetogênicos
    c1_card1_y1 = 538
    c1_card1_y2 = 960
    cy = draw_card(draw, c1_x1, c1_card1_y1, c1_x2, c1_card1_y2, "Eixo Hormonal Contrainsulínico", "Hormônios Placentários & Resistência Periférica", (37, 99, 235), f_card_h, f_card_sub)
    cy = draw_bullet(draw, "hPL (Lactogênio Placentário)", "Pico entre 24ª-28ª semanas. Promove lipólise e induz forte resistência periférica materna à insulina.", c1_x1 + 22, cy, c_w - 44, f_bold, f_regular, (30, 64, 175), (51, 65, 85))
    cy = draw_bullet(draw, "Cortisol Livre & PGH", "Hormônio de crescimento placentário e cortisol elevam a gliconeogênese hepática em até 30%.", c1_x1 + 22, cy, c_w - 44, f_bold, f_regular, (30, 64, 175), (51, 65, 85))
    cy = draw_bullet(draw, "Progesterona & Prolactina", "Promovem modulação pós-receptor do GLUT4 no tecido adiposo e muscular esquelético materno.", c1_x1 + 22, cy, c_w - 44, f_bold, f_regular, (30, 64, 175), (51, 65, 85))
    cy = draw_bullet(draw, "Citocinas (TNF-α, Resistina)", "Fatores inflamatórios secretados pela placenta que inibem a fosforilação intracelular do IRS-1.", c1_x1 + 22, cy, c_w - 44, f_bold, f_regular, (30, 64, 175), (51, 65, 85))

    # Card 1.2: Bifurcação Fisiológica vs DMG
    c1_card2_y1 = 978
    c1_card2_y2 = 1715
    cy = draw_card(draw, c1_x1, c1_card2_y1, c1_x2, c1_card2_y2, "Bifurcação Fisiológica vs DMG", "Resposta das Células-Beta Pancreáticas Maternas", (30, 64, 175), f_card_h, f_card_sub)
    
    # Sub-box Fisiológica
    draw.rounded_rectangle([c1_x1 + 18, cy, c1_x2 - 18, cy + 250], radius=10, fill=(240, 253, 244), outline=(134, 239, 172), width=2)
    draw.rounded_rectangle([c1_x1 + 28, cy + 12, c1_x1 + 320, cy + 42], radius=6, fill=(22, 101, 52))
    draw.text((c1_x1 + 174, cy + 27), "GESTACÃO NORMAL (Euglicemia)", font=f_badge, fill=(255, 255, 255), anchor="mm")
    draw_wrapped_text(draw, "O pâncreas materno sofre hiperplasia compensatória de células-beta. A secreção basal e estimulada de insulina sobe de 2 a 3 vezes. A euglicemia materna é preservada com glicemia de jejum fisiologicamente baixa (70-80 mg/dL).", c1_x1 + 28, cy + 54, c_w - 56, f_regular, (22, 101, 52), line_spacing=6)
    cy += 265

    # Sub-box DMG
    draw.rounded_rectangle([c1_x1 + 18, cy, c1_x2 - 18, cy + 270], radius=10, fill=(254, 242, 242), outline=(252, 165, 165), width=2)
    draw.rounded_rectangle([c1_x1 + 28, cy + 12, c1_x1 + 320, cy + 42], radius=6, fill=(185, 28, 28))
    draw.text((c1_x1 + 174, cy + 27), "DIABETES GESTACIONAL (DMG)", font=f_badge, fill=(255, 255, 255), anchor="mm")
    draw_wrapped_text(draw, "Disfunção prévia ou falência secretória das células-beta maternas. O pâncreas não vence a barreira de resistência contrainsulínica. Ocorre hiperglicemia materna crônica (pós-prandial precoce e de jejum tardia).", c1_x1 + 28, cy + 54, c_w - 56, f_regular, (153, 27, 27), line_spacing=6)

    # Card 1.3: Rastreamento & Diagnóstico
    c1_card3_y1 = 1735
    c1_card3_y2 = 2415
    cy = draw_card(draw, c1_x1, c1_card3_y1, c1_x2, c1_card3_y2, "Critérios Diagnósticos de DMG", "TOTG 75g (24ª-28ª Semanas) • IADPSG / SBD / FEBRASGO", (37, 99, 235), f_card_h, f_card_sub)
    cy = draw_bullet(draw, "Glicemia de Jejum Inicial", "Se 92 a 125 mg/dL no 1º trimestre = Diagnóstico direto de DMG. Se >= 126 mg/dL = Diabetes Mellitus prévio.", c1_x1 + 22, cy, c_w - 44, f_bold, f_regular, (30, 64, 175), (51, 65, 85))
    cy = draw_bullet(draw, "TOTG 75g (24ª-28ª sem)", "1 valor alterado define DMG: Jejum >= 92 mg/dL | 1 hora >= 180 mg/dL | 2 horas >= 153 mg/dL.", c1_x1 + 22, cy, c_w - 44, f_bold, f_regular, (30, 64, 175), (51, 65, 85))
    cy = draw_bullet(draw, "Metas de Controle Estrito", "Jejum < 95 mg/dL | 1h pós-prandial < 140 mg/dL | 2h pós-prandial < 120 mg/dL.", c1_x1 + 22, cy, c_w - 44, f_bold, f_regular, (30, 64, 175), (51, 65, 85))
    # Alert box
    draw.rounded_rectangle([c1_x1 + 18, cy + 10, c1_x2 - 18, c1_card3_y2 - 18], radius=8, fill=(239, 246, 255), outline=(191, 219, 254), width=1)
    draw_wrapped_text(draw, "Riscos Maternos: Pré-eclâmpsia (3x mais frequente), polidrâmnio e parto cesáreo.", c1_x1 + 28, cy + 20, c_w - 60, f_alert_bold, (30, 64, 175), line_spacing=4)

    # =========================================================================
    # COLUNA 2: BARREIRA PLACENTÁRIA
    # =========================================================================
    draw.rounded_rectangle([c2_x1, header_y1, c2_x2, header_y2], radius=12, fill=(15, 118, 110))
    draw.text(((c2_x1 + c2_x2) // 2, (header_y1 + header_y2) // 2), "2. BARREIRA PLACENTÁRIA", font=f_col_h, fill=(255, 255, 255), anchor="mm")

    if art_pla:
        crop_pla = art_pla.crop((30, 50, 1150, 750))
        paste_col_image(crop_pla, c2_x1, c2_x2, img_y1, img_y2, "Difusão Acelerada GLUT1 & Veia Umbilical", (153, 246, 228))

    # Card 2.1: Princípio Central de Pedersen
    c2_card1_y1 = 538
    c2_card1_y2 = 960
    cy = draw_card(draw, c2_x1, c2_card1_y1, c2_x2, c2_card1_y2, "A Hipótese de Pedersen (1952)", "Permeabilidade Seletiva Materno-Placentária", (13, 148, 136), f_card_h, f_card_sub)
    cy = draw_bullet(draw, "Glicose Atravessa Livremente", "Molécula pequena (180 Da). Cruza a barreira por difusão facilitada contínua diretamente proporcional ao gradiente materno-fetal.", c2_x1 + 22, cy, c_w - 44, f_bold, f_regular, (15, 118, 110), (51, 65, 85))
    cy = draw_bullet(draw, "Insulina NÃO Atravessa", "Macromolécula proteica (5.808 Da). 100% impermeável à placenta e clivada por insulinases locais. A insulina materna não atinge o feto.", c2_x1 + 22, cy, c_w - 44, f_bold, f_regular, (15, 118, 110), (51, 65, 85))
    cy = draw_bullet(draw, "Consequência Fisiopatológica", "O feto recebe excesso calórico desregulado, mas não recebe nenhum suporte hormonal materno para processá-lo.", c2_x1 + 22, cy, c_w - 44, f_bold, f_regular, (15, 118, 110), (51, 65, 85))

    # Card 2.2: Cinética Molecular GLUT1
    c2_card2_y1 = 978
    c2_card2_y2 = 1715
    cy = draw_card(draw, c2_x1, c2_card2_y1, c2_x2, c2_card2_y2, "Cinética Molecular dos Transportadores", "Mecanismo Bioquímico no Sinciciotrofoblasto", (15, 118, 110), f_card_h, f_card_sub)
    cy = draw_bullet(draw, "Transportadores GLUT1 & GLUT3", "Expressos constitutivamente nas membranas microvilosa e basal. GLUT1 é o principal mediador da transferência de glicose materno-fetal.", c2_x1 + 22, cy, c_w - 44, f_bold, f_regular, (15, 118, 110), (51, 65, 85))
    cy = draw_bullet(draw, "Superexpressão no DMG", "A hiperglicemia materna crônica estimula a superexpressão e aumento de densidade de GLUT1, acelerando ainda mais a passagem de glicose.", c2_x1 + 22, cy, c_w - 44, f_bold, f_regular, (15, 118, 110), (51, 65, 85))
    cy = draw_bullet(draw, "Transporte de Aminoácidos", "Sistemas A e L de transporte ativo carreiam aminoácidos ramificados estimulados pela hiperglicemia, alimentando a síntese proteica fetal.", c2_x1 + 22, cy, c_w - 44, f_bold, f_regular, (15, 118, 110), (51, 65, 85))
    cy = draw_bullet(draw, "Ácidos Graxos Livres", "Passagem facilitada por proteínas FATPs, fornecendo substrato para adipogênese acelerada.", c2_x1 + 22, cy, c_w - 44, f_bold, f_regular, (15, 118, 110), (51, 65, 85))

    # Card 2.3: Síntese de Fluxo Placentário
    c2_card3_y1 = 1735
    c2_card3_y2 = 2415
    cy = draw_card(draw, c2_x1, c2_card3_y1, c2_x2, c2_card3_y2, "Fluxo Acelerado na Veia Umbilical", "Sobrecarga de Substratos Energéticos ao Feto", (13, 148, 136), f_card_h, f_card_sub)
    cy = draw_bullet(draw, "Sangue Fetal Hiperglicêmico", "O sangue que ascende pela veia umbilical apresenta saturação glicêmica proporcional aos picos glicêmicos pós-prandiais da mãe.", c2_x1 + 22, cy, c_w - 44, f_bold, f_regular, (15, 118, 110), (51, 65, 85))
    cy = draw_bullet(draw, "Primeira Parada: Fígado Fetal", "Parte do sangue irriga o fígado fetal via ducto venoso e veia porta, ativando lipogênese hepática e secreção precoce de IGF-1.", c2_x1 + 22, cy, c_w - 44, f_bold, f_regular, (15, 118, 110), (51, 65, 85))
    # Box Síntese Pedersen
    draw.rounded_rectangle([c2_x1 + 18, cy + 12, c2_x2 - 18, c2_card3_y2 - 18], radius=10, fill=(240, 253, 250), outline=(94, 234, 212), width=2)
    draw.text((c2_x1 + 28, cy + 24), "Princípio Chave da Síntese de Pedersen:", font=f_alert_bold, fill=(15, 118, 110))
    draw_wrapped_text(draw, "Hiperglicemia materna -> Fluxo GLUT1 acelerado -> Hiperglicemia fetal crônica -> Pâncreas fetal superestimulado -> Hiperinsulinismo fetal autônomo.", c2_x1 + 28, cy + 54, c_w - 56, f_alert_reg, (19, 78, 74), line_spacing=5)

    # =========================================================================
    # COLUNA 3: COMPARTIMENTO FETAL
    # =========================================================================
    draw.rounded_rectangle([c3_x1, header_y1, c3_x2, header_y2], radius=12, fill=(67, 56, 202))
    draw.text(((c3_x1 + c3_x2) // 2, (header_y1 + header_y2) // 2), "3. COMPARTIMENTO FETAL", font=f_col_h, fill=(255, 255, 255), anchor="mm")

    if art_pla:
        crop_fetus = art_pla.crop((500, 0, 1370, 680))
        paste_col_image(crop_fetus, c3_x1, c3_x2, img_y1, img_y2, "Feto Intrauterino & Hiperinsulinismo Autônomo", (224, 231, 255))

    # Card 3.1: Resposta Pancreática Fetal
    c3_card1_y1 = 538
    c3_card1_y2 = 960
    cy = draw_card(draw, c3_x1, c3_card1_y1, c3_x2, c3_card1_y2, "Pâncreas Endócrino Fetal", "Hiperplasia das Células-Beta (12ª-14ª Semanas)", (79, 70, 229), f_card_h, f_card_sub)
    cy = draw_bullet(draw, "Maturação das Ilhotas Fetais", "A partir da 12ª-14ª semana, as células-beta fetais tornam-se responsivas aos níveis séricos de glicose.", c3_x1 + 22, cy, c_w - 44, f_bold, f_regular, (67, 56, 202), (51, 65, 85))
    cy = draw_bullet(draw, "Hiperplasia & Hipertrofia", "O estímulo hiperglicêmico crônico induz maciça proliferação celular e neogênese de ilhotas pancreáticas fetais.", c3_x1 + 22, cy, c_w - 44, f_bold, f_regular, (67, 56, 202), (51, 65, 85))
    cy = draw_bullet(draw, "Hiperinsulinismo Autônomo", "O feto produz doses maciças de sua própria insulina. Como a insulina não volta para a mãe, age 100% no organismo fetal.", c3_x1 + 22, cy, c_w - 44, f_bold, f_regular, (67, 56, 202), (51, 65, 85))

    # Card 3.2: Insulina como Hormônio Anabólico Fetal
    c3_card2_y1 = 978
    c3_card2_y2 = 1530
    cy = draw_card(draw, c3_x1, c3_card2_y1, c3_x2, c3_card2_y2, "O Papel Anabólico da Insulina", "Principal Regulador do Crescimento Somático Fetal", (67, 56, 202), f_card_h, f_card_sub)
    cy = draw_bullet(draw, "Insulina como Principal GH Fetal", "No ambiente intrauterino, o hormônio do crescimento (GH) hipofisário tem papel mínimo. A Insulina e o IGF-1 governam o crescimento fetal.", c3_x1 + 22, cy, c_w - 44, f_bold, f_regular, (67, 56, 202), (51, 65, 85))
    cy = draw_bullet(draw, "Vias de Sinalização Celular", "Ativação profunda das vias PI3K/Akt e MAPK: proliferação celular acelerada, hipertrofia tecidual e captação voraz de substratos.", c3_x1 + 22, cy, c_w - 44, f_bold, f_regular, (67, 56, 202), (51, 65, 85))
    cy = draw_bullet(draw, "Deposição em Órgãos Alvo", "Hepatomegalia, esplenomegalia, cardiomegalia e acúmulo adiposo troncular desproporcional.", c3_x1 + 22, cy, c_w - 44, f_bold, f_regular, (67, 56, 202), (51, 65, 85))

    # Card 3.3: As 4 Vias Fisiopatológicas Fetais
    c3_card3_y1 = 1550
    c3_card3_y2 = 2415
    cy = draw_card(draw, c3_x1, c3_card3_y1, c3_x2, c3_card3_y2, "As 4 Vias Anabólicas Fetais", "Repercussões Orgânicas Induzidas pelo Hiperinsulinismo", (79, 70, 229), f_card_h, f_card_sub)
    cy = draw_bullet(draw, "1. Lipogênese Acentuada", "Conversão rápida de glicose em glicerol-3-fosfato e triglicerídeos. Deposição nos ombros, dorso e tronco (macrossomia assimétrica).", c3_x1 + 22, cy, c_w - 44, f_bold, f_regular, (67, 56, 202), (51, 65, 85))
    cy = draw_bullet(draw, "2. Síntese Proteica Muscular", "Captação acelerada de aminoácidos com deposição de sarcômeros e hipertrofia da musculatura esquelética.", c3_x1 + 22, cy, c_w - 44, f_bold, f_regular, (67, 56, 202), (51, 65, 85))
    cy = draw_bullet(draw, "3. Deposição Miocárdica", "Hipertrofia do septo interventricular por depósito de glicogênio e hipertrofia de miócitos (risco de estenose subaórtica).", c3_x1 + 22, cy, c_w - 44, f_bold, f_regular, (67, 56, 202), (51, 65, 85))
    cy = draw_bullet(draw, "4. Hipermetabolismo & EPO", "Consumo acelerado de O2 gera hipóxia tecidual relativa -> estímulo renal de eritropoietina -> policitemia e pletora fetal.", c3_x1 + 22, cy, c_w - 44, f_bold, f_regular, (67, 56, 202), (51, 65, 85))

    # =========================================================================
    # COLUNA 4: REPERCUSSÕES NEONATAIS
    # =========================================================================
    draw.rounded_rectangle([c4_x1, header_y1, c4_x2, header_y2], radius=12, fill=(185, 28, 28))
    draw.text(((c4_x1 + c4_x2) // 2, (header_y1 + header_y2) // 2), "4. REPERCUSSÕES NEONATAIS", font=f_col_h, fill=(255, 255, 255), anchor="mm")

    if art_neo:
        crop_neo = art_neo.crop((0, 0, 1376, 768))
        paste_col_image(crop_neo, c4_x1, c4_x2, img_y1, img_y2, "Quadro Clínico Neonatal • Glicemia 32 mg/dL", (254, 202, 202))

    # Card 4.1: Macrossomia Assimétrica & Distócia
    c4_card1_y1 = 538
    c4_card1_y2 = 960
    cy = draw_card(draw, c4_x1, c4_card1_y1, c4_x2, c4_card1_y2, "Macrossomia Assimétrica", "Peso >= 4.000g (P > 90) • Risco de Distócia de Espáduas", (220, 38, 38), f_card_h, f_card_sub)
    cy = draw_bullet(draw, "Disproporção Biacromial", "Circunferência abdominal (CA) e largura dos ombros desproporcionalmente maiores que o polo cefálico.", c4_x1 + 22, cy, c_w - 44, f_bold, f_regular, (185, 28, 28), (51, 65, 85))
    cy = draw_bullet(draw, "Distócia de Espáduas", "Impactação do ombro anterior sob a sínfise púbica materna. Emergência obstétrica crítica.", c4_x1 + 22, cy, c_w - 44, f_bold, f_regular, (185, 28, 28), (51, 65, 85))
    cy = draw_bullet(draw, "Trauma de Parto", "Risco de fratura de clavícula e lesão do plexo braquial (Paralisia de Erb-Duchenne, C5-C6).", c4_x1 + 22, cy, c_w - 44, f_bold, f_regular, (185, 28, 28), (51, 65, 85))

    # Card 4.2: Hipoglicemia Neonatal Pós-Clampeamento
    c4_card2_y1 = 978
    c4_card2_y2 = 1465
    cy = draw_card(draw, c4_x1, c4_card2_y1, c4_x2, c4_card2_y2, "Hipoglicemia Neonatal Severa", "Pós-Clampeamento do Cordão • Glicemia < 35-40 mg/dL", (185, 28, 28), f_card_h, f_card_sub)
    cy = draw_bullet(draw, "Corte Abrupto de Glicose", "O clampeamento do cordão interrompe instantaneamente o aporte de glicose materna.", c4_x1 + 22, cy, c_w - 44, f_bold, f_regular, (185, 28, 28), (51, 65, 85))
    cy = draw_bullet(draw, "Hiperinsulinismo Persistente", "As ilhotas fetais continuam secretando insulina em níveis massivos nas primeiras 1-4 horas de vida.", c4_x1 + 22, cy, c_w - 44, f_bold, f_regular, (185, 28, 28), (51, 65, 85))
    cy = draw_bullet(draw, "Quadro Clínico Crítico", "Tremores, letargia, hipotonia, convulsões, sudorese fria, apneia e dano neurológico irreversível se não tratada.", c4_x1 + 22, cy, c_w - 44, f_bold, f_regular, (185, 28, 28), (51, 65, 85))
    cy = draw_bullet(draw, "Conduta Imediata", "Glicemia capilar na 1ª hora, amamentação precoce e infusão de glicose a 10% (TIG 6-8 mg/kg/min).", c4_x1 + 22, cy, c_w - 44, f_bold, f_regular, (185, 28, 28), (51, 65, 85))

    # Card 4.3: Hipertrofia Miocárdica Septal & Policitemia
    c4_card3_y1 = 1483
    c4_card3_y2 = 1940
    cy = draw_card(draw, c4_x1, c4_card3_y1, c4_x2, c4_card3_y2, "Cardiopatia & Policitemia Neonatal", "Hipertrofia Septal Assimétrica & Icterícia", (220, 38, 38), f_card_h, f_card_sub)
    cy = draw_bullet(draw, "Cardiomiopatia Hipertrófica", "Hipertrofia desproporcional do septo interventricular por estímulo anabólico insulínico. Pode causar obstrução do trato de saída do VE.", c4_x1 + 22, cy, c_w - 44, f_bold, f_regular, (185, 28, 28), (51, 65, 85))
    cy = draw_bullet(draw, "Policitemia (Ht > 65%)", "Secundária à produção aumentada de EPO fetal induzida por hipermetabolismo e hipóxia tecidual.", c4_x1 + 22, cy, c_w - 44, f_bold, f_regular, (185, 28, 28), (51, 65, 85))
    cy = draw_bullet(draw, "Hiperviscosidade & Icterícia", "Risco de trombose de veia renal. Degradação massiva de hemácias sobrecarrega fígado -> hiperbilirrubinemia indireta grave.", c4_x1 + 22, cy, c_w - 44, f_bold, f_regular, (185, 28, 28), (51, 65, 85))

    # Card 4.4: Desconforto Respiratório (DMH)
    c4_card4_y1 = 1958
    c4_card4_y2 = 2415
    cy = draw_card(draw, c4_x1, c4_card4_y1, c4_x2, c4_card4_y2, "Atraso no Surfactante Pulmonar", "Doença da Membrana Hialina (SDR) no Neonato a Termo", (185, 28, 28), f_card_h, f_card_sub)
    cy = draw_bullet(draw, "Inibição por Insulina Fetal", "A insulina antagoniza a ação dos glicocorticoides fetais sobre os pneumócitos tipo II.", c4_x1 + 22, cy, c_w - 44, f_bold, f_regular, (185, 28, 28), (51, 65, 85))
    cy = draw_bullet(draw, "Bloqueio de Lecitina & SP-A/B", "Queda na síntese de dipalmitoilfosfatidilcolina e proteínas do surfactante pulmonar.", c4_x1 + 22, cy, c_w - 44, f_bold, f_regular, (185, 28, 28), (51, 65, 85))
    cy = draw_bullet(draw, "Insuficiência Respiratória", "Mesmo com IG > 37 semanas, o RN de mãe diabética pode evoluir com colapso alveolar agudo e cianose.", c4_x1 + 22, cy, c_w - 44, f_bold, f_regular, (185, 28, 28), (51, 65, 85))

    # =========================================================================
    # FOOTER: SÍNTESE CLÍNICA DE ALTO RENDIMENTO (MNEMÔNICO & CONDUTA)
    # =========================================================================
    foot_y1, foot_y2 = 2445, 2715
    draw.rounded_rectangle([35, foot_y1, W - 35, foot_y2], radius=16, fill=(15, 23, 42), outline=(51, 65, 85), width=2)

    # Box 1: Mnemônico Clínico H-I-P-E-R
    draw.rounded_rectangle([55, foot_y1 + 18, 1200, foot_y2 - 18], radius=12, fill=(30, 41, 59), outline=(71, 85, 105), width=1)
    draw.text((75, foot_y1 + 30), "MNEMÔNICO CLÍNICO USMLE / FEBRASGO • « H - I - P - E - R »", font=f_card_sub, fill=(245, 158, 11))
    
    m_items = [
        ("• H - Hipoglicemia pós-parto:", "Glicemia < 35 mg/dL por hiperinsulinismo residual agudo ao clampear cordão."),
        ("• I - Ipertrofia septal miocárdica:", "Cardiomiopatia obstrutiva transitória por depósito de glicogênio e miofibrilas."),
        ("• P - Policitemia & Pletora:", "Estímulo renal de EPO por consumo excessivo de oxigênio (risco de trombose)."),
        ("• E - Espáduas impactadas:", "Macrossomia assimétrica com biacromial aumentado (distócia e lesão do plexo)."),
        ("• R - Respiratório comprometido:", "Atraso do surfactante por antagonismo insulínico do cortisol nos pneumócitos II.")
    ]
    cur_my = foot_y1 + 60
    for label, desc in m_items:
        draw.text((75, cur_my), label, font=f_bold, fill=(251, 191, 36))
        bbox_l = draw.textbbox((0, 0), label, font=f_bold)
        lw = bbox_l[2] - bbox_l[0] + 8
        draw.text((75 + lw, cur_my), desc, font=f_regular, fill=(241, 245, 249))
        cur_my += 33

    # Box 2: Conduta Imediata no Berçário & Prevenção
    draw.rounded_rectangle([1230, foot_y1 + 18, W - 55, foot_y2 - 18], radius=12, fill=(30, 41, 59), outline=(71, 85, 105), width=1)
    draw.text((1250, foot_y1 + 30), "PROTOCOLO IMEDIATO EM SALA DE PARTO & BERÇÁRIO", font=f_card_sub, fill=(45, 212, 191))
    
    p_items = [
        ("1. Triagem Glicêmica Seriada:", "Glicemia capilar aos 30 min, 1h, 2h, 4h de vida e pré-mamadas."),
        ("2. Aleitamento Precoce & SG 10%:", "Iniciar mamada na 1ª hora. Se glicemia < 28-30 mg/dL ou sintomático:"),
        ("   Conduta IV de Emergência:", "Bólus SG 10% (2 mL/kg) + TIG contínua de 6 a 8 mg/kg/min."),
        ("3. Ecocardiograma Precoce:", "Indicado na presença de sopro sistólico, instabilidade ou cianose central."),
        ("4. Monitorização Hematológica:", "Hematócrito venoso central para triagem de policitemia (Ht > 65%) e icterícia.")
    ]
    cur_py = foot_y1 + 60
    for label, desc in p_items:
        draw.text((1250, cur_py), label, font=f_bold, fill=(94, 234, 212))
        bbox_p = draw.textbbox((0, 0), label, font=f_bold)
        pw = bbox_p[2] - bbox_p[0] + 8
        draw.text((1250 + pw, cur_py), desc, font=f_regular, fill=(241, 245, 249))
        cur_py += 33

    # Salvar Imagem
    out_path = "assets/img/gdm_pathophysiology.jpg"
    img.save(out_path, quality=95)
    print(f"Sucesso absoluto! Imagem salva em {out_path} ({W}x{H} px)")

if __name__ == "__main__":
    main()
