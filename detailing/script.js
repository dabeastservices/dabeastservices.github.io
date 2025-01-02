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
	feather.replace({
		'aria-hidden': 'true' // Update the icons
	});
}

window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', 'G-RKBJNST9BF');