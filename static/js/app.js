
    document.addEventListener('DOMContentLoaded', () => {
        const forms = document.querySelectorAll('form');

        forms.forEach((form, index) => {
            form.addEventListener('submit', (event) => {
                event.preventDefault(); // Prevent default form submission
                console.log(`Form ${index + 1} submitted.`);

            });
        });
    });

