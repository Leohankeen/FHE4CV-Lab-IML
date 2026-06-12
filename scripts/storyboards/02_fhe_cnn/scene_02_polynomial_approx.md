# Act 2 - Scene 2: Bending the Curve - Polynomial Approximation
# Mã số file code đích: scenes/02_fhe_cnn/scene_02_polynomial_approx.py
# Khung thời gian dự kiến: 01:15:00 -> 01:35:00 (20 phút)

## I. THÔNG TIN METADATA & ĐỒ HỌA CHUẨN
- Hệ màu sử dụng: COLOR_PLAINTEXT (Blue), COLOR_CIPHERTEXT (Red), COLOR_ENCRYPTION (Yellow), COLOR_MATH (White)
- Đối tượng Manim chủ đạo: Axes, CustomFunctionPlot, CiphertextBlock
- Trạng thái Audio: Giọng nói AI TTS - Nhịp điệu: Giải thích học thuật, nhấn mạnh vào các hệ số toán học.

## II. KỊCH BẢN CHI TIẾT (STORYBOARD)

### Phân đoạn 2.1: Ý tưởng xấp xỉ đa thức (00:00 - 07:00)
- **Lời thoại AI (Audio Voiceover):**
  "To bypass the non-linearity barrier, we look into numerical analysis. Since FHE natively supports addition and multiplication, we can evaluate any polynomial function. Therefore, we replace the sharp, broken line of ReLU with a smooth, continuous polynomial curve that minimizes the approximation error."
- **Hoạt ảnh Manim (Visual Actions):**
  1. Khởi tạo hệ trục tọa độ `Axes` lớn ở trung tâm màn hình. Vẽ đồ thị hàm ReLU $f(x) = \max(0, x)$ màu đỏ nhấp nháy.
  2. Xuất hiện một dòng text toán học bằng LaTeX: $P(x) = \sum_{i=0}^{n} c_i x^i$. Các toán tử $+$ và $\times$ trong công thức được highlight bằng `COLOR_ENCRYPTION`.
  3. Hiệu ứng chuyển đổi: Đồ thị ReLU gãy khúc từ từ bị biến dạng, các góc nhọn được bo tròn mềm mại để biến thành một đường cong parabol mượt mà.

### Phân đoạn 2.2: Thuật toán Tối ưu hóa của AutoFHE (07:00 - 14:00)
- **Lời thoại AI (Audio Voiceover):**
  "However, not all polynomials are born equal. A naive Taylor series fails outside a narrow interval. AutoFHE dynamically optimizes the polynomial degree and coefficients, minimizing the composite error of the entire network rather than just a single layer. It balances the trade-off between multiplicative depth and classification accuracy."
- **Hoạt ảnh Manim (Visual Actions):**
  1. Hiển thị đồng thời 3 đường cong đa thức đại diện cho bậc 2, bậc 4 và bậc 6 với các màu sắc khác nhau.
  2. Thể hiện một vùng sai số (Error Margin) dạng dải mờ giữa đồ thị ReLU gốc và đường đa thức. 
  3. Khi AutoFHE tối ưu hóa, dải sai số này co hẹp lại. Một thanh đo "Multiplicative Depth" (Độ sâu nhân tính) tăng dần khi bậc đa thức tăng, cảnh báo nguy cơ cạn kiệt mức (Level Consumption) của CKKS.

### Phân đoạn 2.3: Imaginary-Removing Bootstrapping (14:00 - 20:00)
- **Lời thoại AI (Audio Voiceover):**
  "During these high-degree polynomial evaluations, homomorphic noise grows rapidly, forcing frequent Bootstrapping. In deep architectures like ResNet, the slot-to-coefficient transformations inside Bootstrapping introduce stray complex imaginary components. Lee et al. proposed Imaginary-Removing Bootstrapping to systematically wipe out these errors, preventing catastrophic divergence."
- **Hoạt ảnh Manim (Visual Actions):**
  1. Hiển thị cấu trúc vector các slots dữ liệu của CKKS. Quá trình tính toán đa thức làm xuất hiện các đốm nhiễu xám (`COLOR_NOISE`) xung quanh dữ liệu thực.
  2. Phóng to vào một slot dữ liệu, xuất hiện phần thực (Real) và một bóng mờ đại diện cho phần ảo lỗi (Imaginary Error).
  3. Một bộ lọc đồ họa quét qua vector, triệt tiêu hoàn toàn phần ảo mờ, trả lại sự hội tụ chính xác cho luồng tính toán của mạng ResNet sâu.

## III. QUẢN LÝ TÀI NGUYÊN BỔ TRỢ (ASSETS MAPPING)
- Audio gốc: `assets/audio/act2_scene02_poly_approx.mp3`
- Tài liệu tham khảo lý thuyết: Bài báo "AutoFHE" (Mục tối ưu hóa hàm kích hoạt) và bài báo của Eunsang Lee (ICML 2022 - Thuật toán Imaginary-Removing).

## IV. EXPANDED CONTENT BEATS CHO BẢN 20 PHÚT
- Phân đoạn 2.1: miền xấp xỉ, ý nghĩa hệ số, thứ tự đánh giá Horner/cây cân bằng, sai số tích lũy và fine-tuning nhận biết đa thức.
- Phân đoạn 2.2: giới hạn Taylor, so sánh bậc 2/4/6, phân bổ degree theo layer, mục tiêu accuracy toàn mạng và execution plan của AutoFHE.
- Phân đoạn 2.3: level exhaustion, các bước bootstrapping, biểu diễn complex slot, imaginary leakage, phép chiếu loại phần ảo và tác động lên ResNet sâu.
- Mỗi phân đoạn gồm một visual demonstration và sáu content beats có chuyển động tiến trình.