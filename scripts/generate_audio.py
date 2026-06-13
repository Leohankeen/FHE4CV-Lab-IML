import os
import asyncio
import edge_tts

VOICE = "en-US-GuyNeural" 
RATE = "+0%" 
VOLUME = "+10%"

AUDIO_TASKS = {
    # --- ACT 2: Scene 1 (The Non-Linearity Wall - Wei Ao Tutorial Alignment) - 15 Mins ---
    "assets/audio/02_fhe_cnn/02_01_01.mp3": (
        "In a standard Convolutional Neural Network, the architecture typically involves convolution, batch normalization, and a ReLU activation. "
        "However, when we transition to Fully Homomorphic Encryption to protect user data, we face a fundamental restriction. "
        "FHE only natively supports one-dimensional vector addition, multiplication, and rotation. "
        "Because the ReLU function relies on a maximum operation, it is not a valid polynomial and cannot be directly evaluated on encrypted data."
    ),
    "assets/audio/02_fhe_cnn/02_01_02.mp3": (
        "To adapt these networks, we must replace the non-linear ReLU with polynomial approximations. "
        "But this introduces a significant conflict between the multiplicative depth, meaning the number of multiplications, and the approximation precision. "
        "If we use a low-degree polynomial, it is computationally fast and requires less bootstrapping, but the approximation is poor and necessitates network retraining."
    ),
    "assets/audio/02_fhe_cnn/02_01_03.mp3": (
        "Conversely, if we construct a high-degree approximation, such as a composed polynomial of degree 7 times 7 times 27, "
        "the fit against the ReLU function is highly accurate, eliminating the need to retrain the network. "
        "However, evaluating such high-degree polynomials consumes our multiplication budget rapidly, triggering expensive bootstrapping operations that severely degrade inference speed."
    ),
    "assets/audio/02_fhe_cnn/02_01_04.mp3": (
        "Beyond the degree, the choice of polynomial basis is also crucial. "
        "While standard power basis is simple, employing orthogonal polynomials like Chebyshev or Hermite polynomials "
        "allows the network to capture and preserve more information during the approximation of activation functions."
    ),
    "assets/audio/02_fhe_cnn/02_01_05.mp3": (
        "It is also important to correctly calculate the evaluation cost, defined by the multiplicative depth. "
        "For instance, computing x to the power of four does not require three sequential multiplications. "
        "We can first compute x squared, and then square that result, meaning x to the power of four only consumes a depth of two."
    ),
    "assets/audio/02_fhe_cnn/02_01_06.mp3": (
        "In modern implementations, we typically favor low-degree polynomials to ensure fast inference, which requires retraining the network. "
        "This brings a new challenge: numerical instability during training. "
        "During backpropagation, polynomial activations can easily cause exploding gradients."
    ),
    "assets/audio/02_fhe_cnn/02_01_07.mp3": (
        "While we can clip gradients during backpropagation, forward propagation issues cannot be fixed with simple clipping because the maximum function is too expensive in FHE. "
        "The state-of-the-art solution is to introduce basis-wise normalization, normalizing each polynomial degree separately "
        "before aggregating them with trainable weights, effectively stabilizing the training process."
    ),
    # --- ACT 2: Scene 2 (Polynomial Approximation) - 20 Minutes Math Deep Dive ---
    "assets/audio/02_fhe_cnn/02_02_01.mp3": (
        "To bypass the non-linearity barrier of homomorphic encryption, we must turn to numerical analysis. "
        "Since the encrypted domain natively supports only addition and multiplication, we must replace the non-differentiable ReLU function "
        "with a smooth polynomial curve. A naive Taylor series expansion fails drastically as activation values grow away from the origin. "
        "Instead, we use Minimax approximation to minimize the maximum error over a specific interval, allowing the network to retain non-linearity purely through arithmetic."
    ),
    "assets/audio/02_fhe_cnn/02_02_02.mp3": (
        "However, higher degree polynomials come at a severe cryptographic cost. Every multiplication consumes a level in our modulus chain, "
        "known as the multiplicative depth. But evaluating the cost is non-trivial. For example, computing x to the power of four "
        "does not require three sequential multiplications. By computing x squared and then squaring the result, the multiplicative depth is only two. "
        "Thus, tracking the true depth is critical for efficiency."
    ),
    "assets/audio/02_fhe_cnn/02_02_03.mp3": (
        "Furthermore, not all polynomials are born equal. Instead of the standard power basis, using orthogonal bases like Chebyshev or Hermite polynomials "
        "captures the data distribution more effectively. To balance accuracy and latency, the AutoFHE framework automates the search for optimal polynomial degrees. "
        "It dynamically assigns low-degree polynomials to layers that tolerate error, and high-degree approximations only where mathematically necessary."
    ),
    "assets/audio/02_fhe_cnn/02_02_04.mp3": (
        "Eventually, deep evaluations consume the depth budget, and the ciphertext must be refreshed via Bootstrapping. "
        "But CKKS packing introduces a hidden danger: during the heavy transformations of bootstrapping, numerical errors leak into the imaginary component. "
        "In deep networks, this imaginary leakage amplifies catastrophically. To prevent this, Imaginary-Removing Bootstrapping systematically projects "
        "the ciphertext back to the real subspace, cleansing the noise completely."
    ),
    # --- ACT 2: Scene 3 (Naive CNN Bottleneck) - 10 Minutes Math Deep Dive ---
    "assets/audio/02_fhe_cnn/02_03_01.mp3": (
        "As we transition neural networks into the encrypted domain, a naive approach might be to encrypt each individual pixel into its own separate ciphertext. "
        "While mathematically sound, this mapping is disastrously inefficient. The CKKS encryption scheme operates on massive polynomials, acting as a powerful vector processor. "
        "A single ciphertext can natively pack thousands of complex-valued slots. If we place only one scalar pixel into this structure, we are utilizing a fraction of a percent of the available cryptographic bandwidth. "
        "The remaining slots are filled with zeros or cryptographic noise. Yet, despite being empty, they still incur the massive computational cost of homomorphic evaluation of the entire polynomial."
    ),
    "assets/audio/02_fhe_cnn/02_03_02.mp3": (
        "This extreme underutilization directly triggers a far more fatal bottleneck: the bootstrapping traffic jam. "
        "Because our image data is distributed across thousands of nearly-empty ciphertexts, evaluating a convolutional layer requires an astronomical number of sequential homomorphic multiplications. "
        "Each multiplication rapidly consumes the multiplicative depth of the ciphertexts. When this depth is exhausted, every single sparse ciphertext must individually undergo bootstrapping to refresh its noise budget. "
        "Bootstrapping is the most computationally expensive operation in FHE. Forcing the server to sequentially bootstrap thousands of mostly empty ciphertexts creates a massive processing queue. "
        "The inference latency skyrockets from seconds to days, grinding the throughput to an absolute halt. A paradigm shift in data packing is strictly required."
    ),

    # --- ACT 2: Scene 4 (Multiplexed Parallel Convolutions) - 25 Minutes Math Deep Dive ---
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