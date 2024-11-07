"""Из модуля импортированы рандомайзеры."""
from random import choice, randint


import pygame as pg

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

# Цвет гнилового яблока
ROTTEN_APPLE_COLOR = (255, 0, 255)

# Цвет кирпича
BRICK_COLOR = (101, 67, 33)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Класс GameObject является родительским классом в игре."""

    def __init__(self, body_color=None):
        """Инициализатор класса GameObject.

        Здесь опишем цвет и начальную позицию.
        """
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color

    def draw(self):
        """Метод draw создан для переопределения в дочерних классах."""
        raise NotImplementedError(
            f'Определите draw в {self.__class__.__name__}')

    def draw_rect(self, position):
        """Метод рисует квадрат с границей."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс Snake, наследованный от родительского класса GameObject.

    Будет отвечать за змейку и её поведение в игре.
    """

    def __init__(self, body_color=SNAKE_COLOR):
        """Инициализатор класса Snake.

        Тут описаны: начальная длина змейки,
        заготовка для будующего тела змейки,
        изначальное направление движения змейки,
        её цвет и другие параметры с изначальным значением.
        """
        super().__init__(body_color=body_color)
        self.reset(direction=RIGHT)

    def update_direction(self, next_direction):
        """Метод обновления направления после нажатия на кнопку."""
        if next_direction:
            self.direction = next_direction

    def remove_last_rect(self):
        """Метод удалет последний квадрат змеики и затирает его."""
        self.last = self.positions[-1]
        last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
        self.positions.pop()

    def move(self):
        """Метод описывает движение оъекта класса Snake."""
        x_coordinate, y_coordinate = self.get_head_position()
        x_direction, y_direction = self.direction
        x_coordinate = (
            x_coordinate + (x_direction * GRID_SIZE)
        ) % SCREEN_WIDTH
        y_coordinate = (
            y_coordinate + (y_direction * GRID_SIZE)
        ) % SCREEN_HEIGHT
        self.positions.insert(0, (x_coordinate, y_coordinate))
        if len(self.positions) - self.length == 1:
            self.remove_last_rect()
        elif len(self.positions) - self.length > 1:
            self.remove_last_rect()
            self.remove_last_rect()

    def draw(self):
        """Метод draw класса Snake. Отрисовывает змею."""
        for position in self.positions[:-1]:
            self.draw_rect(position)

        self.draw_rect(self.get_head_position())

    def get_head_position(self) -> tuple:
        """Возвращает координаты головы змеи."""
        return self.positions[0]

    def reset(self, direction=choice([RIGHT, LEFT, UP, DOWN])):
        """Метод reset возвращает игру в изначальное положение."""
        self.length = 1
        self.positions = [self.position]
        self.last = None
        self.direction = direction


class Consumables(GameObject):
    """Класс Consumables, наследованный от класса GameObject.

    Объект этого класса является элементом в игре, которое можно съесть.
    """

    def __init__(self, body_color=None):
        """Инициализатор класса Consumables."""
        super().__init__(body_color=body_color)

    def randomize_position(self, forbiden_cells):
        """Случайным образом выбирает координаты для съедобного элемента."""
        while True:
            random_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            random_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            self.position = (random_x, random_y)
            if self.position not in forbiden_cells:
                break

    def draw(self):
        """Этот метод отрисовывает съедобный элемент на игровом поле."""
        self.draw_rect(self.position)


class Apple(Consumables):
    """Класс яблоко, наследованный от класса Consumables."""

    def __init__(self, body_color=APPLE_COLOR):
        """Инициализатор класса Apple."""
        super().__init__(body_color=body_color)


class RottenApple(Consumables):
    """Класс гнилое яблоко наследник от Consumables."""

    def __init__(self, body_color=ROTTEN_APPLE_COLOR):
        """Иницилизатор класса RottenApple."""
        super().__init__(body_color=body_color)


class Brick(Consumables):
    """Класс кирпич наследник от Consumables."""

    def __init__(self, body_color=BRICK_COLOR):
        """Иницилизатор класса Brick."""
        super().__init__(body_color=body_color)


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
                return UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
                return DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
                return LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
                return RIGHT


def main():
    """Основная фунцкия игры, в который описан цикл, и правил игры."""
    def occupied_cells() -> list:
        cells = [cell for cell in snake.positions]
        cells.append(apple.position)
        cells.append(rotten_apple.position)
        cells.append(brick.position)
        return cells

    pg.init()
    snake = Snake()
    apple = Apple()
    rotten_apple = RottenApple()
    brick = Brick()
    apple.randomize_position(occupied_cells())
    rotten_apple.randomize_position(occupied_cells())
    brick.randomize_position(occupied_cells())

    while True:
        clock.tick(SPEED)
        snake.update_direction(handle_keys(snake))
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(occupied_cells())
        if (snake.get_head_position() in snake.positions[1:]
                or snake.get_head_position() == brick.position):
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position(occupied_cells())
            rotten_apple.randomize_position(occupied_cells())
            brick.randomize_position(occupied_cells())
        if snake.get_head_position() == rotten_apple.position:
            rotten_apple.randomize_position(occupied_cells())
            if snake.length > 1:
                snake.length -= 1

        snake.draw()
        apple.draw()
        rotten_apple.draw()
        brick.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
