import torch
import time
import multiprocessing

# Set the start method to 'spawn'
multiprocessing.set_start_method("spawn", force=True)


def gpu_worker(gpu_id):
    # Set the device for this process
    torch.cuda.set_device(gpu_id)
    print(f"Process started for GPU {gpu_id}: {torch.cuda.get_device_name(gpu_id)}")

    # Multiple sizes to interleave operations
    size1 = 12288  # 96 * 128
    size2 = 8192  # 64 * 128
    dtype = torch.float16

    while True:
        # Create multiple tensors to increase parallel operations
        a1 = torch.randn(size1, size1, dtype=dtype, device=f"cuda:{gpu_id}")
        b1 = torch.randn(size1, size1, dtype=dtype, device=f"cuda:{gpu_id}")
        a2 = torch.randn(size2, size2, dtype=dtype, device=f"cuda:{gpu_id}")
        b2 = torch.randn(size2, size2, dtype=dtype, device=f"cuda:{gpu_id}")

        for _ in range(3):
            # Parallel matrix multiplications
            c1 = torch.matmul(a1, b1)
            c2 = torch.matmul(a2, b2)

            # Attention operations (tensor core optimized)
            d1 = torch.nn.functional.scaled_dot_product_attention(
                c1.view(-1, 128, 96).unsqueeze(0),
                c1.view(-1, 128, 96).unsqueeze(0),
                c1.view(-1, 128, 96).unsqueeze(0),
            ).squeeze(0)

            d2 = torch.nn.functional.scaled_dot_product_attention(
                c2.view(-1, 128, 64).unsqueeze(0),
                c2.view(-1, 128, 64).unsqueeze(0),
                c2.view(-1, 128, 64).unsqueeze(0),
            ).squeeze(0)

            # Mix compute and memory operations
            e1 = torch.nn.functional.layer_norm(c1, [size1])
            e2 = torch.nn.functional.layer_norm(c2, [size2])

            # Update matrices with mixed operations
            a1 = torch.matmul(d1.view(size1, -1), e1) / size1
            b1 = torch.matmul(e1.t(), d1.view(size1, -1))
            a2 = torch.matmul(d2.view(size2, -1), e2) / size2
            b2 = torch.matmul(e2.t(), d2.view(size2, -1))

        torch.cuda.synchronize()


def main():
    # Check if GPU is available
    if not torch.cuda.is_available():
        print("No GPU available!")
        return

    num_gpus = torch.cuda.device_count()
    print(f"Found {num_gpus} GPUs")

    # Create processes for each GPU
    processes = []
    for gpu_id in range(num_gpus):
        p = multiprocessing.Process(target=gpu_worker, args=(gpu_id,))
        p.start()
        processes.append(p)

    # Wait for all processes to complete (which they won't in this case)
    for p in processes:
        p.join()


if __name__ == "__main__":
    main()
