// Fade-in any elements that have the class 'fade' when the page loads 
window.addEventListener('DOMContentLoaded', (event) => {
	init();
	let containerElement = document.querySelector('.fade');
	if (containerElement) {
		containerElement.classList.add('show');
	}
});

// Initialization of the page
function init() {
	// Update the icons
	feather.replace({
		'aria-hidden': 'true'
	});
}