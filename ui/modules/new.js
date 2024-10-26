let current_modules = {};
let moduleName = document.querySelector('.moduleNameEditor');

fetch('/api/modules').then(function (response) {
    if (response.ok) {
        return response.json();
    }
}).then((json) => {
    current_modules = json;
});

let module_data = {
    'command': moduleName.value,
    'type': typeSelect.value
};

function setRandomName() {
    fetch(`https://www.uuidgenerator.net/api/version7`).then(function (response) {
        return response.text();
    }).then(function (data) {
        const names = data.split('-');
        module_data.command = names[Math.floor(Math.random() * names.length)];
    });
}

function updateData() {
    const selectedModule = moduleName.value;

    module_data.type = typeSelect.value;

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
                color: document.getElementById('embedColor').value.trim(),
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

    if (selectedModule.trim() === '') {
        setRandomName();
    }

    if (!('!' + selectedModule in current_modules)) {
        module_data.command = selectedModule;
    } else {
        setRandomName();
    }
}

function save() {
    fetch('/api/newmodule', {
        method: 'POST',
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

setInterval(updateData, 500);
