# FHE4CV-Lab-IML

Dự án minh họa chủ đề **Computer Vision over Homomorphically Encrypted Data**
với case thực tế: **xử lý ảnh X-ray y tế bảo mật**. Project dùng
**TenSEAL/CKKS** thay cho việc gọi trực tiếp Microsoft SEAL để có API Python
phù hợp với demo, notebook và Manim.

Ý tưởng cốt lõi:

1. Bệnh viện/client giữ ảnh X-ray gốc ở local.
2. Client trích xuất vector đặc trưng nhỏ từ ảnh và mã hóa bằng CKKS.
3. Cloud server chỉ nhận ciphertext và tính linear triage score:
   `Enc(x) dot w + b = Enc(score)`.
4. Chỉ client/doctor có secret key mới giải mã score.

> Prototype này dùng một score tuyến tính có trọng số cố định để minh họa
> quyền riêng tư và sai số CKKS. Đây không phải mô hình chẩn đoán lâm sàng.

## Cấu trúc chính

- [requirements.txt](requirements.txt): phụ thuộc Manim, OpenCV, Torch, TenSEAL.
- [configs/manim.cfg](configs/manim.cfg): cấu hình render Manim mặc định.
- [scripts/medical_fhe_pipeline.py](scripts/medical_fhe_pipeline.py): pipeline
  X-ray -> feature -> TenSEAL CKKS encrypted scoring -> decrypt result.
- [scripts/benchmark_tenseal.py](scripts/benchmark_tenseal.py): benchmark
  thời gian mã hóa, encrypted dot product, giải mã, sai số CKKS.
- [scripts/train_plaintext_linear_model.py](scripts/train_plaintext_linear_model.py):
  train/export logistic-regression model plaintext sang JSON dùng cho FHE demo.
- [scripts/storyboards/02_fhe_cnn/](scripts/storyboards/02_fhe_cnn):
  storyboard Act 2 cho phần FHE-friendly CNN, gồm lời thoại, visual actions và
  mapping audio.
- [scripts/render_act2_fhe_cnn.ps1](scripts/render_act2_fhe_cnn.ps1):
  render batch 4 scene Manim của Act 2.
- [models/triage_linear_model.json](models/triage_linear_model.json): model
  artifact mặc định, dễ giải thích, gồm feature order, weights, bias, threshold.
- [models/triage_linear_model_trained_demo.json](models/triage_linear_model_trained_demo.json):
  model logistic-regression demo export từ script training với nhãn demo.
- [notebooks/medical_fhe_tenseal_walkthrough.ipynb](notebooks/medical_fhe_tenseal_walkthrough.ipynb):
  notebook giải thích từng bước từ ảnh đến encrypted inference.
- [scenes/medical_fhe_pipeline_scene.py](scenes/medical_fhe_pipeline_scene.py):
  scene Manim giải thích luồng bảo mật.
- [scenes/fhe4cv_full_explainer.py](scenes/fhe4cv_full_explainer.py):
  scene Manim dài hơn cho video thuyết trình hoàn chỉnh.
- [scenes/02_fhe_cnn/](scenes/02_fhe_cnn):
  4 scene Manim về ReLU barrier, polynomial approximation, naive CNN
  bottleneck và multiplexed parallel convolutions.
- [docs/project_report_vi.md](docs/project_report_vi.md): báo cáo kỹ thuật
  tiếng Việt cho phần thuyết trình/nộp bài.
- [docs/labels_format.md](docs/labels_format.md): định dạng CSV nhãn cho
  training/export model.
- [scenes/library/](scenes/library): primitives dùng lại cho Manim.
- [tests/test_medical_fhe_pipeline.py](tests/test_medical_fhe_pipeline.py):
  kiểm thử tiền xử lý và plaintext scoring.
- `data/chestxray_sample/`: ảnh X-ray mẫu local để demo.

Cài đặt nhanh (Windows)
1. Tạo môi trường ảo và kích hoạt:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Cập nhật pip và cài đặt phụ thuộc:

```powershell
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

Ghi chú quan trọng cho TenSEAL
- Trên Windows, `tenseal` có thể cần trình biên dịch C++ (Visual Studio Build Tools) hoặc cài qua `conda` để tránh lỗi build. Nếu pip cài thất bại, thử:

```powershell
conda create -n fhe4cv python=3.10 -y
conda activate fhe4cv
conda install -c conda-forge cmake eigen pybind11
pip install -r requirements.txt
```

Ghi chú cho Manim trên Windows:
- Nên dùng Python 3.11 hoặc 3.12. Virtualenv Python 3.13 có thể lỗi khi Manim
  import Pydub vì `audioop` đã bị loại khỏi standard library.
- Nếu đã dùng Python 3.13 và gặp lỗi `No module named 'audioop'` hoặc
  `No module named 'pyaudioop'`, chạy:

```powershell
python -m pip install audioop-lts
```

  Dependency này cũng đã được thêm vào `requirements.txt` với marker cho
  Python 3.13.
- Nếu render bị lỗi encoding config trên Windows, đảm bảo `configs/manim.cfg`
  chỉ chứa comment ASCII như file hiện tại.

Hướng dẫn nhanh sử dụng
- Chạy demo plaintext trước để kiểm tra tiền xử lý:

```powershell
python scripts/medical_fhe_pipeline.py --plaintext-only
```

- Chạy demo mã hóa bằng TenSEAL/CKKS:

```powershell
python scripts/medical_fhe_pipeline.py
```

- Chạy demo với model artifact cụ thể:

```powershell
python scripts/medical_fhe_pipeline.py --model-path models/triage_linear_model.json
```

- Chạy demo với model trained-demo:

```powershell
python scripts/medical_fhe_pipeline.py --model-path models/triage_linear_model_trained_demo.json
```

- Ghi báo cáo JSON/CSV ra `outputs/`:

```powershell
python scripts/medical_fhe_pipeline.py --write-report
```

- Benchmark TenSEAL:

```powershell
python scripts/benchmark_tenseal.py
```

- Ghi benchmark CSV/JSON ra `outputs/`:

```powershell
python scripts/benchmark_tenseal.py --write-report
```

- Train/export model plaintext. Nếu chưa có nhãn thật, script sẽ tạo
  pseudo-label deterministic chỉ để demo:

```powershell
python scripts/train_plaintext_linear_model.py --output-model models/triage_linear_model.json
```

- Train với nhãn thật từ CSV có cột `image,label`:

```powershell
python scripts/train_plaintext_linear_model.py --labels-csv data/chestxray_sample_labels_demo.csv --output-model models/triage_linear_model.json
```

- Mở notebook walkthrough:

```powershell
jupyter lab notebooks/medical_fhe_tenseal_walkthrough.ipynb
```

- Render scene Manim chất lượng thấp để test nhanh:

```powershell
manim -c configs/manim.cfg -pql scenes/medical_fhe_pipeline_scene.py MedicalFHEPipeline
```

- Render video giải thích đầy đủ:

```powershell
manim -c configs/manim.cfg -pql scenes/fhe4cv_full_explainer.py FHE4CVFullExplainer
```

- Render Act 2 về FHE-friendly CNN:

```powershell
.\scripts\render_act2_fhe_cnn.ps1
```

Script luôn render nội dung đầy đủ theo storyboard, tổng thời lượng khoảng
70 phút: 15 phút cho scene 1, 20 phút cho scene 2, 10 phút cho scene 3 và
25 phút cho scene 4. Mỗi phân đoạn gồm visual demonstration và nhiều content
beats; thời lượng không được tạo bằng cách giữ một khung hình tĩnh.

- Render từng scene Act 2 riêng:

```powershell
python -m manim -c configs/manim.cfg -ql scenes/02_fhe_cnn/scene_01_relu_barrier.py ReLuBarrier
python -m manim -c configs/manim.cfg -ql scenes/02_fhe_cnn/scene_02_polynomial_approx.py PolynomialApproximation
python -m manim -c configs/manim.cfg -ql scenes/02_fhe_cnn/scene_03_naive_cnn_bottleneck.py NaiveCNNBottleneck
python -m manim -c configs/manim.cfg -ql scenes/02_fhe_cnn/scene_04_multiplexed_conv.py MultiplexedPacking
```

- Render chất lượng cao:

```powershell
manim -c configs/manim.cfg -pqh scenes/medical_fhe_pipeline_scene.py MedicalFHEPipeline
```

- Chạy test:

```powershell
python -B -m pytest -q -p no:cacheprovider
```

## Thiết kế kỹ thuật

### Vì sao dùng TenSEAL?

TenSEAL là thư viện Python cho tensor/vector mã hóa, xây trên Microsoft SEAL.
Nó phù hợp cho demo vì hỗ trợ CKKS vector, dot product và thao tác vector-matrix
ở cấp Python. SEAL vẫn là nền tảng FHE mạnh ở C++, nhưng với project Manim +
notebook + script Python, TenSEAL giúp triển khai ngắn gọn hơn.

### Vì sao không chạy CNN đầy đủ trên ciphertext?

FHE hỗ trợ tốt cộng và nhân, nhưng các lớp CV phổ biến như ReLU, max-pooling,
batch normalization động và các mô hình sâu lớn cần biến đổi đáng kể để tương
thích FHE. Vì vậy project chọn hướng an toàn cho demo:

- ảnh gốc không rời khỏi client;
- chỉ vector đặc trưng nhỏ được mã hóa;
- server tính linear score bằng dot product trên ciphertext;
- sigmoid/threshold cuối cùng thực hiện sau khi client giải mã.

Đây là kiến trúc tối giản nhưng đúng bản chất của encrypted inference.

## Benchmark và model artifact

Model được lưu ở `models/triage_linear_model.json` thay vì hard-code trong
pipeline. Điều này giúp pipeline giống một workflow ML thật hơn:

1. train/export model bằng plaintext;
2. lưu `feature_names`, `weights`, `bias`, `threshold`;
3. TenSEAL pipeline load artifact đó;
4. benchmark đo thời gian và sai số encrypted inference.

Benchmark hiện đo:

- preprocessing/scoring plaintext;
- thời gian tạo CKKS vector;
- thời gian encrypted dot product;
- thời gian decrypt;
- kích thước serialized ciphertext;
- sai số logit giữa encrypted và plaintext.

Sau khi chạy `--write-report`, các artefact kết quả nằm ở:

- `outputs/medical_fhe_results.csv`
- `outputs/medical_fhe_results.json`
- `outputs/benchmark_tenseal.csv`
- `outputs/benchmark_tenseal_summary.json`

Sau khi render Manim, video nằm ở:

- `media/videos/medical_fhe_pipeline_scene/480p15/MedicalFHEPipeline.mp4`
- `media/videos/fhe4cv_full_explainer/480p15/FHE4CVFullExplainer.mp4`
- `media/videos/scene_01_relu_barrier/480p15/ReLuBarrier.mp4`
- `media/videos/scene_02_polynomial_approx/480p15/PolynomialApproximation.mp4`
- `media/videos/scene_03_naive_cnn_bottleneck/480p15/NaiveCNNBottleneck.mp4`
- `media/videos/scene_04_multiplexed_conv/480p15/MultiplexedPacking.mp4`

## Kịch bản thuyết trình Manim

Scene `MedicalFHEPipeline` minh họa 4 bước:

1. Hospital/client giữ ảnh X-ray và tạo feature vector.
2. Client mã hóa feature vector thành CKKS ciphertext.
3. Cloud server tính `Enc(x) dot w + b` mà không có secret key.
4. Doctor/client giải mã `Enc(score)` để xem kết quả.

Scene dùng ảnh mẫu trong `data/chestxray_sample/000001-1.png` nếu file tồn tại;
nếu không, scene tự fallback sang placeholder text.

Scene `FHE4CVFullExplainer` phù hợp hơn cho video dài, gồm:

1. vấn đề privacy khi upload ảnh y tế plaintext;
2. trực giác Homomorphic Encryption;
3. pipeline TenSEAL/CKKS;
4. kết quả demo và giới hạn hiện tại.

Act 2 trong `scenes/02_fhe_cnn/` mở rộng phần CNN trên FHE:

1. `ReLuBarrier`: vì sao ReLU/max cần so sánh và không tương thích trực tiếp
   với ciphertext CKKS;
2. `PolynomialApproximation`: thay ReLU bằng đa thức, trade-off giữa sai số và
   multiplicative depth, cùng ý tưởng imaginary-removing bootstrapping;
3. `NaiveCNNBottleneck`: minh họa lãng phí SIMD slot và nghẽn cổ chai
   bootstrapping khi dịch CNN theo cách ngây thơ;
4. `MultiplexedPacking`: minh họa multiplexed packing, giảm ciphertext
   rotations và dòng dữ liệu qua ResNet block.

Nếu có file audio TTS tương ứng trong `assets/audio/`, các scene Act 2 sẽ tự
gắn âm thanh bằng `self.add_sound(...)`; nếu chưa có audio, scene vẫn render
bình thường.

Các khung thời gian trong storyboard là thời lượng mặc định của scene. Nội dung
được chia thành các visual demonstration, walkthrough, giải thích kỹ thuật,
ví dụ và recap riêng thay vì kéo dài một khung hình tĩnh.

## Nguồn tham chiếu

- FHE4CV CVPR 2025 tutorial: https://fhe4cv.github.io/
- TenSEAL: https://github.com/OpenMined/TenSEAL
- Microsoft SEAL: https://github.com/microsoft/SEAL
