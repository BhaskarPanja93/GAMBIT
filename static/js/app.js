document.addEventListener('DOMContentLoaded', () => {
    const options = document.querySelectorAll('[id^="option"]');
    options.forEach((option, index) => {
        option.addEventListener('click', (event) => {
            document.getElementById('op' + index).checked = true;
            console.log(`Option ${index + 1} clicked`);//for debugging only
            document.getElementById('quiz-form').submit();
        });
    });
});
