const yesButton = document.querySelector('#yes-button');
const noButton = document.querySelector('#no-button');

const moveNoButton = () => {
  var x = Math.random() * (window.innerWidth - noButton.offsetWidth);
  var y = Math.random() * (window.innerHeight - noButton.offsetHeight);

  noButton.style.position = 'absolute';
  noButton.style.left = `${x}px`;
  noButton.style.top = `${y}px`;
}


noButton.addEventListener('click', moveNoButton);
noButton.addEventListener('mouseenter', moveNoButton);
