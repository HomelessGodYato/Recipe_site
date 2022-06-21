const nawigacja = document.querySelector('.navigation');
const link1 = document.querySelectorAll('.link-one');
const link2 = document.querySelectorAll('.link-two');
const link3 = document.querySelector('.link-one-other2');
const przelacz = document.querySelector('.przelacz');
const profil_zalgowany = document.querySelectorAll('.profile-l');
const profil_niezalgowany = document.querySelectorAll('.profile-ul');
const fun1 = () => {
	nawigacja.classList.toggle('navigation-not-logged');
	link1.forEach((elem) => {
		elem.classList.toggle('link-one-not-logged');
	});
	link2.forEach((elem) => {
		elem.classList.toggle('link-two-not-logged');
	});
	profil_zalgowany.forEach((elem) => {
		elem.classList.toggle('not-visable');
	});
	profil_niezalgowany.forEach((elem) => {
		elem.classList.toggle('not-visable');
	});
	link3.classList.toggle('link-one-other-not-logged');
};

przelacz.addEventListener('click', fun1);
