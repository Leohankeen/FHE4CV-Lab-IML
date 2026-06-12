# Act 3 - Scene 4: Medical X-Ray FHE Demo - TenSEAL Linear Triage
# Mã số file code đích: scenes/03_demos/scene_04_Xray.py
# Khung thời gian dự kiến: 00:00:00 -> 00:15:00 (15 phút)

## I. THÔNG TIN METADATA & ĐỒ HỌA CHUẨN
- **Hệ màu sử dụng:** `COLOR_PLAINTEXT` (Blue), `COLOR_CIPHERTEXT` (Red), `COLOR_ENCRYPTION` (Yellow), `COLOR_HOSPITAL` (Cyan).
- **Đối tượng Manim chủ đạo:** `CiphertextBlock`, `PlaintextBlock`, `MathTex` (Công thức Dot Product, Sigmoid), `ImageMobject` (Ảnh X-quang).
- **Trạng thái Audio:** Giọng nói AI TTS (Tiếng Anh) - Nhịp điệu: Chuyên nghiệp, học thuật, tốc độ chậm rãi.

---

## II. KỊCH BẢN CHI TIẾT (STORYBOARD)

### Phân đoạn 4.1: Đặt vấn đề Y tế & Trích xuất Đặc trưng tại Edge (00:00 - 03:30)
- **Lời thoại AI (Audio Voiceover):**
  "Welcome to our next practical demonstration: Medical FHE for X-Ray Priority Triage. In the healthcare sector, hospitals are under immense pressure to quickly triage patient X-rays. While cloud-based AI diagnostics offer immense computational speed, there is a fundamental conflict. Strict data privacy regulations, such as HIPAA, strictly prohibit the transmission of unencrypted, personally identifiable medical images to untrusted third-party servers.To resolve this, we propose an architecture combining Edge Computing with Fully Homomorphic Encryption. Observe the system layout currently on screen. On the left, we have the strictly regulated and trusted environment: The Secure Hospital Client. On the right, we have the highly powerful, but mathematically blinded environment: The Untrusted Cloud Server.
  
  The triage process begins entirely locally. A high-resolution chest X-ray is captured and loaded into the hospital's secure edge device. In a traditional workflow, this massive matrix of pixels would be sent directly to the cloud. However, homomorphically encrypting millions of individual pixels is computationally devastating and creates an unacceptable network bottleneck. Therefore, our architecture intercepts the data at the source. We introduce an 'Edge Feature Extractor'. Before any encryption takes place, the local hospital hardware runs a lightweight, standard plaintext algorithm to analyze the image.
  
  Watch as the raw X-ray is passed through this local extractor. Instead of outputting a full image, the algorithm distills the complex biological structures into a highly compact, 10-dimensional plaintext feature vector. This 1D array captures critical diagnostic indicators—such as global brightness, localized contrast, and structural edge energy. By reducing a massive image matrix down to just ten essential floating-point numbers, we drastically reduce the computational payload. This edge-preprocessing step is the crucial optimization that makes the subsequent homomorphic encryption not just mathematically possible, but practically highly efficient for real-time medical triage.   "

- **Hoạt ảnh Manim (Visual Actions):**
  1. Hiển thị mô hình 2 bên: `Hospital Client` (Trái) và `Untrusted Cloud` (Phải).
  2. Bức ảnh `Chest X-Ray` (Chụp X-quang ngực) xuất hiện tại Hospital.
  3. Bức ảnh trượt qua một khối `Feature Extractor`, sau đó biến đổi thành một mảng vector 10 phần tử (Plaintext 1D Array) với các thông số như `[mean_intensity, edge_energy, ...]`.

### Phân đoạn 4.2: Đóng gói TenSEAL & Mã hóa CKKS (03:30 - 07:30)
- **Lời thoại AI (Audio Voiceover):**
  "Now that we have successfully extracted the 10-dimensional plaintext feature vector, we must secure it before it ever leaves the hospital's local network. To achieve this, we introduce TenSEAL—a highly specialized cryptographic library engineered specifically to perform homomorphic operations on tensors. As you can see on the screen, the system initializes an encryption context using the CKKS scheme. Why do we choose CKKS? Because it natively supports homomorphic arithmetic on floating-point numbers, which is an absolute requirement for evaluating machine learning models. We set the poly_modulus_degree to 8192. This parameter provides a perfect architectural balance: it guarantees a robust level of security against modern cyber threats, while allocating just enough 'noise budget' to support our linear classification.
  
  With the cryptographic environment established, the edge device invokes the hospital's Public Key. Watch closely as the encryption process is executed. The public key mathematically locks the 1D feature array. The continuous floating-point values of the patient's biological data are encoded into high-degree polynomials. Simultaneously, a carefully calibrated layer of cryptographic noise—based on the Ring Learning With Errors assumption—is injected directly into the data. The output is a highly secure, encrypted tensor known as a 'CKKS Vector'. The patient's sensitive medical data is now completely obfuscated, locked behind an impenetrable mathematical vault. Because this is an asymmetric protocol, the Public Key can only lock the data. The corresponding Secret Key—the only mathematical tool capable of reversing this noise—remains strictly confined to the hospital's local server.
  
  With the payload cryptographically secured, the hospital can now safely transmit this locked CKKS Vector across the public internet to the Untrusted Cloud Server. This transition solves the fundamental roadblock of healthcare data regulations like HIPAA. Even if the network traffic is intercepted by a man-in-the-middle attack, or if the cloud infrastructure is completely compromised by a malicious hacker, the attacker will obtain nothing but random, unintelligible polynomial noise. The data is now secure in transit, secure at rest, and perfectly staged for blind computation."

- **Hoạt ảnh Manim (Visual Actions):**
  1. Logo `TenSEAL` hiện lên góc trái. Dòng chữ thiết lập context: `ts.context(CKKS, poly_modulus_degree=8192)`.
  2. `🔑 Public Key` khóa mảng 10 phần tử lại, biến nó thành một khối đỏ có tên `CKKS_Vector (Encrypted Features)`. Biểu tượng 🔒 xuất hiện.
  3. Khối `CKKS_Vector` bay chậm rãi theo đường parabol sang vùng `Untrusted Cloud`.

### Phân đoạn 4.3: Tính toán Hồi quy Tuyến tính Đồng hình (07:30 - 11:30)
- **Lời thoại AI (Audio Voiceover):**
  "The encrypted X-ray features have safely arrived at the Untrusted Cloud Server. The server holds a pre-trained Linear Triage Model, represented here by the Plaintext Model Weights and the Bias value. In a standard machine learning pipeline, generating a diagnostic prediction involves calculating the dot product of the input features and the weights, followed by adding the bias. Remarkably, the TenSEAL library allows the server to execute this exact algebraic formula directly on the ciphertext. Because the server is performing operations between an encrypted tensor and plaintext model weights, we refer to this as a Ciphertext-Plaintext evaluation.
  
  Watch as the homomorphic evaluation unfolds. The server mathematically multiplies its plaintext weights with the encrypted feature vector and adds the plaintext bias. These inputs seamlessly merge to form a single, newly computed tensor: the Encrypted Logit. Now, pay close attention to the Cryptographic Noise bar on the right. In our previous demonstrations with deep Neural Networks, we saw how continuous homomorphic multiplications rapidly depleted the noise budget, risking catastrophic data collapse. However, because this is a linear triage model, the entire evaluation requires a multiplicative depth of exactly one.Notice that the noise level barely drops. This architectural decision—extracting complex features on the local edge and strictly limiting the cloud to shallow linear homomorphic operations—is the definitive key to achieving real-time, privacy-preserving medical diagnostics without exhausting the server's computational resources."

- **Hoạt ảnh Manim (Visual Actions):**
  1. Tại Cloud, hiện ra mảng `Model Weights (Plaintext)` màu xanh và giá trị `Bias`.
  2. Hiển thị công thức `MathTex`: $Logit = \text{Enc}(X) \cdot W + b$.
  3. Mô phỏng phép nhân vô hướng (`dot product`): Từng phần tử của Weights nhân với phần tử của CKKS Vector, sau đó cộng dồn lại.
  4. Thanh `Noise Budget` xuất hiện và sụt giảm nhẹ (do có 1 phép nhân độ sâu = 1).
  5. Kết quả sinh ra một khối duy nhất: `Encrypted Logit` màu đỏ có gắn ổ khóa.

### Phân đoạn 4.4: Giải mã & Kích hoạt Phi tuyến tính (Sigmoid) tại Client (11:30 - 15:00)
- **Lời thoại AI (Audio Voiceover):**
  "The Cloud Server has successfully computed the Encrypted Logit. However, a raw logit is simply a linear continuous value; it is not a clinical probability. To make a diagnostic decision, we must apply a non-linear activation function, such as Sigmoid. Here lies a critical optimization in our architecture. In Fully Homomorphic Encryption, calculating a precise non-linear Sigmoid curve requires highly complex Taylor polynomial approximations. Forcing the cloud to compute this would consume a massive amount of the multiplicative depth, destroying our computational efficiency. Therefore, the cloud strategically stops here and returns the Encrypted Logit back to the secure hospital client.
  
  Upon receiving the locked ciphertext, the hospital's edge device applies its Secret Key. The cryptographic noise is instantly stripped away, revealing the precise plaintext Logit value of 2.45. Now, operating safely within the trusted local environment, the edge device can perform the non-linear Sigmoid activation in plaintext, requiring zero cryptographic overhead. Let us visualize this mathematical transformation. On the screen, we plot the Sigmoid activation curve. The horizontal axis represents the raw logit values, while the vertical axis mathematically compresses these values into a strict probability range between zero and one.
  
  Watch as our specific patient data point is mapped onto this function. The patient's Logit of 2.45 is plotted on the horizontal axis. We project this vertically onto the Sigmoid curve, and then horizontally to the probability axis. The mathematical transformation perfectly calculates a diagnostic Probability of 0.91, meaning there is a 91 percent confidence level regarding the triage condition.
  
  With the probability established, the system makes a deterministic clinical decision. For this specific medical model, the diagnostic threshold is set at 0.5, represented by the red dashed baseline. Any probability above this line demands immediate medical attention. As you can clearly see, our patient's probability sits well inside the critical zone. The local system instantly triggers the response logic, flagging the patient as 'Urgent'. The untrusted cloud successfully triaged the patient without ever seeing the X-ray, the extracted features, or the final result. Absolute medical privacy has been mathematically guaranteed."

- **Hoạt ảnh Manim (Visual Actions):**
  1. Khối `Encrypted Logit` bay từ Cloud về lại Hospital.
  2. Hộp `Decryption` và `🗝️ Secret Key` (đỏ) đâm vào mở khóa khối Logit. Khối Logit đỏ biến thành số thực xanh: `Logit = 2.45`.
  3. Hiển thị công thức `MathTex`: $P = \frac{1}{1 + e^{-logit}}$. Giá trị Logit chui vào công thức.
  4. Kết quả xuất hiện: `Probability = 0.91`.
  5. Thuật toán chốt: `0.91 > Threshold (0.5)` $\rightarrow$ Cảnh báo nhấp nháy: **🚨 TRIAGE FLAG: TRUE (URGENT)**.

---

## III. QUẢN LÝ TÀI NGUYÊN BỔ TRỢ (ASSETS MAPPING)
- **Audio gốc:** `assets/audio/xray_triage_full.mp3`
- **Hình ảnh đầu vào:** Mẫu ảnh X-quang `chestxray_sample.jpg`.
- **Thư viện tham chiếu:** TenSEAL (để mô phỏng các object CKKS).

---

## IV. EXPANDED CONTENT BEATS CHO BẢN 15 PHÚT
- **Phân đoạn 4.1:** Giải thích lý do Edge Computing được sử dụng để giảm băng thông (chuyển ma trận ảnh lớn thành 10 thông số đặc trưng).
- **Phân đoạn 4.2:** Giới thiệu ngắn về thư viện TenSEAL của OpenMined, tại sao nó lại là "cầu nối" hoàn hảo giữa Data Science và FHE.
- **Phân đoạn 4.3:** Phân tích trực quan phép toán Dot Product đồng hình ($Enc(X) \cdot W$) và lý do phép toán này tốn rất ít độ sâu nhân (Multiplicative Depth = 1).
- **Phân đoạn 4.4:** Nhấn mạnh sự thông minh trong việc **chia cắt Pipeline (Split Pipeline)**: Giao phần nặng nhọc (nhân ma trận) cho Cloud, giao phần phi tuyến tính (Sigmoid) cho Client xử lý ở dạng Plaintext để tiết kiệm tài nguyên FHE tối đa.