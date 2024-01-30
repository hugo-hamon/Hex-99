async function display_board() {
    var game_container = document.getElementById("game_container");

    var board = await eel.eel_get_board()();
}

const canvas = document.getElementById('hexagon_canvas');
const ctx = canvas.getContext('2d');
const a = Math.PI / 3;
const r = 30;


function draw_hexagon(x, y, x_idx, y_idx, col_number, row_number) {
    ctx.beginPath();
    for (var i = 0; i < 6; i++) {
        ctx.lineTo(x + r * Math.cos(a * i + a / 2), y + r * Math.sin(a * i + a / 2));
    }
    ctx.closePath();
    ctx.strokeStyle = 'white';
    ctx.lineWidth = 3;
    ctx.stroke();
    if (x_idx == 0) {
        console.log("left", x + r * Math.cos(a * 2 + a / 2));
        ctx.beginPath();
        ctx.lineTo(x + r * Math.cos(a * 3 + a / 2), y + r * Math.sin(a * 3 + a / 2));
        ctx.lineTo(x + r * Math.cos(a * 4 + a / 2), y + r * Math.sin(a * 4 + a / 2));
        ctx.lineTo(x + r * Math.cos(a * 5 + a / 2), y + r * Math.sin(a * 5 + a / 2));
        ctx.strokeStyle = 'red';
        ctx.lineWidth = 3;
        ctx.stroke();
    }
    if (x_idx == row_number - 1) {
        console.log("right", x + r * Math.cos(a * 0 + a / 2));
        ctx.beginPath();
        ctx.lineTo(x + r * Math.cos(a * 0 + a / 2), y + r * Math.sin(a * 0 + a / 2));
        ctx.lineTo(x + r * Math.cos(a * 1 + a / 2), y + r * Math.sin(a * 1 + a / 2));
        ctx.lineTo(x + r * Math.cos(a * 2 + a / 2), y + r * Math.sin(a * 2 + a / 2));
        ctx.strokeStyle = 'red';
        ctx.lineWidth = 3;
        ctx.stroke();
    }
    if (y_idx == 0) {
        console.log("top", y + r * Math.sin(a * 4 + a / 2));
        ctx.beginPath();
        if (x_idx != row_number - 1) {
            ctx.lineTo(x + r * Math.cos(a * 1 + a / 2), y + r * Math.sin(a * 1 + a / 2));
        }
        ctx.lineTo(x + r * Math.cos(a * 2 + a / 2), y + r * Math.sin(a * 2 + a / 2));
        ctx.lineTo(x + r * Math.cos(a * 3 + a / 2), y + r * Math.sin(a * 3 + a / 2));
        ctx.strokeStyle = 'blue';
        ctx.lineWidth = 3;
        ctx.stroke();
    }
    if (y_idx == col_number - 1) {
        console.log("bottom", y + r * Math.sin(a * 0 + a / 2));
        ctx.beginPath();
        if (x_idx != 0) {
            ctx.lineTo(x + r * Math.cos(a * 4 + a / 2), y + r * Math.sin(a * 4 + a / 2));
        }
        ctx.lineTo(x + r * Math.cos(a * 5 + a / 2), y + r * Math.sin(a * 5 + a / 2));
        ctx.lineTo(x + r * Math.cos(a * 0 + a / 2), y + r * Math.sin(a * 0 + a / 2));
        ctx.strokeStyle = 'blue';
        ctx.lineWidth = 3;
        ctx.stroke();
    }
}

function get_coordinates(x, y) {
    let row = Math.floor(y / (r * 1.5));
    let col = Math.floor(x / (r * Math.sqrt(3)));

    let loss_h = Math.sqrt(r ** 2 - (r / 2) ** 2);
    let loss_w = Math.sqrt((2 * r) ** 2 - r ** 2);

    let x_offset = x - (col * r * Math.sqrt(3));
    let y_offset = y - (row * r * 1.5);

    let x_idx = Math.floor(x_offset / loss_w);
    let y_idx = Math.floor(y_offset / loss_h);

    console.log("x: " + x + " y: " + y);
    console.log("row: " + row + " col: " + col);
    console.log("x_idx: " + x_idx + " y_idx: " + y_idx);

    return [row, col, x_idx, y_idx];
}

function draw_grid(row_number, col_number) {
    let s = Math.sqrt((2 * r) ** 2 - r ** 2);
    let loss_h = Math.sqrt(r ** 2 - (s / 2) ** 2);

    let apothem = r * Math.sqrt(3) / 2;
    console.log(apothem);


    canvas.width = 2 * apothem * row_number + r + apothem * (col_number - 1)
    canvas.height = 2 * r * col_number - ((col_number - 1) * (loss_h - 1));

    let width = r * Math.sqrt(3) * row_number;
    let height = r * 1.5 * col_number;

    // clear the canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    let i = 0;
    for (var y = r; y < height; y += r * 1.5) {
        let j = 0;
        for (var x = r; x < width; x += r * Math.sqrt(3)) {
            draw_hexagon(x + y * Math.sqrt(3) / 3, y, i, j, row_number, col_number);
            j++;
        }
        i++;
    }
}

let row_number = 10;
let col_number = 10;

let row_size = r * Math.sqrt(3) * 15;
let col_size = r * 1.5 * 15;

draw_grid(row_number, col_number);