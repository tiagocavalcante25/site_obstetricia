# -*- coding: utf-8 -*-
"""
build_perfect_leopold.py
Gera o infográfico médico em Altíssima Definição das 4 Manobras de Leopold-Zweifel.
- Substitui a imagem incorreta por ilustrações medicamente precisas:
  * Examinador/Médico realizando o exame obstétrico
  * Paciente em decúbito dorsal sem luvas e sem autopalpação
  * Correta orientação das mãos e corpo do examinador em cada manobra
- Resolução Ultra-HD (2400 x 2300 px)
- Tipografia padrão FEBRASGO, Ministério da Saúde e USMLE Step 2 CK
"""

import os
from PIL import Image, ImageDraw, ImageFont

def get_font(name, size):
    font_paths = [
        os.path.join("C:/Windows/Fonts", name),
        os.path.join("C:/Windows/Fonts", name.lower()),
        os.path.join("C:/Windows/Fonts", "segoeui.ttf"),
        os.path.join("C:/Windows/Fonts", "arial.ttf")
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                continue
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

def main():
    base_dir = r"c:\Users\Admin\Downloads\INTERNATO GO\site_obstetricia"
    brain_dir = r"C:\Users\Admin\.gemini\antigravity\brain\c8a7917c-8cbc-4119-b7c7-b6bf1409ed34"
    scratch_dir = os.path.join(brain_dir, "scratch")
    
    p1_path = os.path.join(scratch_dir, "test_cleaned_p1.jpg")
    p2_path = os.path.join(scratch_dir, "test_cleaned_p2.jpg")
    p3_path = os.path.join(scratch_dir, "test_cleaned_p3.jpg")
    p4_path = os.path.join(brain_dir, "leopold_m4_fresh_1791566529324.jpg")
    
    output_path = os.path.join(base_dir, "assets", "img", "leopold_maneuvers.jpg")
    
    print("Carregando painéis corrigidos sem repetições...")
    im1 = Image.open(p1_path).convert("RGB")
    im2 = Image.open(p2_path).convert("RGB")
    im3 = Image.open(p3_path).convert("RGB")
    im4 = Image.open(p4_path).convert("RGB")
    
    # Dimensões da tela final
    W = 2400
    H = 2320
    
    canvas = Image.new("RGB", (W, H), (15, 23, 42)) # Fundo Slate-900 profissional
    draw = ImageDraw.Draw(canvas)
    
    # Fontes
    f_title = get_font("segoeuib.ttf", 46)
    f_sub = get_font("segoeui.ttf", 22)
    f_tag = get_font("segoeuib.ttf", 18)
    f_panel_title = get_font("segoeuib.ttf", 26)
    f_panel_sub = get_font("segoeui.ttf", 19)
    f_panel_bold = get_font("segoeuib.ttf", 19)
    f_footer_title = get_font("segoeuib.ttf", 24)
    f_footer_text = get_font("segoeui.ttf", 19)
    f_badge = get_font("segoeuib.ttf", 28)
    
    # 1. HEADER PRINCIPAL
    # Barra de gradiente superior
    draw.rectangle([0, 0, W, 12], fill=(14, 165, 233)) # Sky 500
    
    # Tag de identificação médica
    tag_text = "SEMIOLOGIA OBSTÉTRICA • EXAME FÍSICO ABDOMINAL DA GESTANTE (≥ 28-30 SEMANAS)"
    bbox_tag = draw.textbbox((0, 0), tag_text, font=f_tag)
    tag_w = bbox_tag[2] - bbox_tag[0]
    draw.rounded_rectangle([40, 26, 40 + tag_w + 30, 60], radius=8, fill=(12, 74, 110), outline=(56, 189, 248), width=1)
    draw.text((55, 32), tag_text, font=f_tag, fill=(186, 230, 253))
    
    title_text = "As 4 Manobras de Leopold-Zweifel (Palpação Obstétrica Sistemática)"
    draw.text((40, 72), title_text, font=f_title, fill=(255, 255, 255))
    
    sub_text = "Demonstração medicamente precisa: Paciente em decúbito dorsal confortável • Examinador à beira do leito executando a palpação com as mãos"
    draw.text((40, 136), sub_text, font=f_sub, fill=(148, 163, 184))
    
    # Divisor suave
    draw.line([40, 175, W - 40, 175], fill=(51, 65, 85), width=2)
    
    # Layout dos 4 Painéis (2 x 2)
    col_w = 1140
    col1_x = 40
    col2_x = 1220
    
    img_h = 750
    header_box_h = 150
    row1_y = 195
    row2_y = row1_y + img_h + header_box_h + 30
    
    panels_meta = [
        {
            "img": im1,
            "x": col1_x,
            "y": row1_y,
            "num": "1",
            "name": "1ª Manobra: Fundo Uterino (Situação e Polo Fetal)",
            "subtitle": "Identifica a situação fetal (longitudinal vs transversa) e qual polo ocupa o fundo.",
            "hands": "Mãos espalmadas no fundo uterino. Polo pélvico é volumoso e mole; polo cefálico é liso e duro.",
            "color_badge": (14, 165, 233), # Sky
            "border_color": (30, 58, 138)
        },
        {
            "img": im2,
            "x": col2_x,
            "y": row1_y,
            "num": "2",
            "name": "2ª Manobra: Dorso Fetal (Posição e Membros)",
            "subtitle": "Define a posição fetal (dorso à direita ou esquerda) e pequenas partes fetais.",
            "hands": "Mãos nos flancos. Dorso contínuo e firme (foco do BCF); membros nodulares e móveis.",
            "color_badge": (16, 185, 129), # Emerald
            "border_color": (6, 78, 59)
        },
        {
            "img": im3,
            "x": col1_x,
            "y": row2_y,
            "num": "3",
            "name": "3ª Manobra: Manobra de Pawlik (Apresentação)",
            "subtitle": "Apreende o polo fetal inferior logo acima da sínfise púbica para determinar a apresentação.",
            "hands": "Executada com 1 ÚNICA MÃO (em garra). Avalia se a apresentação é cefálica e sua mobilidade.",
            "color_badge": (245, 158, 11), # Amber
            "border_color": (120, 53, 15)
        },
        {
            "img": im4,
            "x": col2_x,
            "y": row2_y,
            "num": "4",
            "name": "4ª Manobra: Insinuação e Atitude Cefálica",
            "subtitle": "Avalia a penetração no estreito superior e a flexão/deflexão da cabeça.",
            "hands": "Examinador voltado para os pés. Mãos penetram a pelve: dedos convergem = alto; divergem = insinuado.",
            "color_badge": (168, 85, 247), # Purple
            "border_color": (88, 28, 135)
        }
    ]
    
    for p in panels_meta:
        px = p["x"]
        py = p["y"]
        
        # Moldura do Painel
        total_card_h = img_h + header_box_h
        draw.rounded_rectangle([px, py, px + col_w, py + total_card_h], radius=16, fill=(30, 41, 59), outline=(71, 85, 105), width=2)
        
        # Barra Superior do Card com Número e Títulos
        draw.rounded_rectangle([px, py, px + col_w, py + header_box_h], radius=16, fill=(15, 23, 42))
        draw.rectangle([px, py + header_box_h - 16, px + col_w, py + header_box_h], fill=(15, 23, 42)) # Suaviza o fundo inferior da barra
        draw.line([px, py + header_box_h, px + col_w, py + header_box_h], fill=(51, 65, 85), width=2)
        
        # Badge Circular com Número
        badge_cx = px + 44
        badge_cy = py + 48
        draw.ellipse([badge_cx - 26, badge_cy - 26, badge_cx + 26, badge_cy + 26], fill=p["color_badge"])
        # Centraliza texto do número
        n_bbox = draw.textbbox((0, 0), p["num"], font=f_badge)
        nw = n_bbox[2] - n_bbox[0]
        nh = n_bbox[3] - n_bbox[1]
        draw.text((badge_cx - nw//2, badge_cy - nh//2 - 2), p["num"], font=f_badge, fill=(255, 255, 255))
        
        # Título da Manobra
        draw.text((px + 86, py + 18), p["name"], font=f_panel_title, fill=(255, 255, 255))
        # Subtítulo da Manobra
        draw.text((px + 86, py + 54), p["subtitle"], font=f_panel_sub, fill=(226, 232, 240))
        # Descrição da ação das mãos
        draw.text((px + 86, py + 88), "Técnica: " + p["hands"], font=f_panel_bold, fill=(148, 163, 184))
        
        # Redimensiona imagem preservando qualidade e centralizando
        panel_img = p["img"].resize((col_w - 4, img_h - 4), Image.Resampling.LANCZOS)
        canvas.paste(panel_img, (px + 2, py + header_box_h + 2))
        
    # 3. RODAPÉ DE FIXAÇÃO HIGH-YIELD
    foot_y = row2_y + img_h + header_box_h + 20
    draw.rounded_rectangle([40, foot_y, W - 40, foot_y + 135], radius=16, fill=(15, 23, 42), outline=(56, 189, 248), width=2)
    
    draw.text((65, foot_y + 16), "PÉROLAS DE PROVA & RESIDÊNCIA MÉDICA (MNEMÔNICO DAS 4 MANOBRAS):", font=f_footer_title, fill=(56, 189, 248))
    
    pearl_1 = "1ª Manobra (Fundo) = Situação (Longitudinal / Transversa) e Polo Superior | 2ª Manobra (Flancos) = Posição (Dorso D/E - foco do BCF)"
    pearl_2 = "3ª Manobra (Pawlik) = Apresentação (Cefálica / Pélvica) e Mobilidade (executada com 1 mão) | 4ª Manobra = Insinuação e Atitude (examinador voltado para os pés)"
    pearl_3 = "Correção Médica: O exame é estritamente conduzido pelo profissional de saúde; a gestante não realiza autopalpação nem usa luvas de procedimento."
    
    draw.text((65, foot_y + 54), pearl_1, font=f_footer_text, fill=(241, 245, 249))
    draw.text((65, foot_y + 80), pearl_2, font=f_footer_text, fill=(241, 245, 249))
    draw.text((65, foot_y + 106), pearl_3, font=f_footer_text, fill=(148, 163, 184))
    
    print(f"Salvando imagem final em: {output_path}")
    canvas.save(output_path, "JPEG", quality=95, optimize=True)
    print("Sucesso! Imagem gerada com perfeição técnica e anatômica.")

if __name__ == "__main__":
    main()
