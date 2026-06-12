# Act 2 - Scene 1: The Non-Linearity Wall
# Mã số file code đích: scenes/02_fhe_cnn/scene_01_relu_barrier.py
# Khung thời gian dự kiến: 01:00:00 -> 01:15:00 (15 phút)

## I. THÔNG TIN METADATA & ĐỒ HỌA CHUẨN
- Hệ màu sử dụng: COLOR_PLAINTEXT (Blue), COLOR_CIPHERTEXT (Red), COLOR_ENCRYPTION (Yellow)
- Đối tượng Manim chủ đạo: CiphertextBlock, PlaintextBlock (từ library.ehe_primitives)
- Trạng thái Audio: Giọng nói AI TTS - Nhịp điệu: Chậm, nhấn mạnh thuật ngữ chuyên ngành.

## II. KỊCH BẢN CHI TIẾT (STORYBOARD)

### Phân đoạn 1.1: Nhắc lại kiến trúc CNN truyền thống (00:00 - 05:00)
- **Lời thoại AI (Audio Voiceover):**
  "In a standard Convolutional Neural Network, linear layers like Convolution work hand in hand with non-linear activation functions, primarily ReLU, defined as Max of zero and x. This combination allows the network to learn complex, high-dimensional visual patterns."
- **Hoạt ảnh Manim (Visual Actions):**
  1. Vẽ một lưới ma trận đại diện cho ảnh đầu vào bằng `PlaintextBlock` màu xanh.
  2. Một bộ lọc (Kernel) quét qua ma trận tạo hiệu ứng tích chập tuyến tính.
  3. Giá trị đầu ra đi qua một Node hình tròn có nhãn "ReLU". Đồ thị hàm số $f(x) = \max(0, x)$ hiện lên sắc nét với góc gãy đặc trưng tại gốc tọa độ.

### Phân đoạn 1.2: Rào cản Mật mã học của RNS-CKKS (05:00 - 10:00)
- **Lời thoại AI (Audio Voiceover):**
  "However, when we shift this architecture into the Homomorphic Encryption domain using schemes like RNS-CKKS, a fundamental mathematical barrier arises. FHE ciphertexts are algebraic structures—specifically, polynomial rings. They naturally support only two basic arithmetic operations: homomorphic addition and homomorphic multiplication."
- **Hoạt ảnh Manim (Visual Actions):**
  1. Hiệu ứng làm mờ ma trận xanh, thay thế bằng các hộp mã hóa `CiphertextBlock` màu đỏ bao quanh bởi các ký hiệu toán học hạt nhân.
  2. Hai ký hiệu lớn $\oplus$ (cộng đồng cấu) và $\otimes$ (nhân đồng cấu) xuất hiện rực rỡ bằng `COLOR_ENCRYPTION`.
  3. Mũi tên luồng dữ liệu bảo mật chạy mượt mà qua hai phép toán này để chứng minh tính tương thích tuyệt đối.

### Phân đoạn 1.3: Khi ReLU làm FHE "Bó tay" (10:00 - 15:00)
- **Lời thoại AI (Audio Voiceover):**
  "The $\max(0, x)$ function is non-differentiable at zero and cannot be formed by a finite sequence of additions and multiplications. To evaluate a maximum, a processor must compare two values. But in FHE, data is completely cloaked. The cloud server is completely blind; it cannot know which value is larger without decrypting the data, which fundamentally violates privacy. This is the non-linearity wall."
- **Hoạt ảnh Manim (Visual Actions):**
  1. Khối `CiphertextBlock` (màu đỏ) di chuyển tiến đến Node tròn "ReLU".
  2. Node "ReLU" đột ngột chuyển sang màu đỏ cảnh báo, xuất hiện biểu tượng ổ khóa lớn xám xịt phủ lên. Ký hiệu toán học $\max(0, x)$ nhấp nháy báo lỗi.
  3. Hiệu ứng camera thu nhỏ (Zoom out) để lộ một bức tường lớn ngăn cách luồng dữ liệu mã hóa, minh họa trực quan cho khái niệm "bức tường phi tuyến tính".

## III. QUẢN LÝ TÀI NGUYÊN BỔ TRỢ (ASSETS MAPPING)
- Audio gốc: `assets/audio/act2_scene01_relu_barrier.mp3`
- Tài liệu tham khảo cấu trúc: slide "From Pytorch Models to SEAL FHE" (Trang rào cản tính toán).
- Tài liệu tham khảo cấu trúc: slide "From Pytorch Models to SEAL FHE" (Trang rào cản tính toán).

## IV. EXPANDED CONTENT BEATS CHO BẢN 15 PHÚT
- Phân đoạn 1.1: cấu trúc Conv-Bias-ReLU, ví dụ kernel 3x3, feature maps, giới hạn của chuỗi lớp tuyến tính, vai trò của góc gãy ReLU.
- Phân đoạn 1.2: biểu diễn ciphertext polynomial, SIMD slots, phép cộng, phép nhân, rescaling, modulus chain và giới hạn instruction set.
- Phân đoạn 1.3: max như một phép so sánh ẩn, branching trên dữ liệu mã hóa, chi phí secure comparison, round-trip decryption và kết luận thiết kế FHE-friendly.
- Mỗi phân đoạn gồm một visual demonstration và năm content beats thay đổi liên tục; không dùng một khung hình tĩnh để lấp thời lượng.