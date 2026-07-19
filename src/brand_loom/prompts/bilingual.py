"""Prompt builder for the bilingual translation skill."""

from __future__ import annotations

SUPPORTED_LOCALES = {"en", "zh-TW"}

BILINGUAL_FEW_SHOT = (
    "\n\nHere are examples of voice-preserving translations:\n"
    "Source (en): \"We tested 12 tools. Most were trash. Here's the 3 that actually ship.\"\n"
    "Target (zh-TW): \"我們測試了 12 款工具，多數不值一提。這 3 款才是真正能交付的。\"\n\n"
    "Source (zh-TW): \"別再追求完美了——先上線，再迭代。\"\n"
    "Target (en): \"Stop chasing perfect — ship it, then iterate.\""
)


def build_bilingual_prompt(
    text: str,
    *,
    target_locale: str = "zh-TW",
    brand_context: dict | None = None,
    preserve_terms: list[str] | None = None,
) -> tuple[str, str]:
    """Build (system, user) prompts for bilingual translation.

    Translates between EN and zh-TW while preserving brand voice.
    """
    system = (
        f"You are a bilingual marketing copywriter fluent in English and Traditional Chinese "
        f"(zh-TW). Translate the given text into {target_locale}. "
        "This is NOT word-level translation — it is a voice-preserving rewrite in the target "
        "locale. Preserve the energy, rhythm, and persuasive impact of the original."
        + BILINGUAL_FEW_SHOT
    )

    if brand_context:
        tone = brand_context.get("tone", [])
        audience = brand_context.get("audience", "")
        do_phrases = brand_context.get("do_phrases", [])
        avoid_phrases = brand_context.get("avoid_phrases", [])
        if tone:
            system += f" Tone: {', '.join(tone)}."
        if audience:
            system += f" Target audience: {audience}."
        if do_phrases:
            system += f" Preferred phrases/style: {', '.join(do_phrases)}."
        if avoid_phrases:
            system += f" Avoid: {', '.join(avoid_phrases)}."

    preserve_note = ""
    if preserve_terms:
        preserve_note = (
            f"\n\nPreserve these terms verbatim (do not translate): "
            f"{', '.join(preserve_terms)}"
        )

    user = (
        f"Translate the following into {target_locale}. "
        f"Return a JSON object with keys: \"translation\" (the translated text) "
        f"and \"target_locale\" (\"{target_locale}\")."
        f"{preserve_note}\n\n"
        f"Source text:\n{text}"
    )

    return system, user
