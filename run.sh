# python traffic4.py gtsrb | tee traffic-4-1.txt
# python traffic5.py gtsrb | tee traffic-5-1.txt
# python traffic6.py gtsrb | tee traffic-6-1.txt

# python traffic_Conv2d_KernelSizes4.py gtsrb | tee traffic-4-1.txt
# python traffic_Conv2d_KernelSizes5.py gtsrb | tee traffic-5-1.txt
# python traffic_Conv2d_KernelSizes6.py gtsrb | tee traffic-6-1.txt
# python traffic_Conv2d_KernelSizes7.py gtsrb | tee traffic-7-1.txt

# python traffic_Conv2d_KernelSizes6-filter16.py gtsrb | tee traffic_KernelSizes6-filter16-1.txt
# python traffic_Conv2d_KernelSizes6-filter64.py gtsrb | tee traffic_KernelSizes6-filter64-1.txt
# python traffic_Conv2d_KernelSizes6-denseNumCat16.py gtsrb | tee traffic_KernelSizes6-denseNumCat16-1.txt
# python traffic_Conv2d_KernelSizes6-denseNumCat32.py gtsrb | tee traffic_KernelSizes6-denseNumCat32-1.txt
# python traffic_Conv2d_KernelSizes6-denseNumCat64.py gtsrb | tee traffic_KernelSizes6-denseNumCat64-1.txt

# python traffic_Conv2d_KernelSizes6-denseNumCat16-16.py gtsrb | tee traffic_KernelSizes6-denseNumCat16-16-1.txt
# python traffic_Conv2d_KernelSizes6-denseNumCat128-64.py gtsrb | tee traffic_KernelSizes6-denseNumCat128-64-1.txt

# python traffic_Conv2d_KernelSizes3-denseNumCat16-16.py gtsrb | tee traffic_KernelSizes3-denseNumCat16-16-1.txt
# python traffic_Conv2d_KernelSizes3-denseNumCat128-64.py gtsrb | tee traffic_KernelSizes3-denseNumCat128-64-1.txt

# python traffic.py gtsrb 43 128 0.5 | tee out/1conv2d-43_3-3_1dense128_1drop05.txt
# python traffic.py gtsrb 32 256 0.5 | tee out/1conv2d-32_3-3_1dense256_1drop05.txt
# python traffic.py gtsrb 32 128 0.2 | tee out/1conv2d-32_3-3_1dense128_1drop02.txt

# python traffic.py gtsrb 43 128 0.2 | tee out/1conv2d-43_3-3_1dense128_1drop02.txt

# python traffic_2dense_1dropout.py gtsrb 43 128 128 0.5 | tee out/1conv2d-43_3-3_2dense128-128_1drop05.txt
# python traffic_2dense_1dropout.py gtsrb 43 128 64 0.5 | tee out/1conv2d-43_3-3_2dense128-64_1drop05.txt
# python traffic_2dense_1dropout.py gtsrb 43 128 32 0.5 | tee out/1conv2d-43_3-3_2dense128-32_1drop05.txt
# python traffic_2dense_1dropout.py gtsrb 43 128 16 0.5 | tee out/1conv2d-43_3-3_2dense128-16_1drop05.txt

# python traffic_2dense_1dropout.py gtsrb 43 128 128 0.2 | tee out/1conv2d-43_3-3_2dense128_128_1drop02.txt
# python traffic_2dense_1dropout.py gtsrb 43 128 64 0.2 | tee out/1conv2d-43_3-3_2dense128_64_1drop02.txt
# python traffic_2dense_1dropout.py gtsrb 43 128 32 0.2 | tee out/1conv2d-43_3-3_2dense128-32_1drop02.txt
# python traffic_2dense_1dropout.py gtsrb 43 128 16 0.2 | tee out/1conv2d-43_3-3_2dense128-16_1drop02.txt

# python traffic_2dense_2dropout.py gtsrb 43 128 128 0.5 | tee out/1conv2d-43_3-3_2dense128-128_2drop05.txt
# python traffic_2dense_2dropout.py gtsrb 43 128 64 0.5 | tee out/1conv2d-43_3-3_2dense128-64_2drop05.txt
# python traffic_2dense_2dropout.py gtsrb 43 128 32 0.5 | tee out/1conv2d-43_3-3_2dense128-32_2drop05.txt
# python traffic_2dense_2dropout.py gtsrb 43 128 16 0.5 | tee out/1conv2d-43_3-3_2dense128-16_2drop05.txt

# python traffic_2dense_2dropout.py gtsrb 43 128 128 0.2 | tee out/1conv2d-43_3-3_2dense128_128_2drop02.txt
# python traffic_2dense_2dropout.py gtsrb 43 128 64 0.2 | tee out/1conv2d-43_3-3_2dense128_64_2drop02.txt
# python traffic_2dense_2dropout.py gtsrb 43 128 32 0.2 | tee out/1conv2d-43_3-3_2dense128-32_2drop02.txt
# python traffic_2dense_2dropout.py gtsrb 43 128 16 0.2 | tee out/1conv2d-43_3-3_2dense128-16_2drop02.txt

# python traffic_2dense_2dropout.py gtsrb 43 128 16 0.2 | tee out/1conv2d-43_3-3_2dense128-16_2drop02.txt

# python traffic_2dense_2dropout.py gtsrb 43 128 64 0.1 | tee out/1conv2d-43_3-3_2dense128-64_2drop01.txt
# python traffic_2dense_2dropout.py gtsrb 43 128 32 0.1 | tee out/1conv2d-43_3-3_2dense128-32_2drop01.txt
# python traffic_2dense_2dropout.py gtsrb 43 128 16 0.1 | tee out/1conv2d-43_3-3_2dense128-16_2drop01.txt

# python traffic_2dense_3dropout.py gtsrb 43 128 64 64 0.1 | tee out/1conv2d-43_3-3_3dense128-64-64_3drop01.txt
python traffic_2dense_3dropout.py gtsrb 43 128 64 32 0.1 | tee out/1conv2d-43_3-3_3dense128-64-32_3drop01.txt
python traffic_2dense_3dropout.py gtsrb 43 128 64 16 0.1 | tee out/1conv2d-43_3-3_3dense128-64-16_3drop01.txt

python traffic_2dense_3dropout.py gtsrb 43 128 32 64 0.1 | tee out/1conv2d-43_3-3_3dense128-32-64_3drop01.txt
python traffic_2dense_3dropout.py gtsrb 43 128 32 32 0.1 | tee out/1conv2d-43_3-3_3dense128-32-32_3drop01.txt
python traffic_2dense_3dropout.py gtsrb 43 128 32 16 0.1 | tee out/1conv2d-43_3-3_3dense128-32-16_3drop01.txt

python traffic_2dense_2dropout.py gtsrb 43 256 128 0.1 | tee out/1conv2d-43_3-3_2dense256-128_2drop01.txt
# python traffic_2dense_3dropout.py gtsrb 43 128 32 16 0.1 | tee out/1conv2d-43_3-3_3dense128-32-16_3drop01.txt





# python traffic_3dense_dropout.py gtsrb 43 128 64 0.2 | tee out/1conv2d-43_3-3_1dense128-16_1drop02.txt