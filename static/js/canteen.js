document.addEventListener("DOMContentLoaded", function () {
  const section = document.querySelector(".section-center");
  const filterBtns = document.querySelectorAll(".btn-item");


  // Функция отрисовки меню
  const menuList = (menuItems) => {
    let displayMenu = menuItems.map((item) => {
      return `
        <div class="menu-items col-lg-6 col-sm-12">
          <img src="${item.img}" alt="${item.title}" class="photo">
          <div class="menu-info">
            <div class="menu-title"><h4>${item.title}</h4></div>
            <div class="menu-text">${item.desc}</div>
          </div>
        </div>`;
    }).join("");
    section.innerHTML = displayMenu;
  };

  filterBtns.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      // Убираем/добавляем active
      document.querySelectorAll(".btn-item").forEach(b => b.classList.remove("active"));
      e.currentTarget.classList.add("active");

      // Фильтруем и показываем
      const category = e.currentTarget.dataset.id;
      const menuCategory = menuData.filter(item => item.category === category);
        console.log(menuCategory);
      menuList(menuCategory);
    });
  });

  // Получаем текущий день недели
  const daysOfWeek = ['ВОСКРЕСЕНЬЕ', 'ПОНЕДЕЛЬНИК', 'ВТОРНИК', 'СРЕДА', 'ЧЕТВЕРГ', 'ПЯТНИЦА', 'СУББОТА'];
  const today = new Date();
  console.log(today);
  const currentDay = daysOfWeek[today.getDay()];

  // Ищем кнопку с этим днём
  const defaultBtn = document.querySelector(`[data-id="${currentDay}"]`);

  if (defaultBtn) {
    defaultBtn.classList.add("active"); // Выделяем её
    const category = defaultBtn.dataset.id;
    const menuCategory =menuData.filter(item => item.category === category);
    menuList(menuCategory); // Отображаем меню за сегодня
  } else {
    // Если не нашли — выводим всё
    menuList(menuData);
  }
});