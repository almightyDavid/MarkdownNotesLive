document.addEventListener("DOMContentLoaded", () => {
    const content = document.getElementById("note-content");
    if (!content) return;

    renderMathInElement(content, {
        delimiters: [
            { left: "$$", right: "$$", display: true },
            { left: "$", right: "$", display: false }
        ],
        throwOnError: false
    });
});

// live preview
document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("markdown-input");
    const preview = document.getElementById("markdown-preview");

    if (!input || !preview) return;

    const render = () => {
        const rawHtml = marked.parse(input.value);
        const cleanHtml = DOMPurify.sanitize(rawHtml);

        preview.innerHTML = cleanHtml;

        renderMathInElement(preview, {
            delimiters: [
                { left: "$$", right: "$$", display: true },
                { left: "$", right: "$", display: false }
            ],
            throwOnError: false
        });
        
        Prism.highlightAllUnder(preview);
    };

    input.addEventListener("input", render);
    render();
});