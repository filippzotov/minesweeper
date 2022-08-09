import random
import tkinter as tk
from tkinter import font
import tkinter.messagebox as mb


class Minesweeper(tk.Tk):

    # Инициалзация начальных данных
    def __init__(self):
        super().__init__()
        self.title("My minesweeper")
        self.count_plates = 0
        self.count_bombs = 0
        self.table = []
        self.newt = []
        self.seen = set()
        self.pressedbtns = set()

        self.frame = tk.Frame()

        self.table = [[0 for _ in range(10)] for _ in range(10)]
        for i in range(10):
            for _ in range(random.randint(0, 2)):
                self.table[i][random.randint(0, 9)] = 1
                self.count_bombs += 1

        for i in range(10):
            row = []
            for j in range(10):
                row.append(self.check_table(i, j))
            self.newt.append(row)

        self.myfont = font.Font(
            size=20,
            weight=font.BOLD,
        )

        self.btnlist = []
        for i in range(10):
            temp = []
            for j in range(10):
                btn = tk.Button(
                    text="",
                    width=3,
                    height=1,
                    master=self.frame,
                    borderwidth=5,
                    command=lambda cords=(i, j): self.btn_pressed(cords),
                    relief="raised",
                    font=self.myfont,
                )
                btn.bind("<Button-3>", self.make_flag)
                temp.append(btn)
            self.btnlist.append(temp)

        for i, row in enumerate(self.btnlist):
            for j, col in enumerate(row):
                col.grid(row=i, column=j)

        self.frame.pack()
        restart_button = tk.Button(
            text="restart",
            height=1,
            command=self.start_game,
            font=self.myfont,
        )
        restart_button.pack()

    # Прослушиватель правой кнопки мыши для установки флага
    def make_flag(self, event):
        if event.widget["relief"] != "sunken":
            if not event.widget["text"]:
                event.widget.configure(
                    text="F", disabledforeground="RED", state="disabled"
                )
            else:
                event.widget.configure(text="", state="active")

    # Прослушиватель нажатия кнопки поля
    def btn_pressed(self, cords):
        x, y = cords
        bombs = self.newt[x][y]
        if bombs == -1:
            self.end_game()
            return

        if not bombs:
            self.open_island(x, y)
            self.seen.clear()
        else:
            self.conf_btn(x, y, bombs)
        if 10 * 10 - len(self.pressedbtns) == self.count_bombs:
            self.win_game()

    # Заполнение ячеек вокруг бомб
    def check_table(self, x, y):
        count = 0
        if self.table[x][y] == 1:
            return -1
        if x != 0 and y != 0 and self.table[x - 1][y - 1] == 1:
            count += 1
        if x != 0 and self.table[x - 1][y] == 1:
            count += 1
        if x != 0 and y != 9 and self.table[x - 1][y + 1] == 1:
            count += 1
        if y != 0 and self.table[x][y - 1] == 1:
            count += 1
        if y != 9 and self.table[x][y + 1] == 1:
            count += 1
        if x != 9 and y != 0 and self.table[x + 1][y - 1] == 1:
            count += 1
        if x != 9 and self.table[x + 1][y] == 1:
            count += 1
        if x != 9 and y != 9 and self.table[x + 1][y + 1] == 1:
            count += 1
        return count

    # Начало новой игры, обнуление всех кнопок и создание нового поля
    def start_game(self):
        self.pressedbtns.clear()
        self.count_plates = 0
        self.count_bombs = 0
        self.table = [[0 for _ in range(10)] for _ in range(10)]
        for i, row in enumerate(self.table):
            for _ in range(random.randint(0, 2)):
                self.table[i][random.randint(0, 9)] = 1
                self.count_bombs += 1

        self.newt = []
        for i in range(10):
            row = []
            for j in range(10):
                row.append(self.check_table(i, j))
            self.newt.append(row)

        for i, row in enumerate(self.btnlist):
            for j, col in enumerate(row):
                self.btnlist[i][j].configure(
                    text="",
                    relief="raised",
                    state="active",
                )

    # Конец игры
    def end_game(self):
        for i in range(10):
            for j in range(10):
                if self.newt[i][j] == -1:
                    self.btnlist[i][j]["text"] = "B"
        msg = "u lost.\n Начать заново?"
        f = mb.askyesno("END", msg)
        if f:
            self.start_game()

    # Победа
    def win_game(self):
        for i in range(10):
            for j in range(10):
                if self.newt[i][j] == -1:
                    self.btnlist[i][j]["text"] = "B"
        msg = "u win.\n Начать заново?"
        f = mb.askyesno("END", msg)
        if f:
            self.start_game()

    # Рекурсивное закрытие пустых ячеек без бомб
    def open_island(self, x, y):

        if x < 0 or x > 9 or y < 0 or y > 9:
            return
        if (x, y) in self.seen:
            return
        if self.newt[x][y] != 0:
            self.conf_btn(x, y, self.newt[x][y])
            self.seen.add((x, y))
            return
        else:
            self.conf_btn(x, y, "")
            self.seen.add((x, y))
            self.open_island(x - 1, y)
            self.open_island(x + 1, y)
            self.open_island(x, y - 1)
            self.open_island(x, y + 1)

    # Изменение состояние кнопки
    def conf_btn(self, x, y, text):
        color = {
            "": "BLACK",
            "F": "GREY",
            0: "BLACK",
            1: "BLACK",
            2: "BLUE",
            3: "RED",
            4: "BROWN",
            5: "PURPLE",
        }
        self.btnlist[x][y].configure(
            text=text,
            state="disabled",
            relief="sunken",
            disabledforeground=color[text],
        )
        if (x, y) not in self.pressedbtns:
            self.count_plates += 1
            self.pressedbtns.add((x, y))


if __name__ == "__main__":
    app = Minesweeper()

    app.mainloop()
