# Act 2 - Scene 4: Multiplexed Parallel Convolutions (MPCNN)
# Mã số file code đích: scenes/02_fhe_cnn/scene_04_multiplexed_conv.py
# Khung thời gian dự kiến: 01:45:00 -> 02:10:00 (25 phút)

## I. THÔNG TIN METADATA & ĐỒ HỌA CHUẨN
- Hệ màu sử dụng: COLOR_PLAINTEXT (Blue), COLOR_CIPHERTEXT (Red), COLOR_ENCRYPTION (Yellow), COLOR_MATH (White)
- Đối tượng Manim chủ đạo: CiphertextBlock (Packed), TensorCube, RotationArrow
- Trạng thái Audio: Giọng nói AI TTS - Nhịp điệu: Đột phá, hứng khởi, tốc độ giải thích nhanh và chính xác.

## II. KỊCH BẢN CHI TIẾT (STORYBOARD)

### Phân đoạn 4.1: Nghệ thuật đóng gói đa kênh - Multiplexed Packing (00:00 - 08:00)
- **Lời thoại AI (Audio Voiceover):**
  "To smash the sparsity bottleneck, Eunsang Lee introduced Multiplexed Parallel Convolutions. Instead of wasting slots, this technique stacks and packs multiple feature channels and spatial segments tightly into the SIMD slots of a single ciphertext. We transform loose data into a dense, hyper-efficient cryptographic tensor."
- **Hoạt ảnh Manim (Visual Actions):**
  1. Hiển thị một khối Rubik 3D đại diện cho Tensor ảnh đầu vào gồm nhiều kênh màu (Red, Green, Blue) và các Feature Maps.
  2. Một cánh tay robot ảo xuất hiện, thực hiện thao tác "tháo dỡ" khối Rubik, duỗi phẳng các kênh dữ liệu này và xếp chúng khít rịt vào nhau thành một hàng ngang liên tục.
  3. Toàn bộ hàng dữ liệu nén này được đẩy gọn gàng vào trong các ô slot của một chiếc `CiphertextBlock` màu đỏ duy nhất. Chữ "100% Slot Utilization" hiện lên rực rỡ.

### Phân đoạn 4.2: Cắt giảm Phép quay Bản mã - Reducing Rotations (08:00 - 16:00)
- **Lời thoại AI (Audio Voiceover):**
  "In encrypted convolutions, shifting data to align pixels requires a homomorphic operation called Ciphertext Rotation, which is computationally expensive. By multiplexing the channels in a specific interlocking layout, the shifting of one ciphertext slides all channels simultaneously. This elegant layout design eliminates redundant operations, cutting total rotations by sixty-two percent."
- **Hoạt ảnh Manim (Visual Actions):**
  1. Minh họa phép toán nhân ma trận truyền thống: Các mũi tên xoay vòng (`RotationArrow`) xuất hiện liên tục xung quanh hộp mã hóa, mỗi lần xoay tốn rất nhiều thời gian (thể hiện bằng thanh tải chậm).
  2. Đổi sang mô hình MPCNN: Khối dữ liệu đóng gói di chuyển. Khi một lệnh dịch chuyển được thực thi, một mũi tên đơn quét qua và làm dịch chuyển toàn bộ các kênh màu cùng một lúc (SIMD action).
  3. Một biểu đồ cột xuất hiện, cột "Naive Rotations" rất cao bị cắt phăng xuống chỉ còn 38% ở cột "MPCNN Rotations".

### Phân đoạn 4.3: Hiện thực hóa ResNet-20 và ResNet-110 trên FHE (16:00 - 25:00)
- **Lời thoại AI (Audio Voiceover):**
  "The implications are revolutionary. By combining multiplexed packing, optimized level consumption, and imaginary-removing bootstrapping, inference latency drops by over four-point-six times. For the first time in cryptographic history, deep networks like ResNet-20 and even the massive ResNet-110 can execute secure inference with standard one-hundred-and-twenty-eight-bit security."
- **Hoạt ảnh Manim (Visual Actions):**
  1. Vẽ sơ đồ kiến trúc mạng ResNet với các khối Skip Connection đặc trưng chồng chéo nhau trên màn hình.
  2. Các hộp `CiphertextBlock` chứa dữ liệu nén chạy mượt mà xuyên suốt qua hàng trăm tầng của ResNet-110 mà không bị dừng lại hay báo lỗi.
  3. Xuất hiện một chứng nhận đồ họa lớn lấp lánh ghi: "128-bit Post-Quantum Security Approved" cùng biểu tượng tốc độ "4.67x Faster".

## III. QUẢN LÝ TÀI NGUYÊN BỔ TRỢ (ASSETS MAPPING)
- Audio gốc: `assets/audio/act2_scene04_mpcnn_speedup.mp3`
- Tài liệu tham khảo lý thuyết: Toàn bộ cấu trúc toán học của Table 6 và Hình 9 trong file "lee22e.pdf".
- Tài liệu tham khảo lý thuyết: Toàn bộ cấu trúc toán học của Table 6 và Hình 9 trong file "lee22e.pdf".

## IV. EXPANDED CONTENT BEATS CHO BẢN 25 PHÚT
- Phân đoạn 4.1: tensor dimensions, flatten order, channel multiplexing, boundary masks, weight encoding, packed outputs và resource equation.
- Phân đoạn 4.2: rotation semantics, automorphism/key switching, redundant channel shifts, interlocking layout, masks/accumulation, operation counting và mức giảm 62%.
- Phân đoạn 4.3: residual paths, level planning, bootstrap schedule, imaginary removal, ResNet-20, ResNet-110, security parameters và kết quả speedup tổng hợp.
- Hai phân đoạn đầu gồm bảy content beats; phân đoạn ResNet gồm tám content beats, bên cạnh visual demonstration chính.
