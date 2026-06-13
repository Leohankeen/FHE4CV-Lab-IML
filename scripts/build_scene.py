import os
import sys
import subprocess
import shutil

def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except FileNotFoundError:
        return False

def build_scene(scene_number):
    print(f"\n{'='*50}\n🚀 BẮT ĐẦU XÂY DỰNG SCENE {scene_number}\n{'='*50}")

    scenes = {
        "1": {"script": "scenes/02_fhe_cnn/scene_01_relu_barrier.py", "class": "ReLuBarrier"},
        "2": {"script": "scenes/02_fhe_cnn/scene_02_polynomial_approx.py", "class": "PolynomialApproximation"},
        "3": {"script": "scenes/02_fhe_cnn/scene_03_naive_cnn_bottleneck.py", "class": "NaiveCNNBottleneck"},
        "4": {"script": "scenes/02_fhe_cnn/scene_04_multiplexed_conv.py", "class": "MultiplexedPacking"}
    }

    if scene_number not in scenes:
        print("❌ Lỗi: Vui lòng nhập số Scene hợp lệ (1, 2, 3, hoặc 4).")
        sys.exit(1)

    scene_info = scenes[scene_number]

    print("\n🎧 Bước 1: Khởi tạo Audio TTS...")
    subprocess.run([sys.executable, "scripts/generate_audio.py"], check=True)

    print(f"\n🎬 Bước 2: Render Hình ảnh & TTS qua Manim cho {scene_info['class']}...")
    print("⏳ Đang sử dụng cờ '--disable_caching' để XÓA CACHE. Sẽ mất thời gian nhưng đảm bảo 100% KHÔNG MẤT TIẾNG.")
    
    # THÊM CỜ --disable_caching ĐỂ ÉP MANIM RENDER LẠI TOÀN BỘ, TRÁNH LỖI LẤY LẠI VIDEO CÂM CŨ
    manim_cmd = [
        "manim", "-pqh", "--disable_caching", scene_info["script"], scene_info["class"]
    ]
    subprocess.run(manim_cmd, check=True)

    video_dir = f"media/videos/{os.path.basename(scene_info['script']).split('.')[0]}/1080p60"
    raw_video = os.path.join(video_dir, f"{scene_info['class']}.mp4")
    
    if not os.path.exists(raw_video):
        print("❌ Lỗi: Không tìm thấy Video Manim sinh ra.")
        sys.exit(1)

    output_dir = "deliverables/scene_clips"
    os.makedirs(output_dir, exist_ok=True)
    final_output = os.path.join(output_dir, f"Scene_0{scene_number}_Final.mp4")

    bgm_path = "assets/audio/bgm.mp3"
    
    print(f"\n🎶 Bước 3: Mix Âm thanh nền (BGM) & Kích Volume Giọng đọc...")
    
    if os.path.exists(bgm_path) and check_ffmpeg():
        print("-> Đã phát hiện Nhạc nền. Đang tiến hành hòa trộn...")
        # Lệnh FFmpeg đã được Fix:
        # [0:a]volume=2.5: KÍCH volume giọng đọc AI lên 250% để bù trừ việc amix làm nhỏ tiếng.
        # [1:a]volume=0.12: Giữ volume nhạc nền ở mức 12% để du dương phía sau.
        ffmpeg_mix_cmd = [
            "ffmpeg", "-y", 
            "-i", raw_video, 
            "-stream_loop", "-1", "-i", bgm_path, 
            "-filter_complex", "[0:a]volume=2.5[voice];[1:a]volume=0.12[bgm];[voice][bgm]amix=inputs=2:duration=first:dropout_transition=2",
            "-c:v", "copy", 
            "-c:a", "aac", "-b:a", "192k", 
            "-shortest", final_output
        ]
        
        try:
            subprocess.run(ffmpeg_mix_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"\n✅ HOÀN TẤT! Video (ÂM THANH CỰC RÕ) tại: {final_output}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Lỗi Mix Audio FFmpeg: {e.stderr.decode('utf-8')}")
            shutil.copy2(raw_video, final_output)
    else:
        print("-> Không tìm thấy 'assets/audio/bgm.mp3'. Chỉ copy video thuần.")
        shutil.copy2(raw_video, final_output)
        print(f"\n✅ HOÀN TẤT! Video (Không có BGM) tại: {final_output}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Cách sử dụng: python scripts/build_scene.py <số_scene>")
        print("Ví dụ: python scripts/build_scene.py 1")
    else:
        build_scene(sys.argv[1])