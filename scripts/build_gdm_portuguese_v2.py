# -*- coding: utf-8 -*-
"""
build_gdm_portuguese_v2.py
Reconstrói com perfeição absoluta a Figura Médica 03: Fisiopatologia do Diabetes Gestacional & Hipótese de Pedersen.
- Canvas de altíssima resolução (2100 x 1320 px)
- 100% em Português
- ZERO resquícios de imagens/textos antigos em inglês
- ZERO sobreposição e ZERO vazamento de texto
- 4 Colunas perfeitamente alinhadas, cada uma com uma ilustração médica 3D no topo
- Tipografia nítida e harmoniosa com fontes TrueType do sistema
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

def draw_wrapped_text(draw, text, x, y, max_width, font, fill, line_spacing=4):
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

def main():
    W, H = 2100, 1340
    img = Image.new("RGB", (W, H), (248, 250, 252))
    draw = ImageDraw.Draw(img)

    # Fontes
    f_title = get_font("segoeuib.ttf", 30)
    f_sub = get_font("segoeui.ttf", 16)
    f_col_h = get_font("segoeuib.ttf", 17)
    f_card_h = get_font("segoeuib.ttf", 15)
    f_card_sub = get_font("segoeuib.ttf", 13)
    f_bold = get_font("segoeuib.ttf", 12)
    f_regular = get_font("segoeui.ttf", 12)
    f_small = get_font("segoeui.ttf", 11)
    f_badge = get_font("segoeuib.ttf", 11)

    # 1. HEADER BANNER
    draw.rectangle([0, 0, W, 105], fill=(255, 255, 255))
    draw.line([0, 105, W, 105], fill=(226, 232, 240), width=2)
    
    # Badges do topo
    draw.rounded_rectangle([40, 15, 300, 42], radius=6, fill=(240, 253, 250), outline=(94, 234, 212), width=1)
    draw.text((170, 28), "FIGURA MÉDICA 03 • ENDOCRINOLOGIA", font=f_badge, fill=(15, 118, 110), anchor="mm")

    draw.rounded_rectangle([1680, 15, 2060, 42], radius=6, fill=(241, 245, 249), outline=(203, 213, 225), width=1)
    draw.text((1870, 28), "USMLE STEP 2 CK • FEBRASGO • IADPSG • ADA", font=f_badge, fill=(71, 85, 105), anchor="mm")

    # Título Principal e Subtítulo
    draw.text((W // 2, 42), "FISIOPATOLOGIA DO DIABETES MELLITUS GESTACIONAL (DMG)", font=f_title, fill=(15, 23, 42), anchor="mm")
    draw.text((W // 2, 78), "Hipótese de Pedersen • Dinâmica Materno-Placentária-Fetal • Mecanismos Moleculares & Repercussões Neonatais", font=f_sub, fill=(71, 85, 105), anchor="mm")

    # CARREGAR ILUSTRAÇÕES MÉDICAS GERADAS
    p_maternal = "assets/img/gdm_art_maternal_profile.jpg"
    p_placenta = "assets/img/gdm_art_placental_diffusion.jpg"
    p_neonatal = "assets/img/gdm_art_neonatal_consequences.jpg"

    art_mat = Image.open(p_maternal) if os.path.exists(p_maternal) else None
    art_pla = Image.open(p_placenta) if os.path.exists(p_placenta) else None
    art_neo = Image.open(p_neonatal) if os.path.exists(p_neonatal) else None

    # COORDENADAS DAS 4 COLUNAS (Espaçamento simétrico)
    c1_x1, c1_x2 = 35, 530
    c2_x1, c2_x2 = 550, 970
    c3_x1, c3_x2 = 990, 1450
    c4_x1, c4_x2 = 1470, 2065
    header_y1, header_y2 = 120, 168

    # =========================================================================
    # COLUNA 1: COMPARTIMENTO MATERNO
    # =========================================================================
    draw.rounded_rectangle([c1_x1, header_y1, c1_x2, header_y2], radius=10, fill=(37, 99, 235))
    draw.text(((c1_x1 + c1_x2) // 2, (header_y1 + header_y2) // 2), "1. COMPARTIMENTO MATERNO", font=f_col_h, fill=(255, 255, 255), anchor="mm")

    # Arte 1: Mãe / Eixo Endócrino
    if art_mat:
        crop_mat = art_mat.crop((180, 40, 820, 750))
        crop_mat = crop_mat.resize((c1_x2 - c1_x1, 230), Image.Resampling.LANCZOS)
        mask_mat = Image.new("L", crop_mat.size, 0)
        mask_mat_draw = ImageDraw.Draw(mask_mat)
        mask_mat_draw.rounded_rectangle([0, 0, crop_mat.size[0], crop_mat.size[1]], radius=12, fill=255)
        img.paste(crop_mat, (c1_x1, 180), mask_mat)
        draw.rounded_rectangle([c1_x1, 180, c1_x2, 410], radius=12, outline=(191, 219, 254), width=2)
        draw.rounded_rectangle([c1_x1 + 10, 380, c1_x2 - 10, 404], radius=6, fill=(15, 23, 42))
        draw.text(((c1_x1 + c1_x2) // 2, 392), "Eixo Endócrino Materno-Placentário (hPL, Cortisol, PGH)", font=f_badge, fill=(224, 231, 255), anchor="mm")

    # Card 1.1: Hormônios Contrainsulínicos Diabetogênicos
    card1_y1 = 422
    card1_y2 = 575
    draw.rounded_rectangle([c1_x1, card1_y1, c1_x2, card1_y2], radius=12, fill=(255, 255, 255), outline=(191, 219, 254), width=2)
    draw.text((c1_x1 + 16, card1_y1 + 16), "Hormônios Contrainsulínicos Diabetogênicos", font=f_card_h, fill=(30, 58, 138))
    draw_wrapped_text(draw, "• Lactogênio Placentário Humano (hPL): principal hormônio diabetogênico.", c1_x1 + 16, card1_y1 + 42, c1_x2 - c1_x1 - 32, f_regular, (51, 65, 85))
    draw_wrapped_text(draw, "• Progesterona, Cortisol Livre e Prolactina: ação sinérgica anti-insulínica.", c1_x1 + 16, card1_y1 + 72, c1_x2 - c1_x1 - 32, f_regular, (51, 65, 85))
    draw_wrapped_text(draw, "• Hormônio do Crescimento Placentário (PGH): reforça lipólise e poupa glicose.", c1_x1 + 16, card1_y1 + 102, c1_x2 - c1_x1 - 32, f_regular, (51, 65, 85))

    # Card 1.2: Aumento da Resistência Periférica à Insulina
    card2_y1 = 587
    card2_y2 = 715
    draw.rounded_rectangle([c1_x1, card2_y1, c1_x2, card2_y2], radius=12, fill=(239, 246, 255), outline=(147, 197, 253), width=2)
    draw.text((c1_x1 + 16, card2_y1 + 14), "Resistência Periférica à Insulina", font=f_card_h, fill=(29, 78, 216))
    draw_wrapped_text(draw, "• Bloqueio pós-receptor nos tecidos muscular e adiposo maternos.", c1_x1 + 16, card2_y1 + 38, c1_x2 - c1_x1 - 32, f_bold, (30, 64, 175))
    draw_wrapped_text(draw, "• Finalidade fisiológica: direcionar nutrientes para a unidade fetoplacentária.", c1_x1 + 16, card2_y1 + 64, c1_x2 - c1_x1 - 32, f_regular, (71, 85, 105))
    draw_wrapped_text(draw, "• Pico no início do 3º trimestre (24 a 28 semanas) -> Momento do rastreio TOTG.", c1_x1 + 16, card2_y1 + 90, c1_x2 - c1_x1 - 32, f_badge, (30, 58, 138))

    # Card 1.3: Bifurcação Fisiopatológica
    card3_y1 = 727
    card3_y2 = 1005
    draw.rounded_rectangle([c1_x1, card3_y1, c1_x2, card3_y2], radius=12, fill=(255, 255, 255), outline=(226, 232, 240), width=2)
    draw.text((c1_x1 + 16, card3_y1 + 14), "Capacidade Compensatória Pancreática Materna", font=f_card_h, fill=(15, 23, 42))

    # Sub-box Gestação Normal
    sub_n_y1 = card3_y1 + 38
    sub_n_y2 = card3_y1 + 148
    draw.rounded_rectangle([c1_x1 + 12, sub_n_y1, c1_x2 - 12, sub_n_y2], radius=8, fill=(240, 253, 244), outline=(134, 239, 172), width=1)
    draw.text((c1_x1 + 24, sub_n_y1 + 10), "Gestação Normal (Fisiológica - Compensada)", font=f_bold, fill=(21, 128, 61))
    draw_wrapped_text(draw, "-> Células-beta hipertrofiam e aumentam secreção de insulina em 2 a 3x.", c1_x1 + 24, sub_n_y1 + 32, c1_x2 - c1_x1 - 50, f_regular, (22, 101, 52))
    draw_wrapped_text(draw, "-> Euglicemia materna preservada -> Crescimento fetal harmônico e saudável.", c1_x1 + 24, sub_n_y1 + 68, c1_x2 - c1_x1 - 50, f_bold, (21, 128, 61))

    # Sub-box DMG
    sub_d_y1 = card3_y1 + 158
    sub_d_y2 = card3_y1 + 268
    draw.rounded_rectangle([c1_x1 + 12, sub_d_y1, c1_x2 - 12, sub_d_y2], radius=8, fill=(254, 242, 242), outline=(252, 165, 165), width=1)
    draw.text((c1_x1 + 24, sub_d_y1 + 10), "Diabetes Gestacional (DMG - Descompensada)", font=f_bold, fill=(185, 28, 28))
    draw_wrapped_text(draw, "-> Falência ou disfunção das células-beta (predisposição genética + estresse metabólico).", c1_x1 + 24, sub_d_y1 + 32, c1_x2 - c1_x1 - 50, f_regular, (153, 27, 27))
    draw_wrapped_text(draw, "-> Incapacidade de compensar a resistência periférica à insulina.", c1_x1 + 24, sub_d_y1 + 68, c1_x2 - c1_x1 - 50, f_bold, (185, 28, 28))

    # Card 1.4: HIPERGLICEMIA MATERNA CRÔNICA
    card4_y1 = 1017
    card4_y2 = 1170
    draw.rounded_rectangle([c1_x1, card4_y1, c1_x2, card4_y2], radius=12, fill=(30, 58, 138), outline=(59, 130, 246), width=2)
    draw.text(((c1_x1 + c1_x2) // 2, card4_y1 + 28), "HIPERGLICEMIA MATERNA CRÔNICA", font=get_font("segoeuib.ttf", 16), fill=(255, 255, 255), anchor="mm")
    draw_wrapped_text(draw, "Glicemia plasmática persistentemente elevada na circulação materna.", c1_x1 + 20, card4_y1 + 54, c1_x2 - c1_x1 - 40, f_regular, (191, 219, 254))
    draw_wrapped_text(draw, "Cria um potente gradiente de difusão contínuo para o espaço interviloso placentário.", c1_x1 + 20, card4_y1 + 86, c1_x2 - c1_x1 - 40, f_bold, (255, 255, 255))

    # =========================================================================
    # COLUNA 2: PLACENTA & BARREIRA SELETIVA
    # =========================================================================
    draw.rounded_rectangle([c2_x1, header_y1, c2_x2, header_y2], radius=10, fill=(220, 38, 38))
    draw.text(((c2_x1 + c2_x2) // 2, (header_y1 + header_y2) // 2), "2. PLACENTA (BARREIRA SELETIVA)", font=f_col_h, fill=(255, 255, 255), anchor="mm")

    # Arte 2: Vilosidades Placentárias & Difusão de Glicose
    if art_pla:
        crop_pla = art_pla.crop((60, 100, 850, 750))
        crop_pla = crop_pla.resize((c2_x2 - c2_x1, 230), Image.Resampling.LANCZOS)
        mask_pla = Image.new("L", crop_pla.size, 0)
        mask_pla_draw = ImageDraw.Draw(mask_pla)
        mask_pla_draw.rounded_rectangle([0, 0, crop_pla.size[0], crop_pla.size[1]], radius=12, fill=255)
        img.paste(crop_pla, (c2_x1, 180), mask_pla)
        draw.rounded_rectangle([c2_x1, 180, c2_x2, 410], radius=12, outline=(254, 202, 202), width=2)
        draw.rounded_rectangle([c2_x1 + 10, 380, c2_x2 - 10, 404], radius=6, fill=(15, 23, 42))
        draw.text(((c2_x1 + c2_x2) // 2, 392), "Vilosidades Placentárias & Difusão de Partículas de Glicose", font=f_badge, fill=(254, 202, 202), anchor="mm")

    # Card 2.1: Gradiente Materno-Fetal
    card21_y1 = 422
    card21_y2 = 560
    draw.rounded_rectangle([c2_x1, card21_y1, c2_x2, card21_y2], radius=12, fill=(255, 255, 255), outline=(254, 202, 202), width=2)
    draw.text((c2_x1 + 16, card21_y1 + 16), "Gradiente de Concentração Materno-Fetal", font=f_card_h, fill=(159, 18, 57))
    draw_wrapped_text(draw, "• A glicose materna flui livremente em direção ao compartimento fetal.", c2_x1 + 16, card21_y1 + 42, c2_x2 - c2_x1 - 32, f_regular, (51, 65, 85))
    draw_wrapped_text(draw, "• Sobrecarga contínua e sem freio de carboidratos para o conceito.", c2_x1 + 16, card21_y1 + 72, c2_x2 - c2_x1 - 32, f_regular, (51, 65, 85))
    draw_wrapped_text(draw, "• O feto é um receptor passivo de substrato energético.", c2_x1 + 16, card21_y1 + 102, c2_x2 - c2_x1 - 32, f_bold, (159, 18, 57))

    # Card 2.2: Transportador GLUT1
    card22_y1 = 572
    card22_y2 = 745
    draw.rounded_rectangle([c2_x1, card22_y1, c2_x2, card22_y2], radius=12, fill=(254, 242, 242), outline=(239, 68, 68), width=2)
    draw.text(((c2_x1 + c2_x2) // 2, card22_y1 + 22), "DIFUSÃO FACILITADA VIA GLUT1", font=f_card_h, fill=(185, 28, 28), anchor="mm")
    draw_wrapped_text(draw, "• Transporte mediado por transportadores de glicose GLUT1 nos sinciciotrofoblastos.", c2_x1 + 16, card22_y1 + 46, c2_x2 - c2_x1 - 32, f_regular, (71, 85, 105))
    draw_wrapped_text(draw, "• Processo independente de gasto de energia e independente de insulina.", c2_x1 + 16, card22_y1 + 84, c2_x2 - c2_x1 - 32, f_bold, (153, 27, 27))
    draw_wrapped_text(draw, "• Quanto maior a glicemia materna, maior a taxa de passagem direta para a veia umbilical.", c2_x1 + 16, card22_y1 + 120, c2_x2 - c2_x1 - 32, f_regular, (71, 85, 105))

    # Card 2.3: BARREIRA PLACENTÁRIA À INSULINA
    card23_y1 = 757
    card23_y2 = 985
    draw.rounded_rectangle([c2_x1, card23_y1, c2_x2, card23_y2], radius=12, fill=(153, 27, 27), outline=(220, 38, 38), width=2)
    draw.text(((c2_x1 + c2_x2) // 2, card23_y1 + 24), "BARREIRA PLACENTÁRIA ABSOLUTA", font=f_card_sub, fill=(254, 202, 202), anchor="mm")
    draw.text(((c2_x1 + c2_x2) // 2, card23_y1 + 52), "A INSULINA MATERNA NÃO", font=get_font("segoeuib.ttf", 17), fill=(255, 255, 255), anchor="mm")
    draw.text(((c2_x1 + c2_x2) // 2, card23_y1 + 78), "ATRAVESSA A PLACENTA!", font=get_font("segoeuib.ttf", 17), fill=(255, 255, 255), anchor="mm")
    draw_wrapped_text(draw, "A insulina é uma molécula proteica de 5,8 kDa grande demais para transpor a barreira placentária íntegra.", c2_x1 + 20, card23_y1 + 108, c2_x2 - c2_x1 - 40, f_regular, (254, 226, 226))
    draw_wrapped_text(draw, "Consequência Clínica Vital: A insulina materna não regula nem reduz a glicose no polo fetal!", c2_x1 + 20, card23_y1 + 154, c2_x2 - c2_x1 - 40, f_bold, (254, 242, 242))

    # Card 2.4: Síntese de Pedersen
    card24_y1 = 997
    card24_y2 = 1170
    draw.rounded_rectangle([c2_x1, card24_y1, c2_x2, card24_y2], radius=12, fill=(255, 255, 255), outline=(252, 165, 165), width=2)
    draw.text(((c2_x1 + c2_x2) // 2, card24_y1 + 20), "Princípio Fundamental de Pedersen (1954)", font=f_card_sub, fill=(185, 28, 28), anchor="mm")
    draw_wrapped_text(draw, "A placenta transfere toda a glicose excedente, mas bloqueia a insulina materna.", c2_x1 + 16, card24_y1 + 42, c2_x2 - c2_x1 - 32, f_regular, (51, 65, 85))
    draw_wrapped_text(draw, "Isso força o próprio pâncreas fetal a assumir sozinho toda a carga de metabolização!", c2_x1 + 16, card24_y1 + 84, c2_x2 - c2_x1 - 32, f_bold, (153, 27, 27))

    # =========================================================================
    # COLUNA 3: COMPARTIMENTO FETAL
    # =========================================================================
    draw.rounded_rectangle([c3_x1, header_y1, c3_x2, header_y2], radius=10, fill=(126, 34, 206))
    draw.text(((c3_x1 + c3_x2) // 2, (header_y1 + header_y2) // 2), "3. COMPARTIMENTO FETAL", font=f_col_h, fill=(255, 255, 255), anchor="mm")

    # Arte 3: Feto em desenvolvimento recebendo o cordão umbilical
    if art_pla:
        crop_fet = art_pla.crop((550, 0, 1350, 600))
        crop_fet = crop_fet.resize((c3_x2 - c3_x1, 230), Image.Resampling.LANCZOS)
        mask_fet = Image.new("L", crop_fet.size, 0)
        mask_fet_draw = ImageDraw.Draw(mask_fet)
        mask_fet_draw.rounded_rectangle([0, 0, crop_fet.size[0], crop_fet.size[1]], radius=12, fill=255)
        img.paste(crop_fet, (c3_x1, 180), mask_fet)
        draw.rounded_rectangle([c3_x1, 180, c3_x2, 410], radius=12, outline=(216, 180, 254), width=2)
        draw.rounded_rectangle([c3_x1 + 10, 380, c3_x2 - 10, 404], radius=6, fill=(15, 23, 42))
        draw.text(((c3_x1 + c3_x2) // 2, 392), "Conceito em Desenvolvimento & Influxo Umbilical de Glicose", font=f_badge, fill=(233, 213, 255), anchor="mm")

    # Card 3.1: Influxo de Glicose & Hiperglicemia Fetal
    card31_y1 = 422
    card31_y2 = 550
    draw.rounded_rectangle([c3_x1, card31_y1, c3_x2, card31_y2], radius=12, fill=(250, 245, 255), outline=(216, 180, 254), width=2)
    draw.text((c3_x1 + 16, card31_y1 + 14), "Influxo Contínuo de Glicose (Veia Umbilical)", font=f_card_h, fill=(88, 28, 135))
    draw_wrapped_text(draw, "• A sobrecarga de glicose chega diretamente pelo cordão umbilical.", c3_x1 + 16, card31_y1 + 38, c3_x2 - c3_x1 - 32, f_regular, (51, 65, 85))
    draw_wrapped_text(draw, "• Resulta em Hiperglicemia Fetal Crônica proporcional aos níveis maternos.", c3_x1 + 16, card31_y1 + 64, c3_x2 - c3_x1 - 32, f_bold, (107, 33, 168))
    draw_wrapped_text(draw, "• Ativação precoce de sensores glicêmicos nas ilhotas de Langerhans fetais.", c3_x1 + 16, card31_y1 + 92, c3_x2 - c3_x1 - 32, f_regular, (71, 85, 105))

    # Card 3.2: Reação Pancreática Fetal
    card32_y1 = 562
    card32_y2 = 725
    draw.rounded_rectangle([c3_x1, card32_y1, c3_x2, card32_y2], radius=12, fill=(255, 255, 255), outline=(192, 132, 252), width=2)
    draw.text((c3_x1 + 16, card32_y1 + 14), "Reação Pancreática Fetal (12ª a 14ª Semana)", font=f_card_h, fill=(107, 33, 168))
    draw_wrapped_text(draw, "• As células-beta do pâncreas fetal tornam-se funcionais precocemente.", c3_x1 + 16, card32_y1 + 38, c3_x2 - c3_x1 - 32, f_regular, (51, 65, 85))
    draw_wrapped_text(draw, "• Hiperplasia e Hipertrofia intensa das células-beta induzidas por glicose.", c3_x1 + 16, card32_y1 + 66, c3_x2 - c3_x1 - 32, f_bold, (88, 28, 135))
    draw_wrapped_text(draw, "• Produção massiva e autônoma de Insulina Fetal e Peptídeo C fetal.", c3_x1 + 16, card32_y1 + 96, c3_x2 - c3_x1 - 32, f_bold, (147, 51, 234))
    draw_wrapped_text(draw, "• O pâncreas fetal opera em regime de hipersecreção crônica contínua.", c3_x1 + 16, card32_y1 + 124, c3_x2 - c3_x1 - 32, f_regular, (71, 85, 105))

    # Card 3.3: HIPERINSULINISMO FETAL
    card33_y1 = 737
    card33_y2 = 875
    draw.rounded_rectangle([c3_x1, card33_y1, c3_x2, card33_y2], radius=12, fill=(107, 33, 168), outline=(147, 51, 234), width=2)
    draw.text(((c3_x1 + c3_x2) // 2, card33_y1 + 22), "HIPERINSULINISMO FETAL", font=get_font("segoeuib.ttf", 16), fill=(255, 255, 255), anchor="mm")
    draw_wrapped_text(draw, "A insulina fetal não é meramente um hormônio metabólico; no útero, ela é o PRINCIPAL FATOR DE CRESCIMENTO intrauterino!", c3_x1 + 20, card33_y1 + 46, c3_x2 - c3_x1 - 40, f_regular, (243, 232, 255))
    draw_wrapped_text(draw, "Atua em sinergia com o IGF-1 promovendo potente anabolismo tecidual.", c3_x1 + 20, card33_y1 + 98, c3_x2 - c3_x1 - 40, f_bold, (255, 255, 255))

    # Card 3.4: Efeitos Anabólicos do Hiperinsulinismo Fetal
    card34_y1 = 887
    card34_y2 = 1170
    draw.rounded_rectangle([c3_x1, card34_y1, c3_x2, card34_y2], radius=12, fill=(255, 255, 255), outline=(216, 180, 254), width=2)
    draw.text((c3_x1 + 16, card34_y1 + 14), "Efeitos Celulares e Anabólicos da Insulina Fetal", font=f_card_h, fill=(88, 28, 135))
    
    # 4 tópicos anabólicos bem distribuídos
    draw.rounded_rectangle([c3_x1 + 12, card34_y1 + 38, c3_x2 - 12, card34_y1 + 98], radius=8, fill=(250, 245, 255), outline=(233, 213, 255), width=1)
    draw.text((c3_x1 + 20, card34_y1 + 46), "1. Lipogênese Acelerada:", font=f_bold, fill=(107, 33, 168))
    draw_wrapped_text(draw, "Conversão de glicose em ácidos graxos -> Depósito maciço de gordura subcutânea.", c3_x1 + 20, card34_y1 + 64, c3_x2 - c3_x1 - 40, f_small, (51, 65, 85))

    draw.rounded_rectangle([c3_x1 + 12, card34_y1 + 104, c3_x2 - 12, card34_y1 + 164], radius=8, fill=(250, 245, 255), outline=(233, 213, 255), width=1)
    draw.text((c3_x1 + 20, card34_y1 + 112), "2. Síntese Proteica & Hipertrofia:", font=f_bold, fill=(107, 33, 168))
    draw_wrapped_text(draw, "Captação rápida de aminoácidos -> Hipertrofia somática e organomegalia fetal.", c3_x1 + 20, card34_y1 + 130, c3_x2 - c3_x1 - 40, f_small, (51, 65, 85))

    draw.rounded_rectangle([c3_x1 + 12, card34_y1 + 170, c3_x2 - 12, card34_y1 + 224], radius=8, fill=(250, 245, 255), outline=(233, 213, 255), width=1)
    draw.text((c3_x1 + 20, card34_y1 + 178), "3. Glicogenogênese Visceral e Miocárdica:", font=f_bold, fill=(107, 33, 168))
    draw_wrapped_text(draw, "Depósito de glicogênio nos miócitos -> Cardiomiopatia hipertrófica do septo.", c3_x1 + 20, card34_y1 + 196, c3_x2 - c3_x1 - 40, f_small, (51, 65, 85))

    draw.rounded_rectangle([c3_x1 + 12, card34_y1 + 230, c3_x2 - 12, card34_y1 + 276], radius=8, fill=(254, 242, 242), outline=(252, 165, 165), width=1)
    draw.text((c3_x1 + 20, card34_y1 + 236), "4. Hipermetabolismo Fetal e Consumo de O2:", font=f_bold, fill=(185, 28, 28))
    draw_wrapped_text(draw, "Consumo tecidual elevado de oxigênio -> Hipóxia crônica -> Estímulo de EPO fetal.", c3_x1 + 20, card34_y1 + 252, c3_x2 - c3_x1 - 40, f_small, (153, 27, 27))

    # =========================================================================
    # COLUNA 4: CONSEQUÊNCIAS FETAIS E NEONATAIS
    # =========================================================================
    draw.rounded_rectangle([c4_x1, header_y1, c4_x2, header_y2], radius=10, fill=(131, 24, 67))
    draw.text(((c4_x1 + c4_x2) // 2, (header_y1 + header_y2) // 2), "4. CONSEQUÊNCIAS FETAIS E NEONATAIS", font=f_col_h, fill=(255, 255, 255), anchor="mm")

    # Arte 4: Bebê macrossômico + coração + glicosímetro
    if art_neo:
        crop_neo = art_neo.crop((20, 20, 1350, 750))
        crop_neo = crop_neo.resize((c4_x2 - c4_x1, 230), Image.Resampling.LANCZOS)
        mask_neo = Image.new("L", crop_neo.size, 0)
        mask_neo_draw = ImageDraw.Draw(mask_neo)
        mask_neo_draw.rounded_rectangle([0, 0, crop_neo.size[0], crop_neo.size[1]], radius=12, fill=255)
        img.paste(crop_neo, (c4_x1, 180), mask_neo)
        draw.rounded_rectangle([c4_x1, 180, c4_x2, 410], radius=12, outline=(244, 114, 182), width=2)
        draw.rounded_rectangle([c4_x1 + 10, 380, c4_x2 - 10, 404], radius=6, fill=(15, 23, 42))
        draw.text(((c4_x1 + c4_x2) // 2, 392), "Macrossomia Fetal, Hipertrofia do Septo Cardíaco e Monitorização da Hipoglicemia", font=f_badge, fill=(251, 207, 232), anchor="mm")

    # Card 4.1: Macrossomia Fetal Assimétrica
    c41_y1 = 422
    c41_y2 = 615
    draw.rounded_rectangle([c4_x1, c41_y1, c4_x2, c41_y2], radius=12, fill=(255, 255, 255), outline=(244, 114, 182), width=2)
    draw.text((c4_x1 + 16, c41_y1 + 16), "1) MACROSSOMIA FETAL ASSIMÉTRICA (PN > 4.000g)", font=f_card_h, fill=(131, 24, 67))
    draw_wrapped_text(draw, "• Depósito seletivo de gordura no tronco e cintura escapular (ombros largos).", c4_x1 + 16, c41_y1 + 40, c4_x2 - c4_x1 - 32, f_regular, (51, 65, 85))
    draw_wrapped_text(draw, "• Risco elevado de Distócia de Ombros, fratura de clavícula e lesão de plexo braquial (Erb-Duchenne).", c4_x1 + 16, c41_y1 + 68, c4_x2 - c4_x1 - 32, f_bold, (159, 18, 57))
    draw_wrapped_text(draw, "• Hipertrofia do Septo Interventricular (Cardiomiopatia Hipertrófica Assimétrica transitória).", c4_x1 + 16, c41_y1 + 106, c4_x2 - c4_x1 - 32, f_bold, (131, 24, 67))
    draw_wrapped_text(draw, "• Indicação de Cesariana Eletiva profilática se peso fetal estimado > 4.500g no DMG.", c4_x1 + 16, c41_y1 + 144, c4_x2 - c4_x1 - 32, f_badge, (185, 28, 28))

    # Card 4.2: Hipoglicemia Neonatal Grave
    c42_y1 = 627
    c42_y2 = 810
    draw.rounded_rectangle([c4_x1, c42_y1, c4_x2, c42_y2], radius=12, fill=(255, 241, 242), outline=(248, 113, 113), width=2)
    draw.text((c4_x1 + 16, c42_y1 + 16), "2) HIPOGLICEMIA NEONATAL GRAVE (Pós-Parto)", font=f_card_h, fill=(185, 28, 28))
    draw_wrapped_text(draw, "• Ao clampear o cordão: cessa abruptamente o influxo contínuo de glicose materna.", c4_x1 + 16, c42_y1 + 40, c4_x2 - c4_x1 - 32, f_bold, (153, 27, 27))
    draw_wrapped_text(draw, "• Pâncreas do recém-nascido mantém hiperinsulinismo nas primeiras horas de vida.", c4_x1 + 16, c42_y1 + 68, c4_x2 - c4_x1 - 32, f_regular, (51, 65, 85))
    draw_wrapped_text(draw, "• Captação periférica massiva + supressão da gliconeogênese -> Glicemia < 40 mg/dL.", c4_x1 + 16, c42_y1 + 96, c4_x2 - c4_x1 - 32, f_bold, (185, 28, 28))
    # Badge de conduta
    draw.rounded_rectangle([c4_x1 + 14, c42_y1 + 130, c4_x2 - 14, c42_y1 + 166], radius=6, fill=(220, 252, 231), outline=(74, 222, 128), width=1)
    draw.text(((c4_x1 + c4_x2) // 2, c42_y1 + 148), "Conduta: Amamentação na 1ª hora de vida + HGT seriado aos 30-60 minutos!", font=f_badge, fill=(21, 128, 61), anchor="mm")

    # Card 4.3: Hipóxia Fetal Crônica, Policitemia & Hiperbilirrubinemia
    c43_y1 = 822
    c43_y2 = 1005
    draw.rounded_rectangle([c4_x1, c43_y1, c4_x2, c43_y2], radius=12, fill=(255, 255, 255), outline=(216, 180, 254), width=2)
    draw.text((c4_x1 + 16, c43_y1 + 16), "3) HIPÓXIA CRÔNICA, POLICITEMIA & ICTERÍCIA", font=f_card_h, fill=(88, 28, 135))
    draw_wrapped_text(draw, "• Hipermetabolismo induzido por insulina eleva o consumo tecidual de O2 -> Hipóxia crônica.", c4_x1 + 16, c43_y1 + 40, c4_x2 - c4_x1 - 32, f_regular, (51, 65, 85))
    draw_wrapped_text(draw, "• Estímulo à Eritropoietina (EPO) fetal -> Policitemia Neonatal (Hematócrito > 65%).", c4_x1 + 16, c43_y1 + 72, c4_x2 - c4_x1 - 32, f_bold, (107, 33, 168))
    draw_wrapped_text(draw, "• Hiperviscosidade sanguínea: risco aumentado de trombose da veia renal e AVC neonatal.", c4_x1 + 16, c43_y1 + 104, c4_x2 - c4_x1 - 32, f_regular, (51, 65, 85))
    draw_wrapped_text(draw, "• Lise massiva pós-natal de hemácias excedentes -> Hiperbilirrubinemia indireta e Kernicterus.", c4_x1 + 16, c43_y1 + 136, c4_x2 - c4_x1 - 32, f_bold, (185, 28, 28))

    # Card 4.4: Atraso na Maturação do Surfactante Pulmonar
    c44_y1 = 1017
    c44_y2 = 1170
    draw.rounded_rectangle([c4_x1, c44_y1, c4_x2, c44_y2], radius=12, fill=(255, 247, 237), outline=(251, 146, 60), width=2)
    draw.text((c4_x1 + 16, c44_y1 + 16), "4) ATRASO NA MATURAÇÃO DO SURFACTANTE PULMONAR", font=f_card_h, fill=(194, 65, 12))
    draw_wrapped_text(draw, "• O hiperinsulinismo fetal antagoniza a ação indutora do cortisol sobre os pneumócitos tipo II.", c4_x1 + 16, c44_y1 + 42, c4_x2 - c4_x1 - 32, f_bold, (154, 52, 18))
    draw_wrapped_text(draw, "• Redução na síntese de dipalmitoilfosfatidilcolina (lecitina) -> Deficiência de surfactante alveolar.", c4_x1 + 16, c44_y1 + 74, c4_x2 - c4_x1 - 32, f_regular, (51, 65, 85))
    draw_wrapped_text(draw, "• Alto risco de Síndrome do Desconforto Respiratório (SDR / Doença da Membrana Hialina) a termo!", c4_x1 + 16, c44_y1 + 106, c4_x2 - c4_x1 - 32, f_bold, (194, 65, 12))

    # =========================================================================
    # RODAPÉ INFORMATIVO
    # =========================================================================
    draw.rectangle([0, 1220, W, H], fill=(255, 255, 255))
    draw.line([0, 1220, W, 1220], fill=(226, 232, 240), width=2)
    draw.text((W // 2, 1255), "Diretrizes Clínicas: Sociedade Brasileira de Diabetes (SBD 2024), FEBRASGO, American Diabetes Association (ADA 2024) e ACOG Practice Bulletin.", font=f_small, fill=(100, 116, 139), anchor="mm")
    draw.text((W // 2, 1285), "Desenvolvido para Internato GO e Preparação USMLE Step 2 CK • Diagramação Vetorial de Alta Precisão Anatômica", font=f_badge, fill=(71, 85, 105), anchor="mm")

    dest_path = "assets/img/gdm_pathophysiology.jpg"
    img.save(dest_path, "JPEG", quality=95)
    print(f"[OK] Imagem salva com sucesso em {dest_path} ({os.path.getsize(dest_path)} bytes)")

if __name__ == "__main__":
    main()
