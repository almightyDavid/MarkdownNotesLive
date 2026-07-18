document.addEventListener("DOMContentLoaded", () => {
        const search = document.getElementById("search");
        const list = document.getElementById("note-list");

        search.addEventListener("input", async () => {
            const q = search.value;
                
            if (!search || !list) return;

            const res = await fetch(`/notes/search?q=${encodeURIComponent(q)}`);
            list.innerHTML = await res.text();
        });
});