console.log("script.js loaded");

document.getElementById('urlForm').addEventListener('submit', async (event) => {
     event.preventDefault();
    const targetUrl = document.getElementById('userUrl').value;  // declare FIRST
    console.log("Form submitted, target URL:", targetUrl);        // log AFTER
    const outputDiv = document.getElementById('output');
    outputDiv.textContent = "Loading...";

    try {
        const response = await fetch('http://127.0.0.1:5000/api/download', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: targetUrl })
        });

        const data = await response.json();

        if (data.status === 'success') {
            outputDiv.innerHTML = `
                <p>Done: "${data.title}"</p>
                <a href="http://127.0.0.1:5000${data.download_url}" download>Click here to download</a>
            `;
        } else {
            outputDiv.textContent = `Error: ${data.message}`;
        }
    } catch (error) {
        outputDiv.textContent = `Error: ${error.message}`;
        console.error("Fetch failure:", error);
    }
});