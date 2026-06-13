# Computer Vision over Homomorphically Encrypted Data

Dự án được minh họa bằng Manim, CKKS và TenSEAL. Nội dung được tổ chức thành ba Act:

1. **Act 1 - Mathematical and Cryptographic Foundations**: nền tảng HE, CKKS, ciphertext operations, key management và Microsoft SEAL workflow.
2. **Act 2 - FHE-Friendly CNN**: ReLU barrier, polynomial approximation, bottleneck của CNN native và multiplexed convolution.
3. **Act 3 - Practical Demos**: CryptoFace, HERS, Private Image Matching và Medical X-Ray FHE.

Repo cũng chứa pipeline TenSEAL độc lập cho bài toán X-ray:

```text
X-ray image -> local feature extraction -> CKKS encryption -> encrypted linear score on cloud -> client decryption
```

> Đây là prototype phục vụ giảng dạy và minh họa, không phải hệ thống chẩn
> đoán lâm sàng.

## Cấu trúc dự án

```text
FHE4CV-Lab-IML/
|-- assets/
|   |-- audio/
|   |   |-- 01_math_crypto/
|   |   |-- 02_fhe_cnn/
|   |   `-- 03_demos/
|   `-- image/03_demos/
|-- configs/
|   `-- manim.cfg
|-- data/
|   `-- chestxray_sample/
|-- docs/
|-- models/
|-- notebooks/
|-- outputs/
|-- scenes/
|   |-- 01_math_crypto/
|   |-- 02_fhe_cnn/
|   |-- 03_demos/
|   `-- library/
|-- scripts/
|   |-- audio_manifest/
|   |   |-- act1_audio_manifest.json
|   |   |-- act2_audio_manifest.json
|   |   `-- act3_audio_manifest.json
|   |-- storyboards/
|   |   |-- 01_math_crypto/
|   |   |-- 02_fhe_cnn/
|   |   `-- 03_demos/
|   |-- build_scene.py
|   |-- generate_audio.py
|   |-- validate_audio.py
|   |-- medical_fhe_pipeline.py
|   |-- benchmark_tenseal.py
|   `-- train_plaintext_linear_model.py
|-- tests/
|-- README.md
`-- requirements.txt
```

Các thành phần quan trọng:

- [scenes/](scenes): toàn bộ scene Manim của ba Act.
- [scripts/storyboards/](scripts/storyboards): lời thoại AI, timeline và mô tả
  hoạt ảnh tương ứng với từng scene.
- [scripts/audio_manifest/](scripts/audio_manifest): ánh xạ storyboard, scene
  và file audio.
- [scripts/build_scene.py](scripts/build_scene.py): build một scene bất kỳ từ
  đường dẫn `.py`.
- [scripts/generate_audio.py](scripts/generate_audio.py): tạo narration từ
  phần `Lời thoại AI` trong storyboard.
- [scripts/validate_audio.py](scripts/validate_audio.py): kiểm tra manifest,
  storyboard, scene và các file audio.
- [scenes/library/](scenes/library): primitive và helper Manim dùng chung.
- [configs/manim.cfg](configs/manim.cfg): cấu hình Manim 1920x1080, 60 FPS.

## Cài đặt

### Windows PowerShell

Khuyến nghị dùng Python 3.11 hoặc 3.12:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
```

`edge-tts` đã có trong `requirements.txt`. TenSEAL đang là dependency tùy
chọn; cài thêm nếu cần chạy encrypted X-ray pipeline:

```powershell
python -m pip install tenseal
```

Nếu TenSEAL không cài được bằng pip trên Windows, có thể chuẩn bị toolchain qua
Conda:

```powershell
conda create -n fhe4cv python=3.10 -y
conda activate fhe4cv
conda install -c conda-forge cmake eigen pybind11
python -m pip install -r requirements.txt
python -m pip install tenseal
```

Với Python 3.13, nếu Manim báo thiếu `audioop`:

```powershell
python -m pip install audioop-lts
```

Để trộn nhạc nền trong `build_scene.py`, cần cài FFmpeg và thêm `ffmpeg` vào
`PATH`. Nếu FFmpeg hoặc `assets/audio/bgm.mp3` không tồn tại, script vẫn xuất
video với audio gốc của Manim.

## Thiết kế kỹ thuật

### Vì sao dùng TenSEAL?

TenSEAL là thư viện Python cho tensor/vector mã hóa, xây trên Microsoft SEAL.
Nó phù hợp cho demo vì hỗ trợ CKKS vector, dot product và thao tác vector-matrix
ở cấp Python. SEAL vẫn là nền tảng FHE mạnh ở C++, nhưng với project Manim +
notebook + script Python, TenSEAL giúp triển khai ngắn gọn hơn.

### Vì sao không chạy CNN đầy đủ trên ciphertext?

FHE hỗ trợ tốt cộng và nhân, nhưng các lớp CV phổ biến như ReLU, max-pooling,
batch normalization động và các mô hình sâu lớn cần biến đổi đáng kể để tương
thích FHE. Vì vậy project chọn hướng an toàn với kiến trúc tối giản nhưng đúng bản chất của encrypted inference cho demo:

- ảnh gốc không rời khỏi client;
- chỉ vector đặc trưng nhỏ được mã hóa;
- server tính linear score bằng dot product trên ciphertext;
- sigmoid/threshold cuối cùng thực hiện sau khi client giải mã.

## Danh sách scene

### Act 1 - Math and Crypto

| File | Manim class |
|---|---|
| `scenes/01_math_crypto/scene_01_he_foundations.py` | `HomomorphicEncryptionFoundations` |
| `scenes/01_math_crypto/scene_02_ckks_encoding.py` | `CKKSEncodingAndParameters` |
| `scenes/01_math_crypto/scene_03_ciphertext_operations.py` | `CiphertextOperations` |
| `scenes/01_math_crypto/scene_04_keys_and_seal_pipeline.py` | `KeysAndSEALPipeline` |

### Act 2 - FHE-Friendly CNN

| File | Manim class |
|---|---|
| `scenes/02_fhe_cnn/scene_01_relu_barrier.py` | `ReLuBarrier` |
| `scenes/02_fhe_cnn/scene_02_polynomial_approx.py` | `PolynomialApproximation` |
| `scenes/02_fhe_cnn/scene_03_naive_cnn_bottleneck.py` | `NaiveCNNBottleneck` |
| `scenes/02_fhe_cnn/scene_04_multiplexed_conv.py` | `MultiplexedPacking` |

### Act 3 - Practical Demos

| File | Manim class |
|---|---|
| `scenes/03_demos/scene_01_cryptoface_scene.py` | `CryptoFace` |
| `scenes/03_demos/scene_02_hers.py` | `HERS_System` |
| `scenes/03_demos/scene_03_PIM.py` | `PrivateImageMatching` |
| `scenes/03_demos/scene_04_Xray.py` | `XRayTriage` |

## Build một scene

### Cách 1: Dùng `build_scene.py`

- Quy trình thực hiện
  1. Đọc đường dẫn file `.py`;
  2. Phát hiện Manim Scene class;
  3. Tìm audio manifest tương ứng;
  4. Tạo lại narration bằng `generate_audio.py`;
  5. Render Manim;
  6. Trộn BGM nếu có;
  7. Xuất video vào `deliverables/scene_clips/`.

- Các tùy chọn chính:

  ```text
  --class-name NAME  Chọn class nếu file có nhiều Scene class
  --quality l|m|h|k  Chất lượng Manim, mặc định h
  --no-preview       Không mở video sau khi render
  --use-cache        Cho phép Manim dùng cache
  --skip-audio       Không tạo lại narration
  --skip-bgm         Không trộn BGM
  --bgm PATH         Dùng file BGM khác
  --dry-run          Chỉ in các lệnh sẽ chạy
  ```

- Hướng dẫn chạy:

  - Khi đang đứng tại project root:

    ```powershell
    python scripts/build_scene.py scenes/01_math_crypto/scene_01_he_foundations.py
    ```

  - Khi đang đứng trong thư mục `scripts`:

    ```powershell
    cd scripts
    python build_scene.py scenes/01_math_crypto/scene_01_he_foundations.py
    ```

  - Đường dẫn có thể thay bằng bất kỳ file scene `.py` nào trong `scenes/`:

    ```powershell
    python scripts/build_scene.py scenes/02_fhe_cnn/scene_02_polynomial_approx.py
      python scripts/build_scene.py scenes/03_demos/scene_04_Xray.py
    ```

  - Kiểm tra quy trình mà không tạo audio hoặc render:

    ```powershell
    python scripts/build_scene.py `
      scenes/03_demos/scene_01_cryptoface_scene.py `
      --dry-run
    ```

  - Render nhanh ở chất lượng thấp:

    ```powershell
    python scripts/build_scene.py `
      scenes/02_fhe_cnn/scene_01_relu_barrier.py `
      --quality l
    ```

  - Không mở video sau khi render:

    ```powershell
    python scripts/build_scene.py `
      scenes/01_math_crypto/scene_02_ckks_encoding.py `
      --no-preview
    ```

  - Giữ audio hiện tại, không gọi TTS:

    ```powershell
    python scripts/build_scene.py `
      scenes/03_demos/scene_02_hers.py `
      --skip-audio
    ```

  - Không trộn nhạc nền:

    ```powershell
    python scripts/build_scene.py `
      scenes/03_demos/scene_03_PIM.py `
      --skip-bgm
    ```

### Cách 2: Gọi lệnh Manim trực tiếp

Mỗi file scene hiện tại chỉ chứa một Manim Scene class, nên có thể gọi ngắn
chỉ bằng đường dẫn `.py` (Có thể thay đường dẫn trên bằng bất kỳ file `.py` nào trong ba thư mục Act
dưới `scenes/`.)

```powershell
python -m manim -pqh scenes/01_math_crypto/scene_01_he_foundations.py
```

Để lệnh luôn rõ ràng và không phụ thuộc số class trong file, nên ghi thêm tên
Manim class:

```powershell
python -m manim -pqh <path_scene.py> <ManimSceneClass>
```

Ví dụ:

```powershell
python -m manim -pqh `
  scenes/01_math_crypto/scene_01_he_foundations.py `
  HomomorphicEncryptionFoundations
```

Để dùng file config của repo:

```powershell
python -m manim -c configs/manim.cfg -pqh `
  scenes/01_math_crypto/scene_03_ciphertext_operations.py `
  CiphertextOperations
```

Các quality flag thường dùng:

```text
-pql  preview chất lượng thấp
-pqm  preview chất lượng trung bình
-pqh  preview chất lượng cao
-pqk  preview 4K
```

Khi gọi Manim trực tiếp, audio phải tồn tại trước nếu scene sử dụng
`add_sound()`. Cách này không tự gọi TTS và không trộn BGM.

## Tạo audio từ storyboard

File [generate_audio.py](scripts/generate_audio.py)  sẽ đọc phần Lời thoại AI (Audio Voiceover) trong các storyboard Markdown và tạo MP3 theo audio manifest.

Ví dụ:
- Tạo toàn bộ audio Act 2:

  ```powershell
  python scripts/generate_audio.py `
    --manifest scripts/audio_manifest/act2_audio_manifest.json
  ```

- Chỉ tạo một scene:

  ```powershell
  python scripts/generate_audio.py `
    --manifest scripts/audio_manifest/act3_audio_manifest.json `
    --scene scene_04_xray
  ```

- Liệt kê scene ID trong manifest:

  ```powershell
  python scripts/generate_audio.py `
    --manifest scripts/audio_manifest/act3_audio_manifest.json `
    --list
  ```

- Kiểm tra ánh xạ mà không ghi đè MP3:

  ```powershell
  python scripts/generate_audio.py `
    --manifest scripts/audio_manifest/act2_audio_manifest.json `
    --dry-run
  ```

- Có thể thay giọng và tốc độ:

  ```powershell
  python scripts/generate_audio.py `
    --manifest scripts/audio_manifest/act1_audio_manifest.json `
    --voice en-US-AvaMultilingualNeural `
    --rate=-10%
  ```

## Kiểm tra audio manifest

File `validate_audio.py` không có Act mặc định nên cần phải cung cấp `--manifest` hoặc
`--all`.

Ví dụ:

- Kiểm tra một Act:

  ```powershell
  python scripts/validate_audio.py `
    --manifest scripts/audio_manifest/act1_audio_manifest.json
  ```

- Kiểm tra một scene:

  ```powershell
  python scripts/validate_audio.py `
    --manifest scripts/audio_manifest/act3_audio_manifest.json `
    --scene scene_01_cryptoface_scene
  ```

- Kiểm tra tất cả manifest và yêu cầu mọi MP3 phải tồn tại:

  ```powershell
  python scripts/validate_audio.py --all --check-audio
  ```

- Đối chiếu các clip trong manifest với `add_sound()` hoặc `play_audio()` trong
scene:

  ```powershell
  python scripts/validate_audio.py `
    --manifest scripts/audio_manifest/act2_audio_manifest.json `
    --check-source-audio-refs
  ```

Quy trình thực hiện kiểm tra:

- JSON manifest hợp lệ;
- source `.py` và storyboard `.md` tồn tại;
- số khối voiceover khớp số nhóm audio;
- output audio không bị trùng;
- tổng thời lượng scene khớp manifest;
- cú pháp Python của scene;
- chapter và beat count nếu manifest khai báo `beat_methods`;
- MP3 tồn tại khi dùng `--check-audio`.

## X-ray TenSEAL pipeline

### Chạy plaintext (Không cần TenSEAL)

```powershell
python scripts/medical_fhe_pipeline.py --plaintext-only
```

### Chạy CKKS encrypted scoring

- Yêu cầu đã cài TenSEAL:

  ```powershell
  python scripts/medical_fhe_pipeline.py
  ```

- Dùng model cụ thể:

  ```powershell
  python scripts/medical_fhe_pipeline.py `
    --model-path models/triage_linear_model_trained_demo.json
  ```

- Ghi báo cáo JSON và CSV:

  ```powershell
  python scripts/medical_fhe_pipeline.py --write-report
  ```

- Sau khi chạy `--write-report`, kết quả sẽ được ghi vào:

  ```text
  outputs/medical_fhe_results.json
  outputs/medical_fhe_results.csv
  ```

## Benchmark TenSEAL

- Chạy benchmark cho TenSEAL

  ```powershell
  python scripts/benchmark_tenseal.py
  ```

- Ghi báo cáo:

  ```powershell
  python scripts/benchmark_tenseal.py --write-report
  ```

- Các chỉ số gồm:

  - thời gian preprocessing và plaintext scoring.
  - thời gian tạo CKKS ciphertext.
  - thời gian encrypted dot product.
  - thời gian decrypted.
  - kích thước serialized ciphertext.
  - sai số logit giữa encrypted và plaintext logit.

- Sau khi chạy `--write-report`, kết quả sẽ được ghi vào:

  ```text
  outputs/benchmark_tenseal.csv
  outputs/benchmark_tenseal_summary.json
  ```

## Train model plaintext
Định dạng labels được mô tả tại [docs/labels_format.md](docs/labels_format.md).

- Tạo model bằng pseudo-label deterministic phục vụ demo:

  ```powershell
  python scripts/train_plaintext_linear_model.py `
    --output-model models/triage_linear_model.json
  ```

- Train bằng nhãn CSV có cột `image,label`:

  ```powershell
  python scripts/train_plaintext_linear_model.py `
    --labels-csv data/chestxray_sample_labels_demo.csv `
    --output-model models/triage_linear_model.json
  ```

- Chạy thử mà không ghi model:

  ```powershell
  python scripts/train_plaintext_linear_model.py --dry-run
  ```

## Notebook

```powershell
jupyter lab notebooks/medical_fhe_tenseal_walkthrough.ipynb
```

## Chạy test

```powershell
python -B -m pytest -q -p no:cacheprovider
```

## Output
Tên output sẽ chứa đường dẫn của Act, tên file scene và Manim class để tránh trùng giữa các scene.
- Manim lưu bản render trung gian trong:

  ```text
  media/videos/
  ```

- `build_scene.py` lưu bản cuối cùng trong:

  ```text
  deliverables/scene_clips/
  ```

## Lưu ý kỹ thuật

- Storyboard Markdown là nguồn nội dung cho narration và mô tả hoạt ảnh.
- Act 1 dùng một MP3 dài cho mỗi scene.
- Act 2 và Act 3 dùng nhiều clip nhỏ vì scene gọi audio ở từng beat.
- `build_scene.py` mặc định tạo lại audio trước khi render. Dùng
  `--skip-audio` khi muốn giữ MP3 hiện có.
- Manim được chạy với `--disable_caching` mặc định trong `build_scene.py` để
  tránh tái sử dụng video cache không chứa audio mới. Dùng `--use-cache` nếu
  muốn render nhanh hơn.
- Secret key chỉ thuộc phía client trong các sơ đồ FHE; cloud chỉ nhận
  ciphertext và evaluation capabilities cần thiết.

## Nguồn tham khảo

- FHE4CV CVPR 2025 tutorial: https://fhe4cv.github.io/
- TenSEAL: https://github.com/OpenMined/TenSEAL
- Microsoft SEAL: https://github.com/microsoft/SEAL
