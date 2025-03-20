from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 15

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:  # главный класс
    """Главный инициализатор"""

    def __init__(self):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """метод - общий рисователь переопределяем в дочерних классах"""
        pass


class Apple(GameObject):  # Дочерний класс яблоко
    """инициализатор яблока"""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()  # случайная начальная позиция яблока

    def randomize_position(self):
        """случайная позиция для яблока."""
        self.position = (
            # учесть что индексы сеток начинаются с 0
            randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1) * GRID_SIZE,
            randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1) * GRID_SIZE
        )

    def draw(self):  # Метод - рисователь яблока
        """переопределенная отрисовка для яблока"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):  # Дочерний класс змея
    """инициализатор змеи"""

    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
        """сброс змеи в начальное состояние"""
        self.length = 1
        self.positions = [self.position]
        # случайный выбор направления змеи при ее респауне
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def get_head_position(self):
        """Возвращает текущее положение головы змейки."""
        return self.positions[0]

    def move(self):
        """Получение текущего расположения головы"""
        head_x, head_y = self.get_head_position()

        # Определение новой позиции головы в зависимости от направления
        if self.direction == RIGHT:
            new_head = (head_x + GRID_SIZE, head_y)
        elif self.direction == LEFT:
            new_head = (head_x - GRID_SIZE, head_y)
        elif self.direction == UP:
            new_head = (head_x, head_y - GRID_SIZE)
        elif self.direction == DOWN:
            new_head = (head_x, head_y + GRID_SIZE)

        # проверка перехода на другую сторону экрана
        new_head = (
            new_head[0] % SCREEN_WIDTH,  # работа с x элементом  (горизонталь)
            new_head[1] % SCREEN_HEIGHT  # работа с y элементом (вертикаль)
        )
        # Вставляем новую голову в список
        self.positions.insert(0, new_head)
        # Удаление хвоста, если нет яблока
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Отрисовка головы змеи"""
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Отрисовка тела змейки
        for position in self.positions[1:]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def update_direction(self):
        """Метод - руль для головы змеи"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


def handle_keys(snake):
    """обработка ввода клавиш"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def reset():
    """метод - создает новые яблоко и змею в случае аварии"""
    global snake, apple
    snake = Snake()  # новая змея
    apple = Apple()  # новое яблоко


def main():
    """главная функция"""
    pygame.init()
    # Тут нужно создать экземпляры классов.
    reset()

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)
        handle_keys(snake)
        snake.update_direction()  # Обновление направления змейки
        snake.move()
        if snake.positions[0] == apple.position:  # если змея съела яблоко
            snake.length += 1  # увеличить ее длинну на 1
            apple.randomize_position()
        if snake.positions[0] in snake.positions[1:]:
            reset()  # сброс игры
            apple.randomize_position()
        apple.draw()
        snake.draw()
        pygame.display.update()  # Обновление экрана
        # Тут опишите основную логику игры.


if __name__ == '__main__':
    main()


# Метод draw класса Apple
# def draw(self):
#     rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, rect)
#     pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self):
#     for position in self.positions[:-1]:
#         rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
#         pygame.draw.rect(screen, self.body_color, rect)
#         pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, head_rect)
#     pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя
# def handle_keys(game_object):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             raise SystemExit
#     elif event.type == pygame.KEYDOWN:
#         if event.key == pygame.K_UP and game_object.direction != DOWN:
#             game_object.next_direction = UP
#         elif event.key == pygame.K_DOWN and game_object.direction != UP:
#             game_object.next_direction = DOWN
#         elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
#             game_object.next_direction = LEFT
#         elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
#             game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
