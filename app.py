def add(a, b):
    return a + b

def main():
    print("Simple calculator!")
    a = int(input("Enter first number: "))
    b = int(input("Enter second number: "))
    print(f"The sum is: {add(a, b)}")

if __name__ == "__main__":
    main()
