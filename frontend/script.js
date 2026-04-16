const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

const ws = new WebSocket("ws://localhost:8765");

let finger = null;

let box = {
    x: 200,
    y: 150,
    size: 80,
    dragging: false
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    finger = data.finger;
};

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (finger) {
        let x = finger.x * canvas.width;
        let y = finger.y * canvas.height;

        ctx.beginPath();
        ctx.arc(x, y, 10, 0, Math.PI * 2);
        ctx.fillStyle = "red";
        ctx.fill();
    }

    requestAnimationFrame(draw);
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (finger) {
        let fx = finger.x * canvas.width;
        let fy = finger.y * canvas.height;

        // check if finger is inside the box
        if (
            fx > box.x &&
            fx < box.x + box.size &&
            fy > box.y &&
            fy < box.y + box.size
        ) {
            box.dragging = true;
        } else {
            box.dragging = false;
        }

        // move box if dragging
        if (box.dragging) {
            box.x = fx - box.size / 2;
            box.y = fy - box.size / 2;
        }

        // draw finger
        ctx.beginPath();
        ctx.arc(fx, fy, 10, 0, Math.PI * 2);
        ctx.fillStyle = "red";
        ctx.fill();
    }

    // draw box
    ctx.fillStyle = "blue";
    ctx.fillRect(box.x, box.y, box.size, box.size);

    requestAnimationFrame(draw);
}

draw();