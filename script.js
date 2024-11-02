document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('diabetesForm');
    const resultDiv = document.getElementById('result');

    form.addEventListener('submit', (event) => {
        event.preventDefault();

        // Collect form data
        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => (data[key] = value));

        // Send data to backend
        fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            resultDiv.innerHTML = `
                <p>Prediction: ${result.prediction === 1 ? 'Diabetic' : 'Not Diabetic'}</p>
                <p>Probability of Diabetes: ${result.probability.toFixed(2)}%</p>
            `;
        })
        .catch(error => {
            resultDiv.innerHTML = '<p>An error occurred during prediction.</p>';
            console.error('Error:', error);
        });
    });
});
