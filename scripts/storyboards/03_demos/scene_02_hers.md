# Act 3 - Scene 2: HERS - Privacy-Preserving Health Record System
# Mã số file code đích: scenes/03_demos/scene_02_hers_system.py
# Khung thời gian dự kiến: 00:00:00 -> 00:07:00 (7 phút)

## I. THÔNG TIN METADATA & ĐỒ HỌA CHUẨN
- **Hệ màu:** `COLOR_PLAINTEXT` (Blue), `COLOR_CIPHERTEXT` (Red), `COLOR_ENCRYPTION` (Orange/Yellow).
- **Đối tượng Manim:** `CiphertextBlock`, `PlaintextBlock` (đã tùy chỉnh cho Y tế), `ResNetBlock` (cho Diagnostic CNN).
- **Trạng thái Audio:** Giọng AI trầm, chuyên nghiệp, nhịp điệu chậm rãi để khớp với các bước tính toán phức tạp.

## II. KỊCH BẢN CHI TIẾT (STORYBOARD)

### Phân đoạn 2.1: Bối cảnh & Bài toán bảo mật y tế (00:00 - 01:30)
- **Lời thoại AI (Audio Voiceover):**
  "Welcome back to our exploration of practical privacy solutions. In this section, we move beyond biometric identification to address one of the most critical challenges of our digital age: the Privacy-Preserving Health Record System, or HERS.

Think about the current state of digital healthcare. Patients worldwide generate massive amounts of sensitive data every day—from continuous ECG monitoring to detailed electronic health records. Meanwhile, central cloud hospitals possess advanced Artificial Intelligence models capable of detecting early signs of diseases that human doctors might miss. But there is a fundamental paradox here: to use these powerful AI diagnostic tools, patients are currently forced to surrender their raw, sensitive medical history to the cloud. Once your medical data is stored as plaintext on a remote server, it is permanently vulnerable to data breaches, insider threats, and unauthorized profiling. HERS was designed to resolve this deadlock, creating a framework where the cloud provides diagnosis, while the patient retains absolute ownership of their privacy.'."

- **Hoạt ảnh Manim (Visual Actions):**
  1. Hai vùng tách biệt: `Patient / Local Clinic` (Trái) và `Cloud Hospital AI` (Phải).
  2. Dữ liệu `Health Record (ECG/EHR)` được hiển thị tại Patient.
  3. Mũi tên từ Patient trỏ sang Cloud bị chặn bởi icon khiên bảo mật, minh họa rủi ro nếu không có FHE.



### Phân đoạn 2.2: Luồng mã hóa & Mã hóa Y tế (01:30 - 03:30)
- **Lời thoại AI (Audio Voiceover):**
  "The life cycle of data in HERS begins entirely within the patient's local, trusted environment. Before a single byte of medical data is transmitted, the system invokes a sophisticated encryption layer. We are not talking about standard transport-layer security here; we are utilizing Fully Homomorphic Encryption to encapsulate the data.

By utilizing the patient’s public key, the raw health records are transformed into a secure, homomorphic ciphertext. This isn't just 'hidden' data; it is mathematically structured to allow for complex computations without needing to be unlocked. This encrypted package is then safely uploaded to the cloud hospital. Even if an attacker were to intercept this data packet while it travels across the public internet, they would be met with nothing but high-entropy noise. The patient’s clinical history remains completely opaque to the network, the cloud provider, and any potential malicious actors."

- **Hoạt ảnh Manim (Visual Actions):**
  1. `Health Record` đi qua khối `Encryption` (Orange).
  2. `Public Key` (Orange) kết hợp tạo ra `Encrypted Health Data` (Red) với icon ổ khóa.
  3. Khối Ciphertext bay qua `Network` (vòng tròn xám ở giữa) sang phía `Cloud Hospital`.

### Phân đoạn 2.3: Chẩn đoán trên mây (Blind Diagnostic) (03:30 - 05:30)
- **Lời thoại AI (Audio Voiceover):**
  "Once the encrypted medical data reaches the Cloud Hospital, the system engages the Medical Diagnostic CNN—the core intelligence of HERS. In a traditional setting, the server would be blind if the data were encrypted. But here, the magic of homomorphism takes center stage.

The CNN is specifically architected to perform algebraic operations directly on the polynomial rings representing your health data. It executes the necessary convolutions, activations, and pooling layers by manipulating the encrypted tensors themselves. This is what we call 'Blind Medical Diagnosis'. The model is running, the math is happening, and clinical insights are being generated—all without the cloud server ever knowing what the input data actually is. It is a mathematical guarantee: the server processes your health markers with extreme precision, but it effectively 'sees' nothing, ensuring that your most personal health information is never decrypted in the cloud infrastructure."

- **Hoạt ảnh Manim (Visual Actions):**
  1. `Encrypted Health Data` đi vào `Medical Diagnostic CNN Model` (Blue).
  2. Các layer (ResNetBlock) sáng lên khi dữ liệu đi qua.
  3. Kết quả `Encrypted Diagnosis` (Red) xuất ra từ phía dưới Model.

### Phân đoạn 2.4: Giải mã & Kết quả chẩn đoán (05:30 - 07:00)
- **Lời thoại AI (Audio Voiceover):**
  "The final diagnostic output, now also in an encrypted state, is transmitted securely back to the patient. This is the moment of truth. Only the patient, holding the exclusive secret key, can unlock this result.

With a single operation, the patient’s local device performs the final decryption, revealing the diagnosis—whether it indicates a healthy state, a warning, or a specific condition. By keeping the decryption key entirely local, HERS ensures that the 'privacy perimeter' never expands beyond the patient’s own device. This architecture represents the pinnacle of modern applied cryptography: a system that leverages the infinite power of cloud-based AI while simultaneously upholding the sanctity of medical confidentiality. This is not just a technological demonstration; it is a blueprint for the future of trustworthy, patient-centric digital healthcare."

- **Hoạt ảnh Manim (Visual Actions):**
  1. `Encrypted Diagnosis` bay ngược về vùng `Patient`.
  2. `Secret Key` (Red) mở khóa khối `Decryption` (Dark Blue).
  3. Dòng chữ `Final Diagnosis (e.g., Healthy)` hiện ra với icon tích xanh (`✅`), kết thúc luồng xác thực.

## III. QUẢN LÝ TÀI NGUYÊN BỔ TRỢ (ASSETS MAPPING)
- Audio gốc: `assets/audio/hers_full.mp3`
- Hình ảnh tham khảo: `assets/ecg_record.jpg`, `assets/hospital_cloud.png`
- Tài liệu cấu trúc: Dựa trên mô hình HERS (Health Record Privacy System) đã thiết kế trong file `hers_system.py`.

## IV. GÓP Ý PHÁT TRIỂN
- Hãy nhấn mạnh rằng HERS mang tính thực tiễn và nhân văn hơn so với demo thuần túy.
- Sử dụng khoảng nghỉ 3-5 giây tại đoạn 03:30 để người xem quan sát luồng dữ liệu chạy qua CNN.
- Đảm bảo màu sắc hiển thị kết quả "Healthy" là màu xanh lá (Green) để tạo cảm giác an tâm.