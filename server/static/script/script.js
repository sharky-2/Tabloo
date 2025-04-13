// ===============================================================================
// Upload
const dropZone = document.getElementById("dropZone");
const fileInput = document.getElementById("excelFiles");

dropZone.addEventListener("dragover", (event) => {
    event.preventDefault();
    dropZone.classList.add("dragover");
});

dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("dragover");
});

dropZone.addEventListener("drop", (event) => {
    event.preventDefault();
    dropZone.classList.remove("dragover");
    fileInput.files = event.dataTransfer.files; 
});

function uploadFiles() {
    const formData = new FormData();
    for (let i = 0; i < fileInput.files.length; i++) {
        formData.append('files', fileInput.files[i]);
    }

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            alert('Files uploaded successfully!');
        } else {
            alert('File upload failed.');
        }
    });
}

// ===============================================================================
// Search
function search() {
    const query = document.getElementById("query").value;
    fetch("/search", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: "query=" + encodeURIComponent(query)
    })
    .then(res => res.json())
    .then(data => {
        const resultsDiv = document.getElementById("results");
        resultsDiv.innerHTML = "";
        if (data.length === 0) {
            resultsDiv.innerHTML = "<p class='text-design'>No results found.</p>";
            return;
        }
        data.forEach(item => {
            const block = document.createElement("div");
            block.className = "result-block";
            
            const header = document.createElement("div");
            header.className = "file";
            const name = document.createElement("label");
            name.innerText = ` 📄 ${item.file}`;
            const row = document.createElement("label");
            row.innerText = `Row > ${item.row_number}`;
            header.appendChild(name);
            header.appendChild(row);

            const content = document.createElement("div");
            content.className = "columns";
        
            for (const [key, value] of Object.entries(item.data)) {
                const label = document.createElement("div");
                label.className = "column";
                label.innerHTML = `${key}: ${value}`;
                content.appendChild(label);
            }
        
            block.appendChild(header);
            block.appendChild(content);
            resultsDiv.appendChild(block);
        });
        
    });
}

// ===============================================================
// Auto resize textarea of chat
const textarea = document.getElementById("query")
function autoResize() {
  textarea.style.height = 'auto'; 
  textarea.style.height = (textarea.scrollHeight) + 'px';
}
function resetHeight() {
  textarea.style.height = "auto"
}
