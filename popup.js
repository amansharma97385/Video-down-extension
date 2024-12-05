document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("download-form");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const url = document.getElementById("url").value.trim();
        const type = document.getElementById("type").value;
        const quality = document.getElementById("quality").value;

        if (!url) {
            alert("Please provide a valid URL.");
            return;
        }

        try {
            const response = await fetch("http://127.0.0.1:5000/download", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ url, type, quality }),
            });

            if (response.ok) {
                const blob = await response.blob();
                const downloadUrl = window.URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = downloadUrl;
                a.download = "downloaded_file";
                document.body.appendChild(a);
                a.click();
                a.remove();
            } else {
                const errorText = await response.text();
                console.error("Error response:", errorText);
                alert("Failed to download. Check the console for details.");
            }
        } catch (error) {
            console.error("Error:", error);
            alert("An error occurred. See the console for details.");
        }
    });
});
