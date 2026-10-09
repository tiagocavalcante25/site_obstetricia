import os

def build():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    components_dir = os.path.join(base_dir, "components")
    index_file = os.path.join(base_dir, "index.html")

    # Read components in exact visual order
    order = [
        "header.html",
        "hero.html",
        "modulos-index.html",
        "modulo-1-leopold.html",
        "calculadoras.html",
        "modulo-2-ultrassom.html",
        "modulo-4-imunizacoes.html",
        "modulo-5-dmg-preeclampsia.html",
        "modulo-6-ctg-doppler.html",
        "modulo-7-stff.html",
        "modulo-8-rh.html",
        "modulo-9-10-11-infeccoes.html",
        "flashcards.html",
        "quiz-simulado.html",
        "high-yield-summary.html",
        "footer.html",
        "modals.html"
    ]

    print(f"Verificando {len(order)} componentes em {components_dir}...")
    for comp in order:
        p = os.path.join(components_dir, comp)
        if not os.path.exists(p):
            raise FileNotFoundError(f"Componente não encontrado: {comp}")

    print("Todos os componentes verificados com sucesso!")

if __name__ == "__main__":
    build()
