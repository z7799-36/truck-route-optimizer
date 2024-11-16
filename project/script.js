let points = [];  //array to save pints

// add point to array and draw it
function addPoint(x, y) {
    points.push([x, y]);
    drawPoints();
}

//function to send points to server and calculate the perfect path
function calculateOptimalRoute() {
    fetch('http://localhost:3000/optimize-route', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ points })
    })
    .then(response => response.json())
    .then(data => {
        if (data.optimalRoute) {
            console.log("Received optimal route:", data.optimalRoute);  // print the perfect path
            drawRoute(data.optimalRoute);
        } else {
            alert("لم يتم العثور على مسار أمثل.");
        }
    })
    .catch(error => console.error('Error:', error));
}
// function to draw points in convas
function drawPoints() {
    const canvas = document.getElementById("canvas");
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);  // مسح اللوحة

    points.forEach(([x, y], index) => {
        ctx.beginPath();
        ctx.arc(x, y, 5, 0, Math.PI * 2);
        ctx.fillStyle = "blue";
        ctx.fill();
        ctx.fillText(index + 1, x + 8, y - 8);
    });
}

// function to draw the perfect path
function drawRoute(route) {
    const canvas = document.getElementById("canvas");
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    drawPoints();  // redraw the points

    if (route.length > 1) {
        ctx.beginPath();
        ctx.moveTo(route[0][0], route[0][1]);

        // draw lines between points in path
        for (let i = 1; i < route.length; i++) {
            ctx.lineTo(route[i][0], route[i][1]);
        }

        // close the path in first point
        ctx.lineTo(route[0][0], route[0][1]);

        ctx.strokeStyle = "red";
        ctx.lineWidth = 2;
        ctx.stroke();
    } else {
        alert("المسار يحتوي على نقطة واحدة فقط، يرجى إضافة المزيد من النقاط.");
    }
}

// add points when touch the convas
document.getElementById("canvas").addEventListener("click", (event) => {
    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    addPoint(x, y);
});

// call function in buttom
document.getElementById("calculateButton").addEventListener("click", calculateOptimalRoute);
