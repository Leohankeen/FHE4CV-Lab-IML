# Act 3 - Scene 1: CryptoFace - End-to-End Encrypted Face Recognition
# Mã số file code đích: scenes/03_demos/scene_01_cryptoface_scene.py
# Khung thời gian dự kiến: 00:00:00 -> 00:15:00 (15 phút)

## I. THÔNG TIN METADATA & ĐỒ HỌA CHUẨN
- Hệ màu sử dụng: COLOR_PLAINTEXT (Blue), COLOR_CIPHERTEXT (Red), COLOR_ENCRYPTION (Yellow)
- Đối tượng Manim chủ đạo: CiphertextBlock, PlaintextBlock, ResNetBlock (từ library.ehe_primitives)
- Trạng thái Audio: Giọng nói AI TTS (Tiếng Anh) - Nhịp điệu: Chậm, học thuật, có các khoảng nghỉ dài (3-5s) giữa các câu để đồ họa di chuyển.

## II. KỊCH BẢN CHI TIẾT (STORYBOARD)

### Phân đoạn 1.1: Đặt vấn đề & Khái niệm cốt lõi (00:00 - 03:30)
- **Lời thoại AI (Audio Voiceover):**
  "Welcome to the third and final act of our presentation. In the previous sections, we established the mathematical foundations of Fully Homomorphic Encryption. Now, we will explore how to deploy these theoretical concepts into a highly complex, real-world application: Biometric Face Recognition. 
  
  When we look at standard biometric systems today, they rely heavily on Point-to-Point encryption, such as TLS or SSL. While your data is protected during transmission, it must be decrypted into plaintext once it reaches the cloud server so that neural networks can process the image. In cryptography, we often model these servers as 'Honest-but-Curious'. They execute the protocols correctly, but they might try to learn as much as possible from the user's data. If such a server is compromised by a hacker, your immutable biometric data—your face—is exposed forever. 
  
  CryptoFace was engineered to completely eliminate this vulnerability. It stands as the first truly end-to-end encrypted face recognition system. In this architecture, the entire pipeline—from feature extraction to database storage and similarity matching—is performed strictly on Ciphertexts. The server computes complex visual patterns without ever holding a decryption key, guaranteeing absolute privacy for the users."

- **Hoạt ảnh Manim (Visual Actions):**
  1. Vẽ mô hình mạng lưới cơ bản: Client gửi ảnh (Plaintext) lên máy chủ Đám mây.
  2. Tại Đám mây, xuất hiện biểu tượng cảnh báo đỏ rực: "⚠️ HACKER EXPLOIT (Data Leaked)" mô phỏng rủi ro khi giải mã.
  3. Xóa mô hình cũ, thay thế bằng giải pháp FHE: Ảnh gốc được bọc trong `CiphertextBlock` (hiện ổ khóa) ngay tại thiết bị, bay lên đám mây kèm theo dòng chữ "Direct Computation on Ciphertext (No Decryption Needed)".

### Phân đoạn 1.2: Kiến trúc CryptoFaceNet & Tối ưu CKKS (03:30 - 07:30)
- **Lời thoại AI (Audio Voiceover):**
  "However, integrating Homomorphic Encryption into modern Deep Learning introduces a massive mathematical barrier known as Multiplicative Depth. In the RNS-CKKS scheme, every ciphertext carries a specific noise budget. Each time two ciphertexts are multiplied, this noise grows exponentially. If we pass encrypted data through a standard, deep Convolutional Neural Network like ResNet or VGG, the noise budget will be completely exhausted, resulting in a catastrophic data collapse where decryption yields only garbage values. 
  
  To bypass this fundamental limitation, the researchers designed CryptoFaceNet using a Patch-based processing strategy. Instead of feeding the entire image into a deep network, the input face is divided into a grid of non-overlapping patches. 
  
  Each discrete patch is encrypted independently. Then, utilizing the SIMD—Single Instruction, Multiple Data—capabilities of the CKKS scheme, the server packs these patches and processes them through a very shallow neural network called a Patch CNN. This parallel evaluation strategy not only prevents noise accumulation, keeping the multiplicative depth well within safe limits, but it also dramatically reduces the computational latency on the server side."

- **Hoạt ảnh Manim (Visual Actions):**
  1. Hiển thị một mạng CNN sâu (gồm nhiều khối ResNetBlock nối tiếp). Dùng chữ "Noise Accumulation -> CKKS Data Collapse" màu đỏ để minh họa sự sụp đổ.
  2. Mạng CNN sâu biến mất. Một bức ảnh khuôn mặt hiện ra, bị cắt thành lưới ma trận $8 \times 8$ các ô vuông nhỏ rời rạc (patches).
  3. Mũi tên từ các ô vuông bay song song vào nhiều hộp "PCNN" nhỏ rải rác để biểu diễn luồng chạy Parallel Evaluation bằng SIMD.

### Phân đoạn 1.3: Luồng Đăng ký - Enrollment (07:30 - 11:30)
- **Lời thoại AI (Audio Voiceover):**
  "Now, let us trace the precise cryptographic data flow of the system. The framework is strictly divided into two boundaries: the trusted Client environment and the untrusted Cloud Server. The lifecycle begins with the Enrollment phase. 
  
  On the trusted Client device, the user captures a reference face. The device generates a pair of cryptographic keys and uses the Public Key to lock the image into a ciphertext. This encrypted tensor, alongside an identity ID, is transmitted to the cloud. 
  
  Once the cloud receives the ciphertext, the magic of FHE begins. The server pushes the encrypted image through the CryptoFaceNet architecture. Through Homomorphic Feature Extraction, the network performs convolutions and linear transformations on the polynomial rings, eventually outputting a highly compressed facial feature vector. It is crucial to understand that this vector was generated entirely in the encrypted domain—the server is completely blind to its contents. Finally, the server performs Blind Storage, saving this locked vector into the database under the user's ID, successfully enrolling the user with zero privacy leakage."

- **Hoạt ảnh Manim (Visual Actions):**
  1. Hiển thị màn hình chia 4 layout ($2 \times 2$). Focus vào nửa trên. Khởi tạo ảnh `reference face` và `identity ID` tại vùng Client.
  2. Chìa khóa Public Key (màu xanh) xuất hiện, khóa ảnh lại thành một khối `CiphertextBlock` có biểu tượng ổ khóa.
  3. Khối Ciphertext bay xuyên qua PCNN trên vùng Server, tạo thành cột Feature Vector đỏ. Vector này và Identity ID cùng trôi vào hình trụ Database.

### Phân đoạn 1.4: Luồng Xác thực - Verification (11:30 - 15:00)
- **Lời thoại AI (Audio Voiceover):**
  "Months or even years later, the user returns for Verification. The camera at the Client captures a new live probe face. This new image is immediately locked with the Public Key and sent to the Server along with a claimed ID. 
  
  The server receives the data and pushes this new encrypted image through the Patch CNN to generate a fresh probe feature vector. Simultaneously, it uses the claimed ID to query the database and retrieve the old encrypted reference vector. 
  
  Now comes the Secure Comparison. The Server performs homomorphic subtraction and squaring to calculate the L2 Euclidean distance between these two vectors. To finalize the matching, the server homomorphically subtracts an allowable error threshold from the distance score. The result of this complex math is still a tightly locked ciphertext box. 
  
  This result box is sent back to the Client. Only the Client device, securely holding the Secret Key, can perform the Local Thresholding Decryption. It opens the box to reveal a simple positive or negative value, confirming whether access is granted or denied. The cloud server learns absolutely nothing—not your face, not your features, not even the matching score. This concludes a mathematically perfect biometric security cycle."

- **Hoạt ảnh Manim (Visual Actions):**
  1. Focus xuống nửa dưới màn hình. Khởi tạo ảnh `probe face` và khối `claimed ID`. Lặp lại quy trình bọc ổ khóa mã hóa tại Client.
  2. Gửi `claimed ID` sang Database để kéo cột `Reference Vector` cũ ra, đặt cạnh `Probe Vector` mới vừa trích xuất từ PCNN.
  3. Nối 2 vector lại với nhau để tính `score`, sau đó áp dụng công thức `result = score - threshold` tạo thành hộp Result có gắn ổ khóa.
  4. Hộp Result bay ngược về Client. Secret Key (chìa khóa đỏ) đâm vào khối Decrypt, mở hộp ra để lộ dòng chữ "✅ Access Granted".

## III. QUẢN LÝ TÀI NGUYÊN BỔ TRỢ (ASSETS MAPPING)
- Audio gốc: `assets/audio/cryptoface_full.mp3` (Khuyến nghị dùng `edge-tts` với speed rate -15% để đạt độ dài tối đa).
- Hình ảnh đầu vào: `assets/reference_face.jpg`, `assets/probe_face.jpg`
- Tài liệu tham khảo cấu trúc: slide/paper "CryptoFace: End-to-End Encrypted Face Recognition" (CVPR 2025).

## IV. EXPANDED CONTENT BEATS CHO BẢN 15 PHÚT
- Phân đoạn 1.1: So sánh trực quan cơ chế Point-to-Point vs End-to-End Encryption, định nghĩa khái niệm Honest-but-Curious Cloud Server, và các rủi ro bảo mật sinh trắc học hiện nay.
- Phân đoạn 1.2: Minh họa trực quan độ sâu nhân (Multiplicative Depth) của hệ mã CKKS, lý giải tại sao mạng sâu phá hủy ciphertext, và cơ chế bù trừ của Patch-based CNN nhằm song song hóa (SIMD) các phép tính FHE.
- Phân đoạn 1.3: Trình diễn lộ trình biến đổi dữ liệu chi tiết của Enrollment: Mã hóa -> Truyền tải -> Đánh giá đồng hình trích xuất đặc trưng (Homomorphic Feature Extraction) -> Lưu trữ vector mù (Blind Storage).
- Phân đoạn 1.4: Trình diễn lộ trình Verification: Yêu cầu định danh -> Tạo probe vector đồng hình -> Tính toán khoảng cách (Secure Comparison) -> Giải mã và xác thực ngưỡng cục bộ (Local Thresholding Decryption).
- Mỗi phân đoạn gồm một visual demonstration và năm content beats thay đổi liên tục; không dùng một khung hình tĩnh để lấp thời lượng.