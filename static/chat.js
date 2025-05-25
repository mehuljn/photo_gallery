document.addEventListener('DOMContentLoaded', () => {
    const chatBubble = document.getElementById('chat-bubble');
    const chatOverlay = document.getElementById('chat-overlay');
    const closeChat = document.getElementById('close-chat');
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');

    chatBubble.addEventListener('click', () => {
        chatOverlay.classList.remove('hidden');
        userInput.focus(); // Focus on input when chat opens
    });

    closeChat.addEventListener('click', () => {
        chatOverlay.classList.add('hidden');
    });

    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    async function sendMessage() {
        const message = userInput.value.trim();
        if (message === '') return;

        addMessage(message, 'user-message');
        userInput.value = '';
        chatMessages.scrollTop = chatMessages.scrollHeight; // Scroll to bottom

        // Add a typing indicator
        const typingIndicator = addMessage('...', 'bot-message typing-indicator');
        chatMessages.scrollTop = chatMessages.scrollHeight;

        try {
            const imageData = await getSnapshot();
            await sendToLLM(message, imageData, typingIndicator);
        } catch (error) {
            console.error('Error sending message or taking snapshot:', error);
            removeMessage(typingIndicator); // Remove typing indicator on error
            addMessage('Error: Could not get a response. Please try again.', 'bot-message');
        }
    }

    function addMessage(text, className) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', className);
        messageDiv.textContent = text;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight; // Keep scrolling to bottom
        return messageDiv; // Return the created element for potential removal
    }

    function addMessage(text, className) {
        const messageDiv = document.createElement('div');
        // --- CHANGE THIS LINE ---
        // messageDiv.classList.add('message', className); // ORIGINAL LINE
        messageDiv.classList.add('message', ...className.split(' ')); // CORRECTED LINE
        // --- END CHANGE ---
        messageDiv.textContent = text;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight; // Keep scrolling to bottom
        return messageDiv; // Return the created element for potential removal
    }

    function removeMessage(element) {
        if (element && element.parentNode) {
            element.parentNode.removeChild(element);
        }
    }

    async function getSnapshot() {
        return new Promise((resolve, reject) => {
            html2canvas(document.body).then(canvas => {
                const imgData = canvas.toDataURL('image/jpeg', 0.8); // Get base64 JPEG
                resolve(imgData);
            }).catch(error => {
                console.error('html2canvas error:', error);
                reject(error);
            });
        });
    }

    async function sendToLLM(text, imageData, typingIndicatorElement) {
        try {
            const response = await fetch('/chat_with_llm', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    query: text,
                    image: imageData // Base64 image data
                }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(`Server error: ${response.status} ${response.statusText} - ${errorData.error || 'Unknown error'}`);
            }

            const data = await response.json();
            removeMessage(typingIndicatorElement); // Remove typing indicator
            addMessage(data.response, 'bot-message');
            chatMessages.scrollTop = chatMessages.scrollHeight; // Scroll to bottom
        } catch (error) {
            console.error('Error sending to LLM:', error);
            removeMessage(typingIndicatorElement); // Remove typing indicator on error
            addMessage('Error: Could not connect to the AI assistant.', 'bot-message');
        }
    }
});
