function checkcamera(){
    const video = document.getElementById('video');
        const socket = io();

        navigator.mediaDevices.getUserMedia({ video: true })
            .then(stream => {
                document.getElementById('startQuizBtn').style.display = 'block';
                video.srcObject = stream;
                video.play();
                const canvas = document.createElement('canvas');
                const context = canvas.getContext('2d');
                canvas.width = video.width;
                canvas.height = video.height;
                // setInterval(() => {
                //     context.drawImage(video, 0, 0, video.width, video.height);
                //     const frame = canvas.toDataURL('image/jpeg');
                //     socket.emit('frame', frame);
                // }, 33); // 30 fps
            })
            .catch(error => {
                console.error(error);
            });

       
}

 // socket.on('processed_frame', processedFrame => {
        //     // Do something with the processed frame
        //     // For example, you could display it on a canvas element
        //     const canvas = document.createElement('canvas');
        //     const context = canvas.getContext('2d');
        //     const image = new Image();
        //     image.onload = () => {
        //         canvas.width = image.width;
        //         canvas.height = image.height;
        //         context.drawImage(image, 0, 0);
        //         document.body.appendChild(canvas);
        //     };
        //     image.src = processedFrame;
        // });

function detection(){
    const video = document.getElementById('quizvid');
        const socket = io();

        navigator.mediaDevices.getUserMedia({ video: true })
            .then(stream => {
                // document.getElementById('startQuizBtn').style.display = 'block';
                video.srcObject = stream;
                video.play();
                const canvas = document.createElement('canvas');
                const context = canvas.getContext('2d');
                canvas.width = video.width;
                canvas.height = video.height;
                // setInterval(() => {
                //     context.drawImage(video, 0, 0, video.width, video.height);
                //     const frame = canvas.toDataURL('image/jpeg');
                //     socket.emit('frame', frame);
                // }, 33); // 30 fps
            })
            .catch(error => {
                console.error(error);
            });

        // socket.on('processed_frame', processedFrame => {
        //     // Do something with the processed frame
        //     // For example, you could display it on a canvas element
        //     const canvas = document.createElement('canvas');
        //     const context = canvas.getContext('2d');
        //     const image = new Image();
        //     image.onload = () => {
        //         canvas.width = image.width;
        //         canvas.height = image.height;
        //         context.drawImage(image, 0, 0);
        //         document.body.appendChild(canvas);
        //     };
        //     image.src = processedFrame;
        // });
}