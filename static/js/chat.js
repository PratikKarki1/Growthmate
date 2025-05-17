function toggleChatModal() {
    const modal = document.getElementById('chat-modal');
    const isHidden = modal.classList.contains('hidden');

    if (isHidden) {
        modal.classList.remove('hidden');
        document.getElementById('message-input')?.focus();
    } else {
        modal.classList.add('hidden');
    }
}

function setMessage(text) {
    const input = document.getElementById('message-input');
    input.value = text;
    input.focus();
    document.getElementById('chat-form').dispatchEvent(new Event('submit'));
}

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('chat-form');
    const messagesContainer = document.getElementById('messages');

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        const messageInput = document.getElementById('message-input');
        const message = messageInput.value.trim();

        if (!message) {
            return;
        }

        const currentTime = new Date().toLocaleTimeString('en-US', {
            hour: 'numeric',
            minute: '2-digit',
            hour12: true
        });

        // Add user message
        const userMessageHtml = `
            <div class="flex justify-end gap-2.5">
                <div class="bg-blue-500 rounded-lg p-3 max-w-[80%]">
                    <p class="text-sm text-white">${message}</p>
                    <span class="text-xs text-blue-100 mt-1">${currentTime}</span>
                </div>
            </div>
        `;
        messagesContainer.insertAdjacentHTML('beforeend', userMessageHtml);

        // Clear input
        messageInput.value = '';

        // Show loading
        const loadingHtml = `
            <div id="loading-message" class="flex items-start gap-2.5">
                <div class="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center">
                    <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                            d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-4l-4 4z" />
                    </svg>
                </div>
                <div class="bg-gray-100 rounded-lg p-3 max-w-[80%]">
                    <p class="text-sm text-gray-900">Thinking...</p>
                </div>
            </div>
        `;
        messagesContainer.insertAdjacentHTML('beforeend', loadingHtml);

        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;

        // Submit form
        const formData = new FormData();
        formData.append('message', message);
        formData.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]').value);

        fetch('/send-message/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
            .then(response => {
                if (response.status === 401) {
                    // Redirect to login or show a message
                    window.location.href = '/login/';
                    throw new Error('You must be logged in to use the chat. Redirecting to login...');
                }
                if (!response.ok) {
                    if (response.status === 400) {
                        return response.json().then(data => {
                            throw new Error(data.error || 'Invalid message format');
                        });
                    }
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Remove loading
                const loadingMessage = document.getElementById('loading-message');
                if (loadingMessage) {
                    loadingMessage.remove();
                }

                if (data.error) {
                    throw new Error(data.error);
                }

                // Add bot response
                const botMessageHtml = `
                    <div class="flex items-start gap-2.5">
                        <div class="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center">
                            <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                                    d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-4l-4 4z" />
                            </svg>
                        </div>
                        <div class="bg-gray-100 rounded-lg p-3 max-w-[80%]">
                            <p class="text-sm text-gray-900">${data.bot_message.message}</p>
                            <span class="text-xs text-gray-500 mt-1">${currentTime}</span>
                        </div>
                    </div>
                `;
                messagesContainer.insertAdjacentHTML('beforeend', botMessageHtml);

                // Scroll to bottom
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            })
            .catch(error => {
                console.error('Error:', error);
                // Remove loading
                const loadingMessage = document.getElementById('loading-message');
                if (loadingMessage) {
                    loadingMessage.remove();
                }

                // Show error
                const errorHtml = `
                    <div class="flex items-start gap-2.5">
                        <div class="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center">
                            <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                                    d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-4l-4 4z" />
                            </svg>
                        </div>
                        <div class="bg-red-50 rounded-lg p-3 max-w-[80%]">
                            <p class="text-sm text-red-500">${error.message || 'Sorry, there was an error processing your message. Please try again.'}</p>
                            <span class="text-xs text-red-400 mt-1">${currentTime}</span>
                        </div>
                    </div>
                `;
                messagesContainer.insertAdjacentHTML('beforeend', errorHtml);

                // Scroll to bottom
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            });
    });

    // Initial scroll to bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;

    // Close modal when clicking outside
    document.addEventListener('click', function (e) {
        const modal = document.getElementById('chat-modal');
        const modalContent = modal.querySelector('.bg-white');
        const toggleBtn = document.getElementById('chat-toggle-btn');

        if (!modal.classList.contains('hidden') &&
            !modalContent.contains(e.target) &&
            !toggleBtn.contains(e.target)) {
            toggleChatModal();
        }
    });

    // Prevent closing when clicking inside modal
    document.getElementById('chat-modal').addEventListener('click', function (e) {
        if (e.target === this) {
            e.stopPropagation();
        }
    });
}); 