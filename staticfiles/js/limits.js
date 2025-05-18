document.addEventListener('DOMContentLoaded', function() {
    // Format number with commas
    function formatNumber(number) {
        return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }

    // Function to create and update tooltip
    function createOrUpdateTooltip(slider, value) {
        let tooltip = slider.querySelector('.slider-tooltip');
        
        if (!tooltip) {
            tooltip = document.createElement('div');
            tooltip.className = 'slider-tooltip';
            slider.appendChild(tooltip);
        }
        
        tooltip.textContent = `PKR ${formatNumber(value)}`;
        
        // Position the tooltip
        const sliderRect = slider.getBoundingClientRect();
        const thumbPosition = ((value - slider.min) / (slider.max - slider.min)) * (sliderRect.width - 24); // 24 is thumb width
        tooltip.style.left = `${thumbPosition}px`;
    }

    // Function to handle slider input
    function handleSliderInput(slider, valueDisplay) {
        const value = slider.value;
        valueDisplay.textContent = formatNumber(value);
        createOrUpdateTooltip(slider.parentElement, value);
    }

    // Setup sliders
    const sliders = {
        'dailyLimit': document.getElementById('dailyLimitValue'),
        'monthlyLimit': document.getElementById('monthlyLimitValue'),
        'yearlyLimit': document.getElementById('yearlyLimitValue')
    };

    // Add event listeners to each slider
    Object.keys(sliders).forEach(sliderId => {
        const slider = document.getElementById(sliderId);
        const valueDisplay = sliders[sliderId];

        if (slider && valueDisplay) {
            // Create wrapper for the slider if not exists
            let wrapper = slider.parentElement.querySelector('.slider-wrapper');
            if (!wrapper) {
                wrapper = document.createElement('div');
                wrapper.className = 'slider-wrapper';
                slider.parentNode.insertBefore(wrapper, slider);
                wrapper.appendChild(slider);
            }

            // Add input event listener for real-time updates
            slider.addEventListener('input', () => {
                handleSliderInput(slider, valueDisplay);
            });

            // Add change event listener for final value
            slider.addEventListener('change', () => {
                handleSliderInput(slider, valueDisplay);
            });

            // Initialize tooltip
            createOrUpdateTooltip(wrapper, slider.value);
        }
    });
});
