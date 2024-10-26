let current_modules = {};

fetch('/api/modules').then(function (response) {
    if (response.ok) {
        return response.json();
    }
}).then((json) => {
    current_modules = json;
});

function decimalToHex(decimal) {
    return '#' + decimal.toString(16).padStart(6, '0'); // Ensures at least 6 characters
}

let module_data = {};

function updateData() {
    module_data.type = typeSelect.value

    if (module_data.type === 'reply') {
        module_data.replyContent = {
            message: document.getElementById('Text1_83jh8f1').value
        };

        if (module_data.replyContent.message.trim() === '') {
            delete module_data.replyContent.message;
        }

        const toggleEmbed = document.getElementById('toggleEmbed');

        if (toggleEmbed.checked) {
            module_data.replyContent.embed = {
                title: document.getElementById('embedTitle').value.trim(),
                description: document.getElementById('embedDescription').value.trim(),
                color: document.getElementById('embedColor').value.trim()
            };

            // Remove keys with empty or whitespace-only values
            for (let key in module_data.replyContent.embed) {
                if (module_data.replyContent.embed[key] === '') {
                    delete module_data.replyContent.embed[key];
                }
            }
        } else {
            delete module_data.replyContent.embed; // Remove the embed key if not checked
        }
    }
}

function save() {
    fetch('/api/updatemodule', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(module_data)
    })
        .then(function (response) {
            window.location.href = '/home.html';
        })
        .catch(error => console.error('Error:', error));
}

function load() {
    fetch('/api/getmod?m=' + window.location.hash.replace('#', '').replace('!', ''))
        .then(response => response.json())
        .then(json => {
            module_data = json;

            typeSelect.value = json.type || '';

            if (json.type === 'reply') {
                if (json.replyContent) {
                    if (json.replyContent.message) {
                        document.getElementById('Text1_83jh8f1').value = json.replyContent.message;
                    }

                    if (json.replyContent.embed) {
                        document.getElementById('embedTitle').value = json.replyContent.embed.title || '';
                        document.getElementById('embedDescription').value = json.replyContent.embed.description || '';
                        document.getElementById('embedColor').value = decimalToHex(json.replyContent.embed.color) || '';

                        document.getElementById('toggleEmbed').checked = true;
                        toggleEmbedSection()
                    } else {
                        document.getElementById('toggleEmbed').checked = false;
                    }
                }
            }
        })
        .catch(error => console.error('Error loading module:', error));
}
load()
setInterval(updateData, 500);