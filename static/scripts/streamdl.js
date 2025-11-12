document.addEventListener('DOMContentLoaded', function() {
    const toggle = document.getElementById('download-toggle');
    const sliderLabel = document.getElementById('slider-label');
    const playButtons = document.querySelectorAll('.play-button');

    toggle.addEventListener('change', function() {
        if (this.checked) {
            sliderLabel.textContent = 'Download';
            playButtons.forEach(button => {
                const id = button.getAttribute('data-id');
                button.href = `/movies_play/${id}?stream=false`;
            });
        } else {
            sliderLabel.textContent = 'Stream';
            playButtons.forEach(button => {
                const id = button.getAttribute('data-id');
                button.href = `/movies_play/${id}?stream=true`;
            });
        }
    });
});
