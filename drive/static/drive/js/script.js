document.addEventListener('DOMContentLoaded', function() {
    let form = document.querySelector('form');
    let span = document.querySelector('span');

    class DriveUploadProducer extends UploadProducer {
        close() {
            span.textContent = '';
        }

        serverReport(progress) {
            span.textContent = progress + '%';
        }
    }

    DriveUploadProducer.bind('drive/upload', form);


    let log = document.querySelector('.log');
    let input = document.querySelector('.input');

    class ChatProducer extends Producer {
        append(content) {
            log.textContent += content + '\n';
        }

        serverSignal(name) {
            this.append(name.toUpperCase());
        }

        serverPost(content) {
            this.append(content);
        }
    }

    let producer = new ChatProducer('drive/chat');

    input.addEventListener('keydown', function(event) {
        if (event.code == 'Enter' && input.value != '') {
            producer.sendServer('post', input.value);
            input.value = '';
        }
    });

    input.focus();
});
