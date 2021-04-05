def remove_prefix(text, prefix):
    if text and text.startswith(prefix):
        return text[len(prefix):]
    return text
