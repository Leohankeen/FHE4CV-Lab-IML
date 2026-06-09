# Act 2 - Scene 3: The Naive Translation Bottleneck
# Mã số file code đích: scenes/02_fhe_cnn/scene_03_naive_cnn_bottleneck.py
# Khung thời gian dự kiến: 01:35:00 -> 01:45:00 (10 phút)

## I. THÔNG TIN METADATA & ĐỒ HỌA CHUẨN
- Hệ màu sử dụng: COLOR_PLAINTEXT (Blue), COLOR_CIPHERTEXT (Red), COLOR_NOISE (Grey), COLOR_ENCRYPTION (Yellow)
- Đối tượng Manim chủ đạo: PlaintextBlock, CiphertextBlock, MatrixGrid
- Trạng thái Audio: Giọng nói AI TTS - Nhịp điệu: Trầm, cảnh báo, phân tích về sự lãng phí hiệu năng.

## II. KỊCH BẢN CHI TIẾT (STORYBOARD)

### Phân đoạn 3.1: Sự lãng phí không gian Slot (00:00 - 05:00)
- **Lời thoại AI (Audio Voiceover):**
  "A modern CKKS ciphertext contains tens of thousands of data slots, designed for massive SIMD parallel processing. If we naively translate a CNN by allocating only one pixel or one single channel per ciphertext, we leave over ninety-nine percent of the slots empty. This extreme data sparsity leads to severe resource underutilization."
- **Hoạt ảnh Manim (Visual Actions):**
  1. Vẽ một khối `CiphertextBlock` lớn màu đỏ đại diện cho 1 bản mã CKKS ($N=16384$ slots).
  2. Chia nhỏ khối này thành một lưới ma trận dài chứa hàng ngàn ô nhỏ (slots). 
  3. Hiệu ứng: Chỉ có duy nhất ô đầu tiên chứa một `PlaintextBlock` pixel ảnh màu xanh, toàn bộ các ô còn lại chuyển thành màu xám tối (`COLOR_NOISE`) kèm chữ "Empty Slot" để làm nổi bật sự lãng phí.

### Phân đoạn 3.2: Thảm họa nghẽn cổ chai Bootstrapping (05:00 - 10:00)
- **Lời thoại AI (Audio Voiceover):**
  "Every layer of convolution multiplies the image matrix by cryptographic weights, rapidly consuming the ciphertext level. When the level drops to zero, a heavy Bootstrapping process must be invoked. Performing Bootstrapping on thousands of sparse, mostly empty ciphertexts creates a massive computational bottleneck, exploding inference latency to hours."
- **Hoạt ảnh Manim (Visual Actions):**
  1. Trực quan hóa một luồng gồm rất nhiều hộp `CiphertextBlock` thưa thớt chạy trên một băng chuyền.
  2. Băng chuyền đi qua một trạm kiểm soát lớn có nhãn "Bootstrapping Gate". Trạm này xử lý cực kỳ chậm, khiến các hộp bản mã bị ùn ứ, xếp hàng dài dằng dặc.
  3. Xuất hiện một đồng hồ bấm giờ kỹ thuật số chạy tăng tốc chóng mặt, minh họa trực quan cho khái niệm "bùng nổ độ trễ tính toán" (latency explosion).

## III. QUẢN LÝ TÀI NGUYÊN BỔ TRỢ (ASSETS MAPPING)
- Audio gốc: `assets/audio/act2_scene03_naive_bottleneck.mp3`
- Tài liệu tham khảo lý thuyết: Slide giới thiệu "From Pytorch Models to SEAL FHE" (Phần phân tích hiệu năng tích chập thô sơ).
- Tài liệu tham khảo lý thuyết: Slide giới thiệu "From Pytorch Models to SEAL FHE" (Phần phân tích hiệu năng tích chập thô sơ).

## IV. EXPANDED CONTENT BEATS CHO BẢN 10 PHÚT
- Phân đoạn 3.1: SIMD model, scalar translation, tăng ciphertext count theo tensor, memory traffic và vai trò của data-layout contract.
- Phân đoạn 3.2: level consumption, chi phí refresh trên mỗi ciphertext, queue sparse ciphertext, độ trễ cộng dồn và yêu cầu dense packing.
- Mỗi phân đoạn gồm một visual demonstration và năm content beats; các số liệu utilization được giải thích thay vì chỉ hiện cảnh báo.
