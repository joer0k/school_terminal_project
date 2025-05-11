<h1>Школьный терминал</h1>
<h2>Описание проекта</h2>
<h3 style="font-weight: normal">Проект представляет собой сайт-терминал, содержащий всю необходимую инфоромацию о школе: расписание уроков, меню столовой,
данные об учителях и о классах, информация о дополнительном образовании и другая дополнительная информация</h3>
<h2>Установка</h2>
    <div class="code-block">
        <pre id="code" style="background-color: #282c34"><code>
git clone https://github.com/joer0k/school_terminal_project.git 
pip install -r school_terminal_project/requirements.txt
        </code></pre>
    </div>
<h2>Техническое задание</h2>
<ol style="font-size: 14px">
    <li>Создать базы данных на основе ORM sqlalchemy для учителей, классов, расписания, меню столовой, пользователей</li>
    <li>Главная страница с доступом ко всем другим страницам</li>
    <li>Админ панель в которой будет возможность редактировать расписание, работников, меню столовой, информацию на отдельных страницах</li>
    <li><a><code>/schedule</code></a> страница с расписанием</li>
    <li><a><code>/canteen</code></a> страница с информацией по столовой</li>
    <li><a><code>/administration</code></a> страница с информацией об администрации школы</li>
    <li><a><code>/teachers</code></a> страница с информацией об учителях</li>
    <li><a><code>/it_cube</code></a> информация о It_Cube. с нее будет переход на другие страницы об айти кубе</li>
    <li><a><code>/admin/</code></a> админ панель</li>
    <li><a><code>/admin/schedule</code></a> та же страница с расписанием, только с возможность редактирования</li>
    <li><a><code>/admin/canteen</code></a> та же страница о столовой, только с возможностью редактирования</li>
    <li><a><code>/admin/teachers</code></a> редактирование работников</li>
    <li><a><code>/contacts</code></a> контакты для связи с администрацией</li>
    <li><a><code>/news</code></a> новости школы</li>
    <li><a><code>/gallery</code></a> фотографии школы(с последних мероприятий и т.д.)</li>
    <li><a><code>/medical_room</code></a> медкабинет</li>
</ol>


<h2>Пояснительная записка</h2>
<h2>Авторы проекта</h2>
<h4>
<a href='https://github.com/joer0k'>Рябоконь Никита</a>, <a href='https://github.com/Katja19999'>Горбенко
Екатерина</a>, <a href='https://github.com/AnzhelicaS'>Соболь Анжелика</a>
</h4>
<h3>Структура базы данных</h3>
<img src='https://github.com/joer0k/school_terminal_project/blob/Nikita/static/images/db_diagram.png'>
<h2>Описание технологий</h2>
<h4><a><code>Flask</code></a> - фреймворк для создания веб-приложений на языке программирования Python. В него
входит <a><code>Jinja2</code></a> - язык шаблонов, использующийся для генерации шаблонов. И <a><code>
Werkzeug</code></a> - библиотека упрощающая многие задачи веб-разработки</h2>
<h4><a><code>SqlAlchemy</a></code> - это программная библиотека на языке Python использующаяся для работы с реляционными
СУБД. Она дает возможность работать с БД в концепциях ООП благодаря моделям и <a><code>orm</code></a></h4>

<h2>Уже реализовано</h2>
<ol>
    <li>База данных со всеми необходимыми таблицами</li>
    <li>Задуманная главная страница</li>
    <li>Админ панель</li>
    <li><a><code>/schedule</code></a> страница с расписанием</li>
    <li><a><code>/canteen</code></a> страница с информацией по столовой</li>
    <li><a><code>/administration</code></a> страница с информацией об администрации школы</li>
    <li><a><code>/teachers</code></a> страница с информацией об учителях</li>
    <li><a><code>/it_cube</code></a> информация о It_Cube.</li>
    <li><a><code>/admin/</code></a> админ панель</li>
    <li><a><code>/admin/schedule</code></a> расписание в админ панели</li>
    <li><a><code>/admin/canteen</code></a> столовая в админ панели</li>
    <li><a><code>/admin/teachers</code></a> редактирование работников</li>
</ol>
