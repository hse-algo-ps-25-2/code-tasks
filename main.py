from bd_generator import BDGenerator


def main():
    generator = BDGenerator()
    result = generator.generate_band_determinant(-10, 10)
    print(result)


if __name__ == "__main__":
    main()
