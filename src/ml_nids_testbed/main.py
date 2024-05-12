from methods import boil_the_frog

if __name__ == '__main__':
    boil_the_frog.boil_the_frog_linear_rps_constant_bytes("10.5.0.2", 80, min_rps=3000, max_rps=80000, increment_size=100)
