import sys
import os
import re
from typing import List, Dict

def parse_log_line(line: str) -> Dict[str, str]:
    """Парсить рядок логу на складові частини."""
    parts = line.split(' ', 3) 
    if len(parts) < 4:
        return {}
    
    return {
        'date': parts[0],
        'time': parts[1],
        'level': parts[2],
        'message': parts[3]
    }

def load_logs(file_path: str) -> List[Dict[str, str]]:
    """Завантажує логи з файлу."""
    logs = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                parsed_line = parse_log_line(line.strip())
                if parsed_line:
                    logs.append(parsed_line)
    except FileNotFoundError:
        print(f"Файл не знайдено: {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Помилка при читанні файлу: {e}")
        sys.exit(1)

    return logs

def filter_logs_by_level(logs: List[Dict[str, str]], level: str) -> List[Dict[str, str]]:
    """Фільтрує логи за рівнем."""
    return [log for log in logs if log['level'].upper() == level.upper()]

def count_logs_by_level(logs: List[Dict[str, str]]) -> Dict[str, int]:
    """Підраховує кількість записів за рівнем логування."""
    counts = {}
    for log in logs:
        level = log['level']
        if level not in counts:
            counts[level] = 0
        counts[level] += 1
    return counts

def display_log_counts(counts: Dict[str, int]) -> None:
    """Виводить результати підрахунку в читабельному форматі."""
    print(f"{'Рівень логування':<15} | {'Кількість':<8}")
    print('-' * 30)
    for level, count in counts.items():
        print(f"{level:<15} | {count:<8}")

def main(file_path: str, level_filter: str = None) -> None:
    logs = load_logs(file_path)
    counts = count_logs_by_level(logs)
    display_log_counts(counts)

    if level_filter:
        filtered_logs = filter_logs_by_level(logs, level_filter)
        if filtered_logs:
            print(f"\nДеталі логів для рівня '{level_filter.upper()}':")
            for log in filtered_logs:
                print(f"{log['date']} {log['time']} - {log['message']}")
        else:
            print(f"Не знайдено записів для рівня '{level_filter.upper()}'.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Використання: python main.py <шлях до файлу логів> [рівень логування]")
        sys.exit(1)

    log_file_path = sys.argv[1]
    log_level_filter = sys.argv[2] if len(sys.argv) > 2 else None

    main(log_file_path, log_level_filter)