import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def get_font(name, size):
    font_path = os.path.join("C:/Windows/Fonts", name)
    return ImageFont.truetype(font_path, size)

def build_gdm_portuguese():
    orig_path = r"C:\Users\Admin\.gemini\antigravity\brain\c8a7917c-8cbc-4119-b7c7-b6bf1409ed34\gdm_patho_1790944155405.jpg"
    orig_cv = cv2.imread(orig_path)
    h, w, _ = orig_cv.shape # 768, 1376

    # 1. Extract pure anatomical art pieces from orig
    art_baby = orig_cv[175:285, 1005:1095].copy()
    art_organs = orig_cv[188:245, 1205:1290].copy()
    art_pancreas = orig_cv[648:732, 102:236].copy()
    art_mother = orig_cv[140:335, 35:125].copy()

    # Convert base image to PIL
    base_img = cv2.cvtColor(orig_cv, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(base_img)
    draw = ImageDraw.Draw(img)

    # Fonts
    font_title = get_font("segoeuib.ttf", 25)
    font_sub = get_font("segoeui.ttf", 14)
    font_h_col = get_font("segoeuib.ttf", 17)
    font_card_h = get_font("segoeuib.ttf", 13)
    font_bold = get_font("segoeuib.ttf", 11)
    font_bold_sm = get_font("segoeuib.ttf", 10)
    font_regular = get_font("segoeui.ttf", 11)
    font_sm = get_font("segoeui.ttf", 10)
    font_xs = get_font("segoeui.ttf", 9)

    # ==========================================
    # 1. TOP HEADER BANNER
    # ==========================================
    draw.rectangle([10, 8, 1366, 72], fill=(255, 255, 255))
    draw.text((688, 28), "FISIOPATOLOGIA DO DIABETES MELLITUS GESTACIONAL (DMG)",
              font=font_title, fill=(15, 23, 42), anchor="mm")
    draw.text((688, 54), "Mecanismo Molecular, Hipótese de Pedersen & Repercussões Fetais e Neonatais",
              font=font_sub, fill=(71, 85, 105), anchor="mm")

    # ==========================================
    # 2. FOUR COLUMN HEADERS (y: 76..118)
    # ==========================================
    # Col 1: Compartimento Materno
    draw.rounded_rectangle([18, 76, 498, 118], radius=8, fill=(37, 99, 235))
    draw.text((258, 97), "COMPARTIMENTO MATERNO", font=font_h_col, fill=(255, 255, 255), anchor="mm")

    # Col 2: Placenta
    draw.rounded_rectangle([505, 76, 665, 118], radius=8, fill=(220, 38, 38))
    draw.text((585, 97), "PLACENTA", font=font_h_col, fill=(255, 255, 255), anchor="mm")

    # Col 3: Compartimento Fetal
    draw.rounded_rectangle([672, 76, 972, 118], radius=8, fill=(126, 34, 206))
    draw.text((822, 97), "COMPARTIMENTO FETAL", font=font_h_col, fill=(255, 255, 255), anchor="mm")

    # Col 4: Consequências Fetais e Neonatais
    draw.rounded_rectangle([980, 76, 1362, 118], radius=8, fill=(88, 28, 135))
    draw.text((1171, 97), "CONSEQUÊNCIAS FETAIS E NEONATAIS", font=get_font("segoeuib.ttf", 15), fill=(255, 255, 255), anchor="mm")

    # ==========================================
    # 3. COLUMN 1: COMPARTIMENTO MATERNO
    # Clean entire text zones to guarantee ZERO old English fragments
    # ==========================================
    # Clean background for Col 1 upper/mid
    draw.rectangle([130, 125, 495, 435], fill=(240, 247, 255))
    # Clean background for Col 1 left lower
    draw.rectangle([20, 435, 205, 655], fill=(236, 253, 245))
    # Clean background for Col 1 right mid/lower
    draw.rectangle([210, 435, 495, 665], fill=(248, 250, 252))

    # Re-paste maternal silhouette
    mother_pil = Image.fromarray(cv2.cvtColor(art_mother, cv2.COLOR_BGR2RGB))
    img.paste(mother_pil, (35, 140))

    # Box 1: Hormônios Gestacionais (x: 130..485, y: 135..235)
    draw.rounded_rectangle([130, 135, 485, 235], radius=10, fill=(240, 247, 255), outline=(147, 197, 253), width=2)
    draw.text((307, 155), "Hormônios Gestacionais Diabetogênicos", font=font_card_h, fill=(30, 58, 138), anchor="mm")
    draw.text((145, 175), "• Lactogênio Placentário Humano (hPL)", font=font_bold, fill=(30, 64, 175))
    draw.text((145, 193), "• Progesterona, Cortisol e Prolactina", font=font_regular, fill=(51, 65, 85))
    draw.text((145, 211), "• Hormônio do Crescimento Placentário (PGH)", font=font_regular, fill=(71, 85, 105))

    # Box 2: Aumento da Resistência (x: 130..485, y: 248..318)
    draw.rounded_rectangle([130, 248, 485, 318], radius=10, fill=(219, 234, 254), outline=(96, 165, 250), width=2)
    draw.text((307, 268), "Aumento da Resistência Periférica à Insulina", font=font_card_h, fill=(29, 78, 216), anchor="mm")
    draw.text((307, 290), "Bloqueio pós-receptor na captação de glicose materna", font=font_bold_sm, fill=(30, 58, 138), anchor="mm")
    draw.text((307, 306), "(Pico fisiológico no início do 3º Trimestre: 24-28 semanas)", font=font_xs, fill=(71, 85, 105), anchor="mm")

    # Transition badge: Resposta Pancreática (x: 130..485, y: 330..425)
    draw.rounded_rectangle([130, 330, 485, 425], radius=10, fill=(255, 255, 255), outline=(147, 197, 253), width=2)
    draw.text((307, 348), "Capacidade Compensatória Pancreática", font=font_card_h, fill=(15, 23, 42), anchor="mm")
    draw.text((307, 370), "O pâncreas materno é desafiado a aumentar a secreção de insulina", font=font_sm, fill=(51, 65, 85), anchor="mm")
    draw.text((215, 395), "➔ Resposta Normal (Compensada)", font=font_bold_sm, fill=(4, 120, 87), anchor="mm")
    draw.text((395, 395), "➔ Falência / DMG (Descompensada)", font=font_bold_sm, fill=(185, 28, 28), anchor="mm")

    # Left branch: Gestação Normal (x: 25..200, y: 440..650)
    draw.rounded_rectangle([25, 440, 200, 650], radius=10, fill=(236, 253, 245), outline=(110, 231, 183), width=2)
    draw.text((112, 460), "GESTAÇÃO NORMAL", font=font_card_h, fill=(6, 95, 70), anchor="mm")
    draw.text((112, 485), "Hiperinsulinismo", font=font_bold, fill=(4, 120, 87), anchor="mm")
    draw.text((112, 502), "Compensatório", font=font_bold, fill=(4, 120, 87), anchor="mm")
    draw.text((112, 525), "• Aumento de 2 a 3x na", font=font_sm, fill=(6, 78, 59), anchor="mm")
    draw.text((112, 540), "  secreção de insulina", font=font_sm, fill=(6, 78, 59), anchor="mm")
    draw.text((112, 565), "• Euglicemia Mantida", font=font_bold, fill=(4, 120, 87), anchor="mm")
    draw.text((112, 588), "• Crescimento Fetal", font=font_sm, fill=(6, 78, 59), anchor="mm")
    draw.text((112, 603), "  Harmônico e Normal", font=font_sm, fill=(6, 78, 59), anchor="mm")
    draw.text((112, 628), "➔ Sem Macrossomia", font=font_bold_sm, fill=(6, 95, 70), anchor="mm")

    # Right branch: Pâncreas Materno / Falha (x: 215..485, y: 440..535)
    draw.rounded_rectangle([215, 440, 485, 535], radius=10, fill=(248, 250, 252), outline=(203, 213, 225), width=2)
    draw.text((350, 458), "Pâncreas Materno (Células-β)", font=font_card_h, fill=(15, 23, 42), anchor="mm")
    draw.text((350, 482), "Produção insuficiente de insulina para", font=font_regular, fill=(71, 85, 105), anchor="mm")
    draw.text((350, 502), "superar a resistência periférica", font=font_bold, fill=(185, 28, 28), anchor="mm")
    draw.text((350, 520), "(Fatores genéticos + sobrecarga metabólica)", font=font_xs, fill=(100, 116, 139), anchor="mm")

    # Re-paste maternal pancreas illustration
    pancreas_pil = Image.fromarray(cv2.cvtColor(art_pancreas, cv2.COLOR_BGR2RGB))
    img.paste(pancreas_pil, (102, 648))

    # Right branch badge: Disfunção (x: 215..485, y: 545..625)
    draw.rounded_rectangle([215, 545, 485, 625], radius=10, fill=(30, 64, 175), outline=(30, 58, 138), width=2)
    draw.text((350, 568), "DISFUNÇÃO DE CÉLULAS-BETA", font=get_font("segoeuib.ttf", 13), fill=(255, 255, 255), anchor="mm")
    draw.text((350, 590), "Falência compensatória materna ➔ DMG", font=font_bold_sm, fill=(191, 219, 254), anchor="mm")
    draw.text((350, 608), "Incapacidade de conter a hiperglicemia", font=font_xs, fill=(224, 231, 255), anchor="mm")

    # Bottom banner Col 1: Hiperglicemia Materna (x: 40..475, y: 668..748)
    draw.rounded_rectangle([40, 668, 475, 748], radius=12, fill=(23, 37, 84), outline=(59, 130, 246), width=2)
    draw.text((258, 694), "HIPERGLICEMIA MATERNA", font=get_font("segoeuib.ttf", 16), fill=(255, 255, 255), anchor="mm")
    draw.text((258, 720), "Níveis plasmáticos cronicamente elevados de glicose", font=font_sm, fill=(147, 197, 253), anchor="mm")
    draw.text((258, 736), "Gera alto gradiente de difusão para o concepto", font=font_xs, fill=(191, 219, 254), anchor="mm")

    # ==========================================
    # 4. COLUMN 2: PLACENTA
    # Clean Col 2 background from y: 125..755
    # ==========================================
    draw.rectangle([508, 125, 662, 755], fill=(255, 241, 242))

    # Top card: Excesso de Glicose (x: 512..658, y: 130..220)
    draw.rounded_rectangle([512, 130, 658, 220], radius=10, fill=(255, 241, 242), outline=(252, 165, 165), width=2)
    draw.text((585, 155), "Excesso de", font=font_card_h, fill=(159, 18, 57), anchor="mm")
    draw.text((585, 175), "Glicose Materna", font=font_card_h, fill=(159, 18, 57), anchor="mm")
    draw.text((585, 200), "Alto gradiente materno-fetal", font=font_xs, fill=(136, 19, 55), anchor="mm")

    # Intermediate banner: Gradiente e Fluxo (x: 510..660, y: 240..385)
    draw.rounded_rectangle([510, 240, 660, 385], radius=10, fill=(254, 226, 226), outline=(248, 113, 113), width=2)
    draw.text((585, 260), "FLUXO PLACENTÁRIO", font=font_bold_sm, fill=(153, 27, 27), anchor="mm")
    draw.text((585, 285), "• A glicose atravessa", font=font_sm, fill=(69, 10, 10), anchor="mm")
    draw.text((585, 302), "  livremente a placenta", font=font_sm, fill=(69, 10, 10), anchor="mm")
    draw.text((585, 325), "• Sobrecarga contínua", font=font_bold_sm, fill=(185, 28, 28), anchor="mm")
    draw.text((585, 342), "  de substrato fetal", font=font_bold_sm, fill=(185, 28, 28), anchor="mm")
    draw.text((585, 365), "➔ Sem regulação materna", font=font_xs, fill=(127, 29, 29), anchor="mm")

    # Middle badge: GLUT1 (x: 510..660, y: 405..495)
    draw.rounded_rectangle([510, 405, 660, 495], radius=10, fill=(15, 118, 110), outline=(20, 184, 166), width=2)
    draw.text((585, 427), "DIFUSÃO FACILITADA", font=get_font("segoeuib.ttf", 11.5), fill=(255, 255, 255), anchor="mm")
    draw.text((585, 450), "Transportador GLUT1", font=font_card_h, fill=(94, 234, 212), anchor="mm")
    draw.text((585, 473), "Passagem contínua de glicose", font=font_xs, fill=(204, 251, 241), anchor="mm")

    # Transition arrow/card: Transporte sem insulina (x: 510..660, y: 508..565)
    draw.rounded_rectangle([510, 508, 660, 565], radius=8, fill=(254, 242, 242), outline=(252, 165, 165), width=1)
    draw.text((585, 526), "Transporte Independente", font=font_bold_sm, fill=(153, 27, 27), anchor="mm")
    draw.text((585, 545), "de Insulina Materna", font=font_sm, fill=(127, 29, 29), anchor="mm")

    # Lower barrier: Insulina NÃO atravessa (x: 508..662, y: 578..675)
    draw.rounded_rectangle([508, 578, 662, 675], radius=10, fill=(153, 27, 27), outline=(220, 38, 38), width=2)
    draw.text((585, 598), "BARREIRA PLACENTÁRIA", font=font_bold_sm, fill=(254, 202, 202), anchor="mm")
    draw.text((585, 620), "A INSULINA MATERNA", font=get_font("segoeuib.ttf", 11.5), fill=(255, 255, 255), anchor="mm")
    draw.text((585, 638), "NÃO ATRAVESSA A PLACENTA!", font=font_bold_sm, fill=(254, 242, 242), anchor="mm")
    draw.text((585, 658), "(Macromolécula bloqueada)", font=font_xs, fill=(254, 202, 202), anchor="mm")

    # ==========================================
    # 5. COLUMN 3: COMPARTIMENTO FETAL
    # Clean Col 3 background from y: 125..755
    # ==========================================
    draw.rectangle([675, 125, 970, 755], fill=(250, 245, 255))

    # Top banner: Influxo de glicose (x: 690..950, y: 130..185)
    draw.rounded_rectangle([690, 130, 950, 185], radius=10, fill=(243, 232, 255), outline=(216, 180, 254), width=1)
    draw.text((820, 147), "Influxo Contínuo de Glicose", font=font_bold, fill=(88, 28, 135), anchor="mm")
    draw.text((820, 167), "Sobrecarga de substrato energético fetal descontrolada", font=font_xs, fill=(107, 33, 168), anchor="mm")

    # Top badge: Hiperglicemia Fetal (x: 705..935, y: 195..260)
    draw.rounded_rectangle([705, 195, 935, 260], radius=10, fill=(147, 51, 234), outline=(192, 132, 252), width=2)
    draw.text((820, 217), "HIPERGLICEMIA FETAL", font=get_font("segoeuib.ttf", 14), fill=(255, 255, 255), anchor="mm")
    draw.text((820, 240), "Glicemia fetal proporcional à materna", font=font_sm, fill=(243, 232, 255), anchor="mm")

    # Middle card: Pâncreas fetal (x: 690..950, y: 275..365)
    draw.rounded_rectangle([690, 275, 950, 365], radius=10, fill=(250, 245, 255), outline=(216, 180, 254), width=2)
    draw.text((820, 295), "Pâncreas Endócrino Fetal", font=font_card_h, fill=(88, 28, 135), anchor="mm")
    draw.text((820, 318), "Hiperplasia e Hipertrofia das Células-β Fetais", font=font_bold, fill=(107, 33, 168), anchor="mm")
    draw.text((820, 338), "Estímulo contínuo das ilhotas pancreáticas a partir da 12ª semana", font=font_xs, fill=(79, 70, 229), anchor="mm")
    draw.text((820, 353), "Aumento acentuado na sensibilidade secretora", font=font_xs, fill=(88, 28, 135), anchor="mm")

    # Middle transition: Secreção autócrina (x: 690..950, y: 375..455)
    draw.rounded_rectangle([690, 375, 950, 455], radius=10, fill=(245, 235, 252), outline=(192, 132, 252), width=1)
    draw.text((820, 395), "Secreção Autônoma Exagerada", font=font_bold, fill=(88, 28, 135), anchor="mm")
    draw.text((820, 415), "• Síntese e liberação maciça de insulina pelo próprio feto", font=font_sm, fill=(59, 7, 100), anchor="mm")
    draw.text((820, 435), "• Aumento paralelo de IGF-1 e peptídeo C fetal", font=font_xs, fill=(88, 28, 135), anchor="mm")

    # Middle badge: Hiperinsulinismo Fetal (x: 705..935, y: 465..535)
    draw.rounded_rectangle([705, 465, 935, 535], radius=10, fill=(107, 33, 168), outline=(168, 85, 247), width=2)
    draw.text((820, 490), "HIPERINSULINISMO FETAL", font=get_font("segoeuib.ttf", 14), fill=(255, 255, 255), anchor="mm")
    draw.text((820, 513), "Secreção maciça de insulina pelo próprio feto", font=font_xs, fill=(243, 232, 255), anchor="mm")

    # Bottom card: Hipótese de Pedersen (x: 680..965, y: 555..755)
    draw.rounded_rectangle([680, 555, 965, 755], radius=12, fill=(243, 232, 255), outline=(168, 85, 247), width=2)
    draw.rounded_rectangle([700, 568, 945, 598], radius=6, fill=(126, 34, 206))
    draw.text((822, 583), "HIPÓTESE DE PEDERSEN (1954)", font=get_font("segoeuib.ttf", 12), fill=(255, 255, 255), anchor="mm")
    draw.text((695, 610), "• A insulina atua como o PRINCIPAL hormônio", font=font_bold, fill=(59, 7, 100))
    draw.text((695, 626), "  de crescimento intrauterino.", font=font_bold, fill=(59, 7, 100))
    draw.text((695, 646), "• Potente ação anabólica fetal:", font=font_bold, fill=(88, 28, 135))
    draw.text((695, 664), "  - Síntese acelerada de glicogênio e lipídios", font=font_regular, fill=(59, 7, 100))
    draw.text((695, 682), "  - Estímulo à captação celular de aminoácidos", font=font_regular, fill=(59, 7, 100))
    draw.text((695, 700), "  - Proliferação e hipertrofia celular sistêmica", font=font_regular, fill=(59, 7, 100))
    draw.text((695, 722), "➔ Gera crescimento somático desproporcional", font=font_bold_sm, fill=(153, 27, 27))

    # ==========================================
    # 6. COLUMN 4: CONSEQUÊNCIAS FETAIS E NEONATAIS
    # Background color of all 4 cards: #eedfee -> (237, 222, 237)
    # Border: (216, 180, 226)
    # Clean Col 4 interior from y: 125..765
    # ==========================================
    card_bg = (237, 222, 237)
    card_border = (216, 180, 226)
    draw.rectangle([980, 125, 1365, 765], fill=(245, 235, 246))

    # ------------------------------------------
    # Card 1: MACROSSOMIA FETAL (y: 130..368)
    # ------------------------------------------
    draw.rounded_rectangle([985, 130, 1358, 368], radius=12, fill=card_bg, outline=card_border, width=2)
    draw.text((1171, 148), "1) MACROSSOMIA FETAL (PN > 4.000g)", font=get_font("segoeuib.ttf", 13.5), fill=(88, 28, 135), anchor="mm")

    # Paste preserved anatomical art pieces
    baby_pil = Image.fromarray(cv2.cvtColor(art_baby, cv2.COLOR_BGR2RGB))
    organs_pil = Image.fromarray(cv2.cvtColor(art_organs, cv2.COLOR_BGR2RGB))
    img.paste(baby_pil, (998, 172))
    img.paste(organs_pil, (1210, 178))

    # Text next to baby and organs (Zero white boxes, seamless typography)
    draw.text((1095, 175), "Depósito de Gordura:", font=font_bold, fill=(15, 23, 42))
    draw.text((1095, 192), "• Tronco e ombros volumosos", font=font_sm, fill=(51, 65, 85))
    draw.text((1095, 208), "• Distribuição assimétrica", font=font_sm, fill=(51, 65, 85))
    draw.text((1095, 226), "➔ Risco de Distócia", font=font_bold_sm, fill=(153, 27, 27))
    draw.text((1095, 240), "    de Ombros", font=font_bold_sm, fill=(153, 27, 27))

    draw.text((1205, 242), "Organomegalia:", font=font_bold_sm, fill=(15, 23, 42))
    draw.text((1205, 258), "• Fígado e Coração", font=font_xs, fill=(51, 65, 85))

    # Card 1 bottom details
    draw.text((1000, 290), "• Hipertrofia do Septo Interventricular (Cardiopatia transitória)", font=font_bold_sm, fill=(88, 28, 135))
    draw.text((1000, 310), "• Circunferência Abdominal fetal desproporcional à Cefálica", font=font_sm, fill=(51, 65, 85))
    draw.text((1000, 328), "• Lesões de plexo braquial e asfixia perinatal intraparto", font=font_sm, fill=(51, 65, 85))
    draw.text((1000, 348), "➔ Indicação de cesariana eletiva se PN estimado > 4.500g", font=font_bold_sm, fill=(153, 27, 27))

    # ------------------------------------------
    # Card 2: HIPOGLICEMIA NEONATAL (y: 374..552)
    # ------------------------------------------
    draw.rounded_rectangle([985, 374, 1358, 552], radius=12, fill=card_bg, outline=card_border, width=2)
    draw.text((1171, 392), "2) HIPOGLICEMIA NEONATAL GRAVE", font=get_font("segoeuib.ttf", 13.5), fill=(185, 28, 28), anchor="mm")
    draw.text((1000, 412), "Após o Clampeamento Imediato do Cordão Umbilical:", font=font_bold, fill=(30, 41, 59))
    draw.text((1000, 432), "• Interrupção Abrupta: Cessa a oferta contínua de glicose materna", font=font_sm, fill=(51, 65, 85))
    draw.text((1000, 450), "• Hiperinsulinismo Persistente: Pâncreas neonatal continua hipersecretante", font=font_bold_sm, fill=(153, 27, 27))
    draw.text((1000, 468), "• Rápida captação de glicose pelos tecidos + bloqueio da gliconeogênese", font=font_sm, fill=(51, 65, 85))
    draw.text((1000, 486), "➔ Queda vertiginosa da glicemia nas primeiras 2 a 4 horas (< 40 mg/dL)", font=font_bold_sm, fill=(185, 28, 28))

    # Management mini badge
    draw.rounded_rectangle([998, 510, 1345, 540], radius=6, fill=(220, 252, 231), outline=(134, 239, 172), width=1)
    draw.text((1171, 525), "Conduta: Amamentação na 1ª hora + monitorização de HGT em 30-60 min", font=font_bold_sm, fill=(6, 95, 70), anchor="mm")

    # ------------------------------------------
    # Card 3: HIPÓXIA FETAL & POLICITEMIA (y: 558..700)
    # ------------------------------------------
    draw.rounded_rectangle([985, 558, 1358, 700], radius=12, fill=card_bg, outline=card_border, width=2)
    draw.text((1171, 576), "3) HIPÓXIA FETAL CRÔNICA & POLICITEMIA", font=get_font("segoeuib.ttf", 13), fill=(88, 28, 135), anchor="mm")
    draw.text((1000, 598), "• Hipermetabolismo fetal por insulina aumenta o consumo tecidual de O₂", font=font_sm, fill=(51, 65, 85))
    draw.text((1000, 616), "• Gera hipóxia crônica ➔ Estímulo à Eritropoietina (EPO) fetal", font=font_bold_sm, fill=(107, 33, 168))
    draw.text((1000, 634), "• Policitemia Neonatal (Ht > 65%): Hiperviscosidade e trombose venosa", font=font_sm, fill=(51, 65, 85))
    draw.text((1000, 652), "➔ Hemólise acentuada pós-natal de eritrócitos excedentes", font=font_bold_sm, fill=(153, 27, 27))
    draw.text((1000, 672), "➔ Hiperbilirrubinemia Indireta, icterícia grave e risco de Kernicterus", font=font_bold_sm, fill=(185, 28, 28))

    # ------------------------------------------
    # Card 4: ATRASO NO SURFACTANTE PULMONAR (y: 706..764)
    # ------------------------------------------
    draw.rounded_rectangle([985, 706, 1358, 764], radius=10, fill=card_bg, outline=card_border, width=2)
    draw.text((1171, 722), "4) ATRASO NA MATURAÇÃO DO SURFACTANTE PULMONAR", font=get_font("segoeuib.ttf", 12), fill=(88, 28, 135), anchor="mm")
    draw.text((1171, 744), "Insulina antagoniza o cortisol em pneumócitos II ➔ Déficit de surfactante ➔ Risco de SDR!",
              font=font_bold_sm, fill=(153, 27, 27), anchor="mm")

    # Save final high quality image
    dest_path = "assets/img/gdm_pathophysiology.jpg"
    img.save(dest_path, "JPEG", quality=95)
    print("SUCCESS: GDM pathophysiology completely recreated with ZERO English fragments!")

if __name__ == "__main__":
    build_gdm_portuguese()
