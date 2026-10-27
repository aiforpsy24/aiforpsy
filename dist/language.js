const languageMenus = [...document.querySelectorAll('.language-menu')];
document.addEventListener('click', event => {
  languageMenus.forEach(menu => { if (!menu.contains(event.target)) menu.open = false; });
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape') languageMenus.forEach(menu => { menu.open = false; });
});
languageMenus.forEach(menu => menu.addEventListener('toggle', () => {
  if (menu.open) document.querySelectorAll('.mobile-menu').forEach(other => { other.open = false; });
}));
