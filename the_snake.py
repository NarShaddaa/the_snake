import sys
from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Константа для позиции объекта в центре экрана
START_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

COLORS = {
    'PURPLE': (128, 0, 128),      # Фиолетовый
    'BLUE': (0, 0, 255),          # Синий
    'GREEN': (0, 255, 0),         # Зеленый
    'RED': (255, 0, 0),           # Красный
    'YELLOW': (255, 255, 0),      # Желтый
    'CYAN': (0, 255, 255),        # Голубой
    'WHITE': (255, 255, 255),     # Белый
    'BLACK': (0, 0, 0),           # Черный
    'SNAKE_COLOR': (0, 255, 0),   # Зеленый
    'APPLE_COLOR': (255, 0, 0)    # Красный
}

# Скорость движения змейки:
SPEED = 12

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:  # главный класс
    """Главный инициализатор."""

    def __init__(
            self,
            position=START_POSITION,
            body_color=None,
            border_color=BORDER_COLOR
    ):
        self.position = position
        self.body_color = body_color
        self.border_color = border_color

    def draw_cell(self, position=None, body_color=None):
        """Отрисовывает ячейку объекта"""
        pos = position if position is not None else self.position
        body = body_color if body_color is not None else self.body_color
        rect = pygame.Rect(pos, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, body, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """
        Отрисовывает объект на экране.

        Этот метод должен быть переопределён в дочерних классах.
        Если метод не переопределён, вызывается исключение.
        """
        raise NotImplementedError(
            'Метод draw должен быть переопределён в классе.'
            + f'{self.__class__.__name__}'
        )


class Apple(GameObject):  # Дочерний класс яблоко
    """Инициализатор яблока."""

    random_color = choice(list(COLORS.values()))  # раскраска

    def __init__(self, body_color=random_color, occupied_positions=None):
        super().__init__(body_color=body_color)  # установка цвета яблока
        # передача без сохранения
        self.randomize_position(occupied_positions or [])

    def randomize_position(self, occupied_positions):  # параметр для ячейки
        """Случайная позиция для яблока."""
        while True:
            """Создание случайной позиции."""
            self.position = (
                # учесть что индексы сеток начинаются с 0
                randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1) * GRID_SIZE,
                randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1) * GRID_SIZE
            )
            # проверка занятой ячейки
            if self.position not in occupied_positions:
                break

    def draw(self):  # Метод - рисователь яблока
        """Рисует яблоко с помощью баззового класса."""
        self.draw_cell()


class Snake(GameObject):  # Дочерний класс змея
    """Инициализатор змеи."""

    random_color = choice(list(COLORS.values()))  # раскраска

    def __init__(self, body_color=random_color):
        super().__init__(body_color=body_color)  # установка цвета змеи
        self.reset()

    def reset(self):
        """Сброс змеи в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        # случайный выбор направления змеи при ее респауне
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Возвращает текущее положение головы змеи."""
        return self.positions[0]

    def move(self):
        """Получение текущего расположения головы."""
        # Словарь смещений по направлениям (x, y)
        direction_offsets = {
            RIGHT: (GRID_SIZE, 0),
            LEFT: (-GRID_SIZE, 0),
            UP: (0, -GRID_SIZE),
            DOWN: (0, GRID_SIZE)
        }
        # текущая позиция головы змеи
        head_x, head_y = self.get_head_position()

        # проверка перехода на другую сторону экрана
        dx, dy = direction_offsets[self.direction]
        new_head = (
            (head_x + dx) % SCREEN_WIDTH,  # переход по горизонтали
            (head_y + dy) % SCREEN_HEIGHT  # переход по вертикали
        )

        # Вставляем новую голову в список
        self.positions.insert(0, new_head)
        # Удаление хвоста, если нет яблока
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Отрисовывает змею с помощью базового класса."""
        for position in self.positions:
            self.draw_cell(position=position)

    def update_direction(self):
        """Метод - руль для головы змеи."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


def handle_keys(snake):
    """Обработка ввода клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Завершение игры через ESC
                pygame.quit()
                sys.exit(0)
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def reset():
    """Метод - создает новые яблоко и змею в случае аварии."""
    global snake, apple
    snake = Snake()  # новая змея Синяя
    apple = Apple(occupied_positions=snake.positions)  # новое яблоко


def main():
    """Главная функция."""
    pygame.init()
    reset()

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)
        handle_keys(snake)
        snake.update_direction()  # Обновление направления змейки
        snake.move()
        # новая запись если змея съела яблоко
        if snake.get_head_position() == apple.position:
            snake.length += 1  # увеличить ее длинну на 1
            apple.randomize_position(snake.positions)
        # новое столкновение с самой собой
        elif snake.get_head_position() in snake.positions[4:]:
            snake.reset()  # сброс игры
            apple.randomize_position(snake.positions)
        apple.draw()
        snake.draw()
        pygame.display.update()  # Обновление экрана


if __name__ == '__main__':
    main()
