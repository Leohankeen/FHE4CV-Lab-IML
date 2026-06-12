import os
import asyncio
import edge_tts

VOICE = "en-US-GuyNeural" 
RATE = "+0%" 
VOLUME = "+10%"

AUDIO_TASKS = {
    # --- ACT 2: Scene 1 (The Non-Linearity Wall) - Kịch bản 3B1B Mở rộng ---
    "assets/audio/02_fhe_cnn/02_01_01.mp3": (
        "Let's begin by unpacking the core engine of a Convolutional Neural Network. "
        "Visually, convolution is just a kernel sliding across an image. "
        "But mathematically, it is a strict linear transformation. We take a patch of pixels, multiply them by learned weights, and sum them up. "
        "This is simply a dot product. It extracts local features like edges or textures."
    ),
    "assets/audio/02_fhe_cnn/02_01_02.mp3": (
        "However, a fundamental rule of linear algebra states that the composition of any number of linear transformations is, itself, just another linear transformation. "
        "If our network only contained convolutional layers, a hundred-layer deep network would mathematically collapse into a single, flat linear layer. "
        "It would be entirely incapable of learning complex, non-linear boundaries in high-dimensional space."
    ),
    "assets/audio/02_fhe_cnn/02_01_03.mp3": (
        "This is why we introduce the ReLU activation function. "
        "By simply taking the maximum of zero and x, ReLU maps all negative values to zero. "
        "This single sharp bend, this non-linearity, breaks the linear collapse. It allows deep networks to fold and partition the input space into highly complex decision regions."
    ),
    "assets/audio/02_fhe_cnn/02_01_04.mp3": (
        "Now, let us transport this architecture into the realm of Fully Homomorphic Encryption, specifically the RNS-CKKS scheme. "
        "When data is encrypted, its representation fundamentally changes. A simple scalar pixel value is encoded and embedded into a polynomial ring."
    ),
    "assets/audio/02_fhe_cnn/02_01_05.mp3": (
        "A ciphertext is no longer a number; it is a pair of massive polynomials with coefficients in a finite field. "
        "Because these ciphertexts exist within an algebraic ring, they natively support only two operations: addition, and multiplication. "
        "We can add polynomials, and we can multiply them. That is the entire instruction set."
    ),
    "assets/audio/02_fhe_cnn/02_01_06.mp3": (
        "And here we hit the mathematical barrier: The Non-Linearity Wall. "
        "Consider the ReLU function again. To compute the maximum of zero and x, the processor must execute a comparison: is x greater than zero? "
        "But the cloud server holding our ciphertext is completely blind. It only sees cryptographic noise."
    ),
    "assets/audio/02_fhe_cnn/02_01_07.mp3": (
        "Without the secret key, determining the sign of an encrypted value is mathematically impossible. "
        "Any operation that requires a branch, a condition, or a comparison cannot be evaluated natively. "
        "Thus, the essential bend of ReLU becomes a hard wall, halting our encrypted neural network completely."
    ),
    # --- ACT 2: Scene 2 (Polynomial Approximation) - 20 Minutes ---
    "assets/audio/02_fhe_cnn/02_02_01.mp3": (
        "To bypass the non-linearity barrier of homomorphic encryption, we must turn to numerical analysis. "
        "Since the encrypted domain natively supports only addition and multiplication, we can evaluate any polynomial function. "
        "Therefore, the mathematical solution is to replace the sharp, non-differentiable broken line of the ReLU function "
        "with a smooth, continuous polynomial curve. By carefully tuning the coefficients of this polynomial, we can minimize "
        "the approximation error over a specific interval, allowing the neural network to retain its non-linear properties entirely through arithmetic operations."
    ),
    "assets/audio/02_fhe_cnn/02_02_02.mp3": (
        "However, not all polynomials are born equal. A naive Taylor series expansion might work near the origin but fails drastically "
        "as the activation values grow. Furthermore, polynomials of higher degrees provide a tighter fit to the ReLU function, but they come at a severe cryptographic cost. "
        "Every multiplication consumes a level in our modulus chain, known as the multiplicative depth. The AutoFHE framework dynamically searches "
        "for the optimal balance. It selects the lowest possible polynomial degree that preserves the network's overall classification accuracy, layer by layer."
    ),
    "assets/audio/02_fhe_cnn/02_02_03.mp3": (
        "As these high-degree polynomials are evaluated, homomorphic noise and approximation errors accumulate. Eventually, the ciphertext must be refreshed using a process called Bootstrapping. "
        "But there is a hidden danger. The packing mechanism in CKKS encodes data into complex-valued slots. During the heavy transformations of bootstrapping, "
        "small numerical errors leak into the imaginary component. In deep networks like ResNet, this imaginary leakage will amplify and catastrophically destroy the real data. "
        "To prevent this, Lee and colleagues introduced Imaginary-Removing Bootstrapping, a technique that systematically projects the ciphertext back to the real subspace, cleansing the noise completely."
    ),
    # --- ACT 2: Scene 3 (Naive CNN Bottleneck) - 10 Minutes ---
    "assets/audio/02_fhe_cnn/02_03_01.mp3": (
        "As we transition neural networks into the encrypted domain, a naive approach might be to encrypt each pixel or feature map activation into its own individual ciphertext. "
        "While mathematically sound, this approach is disastrously inefficient. The CKKS encryption scheme operates on massive polynomials, acting as a powerful vector processor. "
        "A single ciphertext can pack thousands of complex-valued slots. If we place only one scalar pixel into one ciphertext, we are effectively utilizing less than a fraction of a percent of the available cryptographic bandwidth. "
        "The remaining thousands of slots are filled with zeros or cryptographic noise. They carry no useful information, yet they still incur the massive computational cost of homomorphic operations. "
        "This severe slot underutilization is the first major bottleneck."
    ),
    "assets/audio/02_fhe_cnn/02_03_02.mp3": (
        "This extreme inefficiency directly triggers the second, far more fatal bottleneck: the bootstrapping traffic jam. "
        "Because we have distributed our image data across thousands of nearly-empty ciphertexts, every convolutional layer requires an astronomical number of homomorphic multiplications. "
        "Each multiplication consumes a portion of our multiplicative depth. When the depth is exhausted, every single one of these sparse ciphertexts must individually undergo bootstrapping to refresh its noise budget. "
        "Bootstrapping is the most computationally expensive operation in fully homomorphic encryption. Forcing the server to sequentially bootstrap thousands of mostly empty ciphertexts creates a massive queue. "
        "The inference latency skyrockets from seconds to days, and the throughput grinds to an absolute halt. To make encrypted computer vision practical, we desperately need a paradigm shift in data packing."
    ),

    # --- ACT 2: Scene 4 (Multiplexed Parallel Convolutions) - 25 Minutes ---
    "assets/audio/02_fhe_cnn/02_04_01.mp3": (
        "To overcome the severe inefficiencies of naive encryption, researchers introduced a paradigm shift: Multiplexed Parallel Convolutions. "
        "Instead of assigning a single pixel to a colossal ciphertext, we can deeply pack the data. By interleaving spatial pixels and multiple feature map channels "
        "into a single, unified vector, we can achieve nearly one hundred percent slot utilization. The sparse, empty voids of the ciphertext are now dense with information, "
        "allowing the CKKS scheme to act as a massive SIMD processor, evaluating thousands of pixels simultaneously."
    ),
    "assets/audio/02_fhe_cnn/02_04_02.mp3": (
        "This dense packing strategy unlocks a profound mathematical advantage during homomorphic convolution. In standard evaluation, sliding a kernel over an image "
        "requires a massive number of ciphertext rotations, which are computationally exorbitant. However, with multiplexed packing, the channels are systematically aligned. "
        "A single shared homomorphic rotation can shift the entire batched tensor at once, evaluating convolutions across multiple channels concurrently. "
        "This elegant alignment reduces the required number of rotations to a mere thirty-eight percent compared to naive layouts, drastically slashing the inference latency."
    ),
    "assets/audio/02_fhe_cnn/02_04_03.mp3": (
        "By combining continuous polynomial approximations, optimized degree tradeoffs, imaginary-removing bootstrapping, and multiplexed parallel convolutions, "
        "the impossible becomes possible. We can now construct deep, encrypted neural networks. Data flows through residual blocks, safely shielded by cryptographic noise. "
        "When the multiplicative depth runs low, our stable bootstrapping refreshes the ciphertext, projecting it back to the real subspace. "
        "This holistic architecture successfully evaluates ResNet-20 and even ResNet-110 over fully homomorphic encryption, achieving unprecedented speedups and maintaining a strict 128-bit security target."
    ),
}

async def generate_all_audio():
    print(f"Bắt đầu tạo {len(AUDIO_TASKS)} file audio...")
    for file_path, text in AUDIO_TASKS.items():
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        print(f"Đang tạo: {file_path}")
        communicate = edge_tts.Communicate(text, VOICE, rate=RATE, volume=VOLUME)
        await communicate.save(file_path)
    print("Hoàn tất! Tất cả audio đã được lưu vào thư mục assets/audio/")

if __name__ == "__main__":
    asyncio.run(generate_all_audio())