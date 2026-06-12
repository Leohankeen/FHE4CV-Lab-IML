# Act 1 - Scene 3: Ciphertext Structure and Homomorphic Operations
# Mã số file code đích: scenes/01_math_crypto/scene_03_ciphertext_operations.py
# Khung thời gian: 00:30:00 -> 00:45:00 (15 phút)

## I. THÔNG TIN METADATA & ĐỒ HỌA CHUẨN
- Hệ màu: ciphertext đỏ, plaintext/scale vàng, key xanh lá, metadata xanh dương hoặc tím và trạng thái trung tính màu xám.
- Đối tượng chính: polynomial components, RNS limbs, metadata gauges, modulus levels, slot rows và các cổng arithmetic.
- Trạng thái Audio: AI TTS tiếng Anh, nối tự nhiên từ Scene 02, mục tiêu `130 từ/phút`; đọc CKKS thành "C-K-K-S", `c0/c1` thành "c-zero/c-one" và `parms_id` thành "parameters I-D".

## II. KỊCH BẢN CHI TIẾT (STORYBOARD)
### Phân đoạn 3.1: Giải phẫu một CKKS Ciphertext (00:00 - 05:00)
- **Lời thoại AI (Audio Voiceover):**
  "Scene two showed how C-K-K-S encodes and packs approximate values. We now continue by opening the ciphertext that carries those slots during computation. The red shell separates into two polynomial components, c-zero of X and c-one of X. Inside each component, the colored rows represent coefficients stored under several active Residue Number System primes. A real polynomial contains many more coefficients than the dots shown here, but the layered structure is the important idea. These are not two independent encrypted messages. Together they form one fresh ciphertext whose component count, or size, is commonly two.

  Decryption explains why both components belong together. The visual expression combines c-zero with c-one multiplied by the secret-key polynomial s of X. Only the trusted client supplies that green key. The combination reconstructs the encoded message together with a small error term, which is expected in lattice encryption. The key then returns to the client instead of remaining beside the ciphertext. This picture is an intuition, not a complete security equation, but it shows the ownership boundary: a server may transform c-zero and c-one, while only the client can combine them with the secret key and decode the hidden slots.

  Polynomial coefficients are only part of the operational state. The central ciphertext now exposes three different kinds of metadata. Two red dots show that its component size is two. The yellow gauge records a scale near two to the power of forty, which tells C-K-K-S how to interpret numerical magnitude. The colored modulus blocks identify the active parameter level. Microsoft SEAL carries this information with the ciphertext because an evaluator cannot infer compatibility from the intended plaintext meaning. Size affects operation cost, scale affects approximate arithmetic, and the parameters I-D determines which modulus set is active.

  The next diagram demonstrates a metadata failure rather than merely naming it. Ciphertext A arrives at level three with scale S, while ciphertext B arrives at level two with scale two S. Both arrows point toward an addition gate, but the gate flashes red because the states do not match. The lower operand is then adjusted to the compatible level and scale shown by the upper operand. Only after those labels agree does the gate turn green and emit a sum. In real code, level alignment and scale handling are separate decisions, but the visual makes the rule clear: related numerical values are not automatically legal operands.

  A ciphertext can travel without transferring decryption authority. On the left, the trusted client keeps the secret key below the network path. The ciphertext is serialized into a row of byte packets and sent across the boundary. On the server side, a compatible SEALContext interprets the parameters and reconstructs a loaded ciphertext object. Notice that no secret key crosses the divider and no plaintext appears during loading. Serialization preserves the encrypted data and necessary representation, while key ownership remains separate. A mismatched context cannot safely interpret the object, so deployments must coordinate parameters as carefully as they coordinate the transmitted bytes."

- **Hoạt ảnh Manim (Visual Actions):**
  1. Mở red ciphertext shell thành `c0(X)` và `c1(X)`. Legend `RNS rows` nằm thành cột riêng bên trái, không đè lên shell; màu `q2/q1/q0` được đối chiếu với các hàng chấm bên trong.
  2. Secret key `s(X)` đi từ vùng trusted client vào biểu thức `c0 + c1*s`, tạo `encoded message + small error`, rồi trở về client.
  3. Một ciphertext ở trái nối sang ba visual state riêng: hai component dots, scale gauge và chuỗi modulus blocks.
  4. Hai ciphertext khác level/scale đi vào cổng cộng; cổng báo mismatch, metadata được căn chỉnh, sau đó mới tạo output.
  5. Dùng luồng ngang năm bước tách biệt: `ciphertext -> serialize -> byte packets -> load -> compatible SEALContext`, sau đó tạo `loaded ciphertext` ở dưới context. SecretKey nằm cố định ở góc client và không đi vào luồng truyền.

### Phân đoạn 3.2: Add, Multiply và Relinearize (05:00 - 10:00)
- **Lời thoại AI (Audio Voiceover):**
  "With compatible metadata, homomorphic addition follows the ciphertext structure directly. The top operand contains c-zero and c-one, and the lower operand contains d-zero and d-one. Matching components flow along separate paths. The first output becomes c-zero plus d-zero, and the second becomes c-one plus d-one. No third component is created, so a normal size-two input pair produces a size-two sum. After decryption and decoding, packed slots approximate element-wise addition. This operation is relatively inexpensive and usually does not consume another modulus-chain level, although the operands still need compatible parameters and suitably aligned scales.

  Multiplication cost depends on which operand must remain private. On the left, encrypted x is multiplied by a public plaintext weight. The short green meter represents the cheaper path commonly used for known model parameters. On the right, both x and w are encrypted ciphertexts, so the red cost meter grows much farther. Protecting both operands requires polynomial products between ciphertext components and creates more state to maintain. This does not mean ciphertext-plaintext multiplication is free; it can still increase scale and require later rescaling. The comparison simply shows why public weights are valuable when the threat model allows them to remain unencrypted.

  Now watch two size-two ciphertexts multiply. Components c-zero and c-one meet d-zero and d-one at the multiplication gate. The result expands into three components. The first contains c-zero times d-zero. The middle combines the two cross terms, and the last contains c-one times d-one. This third term is associated with a higher power of the secret key during decryption. At the same time, two inputs with scale S produce a result with scale near S squared. The diagram therefore reveals two independent consequences of multiplication: the component count grows from two to three, and the numerical scale grows as well.

  Relinearization handles the extra component without decrypting the ciphertext. The three-component result enters a key-switching block. RelinKeys arrive through the green arrow and provide evaluation material related to higher powers of the secret key. The e-two component is absorbed by that transformation, and the output returns to two components, r-zero and r-one. The closed lock remains visible because the server has changed representation, not learned the message. Relinearization reduces future storage and computation, but it does not lower the C-K-K-S scale and it does not restore a consumed modulus level. Those are different maintenance problems.

  The three maintenance stages now appear in their normal order. Multiplication first changes the encrypted value, expands two components into three, and raises the scale. Relinearization then uses evaluation keys to return the representation to two components. Rescaling finally shortens the active modulus chain and brings the scale back toward its planned range. Follow the dots, scale bar, and level blocks rather than treating the boxes as interchangeable cleanup commands. Each stage repairs a different consequence of encrypted multiplication. A correct evaluator schedule places these operations deliberately, because changing their order can produce incompatible metadata or waste scarce modulus capacity."

- **Hoạt ảnh Manim (Visual Actions):**
  1. `c0/c1` và `d0/d1` đi theo hai đường component riêng để tạo `c0+d0`, `c1+d1`; số component vẫn là hai.
  2. Chia màn hình thành `CT x plaintext weight` và `CT x CT`; hai cost meter tăng khác nhau.
  3. Hai ciphertext size-2 đi qua multiply gate và mở ra `e0/e1/e2`; các cross term hiện dưới component tương ứng, scale chuyển `S -> S^2`.
  4. `e2` đi vào key-switch block cùng `RelinKeys`; output chỉ còn `r0/r1`. Biểu tượng ổ khóa được dựng bằng thân và vòng khóa tách biệt, đặt cạnh câu `ciphertext remains encrypted`.
  5. Pipeline `multiply -> relinearize -> rescale` dùng ba snapshot độc lập. Mỗi snapshot chứa component count, scale và số level ngay dưới stage tương ứng; không kéo thanh scale ngang qua các stage.

### Phân đoạn 3.3: Levels, Rescale, Rotations và Packed Dot Product (10:00 - 15:00)
- **Lời thoại AI (Audio Voiceover):**
  "Coefficient-modulus levels behave like a descending resource ladder. Ciphertext A begins on level three, while ciphertext B is already on level two. Sending both directly to the addition gate causes a compatibility warning. A modulus switch moves A downward by removing the final active prime, so it reaches the same parameter level as B. Their arrows can then enter the green gate and produce a sum. The direction matters: ordinary evaluation can move a ciphertext down the chain, but it cannot recreate a prime that has already been removed. Circuit planning must therefore decide where operands meet before either path descends too far.

  Modulus switching and C-K-K-S rescaling both remove an active prime, but the side-by-side animation shows why they are not identical. On the left, mod switch drops the final blue block while the displayed scale remains S. On the right, rescale drops the corresponding yellow block and changes a scale near S squared back toward S. Rescaling divides the encoded magnitude by the removed prime so the decoded value remains approximately stable. In practice, library behavior and valid scale adjustment depend on the scheme and parameters. The durable mental model is to track two coordinates after every operation: the modulus-chain level and the numerical scale.

  Rotations move information between packed positions. The source row contains one, two, three, four. A curved arrow requests a cyclic rotation to the right by one slot. GaloisKeys appear below and feed the key-switching step required by the automorphism. The resulting row becomes four, one, two, three. The first value did not travel through plaintext memory, and the server did not inspect any slot. It applied an authorized encrypted permutation. Applications generate only the rotation keys they plan to use, because every additional key consumes memory. Slot layout and required shifts should therefore be decided before key generation.

  A packed dot product combines slot-wise multiplication with rotations. The blue feature vector one, two, three, four is multiplied by the green weight vector two, one, zero, three. One ciphertext operation produces the red products two, two, zero, twelve. A rotate-by-one copy is added to form the first partial sums. A rotate-by-two copy is then added to that partial row. The final green row contains sixteen in every displayed slot, matching the ordinary dot product. Real implementations may keep the result in one target slot instead, but the staged reduction demonstrates how cross-slot aggregation emerges from rotation and addition.

  The final blueprint turns these operations into a circuit plan. The encrypted path contains three multiplication nodes, and each is followed by a planned rescale marker. A purple rotation connects the data positions needed by the reduction. The counters below record multiplicative depth three, three usable levels, rotations by one and two, and an initial scale near two to the power of forty. These are design decisions made before private input arrives. The evaluator does not improvise a missing level or rotation key at runtime. Scene four can now examine how public, secret, relinearization, and Galois keys provide exactly the capabilities this planned circuit requires."

- **Hoạt ảnh Manim (Visual Actions):**
  1. A bắt đầu ở level 3 và đi thẳng xuống level 2 bằng một mũi tên dọc; B đứng sẵn ở level 2. Khi hai ciphertext cùng hàng, một mũi tên ngang duy nhất đưa cặp đã căn chỉnh vào cổng cộng.
  2. Hai nhánh dùng bố cục `before -> after`: hàng trên có `q2,q1,q0`, hàng dưới còn `q2,q1`. Nhánh mod switch ghi `scale S unchanged`; nhánh rescale ghi `scale S^2 -> scale near S`.
  3. `[1,2,3,4]` quay phải thành `[4,1,2,3]`; `GaloisKeys` phát sáng đúng lúc key switching.
  4. Dot product diễn ra theo bốn tầng không chồng nhau: features/weights, products, rotate-1 partial, rotate-2 final.
  5. Circuit blueprint hiển thị ba multiply node, rescale marker, rotation arc và bốn counter depth/levels/rotations/scale.

## III. QUẢN LÝ TÀI NGUYÊN BỔ TRỢ (ASSETS MAPPING)
- Audio đồng bộ 15 phút: `assets/audio/01_math_crypto/scene_03_ciphertext_operations.mp3`
- Thư viện Manim dùng chung: các màu chuẩn và nền storyboard từ `scenes/library/constants.py`, `scenes/library/storyboard.py`; visual đặc thù được định nghĩa trực tiếp trong file Scene 03.
- Tài liệu tham khảo lý thuyết: Microsoft SEAL `native/examples/3_levels.cpp`, `5_ckks_basics.cpp`, `6_rotation.cpp` và `7_serialization.cpp`.

## IV. EXPANDED CONTENT BEATS
- Phân đoạn 3.1: cấu trúc `c0/c1`, RNS limbs, trực giác decryption, metadata size-scale-level, kiểm tra compatibility và serialization trong SEALContext phù hợp.
- Phân đoạn 3.2: component-wise addition, ciphertext-plaintext so với ciphertext-ciphertext multiplication, component expansion, relinearization và chuỗi maintenance multiply-relinearize-rescale.
- Phân đoạn 3.3: level alignment, mod switch so với CKKS rescale, rotation bằng GaloisKeys, packed dot product và circuit blueprint.
- Mỗi phân đoạn gồm năm visual experiment độc lập; mỗi thay đổi của ciphertext phải được chứng minh bằng chuyển động của component, scale gauge, modulus prime, level token, slot hoặc evaluation key thay vì bằng các ô chứa đoạn văn.
- Chữ trên màn hình chỉ gồm tiêu đề beat, tên component/object, metadata ngắn và một câu kết luận. Phần giải thích đầy đủ nằm trong voiceover.
- Nhịp chuyển động cho mỗi hành động với easing tự nhiên. Các quy trình nhiều bước như multiplication, relinearization, rescale và dot product phải xuất hiện theo từng tầng hoặc snapshot; không đưa mọi trạng thái lên màn hình cùng lúc.
- Toàn bộ visual nằm giữa vùng tiêu đề và footer. Tiêu đề, rule và footer luôn được đưa lên lớp trước; kết thúc mỗi beat phải xóa toàn bộ mobject tạm trước khi dựng beat tiếp theo.
- Không giữ component, mũi tên, scale bar hoặc level marker từ beat trước. Các nhóm `before/after`, hai nhánh so sánh và các tầng dot product phải có khoảng trống đủ để label, ổ khóa và phép biến hình không chèn hoặc che nhau.
