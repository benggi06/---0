# game_data.py
import json
import os
from datetime import datetime

class GameData:
    def __init__(self, filepath="data/game_records.json"):
        self.filepath = filepath
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """기록 파일이 없으면 기본 구조로 생성합니다."""
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w', encoding='utf-8') as f:
                initial_data = {"total_games": 0, "wins": 0, "best_time": None, "history": []}
                json.dump(initial_data, f, indent=4)

    def record_game(self, word, won, elapsed_time=None):
        """게임 결과를 기록 파일에 저장합니다."""
        with open(self.filepath, 'r+', encoding='utf-8') as f:
            records = json.load(f)

            records["total_games"] += 1
            if won:
                records["wins"] += 1
                if elapsed_time and (records["best_time"] is None or elapsed_time < records["best_time"]):
                    records["best_time"] = round(elapsed_time, 2)

            # 플레이 이력 추가
            game_log = {
                "word": word,
                "result": "승리" if won else "패배",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            records["history"].insert(0, game_log) # 최신 기록을 맨 앞에 추가
            records["history"] = records["history"][:20] # 최근 20개 기록만 저장

            f.seek(0)
            json.dump(records, f, indent=4)

    def show_records(self):
        """저장된 게임 기록을 화면에 표시합니다."""
        with open(self.filepath, 'r', encoding='utf-8') as f:
            records = json.load(f)

        print("\n[🏆 게임 기록]")
        wins = records.get("wins", 0)
        total = records.get("total_games", 0)
        win_rate = (wins / total * 100) if total > 0 else 0
        best_time = records.get("best_time")

        print(f"총 플레이 횟수: {total}회")
        print(f"승리 횟수: {wins}회")
        print(f"승률: {win_rate:.2f}%")
        if best_time:
            print(f"최고 기록 (성공 시): {best_time}초")
        else:
            print("최고 기록: 아직 없음")

        print("\n--- 최근 플레이 이력 ---")
        history = records.get("history", [])
        if not history:
            print("플레이 기록이 없습니다.")
        else:
            for log in history:
                print(f"[{log['time']}] 단어: {log['word']}, 결과: {log['result']}")