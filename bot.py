import os
import time
from datetime import datetime

# Папки
VIDEO_FOLDER = "videos"
INDEX_FILE = "index.html"

# Создаем папку для видео
os.makedirs(VIDEO_FOLDER, exist_ok=True)

def get_videos():
    """Получает список видео из папки"""
    videos = []
    
    if not os.path.exists(VIDEO_FOLDER):
        return videos
    
    for file in os.listdir(VIDEO_FOLDER):
        if file.lower().endswith(('.mp4', '.avi', '.mkv', '.mov', '.wmv')):
            file_path = os.path.join(VIDEO_FOLDER, file)
            size_mb = os.path.getsize(file_path) / (1024 * 1024)
            created = datetime.fromtimestamp(os.path.getctime(file_path))
            
            videos.append({
                'file': file,
                'title': file.rsplit('.', 1)[0],
                'size': f"{size_mb:.1f} MB",
                'date': created.strftime('%Y-%m-%d')
            })
    
    return videos

def create_html(videos):
    """Создает HTML страницу с видео"""
    
    html = f'''<!DOCTYPE html>
<html>
<head>
    <title>MyTube</title>
    <meta charset="utf-8">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Segoe UI', Arial, sans-serif;
            background: #0f0f0f;
            color: white;
            padding: 20px;
        }}
        .header {{
            background: linear-gradient(45deg, #ff0000, #cc0000);
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            text-align: center;
        }}
        .logo {{
            font-size: 60px;
            font-weight: bold;
        }}
        .video-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 25px;
        }}
        .video-card {{
            background: #1a1a1a;
            border-radius: 12px;
            overflow: hidden;
            cursor: pointer;
            transition: all 0.3s;
            border: 1px solid #333;
        }}
        .video-card:hover {{
            transform: translateY(-5px);
            border-color: #ff0000;
        }}
        .video-thumb {{
            width: 100%;
            height: 200px;
            background: linear-gradient(135deg, #2a2a2a, #1a1a1a);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 60px;
            color: #ff0000;
        }}
        .video-info {{
            padding: 20px;
        }}
        .video-title {{
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 10px;
        }}
        .video-meta {{
            display: flex;
            justify-content: space-between;
            color: #aaa;
            font-size: 14px;
        }}
        .player-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.98);
            display: none;
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }}
        .player-container {{
            width: 90%;
            max-width: 1000px;
        }}
        video {{
            width: 100%;
            max-height: 70vh;
        }}
        .close-btn {{
            position: absolute;
            top: 20px;
            right: 20px;
            background: #ff0000;
            color: white;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 30px;
            cursor: pointer;
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">🎬 MyTube</div>
        <p>Автоматическое обновление</p>
    </div>
    
    <div class="video-grid" id="videoGrid">'''
    
    for v in videos:
        html += f'''
        <div class="video-card" onclick="playVideo('{v['file']}')">
            <div class="video-thumb">🎬</div>
            <div class="video-info">
                <div class="video-title">{v['title']}</div>
                <div class="video-meta">
                    <span>📁 {v['size']}</span>
                    <span>📅 {v['date']}</span>
                </div>
            </div>
        </div>'''
    
    html += f'''
    </div>
    
    <div class="player-overlay" id="playerOverlay">
        <div class="close-btn" onclick="closePlayer()">✕</div>
        <div class="player-container">
            <video id="videoPlayer" controls>
                <source src="" type="video/mp4">
            </video>
        </div>
    </div>

    <script>
        function playVideo(file) {{
            const player = document.getElementById('videoPlayer');
            const overlay = document.getElementById('playerOverlay');
            player.src = 'videos/' + file;
            overlay.style.display = 'flex';
            player.play();
        }}
        
        function closePlayer() {{
            const player = document.getElementById('videoPlayer');
            const overlay = document.getElementById('playerOverlay');
            player.pause();
            player.src = '';
            overlay.style.display = 'none';
        }}
    </script>
</body>
</html>'''
    
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ Сайт обновлен! Видео: {len(videos)}")
    return len(videos)

if __name__ == "__main__":
    print("🎬 MyTube Bot запущен...")
    videos = get_videos()
    count = create_html(videos)
    print(f"✅ Готово! {count} видео") 
