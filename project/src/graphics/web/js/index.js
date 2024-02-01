class HexagonGame {

    constructor(rowNumber, colNumber, radius) {
        this.rowNumber = rowNumber;
        this.colNumber = colNumber;
        this.radius = radius;
        this.over = false;
        this.offset = this.radius;
        this.centers = this.calculateCenters();

        this.canvas = document.getElementById('hexagon_canvas');
        this.ctx = this.canvas.getContext('2d');
        this.setCanvasSize();

        this.canvas.addEventListener('click', this.handleClick.bind(this), false);
        this.updateInterval = setInterval(this.update.bind(this), 100);
    }

    // REQUEST
    getCoordinates(x, y) {
        let minDist = this.radius;
        let minRow = 0;
        let minCol = 0;

        for (let i = 0; i < this.centers.length; i++) {
            for (let j = 0; j < this.centers[i].length; j++) {
                const dist = Math.sqrt((x - this.centers[i][j][0]) ** 2 + (y - this.centers[i][j][1]) ** 2);
                if (dist < minDist) {
                    minDist = dist;
                    minRow = i;
                    minCol = j;
                }
            }
        }

        return minDist < this.radius * 0.8 ? [minRow, minCol] : [-1, -1];
    }

    // COMMANDS
    drawHexagon(x, y) {
        const a = Math.PI / 3;

        this.ctx.beginPath();
        for (let i = 0; i < 6; i++) {
            const angle = a * i + a / 2;
            this.ctx.lineTo(x + this.radius * Math.cos(angle), y + this.radius * Math.sin(angle));
        }
        this.ctx.closePath();
        this.ctx.strokeStyle = 'white';
        this.ctx.lineWidth = 3;
        this.ctx.stroke();
    }

    drawBoard() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        for (let i = 0; i < this.rowNumber; i++) {
            // Draw row number
            this.ctx.font = "1.5em Poppins";
            this.ctx.fillStyle = "white";
            this.ctx.fillText(i + 1, this.centers[i][0][0] - this.radius * 2, this.centers[i][0][1] + 10);
            for (let j = 0; j < this.colNumber; j++) {
                // Draw col number
                if (i == 0) {
                    this.ctx.font = "1.5em Poppins";
                    this.ctx.fillStyle = "white";
                    // Letter A is 65 in ASCII
                    this.ctx.fillText(String.fromCharCode(65 + j), this.centers[i][j][0] - this.radius, this.centers[i][j][1] - this.radius * 1.5);
                }

                this.drawHexagon(this.centers[i][j][0], this.centers[i][j][1]);
            }
        }
        this.drawHexSide();
    }

    drawHexSide() {
        const a = Math.PI / 3;

        const drawHexSide = (x, y, startAngle, midAngle, endAngle, color) => {
            this.ctx.lineTo(x + this.radius * Math.cos(startAngle), y + this.radius * Math.sin(startAngle));
            this.ctx.lineTo(x + this.radius * Math.cos(midAngle), y + this.radius * Math.sin(midAngle));
            this.ctx.lineTo(x + this.radius * Math.cos(endAngle), y + this.radius * Math.sin(endAngle));
            this.ctx.strokeStyle = color;
            this.ctx.lineWidth = 3;
            this.ctx.stroke();
        };

        this.ctx.beginPath();
        for (let j = 0; j < this.colNumber; j++) {
            let x = this.centers[0][j][0];
            let y = this.centers[0][j][1];

            drawHexSide(x, y, a * 3 + a / 2, a * 4 + a / 2, a * 5 + a / 2, 'red');
        }

        this.ctx.beginPath();
        for (let i = 0; i < this.rowNumber; i++) {
            let x = this.centers[i][this.colNumber - 1][0];
            let y = this.centers[i][this.colNumber - 1][1];

            drawHexSide(x, y, a * 4 + a / 2, a * 5 + a / 2, a * 0 + a / 2, 'blue');
        }

        this.ctx.beginPath();
        for (let j = this.colNumber - 1; j >= 0; j--) {
            let x = this.centers[this.rowNumber - 1][j][0];
            let y = this.centers[this.rowNumber - 1][j][1];

            drawHexSide(x, y, a * 0 + a / 2, a * 1 + a / 2, a * 2 + a / 2, 'red');
        }

        this.ctx.beginPath();
        for (let i = this.rowNumber - 1; i >= 0; i--) {
            let x = this.centers[i][0][0];
            let y = this.centers[i][0][1];

            drawHexSide(x, y, a * 1 + a / 2, a * 2 + a / 2, a * 3 + a / 2, 'blue');
        }

    }

    setCanvasSize() {
        let s = Math.sqrt((2 * this.radius) ** 2 - this.radius ** 2);
        let lossH = Math.sqrt(this.radius ** 2 - (s / 2) ** 2);

        let apothem = this.radius * Math.sqrt(3) / 2;

        this.canvas.width = 2 * apothem * this.colNumber + this.radius + apothem * (this.rowNumber - 1) + this.offset + this.radius;
        this.canvas.height = 2 * this.radius * this.rowNumber - ((this.rowNumber - 1) * (lossH - 1)) + this.offset * 1.5;
    }

    drawCircle(row, col, color) {
        this.ctx.beginPath();
        // Border
        this.ctx.arc(this.centers[row][col][0], this.centers[row][col][1], this.radius * 0.4, 0, 2 * Math.PI);
        this.ctx.fillStyle = color;
        this.ctx.fill();
        this.ctx.strokeStyle = color;
        this.ctx.lineWidth = 3;
        this.ctx.stroke();
    }

    // UTILS
    calculateCenters() {
        const centers = new Array(this.rowNumber);
        for (let i = 0; i < this.rowNumber; i++) {
            centers[i] = new Array(this.colNumber);
        }

        let y = this.radius + this.offset * 1.5;
        for (let i = 0; i < this.rowNumber; i++) {
            let x = this.radius + this.offset;
            for (let j = 0; j < this.colNumber; j++) {
                centers[i][j] = [x + y * Math.sqrt(3) / 3, y];
                x += this.radius * Math.sqrt(3);
            }
            y += this.radius * 1.5;
        }
        return centers;
    }

    async checkGameOver() {
        if (this.over) {
            return true;
        } else {
            this.over = await eel.eel_is_game_over()();
        }
        return this.over;
    }

    async handleClick(event) {
        if (await this.checkGameOver()) {
            console.log("Game Over");
            return;
        }

        let main = document.getElementsByClassName("main");

        let x = event.pageX - this.canvas.offsetLeft;
        let y = event.pageY - this.canvas.offsetTop - main[0].offsetTop;

        let [row, col] = this.getCoordinates(x, y);
        if (row == -1 || col == -1) {
            return;
        }

        var current_player = await eel.eel_get_current_player()();

        eel.eel_set_player_move(current_player, row, col)();
        eel.eel_update_game()();

        displayBoard(this);
    }

    // update function update every 1s
    async update() {
        if (await this.checkGameOver()) {
            swal("Game Over", await eel.eel_get_winner()() + " wins!", "success");
            clearInterval(this.updateInterval);
            return;
        }
        var current_player = await eel.eel_is_current_player_human()();
        if (current_player == false) {
            eel.eel_update_game()();
            displayBoard(this);
        }
    }
}

async function displayBoard(hexagonGame) {
    var board = await eel.eel_get_board()();
    hexagonGame.drawBoard();

    // Time test
    
    for (let i = 0; i < board.length; i++) {
        for (let j = 0; j < board[0].length; j++) {
            if (board[i][j] === 1) {
                hexagonGame.drawCircle(i, j, 'red');
            }
            else if (board[i][j] === 2) {
                hexagonGame.drawCircle(i, j, 'blue');
            }
        }
    }
}

async function main() {
    var hexagonRadius = 30;
    var board = await eel.eel_get_board()();

    const hexagonGame = new HexagonGame(board.length, board[0].length, hexagonRadius);

    displayBoard(hexagonGame);
}

main();