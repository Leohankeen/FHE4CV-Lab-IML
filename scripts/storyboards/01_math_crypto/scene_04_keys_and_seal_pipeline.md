# Act 1 - Scene 4: Keys and the Microsoft SEAL Workflow
# Mã số file code đích: scenes/01_math_crypto/scene_04_keys_and_seal_pipeline.py
# Khung thời gian dự kiến: 00:45:00 -> 01:00:00 (15 phút)

## I. THÔNG TIN METADATA & ĐỒ HỌA CHUẨN
- Hệ màu sử dụng: COLOR_PLAINTEXT (Blue), COLOR_CIPHERTEXT (Red), COLOR_ENCRYPTION (Yellow), Green cho trusted key material.
- Đối tượng Manim chủ đạo: key capability cards, PlaintextBlock, CiphertextBlock và sơ đồ đối tượng SEAL từ `scenes/library/`.
- Trạng thái Audio: Giọng nói AI TTS (Tiếng Anh) - Nhịp điệu: Tổng kết, mạch lạc, phân biệt rõ SecretKey, PublicKey, RelinKeys, GaloisKeys và các lớp API của Microsoft SEAL.

## II. KỊCH BẢN CHI TIẾT (STORYBOARD)

### Phân đoạn 4.1: Họ khóa và nguyên tắc phân quyền tối thiểu (00:00 - 05:00)
- **Lời thoại AI (Audio Voiceover):**
  "Homomorphic Encryption uses several key objects because each operation grants a different cryptographic capability. Treating every key as interchangeable would create both conceptual confusion and an unsafe deployment.

  KeyGenerator samples the Secret Key polynomial. Decryptor uses this key to recover plaintext, so it must remain inside the trusted client boundary. Exposure of the Secret Key compromises the confidentiality of ciphertexts created under that key.

  The Public Key enables randomized public-key encryption. A data producer can encrypt without learning the Secret Key. Depending on the architecture, the Public Key may remain on the client or be distributed to approved producers. Public means shareable for encryption; it does not mean that the object has no security role.

  Relinearization Keys support key switching after ciphertext multiplication. They transform terms associated with higher powers of the Secret Key back to the standard ciphertext form. Galois Keys support selected automorphisms, which appear in C-K-K-S as slot rotations and conjugation. These evaluation keys let the cloud maintain and rearrange encrypted data, but they do not provide ordinary decryption.

  Evaluation keys can be large, and generating every possible rotation wastes memory. A least-privilege design creates only the capabilities required by the circuit, sends only those keys to the server, and keeps Secret Key access isolated, audited, and recoverable through a deliberate key lifecycle."

- **Hoạt ảnh Manim (Visual Actions):**
  1. Dựng lưới 2x2 gồm bốn key card: `SecretKey`, `PublicKey`, `RelinKeys`, `GaloisKeys`.
  2. Đóng dấu `CLIENT ONLY` lên SecretKey; thử đưa nó sang Cloud thì trust boundary chuyển đỏ và hành động bị chặn.
  3. Dùng PublicKey khóa một PlaintextBlock thành CiphertextBlock; nhãn quyền hạn chỉ ghi `Encrypt`.
  4. Cho RelinKeys tác động lên ciphertext size-3 và GaloisKeys tác động lên SlotGrid rotation; cả hai thao tác kết thúc mà không mở khóa dữ liệu.
  5. Hiện biểu đồ kích thước key material khi tạo tất cả rotations so với chỉ các bước cần thiết; chốt bằng `Least privilege for cryptographic capabilities`.

### Phân đoạn 4.2: Các đối tượng cốt lõi trong Microsoft SEAL (05:00 - 10:00)
- **Lời thoại AI (Audio Voiceover):**
  "The Microsoft SEAL workflow begins with EncryptionParameters. For C-K-K-S, the developer selects the scheme type, polynomial modulus degree, and coefficient-modulus chain. These choices define the cryptographic universe in which every later object must operate.

  SEALContext validates the parameters, checks security-related constraints, constructs the modulus-switching chain, and stores precomputed context data. Parameter identifiers from this context allow Plaintext and Ciphertext objects to prove where they belong in the chain.

  KeyGenerator creates the Secret Key and can produce the Public Key, Relinearization Keys, and Galois Keys. CKKSEncoder maps vectors of real or complex values into Plaintext objects at a chosen scale. Encryptor converts a Plaintext into a randomized Ciphertext. Decryptor performs the trusted inverse operation, after which CKKSEncoder decodes the approximate slots.

  Evaluator is the server-side workbench. It performs operations such as add, multiply, relinearize, rescale, modulus switch, and rotate. Evaluator does not need the Secret Key, but it requires compatible ciphertexts, plaintexts, parameters, levels, scales, and the appropriate evaluation keys.

  The separation of these objects mirrors the separation of responsibilities. Encoding is not encryption. Evaluation is not decryption. Context compatibility is not key ownership. Keeping these boundaries explicit is essential for writing correct and reviewable SEAL applications."

- **Hoạt ảnh Manim (Visual Actions):**
  1. Xếp các thẻ API theo thứ tự: `EncryptionParameters -> SEALContext -> KeyGenerator`.
  2. Từ KeyGenerator tách nhánh tạo SecretKey, PublicKey, RelinKeys và GaloisKeys; dùng màu khác nhau cho trusted key và evaluation keys.
  3. Dựng pipeline dữ liệu `vector -> CKKSEncoder -> Plaintext -> Encryptor -> Ciphertext`.
  4. Đặt `Evaluator` trong vùng Cloud và cho nó thực hiện add, multiply, relinearize, rescale, rotate; SecretKey vẫn nằm ngoài vùng Cloud.
  5. Trả ciphertext về Client qua `Decryptor -> Plaintext -> CKKSEncoder.decode -> vector`; hiển thị bảng "Object / Responsibility / Required key".

### Phân đoạn 4.3: Quy trình triển khai SEAL từ đầu đến cuối (10:00 - 15:00)
- **Lời thoại AI (Audio Voiceover):**
  "We can now assemble the complete private-computation lifecycle. Step one is to design the arithmetic circuit. Rewrite unsupported control flow, choose a slot layout, count multiplicative depth, list rotations, and define an acceptable numerical error.

  Step two is parameter selection. Choose the polynomial modulus degree, coefficient-modulus chain, and initial scale according to the circuit and current security recommendations. Create SEALContext and verify that the selected parameters are valid before generating keys.

  Step three is capability provisioning. Generate the Secret Key for the trusted client. Create a Public Key when public-key encryption is required. Create only the Relinearization Keys and Galois Keys needed by the evaluation schedule. Serialize the approved parameters and evaluation material for the server.

  Step four is data preparation. Normalize the input, pack values into the planned slot layout, encode them at the expected scale, and encrypt the Plaintext. The server loads the ciphertext under a compatible context and executes the predetermined evaluator operations while tracking size, level, scale, and rotation requirements.

  Step five is verification. The server returns an encrypted result. The client decrypts and decodes it, compares the values against a plaintext reference, and checks the agreed tolerance. Security, numerical accuracy, latency, memory, and ciphertext size must all be measured. Act One therefore ends with a practical principle: design the computation first, provision cryptographic capability second, and treat every encrypted result as both a security object and a numerical object."

- **Hoạt ảnh Manim (Visual Actions):**
  1. Hiện checklist `1. Circuit design`: thay branch bằng arithmetic, chọn packing, đếm depth và rotations.
  2. Hiện `2. Parameters and context`: dựng modulus chain, scale và dấu kiểm `SEALContext valid`.
  3. Hiện `3. Keys`: SecretKey ở Client; PublicKey, RelinKeys và GaloisKeys cần thiết được chuyển có chọn lọc tới Server.
  4. Trình diễn `4. Encode -> Encrypt -> Evaluate`: vector đầu vào thành ciphertext, đi qua chuỗi phép toán trên Cloud mà không giải mã.
  5. Trình diễn `5. Decrypt -> Decode -> Verify`: so sánh output FHE với plaintext baseline, hiện error tolerance và bảng đo `Security / Accuracy / Latency / Memory`.

## III. QUẢN LÝ TÀI NGUYÊN BỔ TRỢ (ASSETS MAPPING)
- Audio gốc: `assets/audio/01_math_crypto/scene_04_keys_and_seal_pipeline.mp3`
- Ảnh/plate minh họa dự kiến: `assets/image/01_math_crypto/scene_04_seal_keys.png`
- Thư viện Manim dùng chung: PlaintextBlock, CiphertextBlock, constants và storyboard pacing từ `scenes/library/`
- Tài liệu tham khảo lý thuyết: Microsoft SEAL README; `native/examples/3_levels.cpp`, `5_ckks_basics.cpp`, `6_rotation.cpp` và `7_serialization.cpp`.

## IV. EXPANDED CONTENT BEATS CHO BẢN 15 PHÚT
- Phân đoạn 4.1: SecretKey authority, PublicKey encryption, RelinKeys, GaloisKeys, evaluation-key size và least-privilege policy.
- Phân đoạn 4.2: EncryptionParameters, SEALContext, KeyGenerator, CKKSEncoder, Encryptor, Evaluator, Decryptor và trách nhiệm của từng object.
- Phân đoạn 4.3: circuit design, parameter selection, capability provisioning, encode/encrypt/evaluate, decrypt/decode/verify và đo lường hệ thống.
- Mỗi phân đoạn gồm một visual demonstration và năm content beats thay đổi liên tục; không dùng một khung hình tĩnh để lấp thời lượng.
