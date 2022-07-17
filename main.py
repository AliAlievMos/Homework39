import _curses
import logging
import curses
from curses import wrapper
from time import sleep
import random
from abc import ABC, abstractmethod


# Задание 1

x = 2
y = 8


class Singleton(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance
    @classmethod
    def log(cls, list):
        logging.basicConfig(
            level=logging.DEBUG,
            filename="mylog.log",
            format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
            datefmt='%H:%M:%S',
        )
        eval(f'\t\t{list}')


a = Singleton()
string_logs = "logging.info(f'Результат возведения {y} в степень {x} равен: {y**x}')"
a.log(string_logs)


# задание 2


class Subject(ABC):

    @abstractmethod
    def notify(self):
        pass

    @abstractmethod
    def attach(self, Observer):
        pass

    @abstractmethod
    def detach(self, Observer):
        pass


class Observer(ABC):
    @abstractmethod
    def update(self, subject, stdscr):
        pass


class ConcreteSubject(Subject):
    img = '●'
    x_cor: int = random.randint(25, 30)
    y_cor: int = random.randint(25, 30)
    _observers = []

    def __init__(self, stdscr):
        super()
        self.stdscr = stdscr

    def cor_self(self):
        button_code = self.stdscr.getch()
        if button_code == curses.KEY_RIGHT:
            self.y_cor += 1
        elif button_code == curses.KEY_LEFT:
            self.y_cor -= 1
        elif button_code == curses.KEY_UP:
            self.x_cor -= 1
        elif button_code == curses.KEY_DOWN:
            self.x_cor += 1

    def refresh_self(self):
        self.stdscr.addstr(self.x_cor, self.y_cor, self.img)
        self.notify()

    def notify(self):
        for observer in self._observers:
            observer.update(self)

    def attach(self, Observer):
        self._observers.append(Observer)

    def detach(self, observer):
        self._observers.remove(observer)


class ConcreteObserverA(Observer):
    img = '○'
    x_cor: int = random.randint(5, 30)
    y_cor: int = random.randint(5, 30)

    def __init__(self, stdscr):
        super()
        self.stdscr = stdscr

    def update(self, subject):
        if self.x_cor > subject.x_cor:
            self.x_cor -= 1
        if self.x_cor < subject.x_cor:
            self.x_cor += 1
        if self.y_cor < subject.y_cor:
            self.y_cor += 1
        if self.y_cor > subject.y_cor:
            self.y_cor -= 1
        if self.x_cor == subject.x_cor and self.y_cor == subject.y_cor:
            subject.detach(self)
            self.stdscr.addstr(20, 20, 'Тебя поймали!')
        self.refresh_self()

    def refresh_self(self):
        self.stdscr.addstr(self.x_cor, self.y_cor, '○')

class ConcreteObserverB(Observer):
    img = '○'
    x_cor: int = random.randint(5, 20)
    y_cor: int = random.randint(5, 20)

    def __init__(self, stdscr):
        super()
        self.stdscr = stdscr

    def update(self, subject):
        if self.x_cor > subject.x_cor:
            self.x_cor -= 1
        elif self.x_cor < subject.x_cor:
            self.x_cor += 1
        if self.y_cor < subject.y_cor:
            self.y_cor += 1
        elif self.y_cor > subject.y_cor:
            self.y_cor -= 1
        if self.x_cor == subject.x_cor and self.y_cor == subject.y_cor:
            subject.detach(self)
            self.stdscr.addstr(20, 20, 'Тебя поймали!')
        self.refresh_self()

    def refresh_self(self):
        self.stdscr.addstr(self.x_cor, self.y_cor, '○')


def run(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    stdscr.attron(curses.color_pair(1))

    enemy = ConcreteObserverA(stdscr)
    enemy1 = ConcreteObserverB(stdscr)
    player = ConcreteSubject(stdscr)

    player.attach(enemy)
    player.attach(enemy1)
    player.refresh_self()
    enemy.refresh_self()
    enemy1.refresh_self()

    while True:
        try:

            stdscr.clear()
            player.refresh_self()
            stdscr.refresh()
            player.cor_self()

        except _curses.error:
            stdscr.clear()
            stdscr.addstr(10, 10, 'Ты проиграл, выходить за терминал нельзя!')
            stdscr.addstr(15, 15, '5')
            stdscr.refresh()
            sleep(1)
            stdscr.addstr(15, 15, '4')
            stdscr.refresh()
            sleep(1)
            stdscr.addstr(15, 15, '3')
            stdscr.refresh()
            sleep(1)
            stdscr.addstr(15, 15, '2')
            stdscr.refresh()
            sleep(1)
            stdscr.addstr(15, 15, '1')
            stdscr.refresh()
            sleep(1)
            break


        sleep(0.1)


if __name__ == "__main__":
    wrapper(run)
