const chatBox = document.getElementById("chatBox");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");

sendBtn.addEventListener("click", sendMessage);
userInput.addEventListener("keypress", function (e) {
  if (e.key === "Enter") {
    sendMessage();
  }
});

function sendMessage() {
  const userMessage = userInput.value.trim();
  if (userMessage === "") return;

  // Append user message to the chat
  appendMessage("user", userMessage);
  userInput.value = "";

  // Send user message to backend
  fetch("http://localhost:8000/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      instruction: userMessage,
      input_data: "",
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      appendMessage("bot", data.response);
      addReactionButtons(data.chat_history_id);
    })
    .catch((error) => {
      console.error("Error:", error);
      appendMessage("bot", "Maaf, terjadi kesalahan. Silakan coba lagi.");
    });
}

function appendMessage(role, message) {
  const messageDiv = document.createElement("div");
  messageDiv.classList.add("message", role);
  messageDiv.textContent = message;
  chatBox.appendChild(messageDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function addReactionButtons(chatHistoryId) {
  const reactionDiv = document.createElement("div");
  reactionDiv.classList.add("reaction-btns");

  const likeBtn = document.createElement("button");
  likeBtn.classList.add("reaction-btn");
  likeBtn.textContent = "Like";
  likeBtn.addEventListener("click", () => addReaction(chatHistoryId, "like"));

  const dislikeBtn = document.createElement("button");
  dislikeBtn.classList.add("reaction-btn");
  dislikeBtn.textContent = "Dislike";
  dislikeBtn.addEventListener("click", () =>
    addReaction(chatHistoryId, "dislike")
  );

  const regenerateBtn = document.createElement("button");
  regenerateBtn.classList.add("reaction-btn");
  regenerateBtn.textContent = "Regenerate";
  regenerateBtn.addEventListener("click", () =>
    regenerateResponse(chatHistoryId)
  );

  reactionDiv.appendChild(likeBtn);
  reactionDiv.appendChild(dislikeBtn);
  reactionDiv.appendChild(regenerateBtn);

  chatBox.appendChild(reactionDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function addReaction(chatHistoryId, reaction) {
  fetch("http://localhost:8000/react", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      chat_history_id: chatHistoryId,
      reaction: reaction,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Reaction saved:", data);
    })
    .catch((error) => {
      console.error("Error saving reaction:", error);
    });
}

function regenerateResponse(chatHistoryId) {
  fetch("http://localhost:8000/regenerate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      chat_history_id: chatHistoryId,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      appendMessage("bot", data.response);
      addReactionButtons(data.chat_history_id);
    })
    .catch((error) => {
      console.error("Error regenerating response:", error);
      appendMessage(
        "bot",
        "Maaf, terjadi kesalahan saat mencoba regenerasi jawaban. Silakan coba lagi."
      );
    });
}
