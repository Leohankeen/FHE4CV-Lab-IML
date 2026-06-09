Title:
Computer Vision over Homomorphically Encrypted Data | Secure Medical X-ray Demo with TenSEAL

Description:
Demo project minh họa Computer Vision over Homomorphically Encrypted Data cho case xử lý ảnh X-ray y tế bảo mật.

Pipeline:
1. Hospital/client giữ ảnh X-ray gốc ở local.
2. Client trích xuất feature vector nhỏ.
3. Feature vector được mã hóa bằng TenSEAL CKKS.
4. Cloud server tính linear triage score trực tiếp trên ciphertext.
5. Doctor/client giải mã score và đọc kết quả.

Ghi chú: Đây là prototype giáo dục để giải thích encrypted inference, không phải mô hình chẩn đoán y tế.

Suggested chapters:
00:00 Problem: medical image privacy
00:35 Why standard encryption is not enough for cloud inference
01:15 Homomorphic encryption and CKKS
02:10 TenSEAL pipeline
03:05 Encrypted linear scoring demo
04:00 Manim visualization
04:40 Limitations and next steps

Keywords:
Fully Homomorphic Encryption, FHE, TenSEAL, CKKS, Computer Vision, Medical Imaging, X-ray, Privacy Preserving AI, Encrypted Inference, Manim
