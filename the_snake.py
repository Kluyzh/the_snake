"""Из модуля импортированы рандомайзеры."""
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
APPLE_COLOR = (255, 255, 0)

# Цвет змейки
SNAKE_COLOR = (255, 128, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Класс GameObject является родительским классом в игре."""

    def __init__(self):
        """Инициализатор класса GameObject.

        Здесь опишем цвет и начальную позицию.
        """
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self):
        """Метод draw создан для переопределения в дочерних классах."""
        pass


class Snake(GameObject):
    """Класс Snake, наследованный от родительского класса GameObject.

    Будет отвечать за змейку и её поведение в игре.
    """

    def __init__(self):
        """Инициализатор класса Snake.

        Тут описаны: начальная длина змейки,
        заготовка для будующего тела змейки,
        изначальное направление движения змейки,
        её цвет и другие параметры с изначальным значением None.
        """
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def check_the_length(self):
        """Проверка съедено ли яблоко."""
        if len(self.positions) - self.length == 1:
            self.last = [self.positions[-1]]
            self.positions.pop()
        elif len(self.positions) - self.length > 1:
            self.last = self.positions[-2:]
            self.positions.pop()
            self.positions.pop()

    def move(self):
        """Метод описывает движение оъекта класса Snake."""
        x_coordinate, y_coordinate = self.get_head_position()
        if self.direction == RIGHT:
            if x_coordinate + GRID_SIZE > SCREEN_WIDTH - GRID_SIZE:
                x_coordinate = - GRID_SIZE
            self.positions.insert(0, (x_coordinate + GRID_SIZE, y_coordinate))
            self.check_the_length()
        elif self.direction == LEFT:
            if x_coordinate - GRID_SIZE < 0:
                x_coordinate = SCREEN_WIDTH
            self.positions.insert(0, (x_coordinate - GRID_SIZE, y_coordinate))
            self.check_the_length()
        elif self.direction == UP:
            if y_coordinate - GRID_SIZE < 0:
                y_coordinate = SCREEN_HEIGHT
            self.positions.insert(0, (x_coordinate, y_coordinate - GRID_SIZE))
            self.check_the_length()
        elif self.direction == DOWN:
            if y_coordinate + GRID_SIZE > SCREEN_HEIGHT - GRID_SIZE:
                y_coordinate = - GRID_SIZE
            self.positions.insert(0, (x_coordinate, y_coordinate + GRID_SIZE))
            self.check_the_length()

    def draw(self):
        """Метод draw класса Snake.

        Отрисовывает голову змеи.
        Затирает последний элемент змеи.
        """
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            for last in self.last:
                last_rect = pygame.Rect(last, (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self) -> tuple:
        """Возвращает координаты головы змеи."""
        return self.positions[0]

    def reset(self):
        """Метод reset возвращает игру в изначальное положение."""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([RIGHT, LEFT, UP, DOWN])
        self.last = None
        screen.fill(BOARD_BACKGROUND_COLOR)


class Apple(GameObject):
    """Класс Apple, наследованный от класса GameObject.

    Объект этого класса является яблоком в игре, которое нужно съесть.
    """

    def __init__(self):
        """Инициализатор класса Apple."""
        super().__init__()
        self.body_color = APPLE_COLOR

    def randomize_position(self):
        """Случайным образом выбирает координаты для яблока."""
        random_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        random_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (random_x, random_y)

    def draw(self):
        """Этот метод отрисовывает яблоко на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная фунцкия игры, в который описан цикл, и правил игры."""
    pygame.init()
    apple = Apple()
    apple.randomize_position()
    rotten_apple = Apple()
    rotten_apple.body_color = (255, 0, 255)
    rotten_apple.randomize_position()
    brick = Apple()
    brick.body_color = (101, 67, 33)
    brick.randomize_position()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        apple.draw()
        rotten_apple.draw()
        brick.draw()
        snake.draw()
        snake.update_direction()
        snake.move()
        pygame.display.update()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        if (snake.get_head_position() in snake.positions[1:]
                or snake.get_head_position() == brick.position):
            snake.reset()
            apple.randomize_position()
            rotten_apple.randomize_position()
            brick.randomize_position()
        if snake.get_head_position() == rotten_apple.position:
            rotten_apple.randomize_position()
            if snake.length > 1:
                snake.length -= 1


if __name__ == '__main__':
    main()
