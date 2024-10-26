fetch('/api/modules').then(function (response) {
    if (response.ok) {
        return response.json();
    } else {
        throw Error(response.statusText);
    }
}).then(json => {
    document.getElementById("moduleCount_92cef12").innerText = 'There are currently ' + Object.keys(json).length + '  modules installed.'

    let modulesList = document.getElementById('moduleslist');
    let html = ''

    Object.keys(json).forEach(key => {
        html += `<div class="mod"><a onclick="window.location.href = '/modules/edit.html#${key}'" class="module">${key} - ${json[key]['type']}</a> <a onclick="if (window.confirm('Do you really want to delete: `+ key.replace('!', '') +`?')) { del('${key.replace('!', '')}'); }" class="delModule">DELETE</a></div>`
    });

    modulesList.innerHTML = html;
})


const loadingTextElement = document.getElementById("loadingText");
let dotCount = 0;

function dot() {
    let dots = '';

    for (let i = 0; i < dotCount; i++) {
        dots += '.';
    }

    loadingTextElement.innerText = 'Loading' + dots;

    dotCount = (dotCount + 1) % 4;
}

function del(key) {
    fetch('/api/delmod?m='+key, {
        method: 'DELETE',
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            window.location.href = '/redirect.html#/home.html&1000';
        })
}

setInterval(dot, 500);
dot()

setTimeout(() => {
    document.querySelector('.fader').remove();
}, 4000);

document.querySelector('.createModule').addEventListener('click', (e) => {
    window.location.href = '/modules/new.html';
})