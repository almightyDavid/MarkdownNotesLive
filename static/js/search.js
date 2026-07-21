document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("search");
    const noteList = document.getElementById("note-list");

    if (!searchInput || !noteList) {
        return;
    }

    const originalNotesHtml = noteList.innerHTML;
    let searchTimer = null;

    searchInput.addEventListener("input", () => {
        window.clearTimeout(searchTimer);

        searchTimer = window.setTimeout(async () => {
            const query = searchInput.value.trim();

            if (!query) {
                noteList.innerHTML = originalNotesHtml;
                return;
            }

            searchInput.setAttribute("aria-busy", "true");

            try {
                const response = await fetch(
                    `/notes/search?q=${encodeURIComponent(query)}`
                );

                if (!response.ok) {
                    throw new Error(
                        `Search request failed with status ${response.status}`
                    );
                }

                noteList.innerHTML = await response.text();
            } catch (error) {
                console.error("Unable to search notes:", error);

                noteList.innerHTML = `
                    <p role="alert">
                        Search failed. Please try again.
                    </p>
                `;
            } finally {
                searchInput.removeAttribute("aria-busy");
            }
        }, 200);
    });
});