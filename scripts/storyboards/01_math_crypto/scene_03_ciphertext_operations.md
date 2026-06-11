# Act 1 - Scene 3: Ciphertext Structure and Homomorphic Operations
# Mã số file code đích: scenes/01_math_crypto/scene_03_ciphertext_operations.py
# Khung thời gian dự kiến: 00:30:00 -> 00:45:00 (15 phút)

## I. THÔNG TIN METADATA & ĐỒ HỌA CHUẨN
- Hệ màu sử dụng: COLOR_CIPHERTEXT (Red), COLOR_ENCRYPTION (Yellow), COLOR_NOISE (Grey), COLOR_MATH (White).
- Đối tượng Manim chủ đạo: CiphertextBlock, polynomial component cards, level/scale badges và RotationArrow từ `scenes/library/`.
- Trạng thái Audio: Giọng nói AI TTS (Tiếng Anh) - Nhịp điệu: Phân tích từng bước, dừng ngắn sau các thuật ngữ `c-zero`, `c-one`, `relinearization`, `rescale` và `parms I-D`.

## II. KỊCH BẢN CHI TIẾT (STORYBOARD)

### Phân đoạn 3.1: Giải phẫu một CKKS Ciphertext (00:00 - 05:00)
- **Lời thoại AI (Audio Voiceover):**
  "A C-K-K-S ciphertext is a structured numerical object, not a locked scalar. A fresh public-key ciphertext commonly contains two polynomial components, written c-zero of X and c-one of X. Each component is represented across the active Residue Number System primes and contains many machine-word coefficients.

  Decryption combines these components with the Secret Key polynomial. At an intuitive level, the expression c-zero plus c-one times s reconstructs the encoded message together with a small error term. The trusted client then applies the C-K-K-S decoder to recover the packed approximate values.

  The polynomial data is only part of the object. Microsoft SEAL also tracks metadata that determines whether an operation is legal. The parameter identifier records the position in the modulus chain. The scale records the numerical magnitude used by C-K-K-S encoding. The ciphertext size records the number of polynomial components. Operands that represent compatible values can still fail an operation if their levels, scales, or encryption parameters do not agree.

  Ciphertexts may be serialized and transferred between processes, but the receiver must reconstruct a compatible SEALContext. Serialization does not include decryption authority. The Secret Key remains a separate object, and a ciphertext by itself should reveal neither the plaintext nor the key. Correct deployment therefore requires discipline over both cryptographic bytes and their parameter context."

- **Hoạt ảnh Manim (Visual Actions):**
  1. Mở một `CiphertextBlock` thành hai thẻ lớn `c0(X)` và `c1(X)`; phóng to để thấy nhiều hệ số RNS bên trong mỗi thẻ.
  2. Đưa SecretKey polynomial `s(X)` từ phía Client vào công thức trực giác `c0 + c1*s = encoded message + error`; sau đó ẩn SecretKey trở lại.
  3. Gắn ba badge lên ciphertext: `size = 2`, `scale = 2^40`, `parms_id = level 3`.
  4. Đưa hai ciphertext có scale hoặc level khác nhau vào cổng cộng; cổng báo `Mismatch`, sau đó căn chỉnh metadata để phép cộng thành công.
  5. Minh họa serialize thành byte stream gửi qua mạng, rồi load bằng một `SEALContext` tương thích; SecretKey không xuất hiện trong gói dữ liệu.

### Phân đoạn 3.2: Add, Multiply và Relinearize (05:00 - 10:00)
- **Lời thoại AI (Audio Voiceover):**
  "Homomorphic addition is the simplest encrypted operation. Compatible ciphertext components are added polynomial by polynomial, and the decoded slots approximate element-wise sums. Addition is relatively inexpensive and does not consume another level of the coefficient-modulus chain.

  Multiplication is more demanding. A ciphertext can be multiplied by an encoded plaintext constant, which is useful when model weights are public. A ciphertext-ciphertext multiplication protects both operands but increases runtime, approximation error, and scale. Multiplying two size-two ciphertexts produces a size-three result containing a term associated with the square of the Secret Key.

  Relinearization uses RelinKeys to transform this enlarged ciphertext back toward the standard size-two form without decrypting it. RelinKeys contain key-switching material related to powers of the Secret Key, but they do not independently reveal plaintext. Their purpose is to maintain a manageable ciphertext representation for later operations.

  A common C-K-K-S maintenance sequence is multiply, relinearize, and rescale. Multiplication creates component and scale growth. Relinearization reduces component count. Rescaling removes an active coefficient-modulus prime and stabilizes the scale. These steps solve different problems, so none should be described as a generic cleanup operation. The evaluator must execute them according to a circuit plan."

- **Hoạt ảnh Manim (Visual Actions):**
  1. Đặt hai ciphertext size-2 cạnh nhau; thực hiện cộng theo từng component và hiển thị output vẫn có `size = 2`.
  2. So sánh hai nhánh: `Ciphertext × Plaintext weight` và `Ciphertext × Ciphertext`; nhánh thứ hai được đánh dấu chi phí cao hơn.
  3. Cho `(c0,c1) × (d0,d1)` mở rộng thành ba thẻ `(e0,e1,e2)`; badge scale đổi từ `S` thành `S^2`.
  4. Đưa `RelinKeys` vào khối key switching, biến `(e0,e1,e2)` thành `(r0,r1)` nhưng giữ biểu tượng khóa đóng.
  5. Hiện pipeline bảo trì `Multiply -> Relinearize -> Rescale`; dưới mỗi khối ghi đúng trạng thái được xử lý: `scale/size/level`.

### Phân đoạn 3.3: Levels, Rescale, Rotations và Packed Dot Product (10:00 - 15:00)
- **Lời thoại AI (Audio Voiceover):**
  "Microsoft SEAL organizes compatible parameter sets into a modulus-switching chain. Moving downward removes coefficient-modulus primes and produces a lower chain index. Two operands generally need to meet at a compatible level before they can be combined.

  Modulus switching and C-K-K-S rescaling are related but not identical concepts. Modulus switching changes the active coefficient modulus. Rescaling additionally divides the C-K-K-S scale by the removed prime so that the decoded numerical value remains approximately unchanged. A developer must track both chain position and scale.

  Rotations solve a different problem. Slot-wise multiplication cannot by itself combine values from different positions. A Galois automorphism, followed by key switching with GaloisKeys, cyclically permutes the packed slots. Only rotation capabilities represented by the available keys can be evaluated.

  Consider a packed dot product. First, multiply a feature vector by a weight vector slot by slot. Next, rotate partial results by powers of two and add them. After logarithmically many rotation-and-add stages, the sum is replicated into a target slot. This pattern demonstrates how complex tensor operations emerge from a small set of encrypted primitives.

  Before selecting parameters, count multiplicative depth, record scale after every multiplication, determine where levels must align, and list every required rotation. The Evaluator does not discover this schedule at runtime. It executes a cryptographic circuit designed in advance."

- **Hoạt ảnh Manim (Visual Actions):**
  1. Vẽ modulus chain theo chiều dọc; hai ciphertext bắt đầu ở level khác nhau, sau đó một ciphertext được mod-switch xuống level tương thích.
  2. Minh họa riêng `ModSwitch` và `Rescale`: cả hai bỏ một prime, nhưng chỉ Rescale cập nhật scale từ gần `S^2` về gần `S`.
  3. Xoay vector `[1,2,3,4]` thành `[4,1,2,3]` bằng `RotationArrow`; GaloisKeys phát sáng ở thời điểm key switching.
  4. Trình diễn dot product: slot-wise multiply, rotate 1, add, rotate 2, add; cuối cùng hiện tổng trong mọi slot mục tiêu.
  5. Kết thúc bằng checklist bốn dòng: `Depth`, `Scale`, `Level`, `Rotations`; đánh dấu hoàn tất trước khi chuyển sang key management.

## III. QUẢN LÝ TÀI NGUYÊN BỔ TRỢ (ASSETS MAPPING)
- Audio gốc: `assets/audio/01_math_crypto/scene_03_ciphertext_operations.mp3`
- Ảnh/plate minh họa dự kiến: `assets/image/01_math_crypto/scene_03_ciphertext_arithmetic.png`
- Thư viện Manim dùng chung: CiphertextBlock, SlotGrid, constants và storyboard pacing từ `scenes/library/`
- Tài liệu tham khảo lý thuyết: Microsoft SEAL `native/examples/3_levels.cpp`, `5_ckks_basics.cpp`, `6_rotation.cpp` và `7_serialization.cpp`.

## IV. EXPANDED CONTENT BEATS CHO BẢN 15 PHÚT
- Phân đoạn 3.1: tuple of ring polynomials, RNS limbs, decryption intuition, size/scale/parms_id, compatibility và serialization boundary.
- Phân đoạn 3.2: homomorphic addition, ciphertext-plaintext multiply, ciphertext-ciphertext multiply, size growth, RelinKeys và maintenance schedule.
- Phân đoạn 3.3: modulus-chain levels, mod switch versus rescale, Galois automorphism, packed dot product và circuit-planning checklist.
- Mỗi phân đoạn gồm một visual demonstration và năm content beats thay đổi liên tục; không dùng một khung hình tĩnh để lấp thời lượng.
