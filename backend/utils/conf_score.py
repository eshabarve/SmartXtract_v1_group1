def compute_confidence(ocr_lines, llm_output, embedding_similarity=0.8):
    """
    ocr_lines: list of strings from OCR
    llm_output: dict with keys {"table": [...], "confidence": float, "flags": [...]}
    embedding_similarity: placeholder avg similarity (0-1), replace with real model
    """
    
    llm_table = llm_output["table"]
    llm_conf = llm_output.get("confidence", 0.0)

    # 1. Row count check
    row_score = min(len(llm_table) / max(len(ocr_lines), 1), 1.0)

    # 2. Field alignment (simple string containment)
    matched = 0
    for row in llm_table:
        row_text = " ".join(str(v) for v in row.values())
        if any(row_text in line for line in ocr_lines):
            matched += 1
    field_score = matched / max(len(llm_table), 1)

    # 3. Embedding similarity (use real embeddings later)
    embed_score = embedding_similarity

    # Weighted sum
    final_conf = (
        0.35 * row_score +
        0.25 * field_score +
        0.25 * embed_score +
        0.15 * llm_conf
    )

    return final_conf