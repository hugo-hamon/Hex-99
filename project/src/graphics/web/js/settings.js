async function loadConfigFromFile(event) {
    const file = event.target.files[0];
    if (!file) {
        return;
    }
    
    const filePath = file.name;

    try {
        await eel.eel_load_config_from_file(filePath)();
        Swal.fire({
            title: 'Success!',
            text: 'Configuration loaded successfully!',
            icon: 'success',
            confirmButtonText: 'OK'
        });
    } catch (error) {
        console.error("Error loading configuration:", error);
        Swal.fire({
            title: 'Error!',
            text: 'There was an error loading the configuration.',
            icon: 'error',
            confirmButtonText: 'OK'
        });
    }
}

async function saveConfig() {
    const config = {
        user: {
            player1_algorithm: document.getElementById('player1_algorithm').value,
            player1_depth: parseInt(document.getElementById('player1_depth').value, 10),
            player2_algorithm: document.getElementById('player2_algorithm').value,
            player2_depth: parseInt(document.getElementById('player2_depth').value, 10)
        },
        game: {
            board_width: parseInt(document.getElementById('board_width').value, 10),
            board_height: parseInt(document.getElementById('board_height').value, 10)
        }
    };

    const { value: fileName } = await Swal.fire({
        title: 'Enter file name',
        input: 'text',
        inputLabel: 'File name',
        inputPlaceholder: 'Enter the file name without extension',
        showCancelButton: true,
        inputValidator: (value) => {
            if (!value) {
                return 'You need to enter a file name!'
            }
        }
    });

    if (fileName) {
        try {
            await eel.eel_save_config(config, fileName)();
            Swal.fire({
                title: 'Success!',
                text: 'Configuration saved successfully!',
                icon: 'success',
                confirmButtonText: 'OK'
            });
        } catch (error) {
            console.error("Error saving configuration:", error);
            Swal.fire({
                title: 'Error!',
                text: 'There was an error saving the configuration.',
                icon: 'error',
                confirmButtonText: 'OK'
            });
        }
    }
}