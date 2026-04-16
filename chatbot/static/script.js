 const chatWindow = document.getElementById('chat-window');

const chatInput = document.getElementById('chat-input');

const loader = document.getElementById('loader');

const micBtn = document.getElementById('mic-btn'); 


let mediaRecorder; 

let audioChunks = []; 

let isRecording = false; 


// EXISTING: sendMessage function

async function sendMessage() {

const text = chatInput.value.trim();

if (!text) return;


appendMessage(text, 'user-msg');

chatInput.value = '';


chatWindow.appendChild(loader);

loader.classList.add('active');

chatWindow.scrollTop = chatWindow.scrollHeight;


try {

const response = await fetch('/chat', {

method: 'POST',

headers: { 'Content-Type': 'application/json' },

body: JSON.stringify({ query: text })

});

const data = await response.json();

loader.classList.remove('active');


if(data.error) {

appendMessage("Error: " + data.error, 'bot-msg');

} else {

appendMessage(data.answer, 'bot-msg');

}


} catch (error) {

loader.classList.remove('active');

appendMessage("Error reaching the assistant. Ensure the backend is running and data is loaded.", 'bot-msg');

}

}


// EXISTING: appendMessage function

function appendMessage(text, className) {

const div = document.createElement('div');

div.className = `message-bubble ${className}`;

div.innerText = text;

chatWindow.appendChild(div);

if (loader.classList.contains('active')) {

chatWindow.appendChild(loader);

}

chatWindow.scrollTop = chatWindow.scrollHeight;

}


// ==========================================

// NEW: Speech to Text Functionality

// ==========================================


async function toggleRecording() {

if (isRecording) {

stopRecording();

} else {

startRecording();

}

}


async function startRecording() {

try {

const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

mediaRecorder = new MediaRecorder(stream);

audioChunks = [];


mediaRecorder.addEventListener("dataavailable", event => {

audioChunks.push(event.data);

});


mediaRecorder.addEventListener("stop", async () => {

const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });

await transcribeAudio(audioBlob);

});


mediaRecorder.start();

isRecording = true;

micBtn.classList.add('recording');

chatInput.placeholder = "Listening... Click mic to stop.";

} catch (err) {

console.error("Error accessing microphone:", err);

alert("Please allow microphone access in your browser to use speech-to-text.");

}

}


function stopRecording() {

if (mediaRecorder && mediaRecorder.state !== "inactive") {

mediaRecorder.stop();

// Stop all tracks to release the microphone

mediaRecorder.stream.getTracks().forEach(track => track.stop());

}

isRecording = false;

micBtn.classList.remove('recording');

chatInput.placeholder = "Processing audio...";

}


async function transcribeAudio(audioBlob) {

const formData = new FormData();


formData.append("audio", audioBlob, "recording.webm");


try {


const response = await fetch('/transcribe-chunk', {

method: 'POST',

body: formData

});

const data = await response.json();

if (data.text && data.text !== "No speech detected.") {


const currentText = chatInput.value;

chatInput.value = currentText ? `${currentText} ${data.text}` : data.text;

}

} catch (error) {

console.error("Transcription error:", error);

alert("Failed to transcribe audio. Ensure the STT backend is running.");

} finally {

// Reset placeholder

chatInput.placeholder = "Ask anything about the website data...";

chatInput.focus();

}

} 