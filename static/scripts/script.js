const toggleBtn = document.querySelector('.toggle_btn');
const navbar = document.querySelector('.navbar');
const profile = document.getElementById("profile");

toggleBtn.addEventListener('click', function() {
    navbar.classList.toggle('open');
});

document.getElementById('runTestBtn').addEventListener('click', function() {
    const loadingMessage = document.getElementById('loadingMessage');
    loadingMessage.textContent = 'Loading...';

    fetch('/run_test', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            loadingMessage.textContent = '';  // Clear loading message

            // Display the result in the resultContainer
            const resultContainer = document.getElementById('resultContainer');
            resultContainer.innerHTML = `<p>${data.result}</p>`;
        })
        .catch(error => {
            console.error('Error:', error);
            loadingMessage.textContent = 'Error occurred. Please try again.';
        });
});

// Function to fetch outputs initially and then every 5 seconds
function fetchOutputs() {
    fetch('/get_outputs')
        .then(response => response.json())
        .then(outputs => {
            const outputsList = document.getElementById('outputsList');
            outputsList.innerHTML = ''; // Clear previous outputs

            outputs.forEach(output => {
                const li = document.createElement('li');
                li.textContent = output;
                outputsList.appendChild(li);
            });
        })
        .catch(error => {
            console.error('Error fetching outputs:', error);
        });
}

// Fetch outputs initially and then every 5 seconds
fetchOutputs();
setInterval(fetchOutputs, 5000); // Fetch every 5 seconds

// Speaker button click event
document.getElementById('speakTheResult').addEventListener('click', function() {
    const resultText = document.getElementById('resultContainer').textContent.trim();
    
    if (resultText) {
        fetch('/speak', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: resultText })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Text-to-speech request successful:', data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    } else {
        console.log('No result text to speak.');
    }
});
