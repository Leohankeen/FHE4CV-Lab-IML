# Metadata YouTube - Khóa học trực quan FHE4CV

## Tiêu đề chính

FHE4CV: Computer Vision trên dữ liệu mã hóa | CKKS, FHE-CNN và Private AI

## Tiêu đề thay thế

1. Fully Homomorphic Encryption cho Computer Vision | CKKS, CNN và Private AI
2. Computer Vision không cần giải mã: Khóa học trực quan về FHE và CKKS
3. Privacy-Preserving Computer Vision | Từ nền tảng CKKS đến ứng dụng FHE

## Mô tả

Liệu một Cloud Server có thể thực hiện các phép tính Computer Vision mà không
bao giờ nhìn thấy dữ liệu đầu vào riêng tư?

Khóa học trực quan này trình bày Computer Vision over Homomorphically Encrypted
Data, từ nền tảng toán học đến thiết kế hệ thống thực tế. Thông qua hoạt ảnh
Manim, CKKS, các khái niệm của Microsoft SEAL và thí nghiệm bằng TenSEAL, video
mô tả toàn bộ hành trình của dữ liệu mã hóa: encoding, homomorphic arithmetic,
biến đổi Neural Network để tương thích với FHE và các ứng dụng
Privacy-Preserving AI.

Nội dung được tổ chức thành ba Act:

- Act 1 xây dựng nền tảng toán học và mật mã học: bài toán data in use,
  homomorphic correctness, polynomial ring, trực giác RLWE, CKKS encoding,
  SIMD packing, scale, modulus chain, cấu trúc ciphertext, relinearization,
  rotation và các key capability trong Microsoft SEAL.
- Act 2 giải thích vì sao CNN thông thường không thể được chuyển trực tiếp sang
  FHE: rào cản ReLU và comparison, polynomial activation approximation,
  multiplicative depth, chi phí bootstrapping, lãng phí SIMD slot và
  multiplexed parallel convolution.
- Act 3 kết nối lý thuyết với các demo định hướng ứng dụng: CryptoFace,
  Privacy-Preserving Health Record System, Private Image Matching và pipeline
  X-ray linear triage sử dụng TenSEAL CKKS.

Trong thí nghiệm X-ray, ảnh gốc luôn được giữ tại Client. Client trích xuất một
feature vector nhỏ, mã hóa vector bằng CKKS và chỉ gửi ciphertext đến Server.
Server thực hiện encrypted linear scoring, trong khi sigmoid, threshold và
quyết định cuối cùng chỉ được xử lý tại Client sau khi giải mã.

Kết quả benchmark trên workspace hiện tại với tám ảnh mẫu:

- Thời gian CKKS encryption trung bình: khoảng 6,49 ms
- Thời gian encrypted dot product trung bình: khoảng 8,30 ms
- Thời gian decryption trung bình: khoảng 0,74 ms
- Tổng thời gian encrypted pipeline trung bình: khoảng 15,53 ms
- Sai số logit tuyệt đối trung bình giữa encrypted và plaintext: khoảng 2,54e-7
- Kích thước ciphertext sau serialization trung bình: khoảng 334 KB

Các số liệu trên được thu thập từ môi trường thử nghiệm của dự án và chỉ mang
tính chất minh họa. Kết quả thực tế có thể thay đổi theo phần cứng, phiên bản
thư viện và bộ CKKS parameters được sử dụng.

Điểm cốt lõi của kiến trúc:

- Dữ liệu riêng tư và Secret Key luôn thuộc Trusted Client.
- Cloud chỉ nhận ciphertext và evaluation capabilities cần thiết.
- Các phép tính được thực hiện trực tiếp trong encrypted domain.
- Kết quả vẫn ở dạng ciphertext cho đến khi quay về Client.
- Quyền giải mã không bao giờ được chuyển cho Cloud Server.

Lưu ý quan trọng: repository và video này là prototype phục vụ nghiên cứu,
giảng dạy và minh họa kỹ thuật. Mô hình X-ray sử dụng các trọng số cố định dành
cho demo, không được huấn luyện hoặc kiểm định cho chẩn đoán lâm sàng. Mọi kết
quả trong video không phải tư vấn y tế và không được sử dụng để đưa ra quyết
định điều trị.

Source code: [THÊM URL REPOSITORY]

Công nghệ sử dụng: Python, Manim, TenSEAL, Microsoft SEAL concepts, CKKS,
NumPy, Pillow, OpenCV, PyTorch và scikit-learn.

Tài liệu tham khảo:

- FHE4CV CVPR 2025 Tutorial: https://fhe4cv.github.io/
- TenSEAL: https://github.com/OpenMined/TenSEAL
- Microsoft SEAL: https://github.com/microsoft/SEAL

#FullyHomomorphicEncryption #PrivacyPreservingAI #ComputerVision

## Chapters

00:00 Act 1 - Tại sao cần Homomorphic Encryption?
15:00 CKKS Encoding, Packing và Parameters
30:00 Cấu trúc Ciphertext và Homomorphic Operations
45:00 Key Management và Microsoft SEAL Workflow

1:00:00 Act 2 - Rào cản Non-Linearity
1:15:00 Polynomial Approximation cho Encrypted Activation
1:35:00 Bottleneck khi chuyển đổi CNN theo cách thông thường
1:45:00 Multiplexed Parallel Convolution

2:10:00 Act 3 - CryptoFace và Encrypted Face Recognition
2:25:00 HERS - Privacy-Preserving Health Record System
2:40:00 Private Image Matching
2:55:00 Medical X-Ray FHE Demo với TenSEAL

## Tags

Fully Homomorphic Encryption, FHE, CKKS, RNS-CKKS, Microsoft SEAL, TenSEAL,
Computer Vision, Encrypted Inference, Privacy-Preserving AI, Private AI,
Homomorphic Encryption Tutorial, FHE-CNN, Encrypted Neural Network,
Polynomial Approximation, Multiplicative Depth, Bootstrapping, SIMD Packing,
Ciphertext Rotation, Relinearization, CryptoFace, Medical Imaging, X-ray AI,
Private Image Matching, Manim, Python Cryptography

## Nội dung đề xuất cho Thumbnail

1. COMPUTER VISION KHÔNG CẦN GIẢI MÃ
2. AI TÍNH TOÁN - CLOUD KHÔNG THỂ ĐỌC
3. FHE + COMPUTER VISION
4. PRIVATE AI VỚI CKKS

## Bố cục Thumbnail đề xuất

- Bên trái: ảnh hoặc feature grid plaintext nằm trong Trusted Client.
- Chính giữa: biểu tượng ổ khóa nổi bật và CKKS ciphertext đang vượt qua trust
  boundary.
- Bên phải: Cloud Evaluator tạo ra encrypted result.
- Dòng chữ chính: `AI TÍNH TOÁN - CLOUD KHÔNG THỂ ĐỌC`.
- Màu nhấn: xanh cyan cho plaintext, đỏ cho ciphertext, vàng cho encryption
  operations và xanh lá cho client-side decryption.

## Bình luận ghim đề xuất

Đây là dự án nghiên cứu và minh họa về Fully Homomorphic Encryption dành cho
Computer Vision. Bạn muốn nội dung tiếp theo đi sâu vào chủ đề nào: CKKS
encoding, polynomial activation, ciphertext rotation, bootstrapping,
CryptoFace hay pipeline X-ray bằng TenSEAL?

Kết quả X-ray chỉ là demo kỹ thuật, không phải kết quả chẩn đoán lâm sàng.

Repository: https://github.com/Leohankeen/FHE4CV-Lab-IML.git
