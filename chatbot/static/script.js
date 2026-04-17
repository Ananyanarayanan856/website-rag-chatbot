const chatWindow = document.getElementById('chat-window');
const chatInput = document.getElementById('chat-input');
const loader = document.getElementById('loader');

// Keep track of the globally playing audio
let currentAudio = null;

async function sendMessage() {
    // If audio is currently playing, force stop it immediately!
    if (currentAudio) {
        currentAudio.pause();
        currentAudio.currentTime = 0;
    }
    
    // Create a new audio object synchronously during the user gesture to bypass browser autoplay restrictions
    currentAudio = new Audio();
    
    const text = chatInput.value.trim();
    if (!text) return;

    // Add user bubble
    appendMessage(text, 'user-msg');
    chatInput.value = '';

    // Show Loader
    chatWindow.appendChild(loader);
    loader.classList.add('active');
    chatWindow.scrollTop = chatWindow.scrollHeight;

    try {
        // Call /chat API defined in main.py
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: text })
        });
        
        const data = await response.json();
        
        // Hide Loader
        loader.classList.remove('active');

        if(data.error) {
            appendMessage("Error: " + data.error, 'bot-msg');
        } else {
            appendMessage(data.answer, 'bot-msg', data.audio);
        }

    } catch (error) {
        loader.classList.remove('active');
        appendMessage("Error reaching the assistant. Ensure the backend is running and data is loaded.", 'bot-msg');
    }
}

function appendMessage(text, className, audioBase64 = null) {
    const div = document.createElement('div');
    div.className = `message-bubble ${className}`;
    
    // Add text content
    const textSpan = document.createElement('span');
    textSpan.className = 'message-text';
    textSpan.innerText = text;
    div.appendChild(textSpan);
    
    // Create actions bar if audio exists
    if (audioBase64) {
        const actionsDiv = document.createElement('div');
        actionsDiv.className = 'message-actions';
        
        const audioBtn = document.createElement('button');
        audioBtn.className = 'play-audio-btn';
        audioBtn.title = 'Listen to response';
        audioBtn.innerHTML = '🔊';
        audioBtn.onclick = () => {
            if (currentAudio) {
                currentAudio.pause();
                currentAudio.currentTime = 0;
            }
            currentAudio = new Audio("data:audio/wav;base64," + audioBase64);
            currentAudio.play().catch(e => console.error("Playback failed:", e));
        };
        
        actionsDiv.appendChild(audioBtn);
        div.appendChild(actionsDiv);
    }
    
    chatWindow.appendChild(div);
    // Re-append loader to ensure it stays at the bottom during activity
    if (loader.classList.contains('active')) {
        chatWindow.appendChild(loader);
    }
    chatWindow.scrollTop = chatWindow.scrollHeight;
}