const chatForm = document.getElementById("chatForm");
const messageInput = document.getElementById("messageInput");
const chatBox = document.getElementById("chatBox");

function addMessage(role, text) {
    const div = document.createElement("div");
    div.className = "chat-message";
    if (role === "user") {
        div.innerHTML = `<p><strong>使用者：</strong>${text}</p>`;
    } else {
        div.innerHTML = `<p><strong>智能客服回應：</strong>${text}</p>`;
    }
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;

    addMessage("user", message);
    messageInput.value = "";

    fetch("/send_message", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => addMessage("gpt_text", data.reply))
    .catch(err => console.error(err));
}

messageInput.addEventListener("keydown", function(event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
});

chatForm.addEventListener("submit", function(event) {
    event.preventDefault();
    sendMessage();
});

window.addEventListener("DOMContentLoaded", () => {
    messageInput.focus();
    messageInput.setSelectionRange(messageInput.value.length, messageInput.value.length);
});

window.addEventListener("beforeunload", function () {
    const messages = Array.from(document.querySelectorAll(".chat-message")).map(div => {
        const text = div.textContent.replace(/^使用者：|^智能客服回應：/, '').trim();
        const role = div.textContent.startsWith("使用者") ? "user" : "gpt_text";
        return { role: role, text: text };
    });

    if (messages.length > 0) {
        const blob = new Blob([JSON.stringify({ chat_history: messages })], { type: "application/json" });
        navigator.sendBeacon("/save_chat", blob);
    }
});