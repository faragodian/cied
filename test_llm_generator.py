from app.services.llm_generator import generate_week01_exercise

if __name__ == "__main__":
    ejercicio = generate_week01_exercise(
        r"\int x e^{x} \, dx"
    )
    print("Ejercicio generado por la LLM:")
    print(ejercicio)
