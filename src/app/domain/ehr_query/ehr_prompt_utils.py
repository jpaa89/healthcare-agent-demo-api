from app.domain.ehr_ingestion.ehr_context_models import EHRContextItem


def build_ehr_contexts_selection_prompt(
    question: str, ehr_context_items: list[EHRContextItem]
) -> str:
    lines = [
        "Eres un asistente clínico.",
        'Selecciona únicamente los "id" de los contextos relevantes.',
        "No inventes información, datos, ni hagas suposiciones.",
        "",
        f"Pregunta: {question}",
        "",
        "Contextos:",
    ]

    for item in ehr_context_items:
        lines.append(f"")
        lines.append(f"- id: {item.id}")
        lines.append(f"\ttipo: {item.type}")
        lines.append(f"\tcontenido: {item.content}")
        lines.append(f"\tdatos: {item.data}")

    lines.append(f"")

    return "\n".join(lines)


def build_grounded_query_output_prompt(
    question: str,
    ehr_context_items: list[EHRContextItem],
) -> str:
    lines = [
        "Eres un asistente clínico.",
        "Responde la pregunta usando únicamente la información proporcionada.",
        "No inventes información, datos, ni hagas suposiciones.",
        "Si la información no es suficiente, indícalo explícitamente.",
        "Al terminar de dar la respuesta, incluye información clara sobre las fuentes o referencias utilizadas.",
        "",
        "Ejemplos de respuestas esperadas (los valores son solo ilustrativos):",
        "",
        "Pregunta: ¿Cuál es la medicación actual del paciente?",
        "Respuesta:",
        "El paciente actualmente se encuentra en tratamiento con <MEDICAMENTO_1> <DOSIS_1> y <MEDICAMENTO_2> <DOSIS_2>.",
        "Fuentes: Según el historial médico del paciente (medicación actual registrada).",
        "",
        "Pregunta: ¿Cuándo fue su última visita y por qué?",
        "Respuesta:",
        "La última visita del paciente fue el <FECHA_VISITA> y correspondió a una <RAZÓN_DE_LA_VISITA>.",
        "Fuentes: Según la visita clínica del <FECHA_VISITA>, documentada por <PROFESIONAL_DE_SALUD>.",
        "",
        "Pregunta: ¿Tiene alguna alergia que deba considerar?",
        "Respuesta:",
        "Sí. El paciente presenta alergia a <ALERGIA>, la cual debe considerarse antes de prescribir tratamientos.",
        "Fuentes: Según el historial médico del paciente, sección de alergias.",
        "",
        "Pregunta: ¿Cómo ha evolucionado un parámetro clínico relevante?",
        "Respuesta:",
        "En el estudio realizado el <FECHA_ESTUDIO>, se registró un valor de <PARÁMETRO_CLÍNICO> igual a <VALOR>, junto con <OTRO_INDICADOR>, lo que sugiere <INTERPRETACIÓN_GENERAL>.",
        "Fuentes: Según el resultado del estudio del <FECHA_ESTUDIO>.",
        "",
        "Sigue el mismo estilo y nivel de detalle mostrado en los ejemplos anteriores.",
        "Los ejemplos anteriores no contienen datos reales y no deben reutilizarse en la respuesta.",
        "",
        f"Pregunta: {question}",
        "",
        "Información del paciente:",
    ]

    for ctx in ehr_context_items:
        lines.append(f"- id: {ctx.id}\n")
        lines.append(f"\ttipo: {ctx.type}\n")
        lines.append(f"\tcontenido: {ctx.content}")
        lines.append(f"\tdatos: {ctx.data}")
        lines.append(f"\tfuente/referencia: {ctx.data}")

    return "\n".join(lines)
