# Act 1 - Scene 4: Keys and the Microsoft SEAL Workflow
# Mã số file code đích: scenes/01_math_crypto/scene_04_keys_and_seal_pipeline.py
# Khung thời gian: 00:45:00 -> 01:00:00 (15 phút)

## I. THÔNG TIN METADATA & ĐỒ HỌA
- Hệ màu: SecretKey và trusted client màu xanh lá; PublicKey/encoding màu vàng hoặc xanh dương; ciphertext đỏ; evaluation operations tím.
- Scene gồm 15 visual demonstration độc lập, không dùng chapter plate hoặc lưới thẻ lý thuyết nằm lâu trên màn hình.
- Audio: AI TTS tiếng Anh, nối trực tiếp từ Scene 03, mục tiêu `130 từ/phút`.

## II. KỊCH BẢN CHI TIẾT
### Phân đoạn 4.1: Key capabilities và least privilege (00:00 - 05:00)
- **Lời thoại AI (Audio Voiceover):**
  "Scene three showed relinearization and rotations using special evaluation keys. We now continue by asking who creates each key and what capability it grants. KeyGenerator samples hidden polynomial material and produces the SecretKey s of X. The key moves directly into a protected client vault. When an encrypted result arrives, the client combines that ciphertext with the SecretKey and recovers a plaintext object. The lock remains around the key because decryption authority is never sent with ordinary evaluation data. Losing this one capability compromises confidentiality, so SecretKey storage defines the trusted boundary of the application.

  The PublicKey grants a different capability. The key owner can copy it to an approved data producer without exposing the SecretKey. Inside the producer region, a plaintext vector enters the encryption operation together with the shared PublicKey. The first output is ciphertext A. Repeating randomized encryption on the same input produces ciphertext B with a different representation. Both decrypt to the same encoded value, but their bytes need not match. Public therefore means distributable for encryption, not meaningless. Architects still decide which producers receive the key and which contexts are allowed to use it.

  Relinearization Keys support maintenance after ciphertext multiplication. The enlarged ciphertext begins with three components, e-zero, e-one, and e-two. It enters a key-switching block while RelinKeys arrive through a separate green path. The extra component is absorbed, and the output returns to r-zero and r-one. The closed lock underneath shows that the result remains encrypted throughout the transformation. RelinKeys provide information related to higher secret-key powers, so they are sensitive evaluation material, but they do not perform normal decryption. Their capability is narrow: reduce representation size so later encrypted operations remain manageable.

  Galois Keys authorize movement between packed slots. The source vector contains one, two, three, four. A key for rotation by one produces four, one, two, three. A separate key for rotation by two produces three, four, one, two. The two colored paths make the authorization explicit: generating one rotation key does not automatically grant every possible shift. Microsoft SEAL can package several requested automorphisms into GaloisKeys, but each capability increases key material. The circuit should list its required rotations before key generation so the deployment creates useful movement without provisioning unnecessary operations.

  Least privilege now becomes a concrete key policy. The SecretKey attempts to cross the client-server boundary and is blocked, then returns to the client. PublicKey, RelinKeys, and only the required Galois rotations cross through separate approved paths. The bars below compare generating every possible rotation with generating only the two shifts used by the circuit. The shorter green bar represents less memory and a smaller capability surface. Evaluation keys still deserve protection and auditing, even though they cannot directly decrypt ordinary ciphertexts. A secure design sends the server exactly what its planned program needs and nothing more."

- **Hoạt ảnh Manim (Visual Actions):**
  1. `KeyGenerator` tạo SecretKey từ random samples; key vào client vault và tham gia decrypt ciphertext thành plaintext.
  2. PublicKey được sao chép sang data producer; cùng một vector được encrypt ngẫu nhiên thành hai ciphertext khác nhau.
  3. Ciphertext `e0,e1,e2` đi qua key switch với RelinKeys và thành `r0,r1`; ổ khóa xác nhận không giải mã.
  4. Hai Galois key riêng biệt tạo rotate +1 và rotate +2 trên cùng slot row.
  5. SecretKey bị chặn ở boundary; Public/Relin/Galois cần thiết đi qua. Hai bar so sánh all rotations với required only.

### Phân đoạn 4.2: Core Microsoft SEAL objects (05:00 - 10:00)
- **Lời thoại AI (Audio Voiceover):**
  "The Microsoft SEAL workflow starts by constructing EncryptionParameters. The left panel selects the C-K-K-S scheme, polynomial modulus degree 8192, and a coefficient-modulus chain with 60, 40, 40, and 60-bit primes. These choices enter SEALContext as one configuration rather than unrelated settings. The context validates whether the scheme is supported, the security constraints are acceptable, and the modulus chain is structurally valid. Only after all checks pass should the application create dependent objects. Parameters define the cryptographic universe; changing them later creates a different compatibility domain.

  A valid SEALContext builds the linked modulus chain used during evaluation. The rows descend from level three to level zero, and each lower row contains fewer active primes. As the white token visits a row, the matching parameters I-D appears on the right. That identity is not a human-readable level number stored for decoration. It connects plaintexts and ciphertexts to exact context data. Objects at different parameters identifiers cannot simply be combined because their coefficient moduli differ. The context therefore supplies both precomputation and the compatibility map used by Encryptor, Evaluator, Decryptor, and serialized objects.

  KeyGenerator follows the capability plan derived from the circuit. The first branches create the SecretKey, PublicKey, and Relinearization Keys. The purple branch creates GaloisKeys only for rotations by one and two, matching the earlier reduction schedule. This ordering matters: the application should know its operations before requesting large evaluation-key sets. The SecretKey remains the root decryption authority, while the other objects support encryption or selected evaluation tasks. KeyGenerator does not decide the deployment policy automatically. Developers must serialize, distribute, protect, rotate, and eventually retire these objects according to their distinct capabilities.

  Encoding and encryption are separate transformations. On the client, a numerical vector enters CKKSEncoder and becomes a Plaintext ring representation at the planned scale. Encryptor then uses the appropriate key to randomize that Plaintext into a Ciphertext. Only the Ciphertext crosses into the cloud region, where Evaluator can add, multiply, or rotate it. The SecretKey remains below the client pipeline. Keeping these stages visually separate prevents a common misconception: encoding changes numerical representation but provides no confidentiality, while encryption protects the encoded data. Correct applications must manage both numerical metadata and cryptographic ownership.

  Evaluator is the server-side workbench. An input ciphertext enters the purple region and passes through multiplication, rotation, and addition nodes. RelinKeys and GaloisKeys support the specific maintenance and movement operations shown below. The output is still a red encrypted result. Across the boundary, the client retains the SecretKey, and the dashed separation states that this key never enters Evaluator. The server may learn the circuit structure, operation sequence, ciphertext sizes, and runtime behavior, but it does not receive ordinary plaintext values. Evaluation is powerful computation over protected objects, not a hidden form of decryption."

- **Hoạt ảnh Manim (Visual Actions):**
  1. `EncryptionParameters` gom scheme, N và modulus chain rồi đi vào SEALContext; ba validation check lần lượt PASS.
  2. SEALContext dựng bốn modulus levels; token đi qua từng level và nối với `parms ID` riêng.
  3. KeyGenerator tách nhánh Secret/Public/Relin/Galois; Galois chỉ chứa rotation +1 và +2.
  4. Client pipeline tách rõ `vector -> CKKSEncoder -> Plaintext -> Encryptor -> Ciphertext`; chỉ ciphertext sang Evaluator.
  5. Evaluator chạy multiply/rotate/add trong cloud với evaluation keys; SecretKey đứng riêng ở trusted client.

### Phân đoạn 4.3: End-to-end SEAL lifecycle (10:00 - 15:00)
- **Lời thoại AI (Audio Voiceover):**
  "The complete deployment begins with the arithmetic circuit, not with a random parameter preset. The packed input enters three multiplication nodes before reaching the output. A purple arc records the rotations required by the reduction. The counters below summarize the design: multiplicative depth three, two rotation steps, and 4096 available slots. Unsupported branches and comparisons must already have been rewritten into compatible arithmetic. These counts become requirements for scale, modulus levels, evaluation keys, memory, and latency. Designing the graph first prevents cryptographic setup from becoming trial and error after private data arrives.

  Circuit requirements now drive parameter selection. Depth three, 4096 slots, and roughly 40 bits of working precision enter the configuration stage. The example selects polynomial modulus degree 8192, a 60, 40, 40, 60 coefficient-modulus chain, and initial scale two to the power of forty. The completed configuration enters SEALContext, which reports valid only when the settings satisfy its checks. This diagram illustrates the reasoning flow, not a universal recommendation. Production systems must use current security guidance, actual workload measurements, and the library's validation rules rather than copying educational numbers without analysis.

  After validation, the client provisions capabilities before processing data. KeyGenerator creates the SecretKey, which follows the short green path and remains on the client. Copies of the PublicKey, RelinKeys, and only Galois rotations one and two travel across the boundary to the server. Separate arrows make the ownership policy visible. The server receives enough authority to accept encrypted inputs and execute the planned circuit, but not enough to perform normal decryption. Key files, parameter files, versioning, access control, backups, and rotation procedures all belong to this provisioning stage.

  Data can now follow the prepared route. The client starts with a packed numerical vector, encodes it, and encrypts the resulting Plaintext. The red Ciphertext crosses the boundary and passes through multiplication, rotation, and addition nodes on the server. At no point does the server display a decoded slot value. The final object remains an encrypted result and returns through the application protocol. Real programs must track scale, level, size, and parameter identity along this path, but those decisions were already scheduled during circuit design. Remote evaluation should execute a plan, not improvise around metadata failures.

  The trusted client completes the lifecycle. The encrypted result enters Decryptor, then the recovered Plaintext enters the decoder. On the number line, the blue point is the ordinary plaintext baseline and the red point is the FHE result. Both lie inside the green accepted tolerance, so the numerical check reports pass. The final row reminds us that correctness alone is not enough: deployments also measure security, accuracy, latency, and memory. Act One therefore ends with one connected mental model: design the computation, validate parameters, provision minimum capabilities, evaluate encrypted data, and verify the returned numerical result."

- **Hoạt ảnh Manim (Visual Actions):**
  1. Circuit graph hiển thị packed input, ba multiply node, rotation arc và counter depth/rotations/slots.
  2. Requirements đi vào cấu hình N/modulus/scale rồi SEALContext báo VALID.
  3. SecretKey ở client; Public/Relin/Galois +1,+2 được chuyển riêng sang server.
  4. Vector đi qua encode/encrypt, ciphertext qua boundary và chuỗi multiply/rotate/add, tạo encrypted result.
  5. Client decrypt/decode; FHE point so với plaintext baseline trong tolerance, sau đó hiện Security/Accuracy/Latency/Memory.

## III. QUẢN LÝ TÀI NGUYÊN BỔ TRỢ (ASSETS MAPPING)
- Audio đồng bộ 15 phút: `assets/audio/01_math_crypto/scene_04_keys_and_seal_pipeline.mp3`
- Thư viện Manim dùng chung: các màu chuẩn và nền storyboard từ `scenes/library/constants.py`, `scenes/library/storyboard.py`; visual key, lock, SEAL object và lifecycle được định nghĩa trực tiếp trong file Scene 04.
- Tài liệu tham khảo lý thuyết: Microsoft SEAL README; `native/examples/3_levels.cpp`, `5_ckks_basics.cpp`, `6_rotation.cpp` và `7_serialization.cpp`.

## IV. EXPANDED CONTENT BEATS
- Phân đoạn 4.1: SecretKey, PublicKey, RelinKeys, GaloisKeys, capability boundary và nguyên tắc chỉ cấp các evaluation key thực sự cần thiết.
- Phân đoạn 4.2: EncryptionParameters, SEALContext và modulus chain, KeyGenerator, CKKSEncoder-Encryptor pipeline cùng vai trò server-side của Evaluator.
- Phân đoạn 4.3: thiết kế arithmetic circuit, chọn parameter theo requirements, provision key theo trust boundary, remote encrypted evaluation và decrypt-decode-verify.
- Mỗi phân đoạn gồm năm visual experiment độc lập; quyền hạn của key và vai trò của SEAL object phải được chứng minh bằng chuyển động của key, dữ liệu, ciphertext, boundary, modulus level hoặc operation node thay vì bằng các bảng chữ lý thuyết.
- Chữ trên màn hình chỉ gồm tiêu đề beat, tên object/capability, trạng thái ngắn và một câu kết luận. Phần giải thích đầy đủ nằm trong voiceover.
- Nhịp chuyển động cho mỗi hành động với easing tự nhiên. Thời gian narration còn lại dùng focus cue đổi stroke ngắn trên đúng đối tượng; không phóng object sát nhau hoặc kéo một mũi tên đơn giản chạy chậm theo toàn bộ lời thoại.
- Toàn bộ visual nằm giữa vùng tiêu đề và footer. Tiêu đề, rule và footer luôn được đưa lên lớp trước; kết thúc mỗi beat phải xóa toàn bộ mobject tạm trước khi dựng beat tiếp theo.
- Không giữ key, lock, card, boundary hoặc operation node từ beat trước. Các vùng client/server, chuỗi encode-encrypt-evaluate và các hàng parameter phải có khoảng trống đủ để mũi tên, nhãn và phép biến hình không chèn hoặc che nhau.
