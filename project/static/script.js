const socket = io();

function sendMessage() {
  const to = document.getElementById("recipient").value.trim();
  const message = document.getElementById("message").value.trim();

  if (!to || !message) return;

  socket.emit("send_message", {
    from: sessionUsername,
    to: to,
    message: message
  });

  // Remove local display of sent message
  document.getElementById("message").value = "";
  scrollToBottom();
}

socket.on("connect", () => {
  socket.emit("register_socket", { username: sessionUsername });
});

socket.on("receive_message", (data) => {
  const from = data.from;
  const message = data.message;

  const msg = `<div class="message-other">${from} : ${message}</div>`;
  document.getElementById("chat").innerHTML += msg;
  scrollToBottom();
});

function scrollToBottom() {
  const chat = document.getElementById("chat");
  chat.scrollTop = chat.scrollHeight;
}
