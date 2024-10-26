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
        html += `<a class="module">${key} - ${json[key]['type']}</a>`
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

setInterval(dot, 500);
dot()

setTimeout(() => {
    document.querySelector('.fader').remove();
}, 6000);
