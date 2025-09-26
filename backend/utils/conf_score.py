from sentence_transformers import SentenceTransformer, util

# Load once
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def conf_scoring(ocr_extracted_text, llm_structured_text):
    """
    Compute confidence score by combining:
      1. Row count ratio
      2. Field alignment check
      3. Embedding similarity
      4. LLM's own confidence (if provided)

    Args:
        ocr_extracted_text (str | list): OCR raw text or list of lines
        llm_structured_text (dict): dict with keys {"table": [...], "confidence": float, "flags": [...]}

    Returns:
        dict: component scores + final_conf
    """
    # Ensure OCR text is a list of lines
    if isinstance(ocr_extracted_text, str):
        ocr_lines = [line.strip() for line in ocr_extracted_text.splitlines() if line.strip()]
    elif isinstance(ocr_extracted_text, list):
        ocr_lines = [str(line) for line in ocr_extracted_text]
    else:
        ocr_lines = []
        print("[Error] OCR extracted text has unsupported type.")

    # Extract table
    try:
        table = llm_structured_text.get("table", [])
    except Exception as e:
        print(f"[Error] Unable to extract 'table': {e}")
        table = []

    # Row count score
    try:
        row_count_score = min(len(table) / max(len(ocr_lines), 1), 1.0)
    except Exception as e:
        print(f"[Error] Row count check failed: {e}")
        row_count_score = 0.0

    # Field alignment
    try:
        matched = 0
        for row in table:
            row_text = " ".join(str(v) for v in row.values())
            if any(row_text in line for line in ocr_lines):
                matched += 1
        field_score = matched / max(len(table), 1)
    except Exception as e:
        print(f"[Error] Field alignment check failed: {e}")
        field_score = 0.0

    # Embedding similarity
    embed_score = 0.0
    row_score = []
    try:
        if ocr_lines and table:
            llm_texts = [" ".join(str(v) for v in row.values()) for row in table]
            ocr_embeds = model.encode(ocr_lines, convert_to_tensor=True)
            llm_embeds = model.encode(llm_texts, convert_to_tensor=True)
            sim_matrix = util.cos_sim(llm_embeds, ocr_embeds)  # shape [rows, lines]

            row_score = [float(sim_matrix[i].max()) for i in range(len(llm_texts))]
            embed_score = sum(row_score) / max(len(row_score), 1)
    except Exception as e:
        print(f"[Error] Embedding similarity failed: {e}")
        embed_score = 0.0
        row_score = []

    # LLM Self Confidence
    try:
        llm_conf = float(llm_structured_text.get("confidence", 0.0))
    except Exception as e:
        print(f"[Error] LLM confidence extraction failed: {e}")
        llm_conf = 0.0

    # Final weighted score
    try:
        final_conf = (
            0.25 * row_count_score +
            0.25 * field_score +
            0.35 * embed_score +
            0.15 * llm_conf
        )
    except Exception as e:
        print(f"[Error] Final confidence calculation failed: {e}")
        final_conf = 0.0

    return {
        "row_score": row_score,
        "row_count_score": row_count_score,
        "field_score": field_score,
        "embed_score": embed_score,
        "llm_conf": llm_conf,
        "final_conf": final_conf
    }