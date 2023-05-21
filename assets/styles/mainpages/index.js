const menuBtn = document.querySelector('.menu-button');
const menuBtn2 = document.querySelector('.menu-button2');
const mobileNav = document.querySelector('.mobile-nav');

const btnClick = (param) => {
  // let nav = true;
  if (param === 'open') {
    mobileNav.classList.add('left-0');
    mobileNav.classList.remove('left-[-100%]');
    menuBtn.classList.add('hidden');
    menuBtn2.classList.remove('hidden');
    // nav = false;
  } else if (param === 'close') {
    // nav = true;
    mobileNav.classList.remove('left-0');
    mobileNav.classList.add('left-[-100%]');
    menuBtn.classList.remove('hidden');
    menuBtn2.classList.add('hidden');
  }
};