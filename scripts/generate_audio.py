import os
import asyncio
import edge_tts

VOICE = "en-US-ChristopherNeural" 
RATE = "-10%" 

# Cấu trúc dữ liệu: { "Đường_dẫn_file_đích": "Nội_dung_câu_thoại" }
AUDIO_TASKS = {
    # --- ACT 1: MATH & CRYPTO ---
    "assets/audio/01_math_crypto/01_01.mp3": "Before we can perform any encrypted computation, we must understand how data is prepared. In the CKKS scheme, we don't encrypt single numbers. Instead, we pack a vector of real numbers into what we call 'slots' inside a plaintext polynomial.",
    
    "assets/audio/01_math_crypto/01_02.mp3": "Once encoded, we apply the Public Key and add a small amount of cryptographic noise. The mathematical structure is completely masked, becoming an encrypted polynomial ring—a Ciphertext.",
    
    "assets/audio/01_math_crypto/01_03.mp3": "The true magic of Fully Homomorphic Encryption is that it allows arithmetic operations directly on these locked boxes. If we homomorphically add two ciphertexts, the underlying slots are added in parallel, without ever unlocking the boxes.",

    # --- ACT 2: FHE CNN (Scene 1: ReLU Barrier) ---
    "assets/audio/02_fhe_cnn/02_01_01.mp3": "In a standard Convolutional Neural Network, linear layers like Convolution work hand in hand with non-linear activation functions, primarily ReLU, defined as Max of zero and x. This combination allows the network to learn complex, high-dimensional visual patterns.",
    
    "assets/audio/02_fhe_cnn/02_01_02.mp3": "However, when we shift this architecture into the Homomorphic Encryption domain using schemes like RNS-CKKS, a fundamental mathematical barrier arises. FHE ciphertexts are algebraic structures—specifically, polynomial rings. They naturally support only two basic arithmetic operations: homomorphic addition and homomorphic multiplication.",
    
    "assets/audio/02_fhe_cnn/02_01_03.mp3": "The max of zero and x function is non-differentiable at zero and cannot be formed by a finite sequence of additions and multiplications. To evaluate a maximum, a processor must compare two values. But in FHE, data is completely cloaked. The cloud server is completely blind; it cannot know which value is larger without decrypting the data, which fundamentally violates privacy. This is the non-linearity wall."
}

async def generate_all_audio():
    print(f"Bắt đầu tạo {len(AUDIO_TASKS)} file audio...")
    for file_path, text in AUDIO_TASKS.items():
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        print(f"Đang tạo: {file_path}")
        communicate = edge_tts.Communicate(text, VOICE, rate=RATE)
        await communicate.save(file_path)
        
    print("Hoàn tất! Tất cả audio đã được lưu vào thư mục assets/audio/")

if __name__ == "__main__":
    asyncio.run(generate_all_audio())