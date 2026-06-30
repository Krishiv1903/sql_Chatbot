// ✅ Welcome message on load
window.onload = function () {
    setTimeout(() => {
        addMessage("👋 Hello! I can help you create or view appointments.\nTry: 'Book a meeting with Krishiv tomorrow'", "bot");
    }, 500);
};

async function sendMessage() {
    const input = document.getElementById("message");
    const text = input.value.trim();
    if (!text) return;

    addMessage(text, "user");
    input.value = "";

    showLoader();

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: text })
        });

        const data = await response.json();

        hideLoader();
        addMessage(formatResponse(data.response), "bot");

    } catch (error) {
        hideLoader();
        addMessage("❌ Server error", "bot");
    }
}

// ✅ Add message
function addMessage(text, sender) {
    const chat = document.getElementById("chat");

    const msg = document.createElement("div");
    msg.className = "message " + sender;
    msg.innerHTML = text;

    chat.appendChild(msg);
    chat.scrollTop = chat.scrollHeight;
}

// ✅ Loader
function showLoader() {
    document.getElementById("loader").classList.remove("hidden");
}

function hideLoader() {
    document.getElementById("loader").classList.add("hidden");
}

// ✅ Format response
function formatResponse(res) {
    if (typeof res === "string") return res;

    let output = "";
    res.forEach(item => {
        output += `
        <div class="card">
            <b>${item.name}</b><br>
            📅 ${item.date}<br>
            📝 ${item.desc}
        </div>`;
    });

    return output;
}

// ✅ Enter key support
document.getElementById("message").addEventListener("keypress", function(e) {
    if (e.key === "Enter") {
        sendMessage();
    }
});