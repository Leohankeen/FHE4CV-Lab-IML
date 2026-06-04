# Computer Vision over Homomorphically Encrypted Data

## Chủ đề

Project triển khai demo **Computer Vision over Homomorphically Encrypted Data**
cho case **xử lý ảnh X-ray y tế bảo mật**. Mục tiêu là chứng minh rằng server
có thể tính toán một bước inference đơn giản trên dữ liệu đã mã hóa mà không
nhìn thấy ảnh gốc hoặc vector đặc trưng plaintext.

Thư viện chính:

- Manim: dựng animation giải thích pipeline.
- TenSEAL: CKKS encrypted vector và dot product.
- Pillow/Numpy: đọc ảnh, tiền xử lý và trích xuất đặc trưng.
- Pytest: kiểm thử pipeline lõi.

## Bài toán thực tế

Ảnh y tế như X-ray, CT, MRI là dữ liệu nhạy cảm. Trong mô hình cloud AI thông
thường, bệnh viện phải gửi ảnh hoặc feature plaintext lên server để inference.
Điều này tạo rủi ro về quyền riêng tư, quản trị dữ liệu, tuân thủ pháp lý và
rò rỉ thông tin bệnh nhân.

Homomorphic Encryption giải quyết một phần bài toán bằng cách cho phép server
tính trực tiếp trên ciphertext. Với CKKS, kết quả là approximate arithmetic,
phù hợp cho vector số thực và các mô hình tuyến tính hoặc neural network đã
được biến đổi để tránh phép toán không tương thích.

## Kiến trúc demo

Luồng xử lý trong project:

1. Client/bệnh viện đọc ảnh X-ray local trong `data/chestxray_sample/`.
2. Ảnh được chuyển grayscale, resize về `32x32`, chuẩn hóa về `[0, 1]`.
3. Client trích xuất 10 đặc trưng ảnh nhỏ:
   `mean`, `std`, trung bình 4 vùng, trung tâm, edge energy, bright ratio,
   dark ratio.
4. Client tạo CKKS context và mã hóa feature vector bằng TenSEAL.
5. Server nhận `Enc(x)` và tính:

   ```text
   Enc(x) dot w + b = Enc(score)
   ```

6. Client giải mã score và áp dụng sigmoid/threshold để lấy triage flag.

Server không có secret key, không giải mã được ảnh, feature hoặc score.

## Vì sao chọn linear triage score?

CNN đầy đủ trên FHE cần xử lý nhiều vấn đề: ReLU, max-pooling, batch norm,
độ sâu nhân ciphertext, noise budget, kích thước ciphertext và thời gian chạy.
Để demo đúng trọng tâm và chạy được trên máy cá nhân, project chọn encrypted
linear scoring. Đây là tầng nền tảng của encrypted inference:

- dot product là phép toán tự nhiên trong CKKS;
- dễ so sánh sai số encrypted-vs-plaintext;
- dễ giải thích bằng Manim;
- đủ để minh họa privacy boundary giữa client và server.

Model trong demo dùng trọng số cố định, không phải model y tế đã huấn luyện.
Kết quả chỉ phục vụ minh họa kỹ thuật, không dùng cho chẩn đoán.

## File quan trọng

- `scripts/medical_fhe_pipeline.py`: pipeline executable.
- `scripts/benchmark_tenseal.py`: benchmark thời gian, kích thước ciphertext và sai số.
- `scripts/train_plaintext_linear_model.py`: train/export model tuyến tính.
- `models/triage_linear_model.json`: model artifact mặc định dùng bởi pipeline và benchmark.
- `models/triage_linear_model_trained_demo.json`: model logistic-regression demo export từ script training.
- `notebooks/medical_fhe_tenseal_walkthrough.ipynb`: notebook walkthrough.
- `scenes/medical_fhe_pipeline_scene.py`: animation Manim.
- `scenes/fhe4cv_full_explainer.py`: animation Manim dạng video giải thích đầy đủ.
- `tests/test_medical_fhe_pipeline.py`: unit tests.
- `configs/manim.cfg`: cấu hình render.
- `scripts/youtube_meta.md`: metadata video trình bày.

## Cách chạy

Demo plaintext:

```powershell
python scripts/medical_fhe_pipeline.py --plaintext-only
```

Demo encrypted inference:

```powershell
python scripts/medical_fhe_pipeline.py
```

Xuất report:

```powershell
python scripts/medical_fhe_pipeline.py --write-report
```

Benchmark TenSEAL:

```powershell
python scripts/benchmark_tenseal.py --write-report
```

Train/export model:

```powershell
python scripts/train_plaintext_linear_model.py --output-model models/triage_linear_model.json
```

Mở notebook:

```powershell
jupyter lab notebooks/medical_fhe_tenseal_walkthrough.ipynb
```

Render Manim:

```powershell
python -m manim -c configs\manim.cfg -ql scenes\medical_fhe_pipeline_scene.py MedicalFHEPipeline
```

Render video giải thích đầy đủ:

```powershell
python -m manim -c configs\manim.cfg -ql scenes\fhe4cv_full_explainer.py FHE4CVFullExplainer
```

Chạy test:

```powershell
python -B -m pytest -q -p no:cacheprovider
```

## Kết quả kiểm thử trên workspace hiện tại

Pipeline đã xử lý 8 ảnh trong `data/chestxray_sample/`. Khi chạy TenSEAL CKKS,
sai số logit giữa encrypted inference và plaintext nằm khoảng `1e-7` đến
`1e-6`, phù hợp với tính chất approximate của CKKS.

Scene Manim đã render thành công tại:

```text
media/videos/medical_fhe_pipeline_scene/480p15/MedicalFHEPipeline.mp4
media/videos/fhe4cv_full_explainer/480p15/FHE4CVFullExplainer.mp4
```

Các file kết quả đã được tạo tại:

```text
outputs/medical_fhe_results.csv
outputs/medical_fhe_results.json
outputs/benchmark_tenseal.csv
outputs/benchmark_tenseal_summary.json
```

## Giới hạn

- Không dùng ảnh bệnh nhân thật hoặc nhãn chẩn đoán thật.
- Không triển khai CNN/FHE end-to-end.
- Feature extraction đang chạy phía client ở plaintext.
- Server mới tính linear score, chưa benchmark latency/bandwidth ciphertext.
- Chưa có quản lý key production-grade.

## Thành phần đã hoàn thiện thêm

Project hiện có đủ artefact cho một bài nộp/demo chuyên nghiệp:

- code inference chạy thật bằng TenSEAL;
- model artifact tách khỏi source code;
- training/export script cho workflow ML;
- benchmark script để có số liệu thực nghiệm;
- notebook walkthrough để giải thích từng bước;
- Manim scene ngắn và Manim scene dài;
- báo cáo kỹ thuật và metadata video;
- unit tests cho logic lõi.

## Hướng mở rộng

1. Huấn luyện logistic regression hoặc shallow MLP trên dataset X-ray có nhãn.
2. Chuẩn hóa feature theo thống kê train set và lưu model artifact.
3. Thử encrypted matrix-vector inference batch nhiều ảnh.
4. Đo thời gian mã hóa, inference, giải mã và kích thước serialized ciphertext.
5. Thay sigmoid bằng polynomial approximation nếu cần giữ toàn bộ hậu xử lý trên
   ciphertext.
6. So sánh TenSEAL với pipeline SEAL C++ cho latency và kiểm soát tham số thấp
   hơn.
