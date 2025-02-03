	__Папка SRC__
	Файлы и классы:

__MainGameScreen__ (файл MainGameScreen.py)
Назначение: Основной игровой процесс, включает управление объектами, событиями и визуализацией.
Методы:
Назначение: Основной игровой процесс, включает управление объектами, событиями и визуализацией.
Методы:
init: Передаваемый параметр: screen: экземпляр объекта pygame.Surface, представляющий игровое окно. Инициализация игрового экрана, настройка таймера, фонового изображения и объектов.
run: Параметры не передаются, так как метод работает с внутренними данными экземпляра класса. Главный цикл игры, обрабатывает события, обновляет объекты и рендерит графику.

__Ship__ (Ship.py)
Назначение: Представляет корабль игрока, управляется пользователем.
Методы:
init: Передаваемые параметры: x, y: координаты начальной позиции корабля на экране. Инициализация корабля, загрузка изображений, установка скорости и других параметров.
update: Передаваемые параметры: keys: словарь, содержащий информацию о состоянии клавиш (нажаты или нет). dt: дельта времени, прошедшая с последнего кадра, используется для корректировки скорости перемещения.Обновление позиции корабля в зависимости от нажатых клавиш и состояния щита.
activate_double_speed: Передаваемый параметр: duration: длительность эффекта удвоенной скорости в миллисекундах (по умолчанию 5000 мс).Активация режима удвоенной скорости на определённое время.
activate_shield: Передаваемый параметр: duration: длительность эффекта щита в миллисекундах (по умолчанию 10000 мс).Активация защитного щита на определённое время.

__Enemy_Hight__ (Enemy_Hight.py)
Назначение: Представляет вражеские корабли, преследующие игрока.
Методы:
init: Передаваемые параметры: x, y: координаты начальной позиции врага на экране.Инициализация вражеского корабля, загрузка изображений и установка начальной позиции.
update: Передаваемые параметры: keys: словарь, содержащий информацию о состоянии клавиш (нажаты или нет). x_p, y_p: координаты текущего положения игрока, чтобы враг мог следовать за ним. Обновление позиции вражеского корабля в зависимости от положения игрока.

__Bullet__ (Bullet.py)
Назначение: Представляют выстрелы игрока.
Методы:
init: Передаваемые параметры: x, y: координаты начальной позиции пули на экране. Инициализация пули, задание её начального положения и скорости.
update: Параметры не передаются, так как метод работает с внутренними данными экземпляра класса. Обновление позиции пули, уничтожение при выходе за пределы экрана.

__GameObject__ (GameObject.py)
Назначение: Базовый класс для всех игровых объектов, таких как корабль игрока, враг и пули.
Методы:
init: Передаваемые параметры: image_path: строка, содержащая путь к изображению объекта.
x, y: координаты начальной позиции объекта на экране. Инициализация объекта, загрузка изображения и создание маски для точных столкновений.

  __Основные особенности__:
Управление кораблём: Игрок может перемещать корабль с помощью клавиатуры, активировать бафы скорости и щит.
Столкновения: Реализовано точное определение столкновений с использованием масок.
Интерфейс: Игровое поле содержит фоновые изображения, иконки для активации двойного ускорения и защиты, а также индикаторы здоровья.
Визуальные эффекты: Анимации движения кораблей и пуль, изменение изображений в зависимости от направления движения, взрывы при попадании выстрелов.

  __Логическая связь классов__:
MainGameScreen управляет всеми аспектами игры, включая обработку событий, обновление объектов и рендеринг графики.
Ship отвечает за движение и состояние корабля игрока, включая активацию бафов.
Enemy_Hight контролирует поведение врагов.
Bullet генерируется игроком и летит вверх, уничтожаясь при достижении верхней границы экрана.
GameObject служит основой для создания всех игровых объектов, обеспечивая общие методы и свойства.
