# word_manager.py
import os
import random
import json

class WordManager:
    def __init__(self):
        self.word_lists_path = "word_lists"
        self.my_wordbook_path = "data/my_wordbook.json"
        self.word_meaning_path = "data/word_meanings.json"
        self._ensure_files_exist()

    def _ensure_files_exist(self):
        if not os.path.exists(self.word_lists_path):
            os.makedirs(self.word_lists_path)
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists(self.my_wordbook_path):
            with open(self.my_wordbook_path, 'w', encoding='utf-8') as f:
                json.dump([], f)
        if not os.path.exists(self.word_meaning_path):
            sample_meanings = {
                "apple": {"meaning": "사과", "example": "An apple a day keeps the doctor away."},
                "banana": {"meaning": "바나나", "example": "Monkeys love to eat bananas."}
            }
            with open(self.word_meaning_path, 'w', encoding='utf-8') as f:
                json.dump(sample_meanings, f, ensure_ascii=False, indent=4)

    def get_word_list(self, filename):
        try:
            with open(os.path.join(self.word_lists_path, filename), 'r', encoding='utf-8') as f:
                words = [line.strip().lower() for line in f if line.strip()]
            return words
        except FileNotFoundError:
            return []

    def get_available_topics(self):
        try:
            files = [f.split('.')[0] for f in os.listdir(self.word_lists_path) if f.endswith('.txt')]
            return sorted(files)
        except FileNotFoundError:
            return []

    def create_topic(self, topic_name):
        """새로운 주제(.txt 파일)를 생성합니다."""
        if not topic_name.isalpha():
            print("⚠️ 주제 이름은 알파벳으로만 구성해주세요.")
            return
        filepath = os.path.join(self.word_lists_path, f"{topic_name}.txt")
        if os.path.exists(filepath):
            print(f"⚠️ '{topic_name}' 주제는 이미 존재합니다.")
            return
        with open(filepath, 'w', encoding='utf-8') as f:
            pass
        print(f"✅ 새로운 주제 '{topic_name}'이(가) 성공적으로 추가되었습니다.")
        print("   이제 '단어 추가하기' 메뉴에서 새 주제에 단어를 추가할 수 있습니다.")

    def delete_topic(self, topic_name):
        """주제(.txt 파일)를 삭제합니다."""
        if not topic_name:
            print("⚠️ 주제 이름이 입력되지 않았습니다.")
            return
        filepath = os.path.join(self.word_lists_path, f"{topic_name}.txt")
        if not os.path.exists(filepath):
            print(f"⚠️ '{topic_name}' 주제를 찾을 수 없습니다.")
            return
        try:
            os.remove(filepath)
            print(f"✅ 주제 '{topic_name}'이(가) 성공적으로 삭제되었습니다.")
        except OSError as e:
            print(f"⚠️ 파일을 삭제하는 중 오류가 발생했습니다: {e}")

    def get_word_by_topic(self, topic):
        words = self.get_word_list(f"{topic}.txt")
        return random.choice(words) if words else None

    def get_word_by_level(self, level):
        level_lengths = {'초급': (3, 5), '중급': (6, 8), '고급': (9, 99)}
        if level not in level_lengths:
            return None
        min_len, max_len = level_lengths[level]
        all_words = self._get_all_words()
        if not all_words:
            return None
        eligible_words = [word for word in all_words if min_len <= len(word) <= max_len]
        return random.choice(eligible_words) if eligible_words else None

    def _get_all_words(self):
        all_words = []
        topics = self.get_available_topics()
        for topic in topics:
            all_words.extend(self.get_word_list(f"{topic}.txt"))
        if not all_words:
            print("\n🔔 사용자 단어 목록이 없어, 기본 단어 목록으로 게임을 시작합니다.")
            all_words = ['apple', 'banana', 'python', 'game', 'student', 'teacher']
        return list(set(all_words))

    def get_random_word(self):
        all_words = self._get_all_words()
        return random.choice(all_words) if all_words else None

    def manage_words(self):
        # [수정] 주제 추가/삭제 및 뒤로가기 기능이 통합된 메뉴
        while True:
            print("\n[📖 단어/주제 관리]")
            print("1. 단어 추가하기")
            print("2. 단어 삭제하기")
            print("3. 전체 단어 목록 보기")
            print("4. 새로운 주제 추가하기 ✨")
            print("5. 주제 삭제하기 🗑️")
            print("6. 돌아가기")
            choice = input(">> 선택: ")

            if choice == '1':
                topic = input("추가할 단어의 주제를 입력하세요 (메뉴로 돌아가려면 Enter): ").lower()
                if not topic: continue
                word = input(f"'{topic}'에 추가할 단어를 입력하세요 (메뉴로 돌아가려면 Enter): ").lower()
                if not word: continue
                meaning = input(f"'{word}'의 뜻을 입력하세요 (메뉴로 돌아가려면 Enter): ")
                if not meaning: continue
                example = input(f"'{word}'의 예문을 입력하세요 (메뉴로 돌아가려면 Enter): ")
                if not example: continue
                self.add_word(topic, word, meaning, example)
            elif choice == '2':
                topic = input("삭제할 단어의 주제를 입력하세요 (메뉴로 돌아가려면 Enter): ").lower()
                if not topic: continue
                word = input(f"'{topic}'에서 삭제할 단어를 입력하세요 (메뉴로 돌아가려면 Enter): ").lower()
                if not word: continue
                self.delete_word(topic, word)
            elif choice == '3':
                self.view_all_words()
            elif choice == '4':
                new_topic = input("추가할 새로운 주제의 이름을 영어로 입력하세요 (메뉴로 돌아가려면 Enter): ").lower()
                if not new_topic: continue
                self.create_topic(new_topic)
            elif choice == '5':
                topics = self.get_available_topics()
                if not topics:
                    print("⚠️ 삭제할 수 있는 주제가 없습니다.")
                    continue
                print("--- 현재 주제 목록 ---")
                for t in topics:
                    print(f"- {t}")
                topic_to_delete = input("삭제할 주제의 이름을 입력하세요 (메뉴로 돌아가려면 Enter): ").lower()
                if not topic_to_delete: continue
                self.delete_topic(topic_to_delete)
            elif choice == '6':
                break
            else:
                print("⚠️ 잘못된 입력입니다.")

    def add_word(self, topic, word, meaning, example):
        if not word.isalpha():
            print("⚠️ 알파벳으로만 구성된 단어를 입력해주세요.")
            return
        filepath = os.path.join(self.word_lists_path, f"{topic}.txt")
        if not os.path.exists(filepath):
            print(f"⚠️ '{topic}' 주제를 찾을 수 없습니다. '주제 추가하기' 메뉴로 먼저 주제를 만들어주세요.")
            return
        existing_words = self.get_word_list(f"{topic}.txt")
        if word in existing_words:
            print(f"⚠️ 단어 '{word}'은(는) 이미 주제 '{topic}'에 존재합니다.")
            return
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(f"\n{word}")
        print(f"✅ 주제 '{topic}'에 단어 '{word}'이(가) 추가되었습니다.")
        try:
            with open(self.word_meaning_path, 'r', encoding='utf-8') as f:
                meanings_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            meanings_data = {}
        meanings_data[word] = {"meaning": meaning, "example": example}
        with open(self.word_meaning_path, 'w', encoding='utf-8') as f:
            json.dump(meanings_data, f, ensure_ascii=False, indent=4)
        print(f"✅ '{word}'의 뜻과 예문 정보가 저장되었습니다.")

    def delete_word(self, topic, word_to_delete):
        filepath = os.path.join(self.word_lists_path, f"{topic}.txt")
        deleted_from_txt = False
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                words = [line.strip() for line in f if line.strip()]
            if word_to_delete in words:
                words.remove(word_to_delete)
                with open(filepath, 'w', encoding='utf-8') as f:
                    for word in words:
                        f.write(f"{word}\n")
                print(f"✅ 주제 '{topic}'에서 단어 '{word_to_delete}'을(를) 삭제했습니다.")
                deleted_from_txt = True
            else:
                print(f"⚠️ 주제 '{topic}'에 '{word_to_delete}' 단어가 존재하지 않습니다.")
        except FileNotFoundError:
            print(f"⚠️ '{topic}'이라는 주제(파일)를 찾을 수 없습니다.")
        if deleted_from_txt:
            try:
                with open(self.word_meaning_path, 'r', encoding='utf-8') as f:
                    meanings_data = json.load(f)
                if word_to_delete in meanings_data:
                    del meanings_data[word_to_delete]
                    with open(self.word_meaning_path, 'w', encoding='utf-8') as f:
                        json.dump(meanings_data, f, ensure_ascii=False, indent=4)
                    print(f"✅ '{word_to_delete}'의 뜻과 예문 정보가 삭제되었습니다.")
            except (FileNotFoundError, json.JSONDecodeError):
                pass

    def view_all_words(self):
        topics = self.get_available_topics()
        if not topics:
            print("⚠️ 추가된 단어가 없습니다.")
            return
        for topic in topics:
            words = self.get_word_list(f"{topic}.txt")
            if words:
                print(f"\n--- 주제: {topic} ---")
                print(', '.join(words))

    def show_word_meaning(self, word):
        try:
            with open(self.word_meaning_path, 'r', encoding='utf-8') as f:
                meanings = json.load(f)
            info = meanings.get(word.lower())
            if info:
                print(f"\n--- '{word}' 단어 정보 ---")
                print(f"뜻: {info['meaning']}")
                print(f"예문: {info['example']}")
            else:
                print(f"⚠️ '{word}' 단어의 정보를 찾을 수 없습니다.")
        except (FileNotFoundError, json.JSONDecodeError):
            print("⚠️ 단어 정보 파일이 없거나 손상되었습니다.")

    def add_to_my_wordbook(self, word):
        with open(self.my_wordbook_path, 'r+', encoding='utf-8') as f:
            try:
                wordbook = json.load(f)
            except json.JSONDecodeError:
                wordbook = []
            if word not in wordbook:
                wordbook.append(word)
                f.seek(0)
                f.truncate()
                json.dump(wordbook, f, ensure_ascii=False, indent=4)
                print(f"✔️ '{word}'을(를) 나만의 단어장에 추가했습니다.")

    def manage_my_wordbook(self):
        try:
            with open(self.my_wordbook_path, 'r', encoding='utf-8') as f:
                wordbook = json.load(f)
            if not wordbook:
                print("\n텅 비어있습니다. 게임에서 단어를 틀리면 자동으로 추가됩니다.")
                return
            print("\n[📚 나만의 단어장]")
            sorted_wordbook = sorted(wordbook)
            for i, word in enumerate(sorted_wordbook, 1):
                print(f"{i}. {word}")
            while True:
                choice = input("\n단어의 뜻을 보려면 번호를, 돌아가려면 'q'를 입력하세요: ")
                if choice.lower() == 'q':
                    break
                try:
                    index = int(choice) - 1
                    if 0 <= index < len(sorted_wordbook):
                        self.show_word_meaning(sorted_wordbook[index])
                    else:
                        print("⚠️ 잘못된 번호입니다.")
                except ValueError:
                    print("⚠️ 숫자 또는 'q'를 입력해주세요.")
        except (FileNotFoundError, json.JSONDecodeError):
            print("⚠️ 단어장 파일을 찾을 수 없거나 파일이 비어있습니다.")