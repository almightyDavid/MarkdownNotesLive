document.addEventListener("DOMContentLoaded", () => {
    const title = document.getElementById("title-input");
    const content = document.getElementById("markdown-input");
    const status = document.getElementById("autosave-status");

    if (!title || !content) return;

    const noteId = window.location.pathname.split("/")[2];
    let timeout;

    async function autosave() {
        status.textContent = "Saving...";

        await fetch(`/notes/${noteId}/autosave`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": document.querySelector(
                    'input[name="csrf_token"]'
                )?.value
            },
            body: JSON.stringify({
                title: title.value,
                content: content.value
            })
        });

        status.textContent = "Saved ✓";
    }

    function scheduleSave() {
        clearTimeout(timeout);
        timeout = setTimeout(autosave, 1000);
    }

    title.addEventListener("input", scheduleSave);
    content.addEventListener("input", scheduleSave);
});
;