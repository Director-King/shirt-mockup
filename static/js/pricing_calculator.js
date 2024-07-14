document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('pricingForm');
    const printingType = document.getElementById('printingType');
    const digitalOptions = document.getElementById('digitalOptions');
    const noCutOptions = document.getElementById('noCutOptions');
    const resultDiv = document.getElementById('result');
    const totalPriceSpan = document.getElementById('totalPrice');
    const createMockupBtn = document.getElementById('createMockupBtn');

    printingType.addEventListener('change', function() {
        if (this.value === 'digital') {
            digitalOptions.style.display = 'block';
            noCutOptions.style.display = 'none';
            createMockupBtn.style.display = 'none';
        } else {
            digitalOptions.style.display = 'none';
            noCutOptions.style.display = 'block';
            createMockupBtn.style.display = 'inline-block';
        }
    });

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(form);

        fetch('/pricing', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            totalPriceSpan.textContent = data.price.toFixed(2);
            resultDiv.style.display = 'block';
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while calculating the price. Please try again.');
        });
    });

    // Initialize the button visibility based on the initial selection
    if (printingType.value === 'no_cut') {
        createMockupBtn.style.display = 'inline-block';
    } else {
        createMockupBtn.style.display = 'none';
    }
});