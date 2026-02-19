import os
import time
import subprocess
from datetime import datetime

def run_command(command):
    """Выполняет команду и возвращает результат"""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.returncode == 0, result.stdout, result.stderr

def setup_git():
    """Проверка и настройка Git"""
    print("🔧 Проверка Git...")
    
    # Проверяем наличие Git
    has_git, out, _ = run_command('git --version')
    if not has_git:
        print("❌ Git не найден! Установите Git с git-scm.com")
        return False
    
    print(f"✅ Git: {out.strip()}")
    
    # Проверяем наличие remote
    has_remote, out, _ = run_command('git remote -v')
    if not has_remote:
        print("❌ Нет remote репозитория!")
        print("Выполните: git remote add origin https://github.com/iiikpeki-cloud/mytubl.git")
        return False
    
    print("✅ Remote найден")
    return True

def auto_push():
    """Автоматический git push каждые 10 секунд"""
    
    if not setup_git():
        input("\nНажмите Enter для выхода...")
        return
    
    print("\n" + "="*60)
    print("🤖 АВТОМАТИЧЕСКИЙ GIT PUSH ЗАПУЩЕН!")
    print("="*60)
    print(f"📁 Папка: {os.path.abspath('.')}")
    print(f"🕒 Проверка каждые 10 секунд")
    print("📹 Кидайте видео в папку 'videos'")
    print("="*60 + "\n")
    
    last_change_time = time.time()
    changes_detected = False
    
    try:
        while True:
            # Проверяем изменения в папке
            has_changes, out, _ = run_command('git status --porcelain')
            
            if has_changes and not changes_detected:
                changes_detected = True
                last_change_time = time.time()
                print(f"\n🕒 {datetime.now().strftime('%H:%M:%S')} - Обнаружены изменения!")
                print("⏳ Жду 10 секунд для накопления изменений...")
            
            elif has_changes and changes_detected:
                # Если прошло 10 секунд с последнего изменения
                if time.time() - last_change_time >= 10:
                    print(f"\n🕒 {datetime.now().strftime('%H:%M:%S')} - Начинаю отправку...")
                    
                    # Запускаем бота для обновления index.html
                    print("🔄 Запуск бота...")
                    run_command('python bot.py')
                    
                    # Git команды
                    print("📤 Добавление в Git...")
                    run_command('git add .')
                    
                    # Коммит
                    commit_msg = f"авто-обновление {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                    run_command(f'git commit -m "{commit_msg}"')
                    
                    # Push
                    print("🚀 Push на GitHub...")
                    success, out, err = run_command('git push')
                    
                    if success:
                        print(f"✅ Успешно отправлено! {commit_msg}")
                        print("🌐 Netlify обновит сайт через 1-2 минуты")
                    else:
                        print(f"❌ Ошибка push: {err}")
                    
                    changes_detected = False
                    print("\n👀 Снова слежу за изменениями...")
            
            elif not has_changes:
                # Просто показываем точки
                print(".", end="", flush=True)
                changes_detected = False
            
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("\n\n👋 Авто-Git остановлен")
        print("До встречи!")

if __name__ == "__main__":
    # Переходим в папку скрипта
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    auto_push()