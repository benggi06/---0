import random
import customtkinter as ctk
from tkinter import messagebox

# Set the appearance mode and default color theme
ctk.set_appearance_mode("Dark")  # Options: "Light", "Dark", "System"
ctk.set_default_color_theme("blue") # Options: "blue", "green", "dark-blue"

# 영어 단어와 그에 해당하는 한국어 뜻
words = {
    'apple': '사과', 'banana': '바나나', 'grape': '포도',
    'orange': '오렌지', 'strawberry': '딸기', 'melon': '멜론',
    'pineapple': '파인애플', 'watermelon': '수박', 'kiwi': '키위',
    'mango': '망고', 'tiger': '호랑이', 'lion': '사자',
    'elephant': '코끼리', 'monkey': '원숭이', 'zebra': '얼룩말',
    'giraffe': '기린', 'dolphin': '돌고래', 'penguin': '펭귄',
    'kangaroo': '캥거루', 'bear': '곰'
}

# 행맨 그림 단계
hangman_stages = [
    """
      +---+
      |   |
          |
          |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
          |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
      |   |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
     /|   |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
     /|\\  |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
     /|\\  |
     /    |
          |
    =========""",
    """
      +---+
      |   |
      O   |
     /|\\  |
     / \\  |
          |
    ========="""
]

class HangmanApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("행맨 게임")
        self.geometry("500x600")
        self.resizable(False, False)
        
        self.learned_words = {}
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.create_main_menu()

    def clear_frame(self):
        """현재 윈도우의 모든 위젯을 제거하는 함수."""
        for widget in self.winfo_children():
            widget.destroy()
            
    def create_main_menu(self):
        """메인 메뉴 화면을 구성하는 함수."""
        self.clear_frame()
        
        frame = ctk.CTkFrame(self, corner_radius=15)
        frame.pack(expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(frame, text="행맨 게임", font=("Helvetica", 32, "bold")).pack(pady=20, padx=20)
        
        ctk.CTkButton(frame, text="게임 시작", font=("Helvetica", 18), width=250, height=50,
                      command=self.start_game).pack(pady=10)
        ctk.CTkButton(frame, text="맞힌 단어 목록 보기", font=("Helvetica", 18), width=250, height=50,
                      command=self.show_learned_words).pack(pady=10)
        ctk.CTkButton(frame, text="종료", font=("Helvetica", 18), width=250, height=50,
                      command=self.quit).pack(pady=10)

    def start_game(self):
        """게임 화면을 구성하고 게임 변수를 초기화하는 함수."""
        self.clear_frame()
        
        secret_word_tuple = random.choice(list(words.items()))
        self.secret_word = secret_word_tuple[0].lower()
        self.secret_meaning = secret_word_tuple[1]
        
        while self.secret_word in self.learned_words:
            secret_word_tuple = random.choice(list(words.items()))
            self.secret_word = secret_word_tuple[0].lower()
            self.secret_meaning = secret_word_tuple[1]
            
        self.guessed_word = ['_'] * len(self.secret_word)
        self.attempts_left = len(hangman_stages) - 1
        self.guessed_letters = set()
        
        game_frame = ctk.CTkFrame(self, corner_radius=15)
        game_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        self.hangman_label = ctk.CTkLabel(game_frame, text=hangman_stages[0], font=("Courier", 12), justify="left")
        self.hangman_label.pack(pady=10)
        
        self.word_label = ctk.CTkLabel(game_frame, text=" ".join(self.guessed_word), font=("Helvetica", 40, "bold"))
        self.word_label.pack(pady=20)
        
        self.wrong_guesses_frame = ctk.CTkFrame(game_frame, corner_radius=10, fg_color="transparent")
        self.wrong_guesses_frame.pack(pady=10)
        
        self.guess_dots = []
        for i in range(len(hangman_stages) - 1):
            dot = ctk.CTkLabel(self.wrong_guesses_frame, text="●", font=("Helvetica", 20), text_color="green")
            dot.pack(side="left", padx=5)
            self.guess_dots.append(dot)
            
        self.guess_entry = ctk.CTkEntry(game_frame, width=100, font=("Helvetica", 20), justify="center")
        self.guess_entry.pack(pady=10)
        self.guess_entry.focus()
        self.guess_entry.bind("<Return>", self.check_guess)
        
        ctk.CTkButton(game_frame, text="추측", font=("Helvetica", 18),
                      command=self.check_guess).pack(pady=5)
        
        ctk.CTkButton(game_frame, text="힌트", font=("Helvetica", 18),
                      command=self.show_hint).pack(pady=5)
                      
        ctk.CTkButton(game_frame, text="메인 메뉴로", font=("Helvetica", 14),
                      command=self.create_main_menu, fg_color="transparent", hover_color="#222").pack(side="bottom", pady=10)

    def check_guess(self, event=None):
        """사용자 입력을 확인하고 게임 상태를 업데이트하는 함수."""
        guess = self.guess_entry.get().lower()
        self.guess_entry.delete(0, ctk.END)
        
        if not guess.isalpha() or len(guess) != 1:
            messagebox.showerror("오류", "한 개의 알파벳만 입력해주세요.")
            return
        
        if guess in self.guessed_letters:
            messagebox.showinfo("알림", "이미 추측한 글자입니다. 다른 글자를 입력해주세요.")
            return
        
        self.guessed_letters.add(guess)
        
        if guess in self.secret_word:
            messagebox.showinfo("정답", "정답입니다!👍")
            for i, letter in enumerate(self.secret_word):
                if letter == guess:
                    self.guessed_word[i] = guess
        else:
            messagebox.showinfo("오답", "틀렸습니다.😢")
            self.attempts_left -= 1
        
        self.update_display()
        self.check_game_status()

    def show_hint(self):
        """힌트를 제공하고 기회를 차감하는 함수."""
        if self.attempts_left > 1:
            remaining_letters = [c for c in self.secret_word if c not in self.guessed_letters]
            if remaining_letters:
                hint_char = random.choice(remaining_letters)
                self.guessed_letters.add(hint_char)
                for i, letter in enumerate(self.secret_word):
                    if letter == hint_char:
                        self.guessed_word[i] = hint_char
                self.attempts_left -= 1
                messagebox.showinfo("힌트", f"힌트: 단어에 '{hint_char}'가 포함되어 있습니다.\n\n남은 기회가 1회 차감됩니다.")
                self.update_display()
                self.check_game_status()
            else:
                messagebox.showinfo("알림", "더 이상 힌트가 없습니다.")
        else:
            messagebox.showwarning("경고", "남은 기회가 1회 이하이므로 힌트를 사용할 수 없습니다.")

    def update_display(self):
        """화면의 시각적 요소를 업데이트하는 함수."""
        self.word_label.configure(text=" ".join(self.guessed_word))
        self.hangman_label.configure(text=hangman_stages[len(hangman_stages) - 1 - self.attempts_left])
        
        for i in range(len(self.guess_dots)):
            if i < (len(hangman_stages) - 1 - self.attempts_left):
                self.guess_dots[i].configure(text_color="red")
            else:
                self.guess_dots[i].configure(text_color="green")

    def check_game_status(self):
        """게임의 승패를 확인하고 메시지를 보여주는 함수."""
        if '_' not in self.guessed_word:
            messagebox.showinfo("승리", f"축하합니다! 정답은 '{self.secret_word}'({self.secret_meaning})였습니다.🎉")
            self.learned_words[self.secret_word] = self.secret_meaning
            self.create_main_menu()
        elif self.attempts_left == 0:
            messagebox.showinfo("패배", f"가능 횟수를 초과하였습니다.😭\n정답은 '{self.secret_word}'({self.secret_meaning})였습니다.")
            self.create_main_menu()
            
    def show_learned_words(self):
        """맞힌 단어 목록을 보여주는 함수."""
        self.clear_frame()
        
        frame = ctk.CTkFrame(self, corner_radius=15)
        frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        ctk.CTkLabel(frame, text="맞힌 단어 목록", font=("Helvetica", 24, "bold")).pack(pady=10)
        
        if not self.learned_words:
            ctk.CTkLabel(frame, text="아직 맞힌 단어가 없습니다.", font=("Helvetica", 16)).pack(pady=20)
        else:
            text_widget = ctk.CTkTextbox(frame, height=250, width=400, font=("Helvetica", 14), corner_radius=10)
            text_widget.pack(pady=10, padx=10)
            text_widget.insert("end", "단어: 뜻\n" + "-"*20 + "\n")
            for word, meaning in self.learned_words.items():
                text_widget.insert("end", f"'{word}': {meaning}\n")
            text_widget.configure(state="disabled")
        
        ctk.CTkButton(frame, text="메인 메뉴로", font=("Helvetica", 18),
                      command=self.create_main_menu, width=200, height=40).pack(pady=10)

if __name__ == "__main__":
    app = HangmanApp()
    app.mainloop()