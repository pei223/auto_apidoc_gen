def round_text(_text: str, length: int):
    arranged_text = (str(_text) + "　" * length)[:length]
    if len(_text) > length:
        arranged_text = list(arranged_text)
        arranged_text[-1] = "…"
        arranged_text = "".join(arranged_text)
    return arranged_text
