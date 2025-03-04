document.addEventListener("DOMContentLoaded", function () {
    const translateBtn = document.getElementById("translate-btn");
    const sourceText = document.getElementById("source-text");
    const targetText = document.getElementById("target-text");
    const sourceLang = document.getElementById("source-language");
    const targetLang = document.getElementById("target-language");

    translateBtn.addEventListener("click", function () {
        const text = sourceText.value;
        if (!text.trim()) {
            alert("Enter text to translate.");
            return;
        }

        fetch("/translate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                text: text,
                source_lang: sourceLang.value,
                target_lang: targetLang.value,
            }),
        })
            .then((response) => response.json())
            .then((data) => {
                targetText.value = data.translated_text || "Translation failed.";
            })
            .catch((error) => console.error("Translation error:", error));
    });
});