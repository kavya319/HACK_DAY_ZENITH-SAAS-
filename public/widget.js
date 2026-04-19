(function () {
  const script = document.currentScript;
  const botId = script.getAttribute("data-bot-id");

  const box = document.createElement("div");
  box.style.position = "fixed";
  box.style.bottom = "20px";
  box.style.right = "20px";
  box.style.width = "300px";
  box.style.background = "white";
  box.style.border = "1px solid #ccc";
  box.style.padding = "10px";
  box.style.zIndex = "9999";

  box.innerHTML = `
    <div id="chat-box" style="height:200px; overflow:auto;"></div>
    <input id="chat-input" placeholder="Ask..." style="width:70%" />
    <button id="send-btn">Send</button>
  `;

  document.body.appendChild(box);

  const input = box.querySelector("#chat-input");
  const chatBox = box.querySelector("#chat-box");

  box.querySelector("#send-btn").onclick = async () => {
    const message = input.value;

    const res = await fetch(
      `http://localhost:8000/chat?query=${encodeURIComponent(message)}&bot_id=${botId}`,
      { method: "POST" }
    );

    const data = await res.json();

    chatBox.innerHTML += `<p><b>You:</b> ${message}</p>`;
    chatBox.innerHTML += `<p><b>Bot:</b> ${data.reply}</p>`;

    input.value = "";
  };
})();