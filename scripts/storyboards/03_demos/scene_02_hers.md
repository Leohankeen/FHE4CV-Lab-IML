# Act 3 - Scene 2: HERS - Privacy-Preserving Health Record System
# Mã số file code đích: scenes/03_demos/scene_02_hers_system.py
# Khung thời gian dự kiến: 00:00:00 -> 00:15:00 (15 phút)

## I. THÔNG TIN METADATA & ĐỒ HỌA CHUẨN
- **Hệ màu:** `COLOR_PLAINTEXT` (Blue), `COLOR_CIPHERTEXT` (Red), `COLOR_ENCRYPTION` (Orange/Yellow), `COLOR_MATH` (Green).
- **Đối tượng Manim:** `CiphertextBlock`, `PlaintextBlock` (đã tùy chỉnh cho Y tế), `ResNetBlock` (cho Diagnostic CNN), `Axes` (đồ thị hàm số), `Rectangle` (thanh Noise Budget).
- **Trạng thái Audio:** Giọng AI học thuật, trầm, chuyên nghiệp. Cần đọc chậm, ngắt quãng rõ ràng ở các thuật ngữ kỹ thuật chuyên sâu.

---

## II. KỊCH BẢN CHI TIẾT (STORYBOARD)

### Phân đoạn 2.1: Bối cảnh, Lỗ hổng Data in Use & Mô hình đe dọa (00:00 - 03:00)
- **Lời thoại AI (Audio Voiceover):**
  "Welcome to the architectural deep dive of HERS, the Privacy-Preserving Health Record System. In this specific scenario, we are addressing a fundamental security flaw in how modern telemedicine handles sensitive data.

Consider the current landscape of digital healthcare. On the left side of our framework, we have the patient's local environment. This local node continuously generates dense, highly personal clinical data, such as real-time Electrocardiograms, or ECGs. On the right side, we have the Cloud Hospital—a centralized infrastructure equipped with powerful Deep Learning models, such as Convolutional Neural Networks, capable of detecting early signs of cardiovascular diseases far earlier than a human specialist.

However, connecting these two nodes exposes a critical vulnerability regarding Data in Use. Standard cryptographic protocols, such as TLS or SSL, do an excellent job of protecting your medical records while they are in transit across the network. Furthermore, standard symmetric encryption like AES protects data at rest in the database. But there is a fatal gap: the moment the Cloud AI needs to run its diagnostic inference, the data must be completely decrypted in the server's memory.

This brings us to our specific threat model: the 'Honest-but-Curious' adversary, also known as a semi-honest server. In this threat model, we assume the cloud provider will faithfully execute the diagnostic algorithms without tampering with the computation. However, they are 'curious'—meaning the server administrators, data brokers, or an insider threat can monitor memory states, analyze access logs, and attempt to harvest your raw medical history.

Unlike a compromised password that can easily be changed, your biometric and clinical data is immutable. Once your raw ECG is exposed in plaintext on a remote server, it is permanently vulnerable to unauthorized profiling and advanced persistent threats.

This is the exact deadlock HERS is engineered to break. By activating the Fully Homomorphic Encryption shield at the patient's local node, we completely eliminate the need for server-side decryption. The cloud will compute its complex neural network layers directly on the ciphertexts. We achieve true 'Blind Medical Diagnosis'—leveraging the computational supremacy of the cloud, while mathematically restricting the privacy perimeter exclusively to the patient's own device."

- **Hoạt ảnh Manim (Visual Actions):**
  1. Tiêu đề hiện lên và thu nhỏ dần lên góc trên. Hai vùng tách biệt: `Patient / Local Clinic` (Trái) và `Cloud Hospital AI` (Phải) cùng `Network` xuất hiện.
  2. Màn hình tĩnh để khán giả nghe phân tích về lỗ hổng Data in Use.
  3. Dòng chữ `Threat: Honest-but-Curious Cloud` hiện lên màu đỏ nhấp nháy bên vùng Cloud.
  4. Dòng chữ `FHE Protection Enabled` hiện lên màu xanh lá bên vùng Patient, sau đó dòng cảnh báo đỏ bị xóa đi để chuẩn bị cho bước mã hóa.

---

### Phân đoạn 2.2: Tiền xử lý & Kỹ thuật đóng gói (SIMD Batching) (03:00 - 05:00)
- **Lời thoại AI (Audio Voiceover):**
  "Before any encryption can occur in the HERS pipeline, we must address a massive structural and computational bottleneck. Look at the patient's local environment. The raw medical data generated here, such as a continuous Electrocardiogram or ECG signal, is not just a single, simple number. It is a high-frequency, continuous stream of analog data. To process this using any Deep Learning model, the local device must first digitize this continuous wave into a dense, high-dimensional array of floating-point values.
  
  Now, consider the naive approach to encrypting this array. Fully Homomorphic Encryption schemes naturally operate on massive polynomial rings, making a single ciphertext extremely large—often several megabytes in size. If we were to encrypt each individual heartbeat data point, like 0.85 or 1.20, into its own separate ciphertext, we would trigger a catastrophic explosion in both memory footprint and computational overhead. A simple vector of a few thousand floats would quickly balloon into gigabytes of encrypted data, making real-time network transmission and cloud computation practically impossible
  
  To overcome this fatal limitation, HERS leverages one of the most powerful features of the CKKS homomorphic encryption scheme: SIMD, which stands for Single Instruction, Multiple Data batching.

Instead of encrypting numbers one by one, the CKKS scheme allows us to mathematically pack thousands of discrete floating-point values into the independent message slots of a single plaintext polynomial. In our specific architecture, we utilize a polynomial degree that provides 4096 packing slots. This means a single plaintext object encapsulates an entire time-series segment of the ECG.

This is not merely a data compression trick; it is a profound computational optimization. Because the data is packed homomorphically, when the Cloud CNN later performs a single multiplication or addition on this ciphertext, that exact algebraic operation is executed simultaneously across all 4096 data points in parallel. By transforming a high-dimensional tensor into a single polynomial ring, HERS completely bypasses the ciphertext expansion problem, enabling the system to achieve the extreme throughput required for real-time medical AI."

- **Hoạt ảnh Manim (Visual Actions):**
  1. `Continuous ECG Signal` được hiển thị tại Patient.
  2. Tín hiệu này chuyển đổi thành một mảng số thực: `[0.85, 1.20, -0.45, 2.10, ...]`.
  3. Mảng số này thu nhỏ lại và chạy vào trong một khối `PlaintextBlock` khổng lồ có nhãn "SIMD Batching: 4096 slots". Mảng số sau đó biến mất.

---

### Phân đoạn 2.3: Luồng mã hóa FHE & Truyền tải an toàn (05:00 - 07:00)
- **Lời thoại AI (Audio Voiceover):**
  "With our medical data efficiently packed into a single plaintext polynomial, the HERS pipeline advances to the critical cryptographic phase: Fully Homomorphic Encryption. Notice the introduction of the Patient’s Public Key. In traditional systems, we might use standard RSA or Elliptic Curve Cryptography. However, to enable homomorphic operations, HERS relies on Lattice-based cryptography, specifically the Ring Learning With Errors, or Ring-LWE, mathematical assumption. This not only allows for computation on encrypted data but also inherently provides robust post-quantum security against future quantum computing attacks 
  
  As the plaintext and the Public Key enter the encryption module, a highly complex transformation occurs. We are not simply scrambling bits. The encryption algorithm intentionally injects a meticulously calibrated, high-entropy mathematical 'noise' into the polynomial. This noise addition is the absolute cornerstone of lattice-based security. It guarantees Semantic Security, specifically Indistinguishability under Chosen-Plaintext Attack, or IND-CPA. This ensures that even if the exact same ECG data is encrypted multiple times, it will produce a completely different ciphertext every single time, completely thwarting any statistical pattern analysis.
  
  The output of this module is our Encrypted Health Data. It is crucial to understand that this is vastly different from a standard symmetric ciphertext. An AES ciphertext, for example, is a rigid, opaque block of bits. In contrast, our FHE ciphertext typically consists of a pair of massive, high-degree polynomials. It securely hides the patient's data while perfectly preserving its underlying homomorphic algebraic structure, allowing it to be mathematically manipulated.
  
  Finally, this massive ciphertext is transmitted across the public internet to the Cloud Hospital infrastructure. During this transit, the data is cryptographically bulletproof. Even if a highly sophisticated attacker intercepts this specific network packet, they are confronted with solving the Shortest Vector Problem on a multidimensional lattice—a task considered mathematically infeasible. Once it arrives at the cloud, the server possesses a computationally malleable, yet completely opaque representation of the patient's clinical history. The stage is now set for blind AI inference."

- **Hoạt ảnh Manim (Visual Actions):**
  1. `Public Key` (Orange) và hộp `Encryption` xuất hiện.
  2. `Plaintext` và `Public Key` trượt vào trong hộp mã hóa, và khối `Encrypted Health Data` (Red) xuất hiện cùng icon ổ khóa và mũi tên chỉ xuống.
  3. Dọn dẹp toàn bộ công cụ mã hóa ở vùng Patient.
  4. Khối Ciphertext bay vòng cung qua vùng `Network` sang phía `Cloud Hospital`.

---

### Phân đoạn 2.4: CNN chẩn đoán mù & Xấp xỉ đa thức (07:00 - 10:00)
- **Lời thoại AI (Audio Voiceover):**
  "With the encrypted data now inside the Cloud CNN, we collide with the most notorious bottleneck in FHE: Non-linear Activation Functions. Notice the ReLU graph on screen. Deep learning depends on these non-linearities to learn abstract medical patterns. However, ReLU is a piecewise function requiring a 'greater-than' comparison. Here lies the fundamental incompatibility. FHE schemes, like CKKS, restrict us entirely to polynomial arithmetic—we are confined strictly to homomorphic addition and multiplication. Because encrypted data inherently blocks branching logic and comparison operations, evaluating a standard ReLU activation on a ciphertext is mathematically impossible.
  
  To bypass this roadblock, HERS employs a radical architectural shift: Polynomial Approximation. As you can see on the screen, we replace the sharp, non-computable ReLU boundary with a smooth, low-degree polynomial curve—in this simplified visual case, the square function, $y = x^2$.Why does this work? Because computing $x^2$ requires only a single homomorphic multiplication—an operation perfectly supported by the CKKS scheme. By substituting all non-linear activation layers with polynomial approximations, we trick the network. We provide the essential non-linearity required for deep feature extraction, but we do so using exclusively valid homomorphic operations.
  
  Of course, this cryptographic workaround is not without its trade-offs. Replacing ReLU with a polynomial alters the mathematical landscape and convergence dynamics of the neural network. This requires us to carefully retrain the medical model from scratch to maintain high diagnostic accuracy.
  Furthermore, computing these polynomials consumes our most precious cryptographic resource: the multiplicative depth. Every time we approximate an activation function via multiplication, we inject more noise into the ciphertext, which leads us directly to the critical concept of the noise budget."

- **Hoạt ảnh Manim (Visual Actions):**
  1. Xuất hiện hệ trục tọa độ tại đám mây. Đồ thị gấp khúc màu đỏ hiện lên kèm nhãn `❌ ReLU (Incompatible)`. Màn hình tĩnh lại để chờ AI giải thích.
  2. Đồ thị màu đỏ chuyển hóa mượt mà thành đường cong Parabol màu xanh lá với nhãn `✅ Polynomial Appx (y = x²)`.
  3. Đồ thị bị xóa để nhường chỗ cho mạng CNN xuất hiện ở bước tiếp theo.

---

### Phân đoạn 2.5: Quản lý Độ sâu & Nhiễu FHE (Noise Budget) (10:00 - 12:30)
- **Lời thoại AI (Audio Voiceover):**
"To evaluate our polynomial approximations, the Cloud CNN must perform sequential homomorphic multiplications. However, this introduces the most stringent cryptographic limitation in the CKKS scheme: the Multiplicative Depth constraint.
Notice the 'Noise Budget' meter appearing on screen. In lattice-based cryptography, security relies on the 'Learning With Errors' assumption. This means every freshly encrypted ciphertext inherently contains a small amount of random mathematical noise. Without this initial noise, the encryption could be easily broken by linear algebra attacks. We refer to the maximum tolerable limit of this noise as our 'Noise Budget'.

As our encrypted tensor enters the CNN, watch the noise meter closely. In FHE, homomorphic addition only adds noise linearly, which is highly manageable. But homomorphic multiplication—which is strictly required for every single polynomial activation and feature convolution—causes the noise to multiply and grow exponentially.As the tensor passes through Conv 1, Conv 2, and Conv 3, the meter shifts from green, to yellow, and plummets into the red zone. This visualizes the rapid degradation of our plaintext precision. If the accumulated noise breaches the upper threshold—meaning the budget drops to zero—the mathematical noise will completely overlap and drown out the encoded medical features. If that happens, the ciphertext is permanently corrupted, resulting in catastrophic decryption failure.

This is exactly why deploying Deep Learning over FHE is incredibly challenging. While we could theoretically use a cryptographic technique called 'Bootstrapping' to clean the ciphertext and refresh the noise budget midway, bootstrapping operations are notoriously slow and computationally prohibitive for real-time medical systems. Therefore, the HERS architecture is fundamentally driven by this budget. The model is meticulously optimized to be intentionally shallow. We mathematically constrain the CNN to perform the exact minimum number of convolutions required to achieve an accurate clinical diagnosis, successfully extracting the final Encrypted Diagnosis just moments before the noise budget is completely exhausted."

- **Hoạt ảnh Manim (Visual Actions):**
  1. Khối `Medical Diagnostic CNN Model` xuất hiện gồm 3 lớp ResNetBlock xếp dọc. Bên cạnh là thanh năng lượng `Noise Budget` màu xanh lá đầy ắp.
  2. Khối Ciphertext nhảy dần qua từng lớp Conv.
  3. Sau mỗi lớp, thanh Noise tụt xuống dần, đổi màu từ Xanh -> Vàng -> Đỏ.
  4. Trước khi thanh Noise cạn kiệt, Ciphertext biến đổi thành `Encrypted Diagnosis` và thoát ra an toàn. Đám mây được dọn dẹp.

---

### Phân đoạn 2.6: Giải mã Cục bộ & Kết quả chẩn đoán (12:30 - 15:00)
- **Lời thoại AI (Audio Voiceover):**
  "The diagnostic inference is now complete. Look at the output currently traversing the network back to the patient. The Cloud Hospital has successfully executed a deep Convolutional Neural Network on the patient's ECG data, yet, remarkably, the server is entirely blind to what it just computed.The cloud does not know if the patient is suffering from arrhythmia, or if their heart is perfectly normal. It merely performed algebraic manipulations on encrypted polynomials and produced a new, highly compressed ciphertext. This 'Encrypted Diagnosis' is now safely transmitted back across the public internet. Because the data remains in its homomorphic ciphertext state, it is immune to network sniffing, man-in-the-middle attacks, or any form of interception.
   
  The encrypted result now safely arrives back at the patient's local environment. This brings us to the absolute core of the HERS architecture: The Zero-Trust Privacy Perimeter.Notice the introduction of the Secret Key. In asymmetric homomorphic encryption, while the Public Key is used to lock the data and perform cloud computations, only the corresponding Secret Key can reverse the mathematical noise and unlock the final result. Throughout this entire lifecycle—from the initial ECG reading to the final AI inference—this Secret Key has never once left the patient's device. It was never shared with the hospital, it was never uploaded to the cloud, and it was never transmitted over the network. We have established a mathematically enforced 'Trustless' system. The patient does not need to trust the cloud provider's security policies, because the mathematics of Lattice Cryptography guarantees their privacy.
  
  Now, with a single, highly efficient local operation, the patient's device applies the Secret Key to the decryption module. The cryptographic noise that accumulated during the cloud's neural network processing is finally stripped away. The underlying plaintext polynomial is revealed and evaluated against the diagnostic threshold.And there is our output: A definitive, plaintext clinical diagnosis—in this case, 'Healthy'. The loop is closed. The patient receives world-class, AI-driven medical insights instantly, entirely processed on edge and cloud infrastructure, without ever exposing a single raw data point.
  
  As we conclude this architectural deep dive, let us reflect on the broader implications of the HERS framework. Today, the rapid advancement of Artificial Intelligence in healthcare is constantly colliding with strict data protection regulations like GDPR and HIPAA. Medical institutions are paralyzed by the fear of data breaches, severely limiting the deployment of life-saving AI models.HERS represents a fundamental paradigm shift. It proves that privacy and utility are not mutually exclusive. We do not have to surrender our fundamental human right to privacy in order to benefit from the computational supremacy of the cloud. By bridging Deep Learning with Fully Homomorphic Encryption, we are paving the way for a future where intelligent, predictive telemedicine is accessible to everyone, fundamentally secured not by trust, but by the irrefutable laws of mathematics. "

- **Hoạt ảnh Manim (Visual Actions):**
  1. `Encrypted Diagnosis` bay ngược về vùng `Patient`.
  2. `Secret Key` (Red) và hộp `Decryption` xuất hiện. Cả hai trượt vào hộp giải mã.
  3. Khối Plaintext chứa `Final Diagnosis: ✅ HEALTHY` hiện ra.
  4. Màn hình tĩnh, khán giả chiêm ngưỡng toàn bộ luồng hệ thống ở những giây cuối cùng.

---

## III. QUẢN LÝ TÀI NGUYÊN BỔ TRỢ (ASSETS MAPPING)
- Các file Audio gốc (Cần chia nhỏ 6 đoạn tương ứng với các mục code `self.add_sound`): `02_01_1.mp3`, `02_01_2.mp3`, `02_01_3.mp3`, v.v...
- Hình ảnh tham khảo: `assets/ecg_record.jpg`, `assets/hospital_cloud.png`
- Tài liệu cấu trúc: Dựa trên mô hình HERS (Health Record Privacy System) đã thiết kế trong file `scene_02_hers_system.py`.

---

## IV. GÓP Ý PHÁT TRIỂN
- Hãy nhấn mạnh rằng HERS mang tính thực tiễn và nhân văn hơn so với demo thuần túy.
- Sử dụng các khoảng nghỉ dài `self.wait(x)` đã được thiết lập trong code để người xem quan sát và tiêu hóa các khái niệm trừu tượng (như Polynomial Approximation và Noise Budget).
- Đảm bảo màu sắc thanh Noise đổi sang Đỏ ở lớp cuối cùng để tăng tính kịch tính về giới hạn độ sâu của FHE.