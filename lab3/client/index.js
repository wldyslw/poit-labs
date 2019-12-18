const commandInput = document.getElementById('command');
const messagesBlock = document.getElementById('messages');

const updateMessages = () => {};

document.getElementById('send').addEventListener('click', () => {
    const [command, ...meta] = commandInput.value.split(' ');
    fetch(`http://localhost:9000`, {
        method: 'POST',
        body: JSON.stringify({
            command,
            meta: meta ? meta.join(' ') : ''
        })
    })
        .then(res => res.json())
        .then(res => {
            const message = document.createElement('p');
            message.innerHTML = `${new Date().toLocaleString('be-BY')} ${res.message}`;
            messagesBlock.prepend(message);
        });
});