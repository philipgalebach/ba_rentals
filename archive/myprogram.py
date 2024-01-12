def write_hello_world_to_file():
    with open("hello_world.txt", "w") as file:
        file.write("Hello World")

if __name__ == "__main__":
    write_hello_world_to_file()
    print("Hello World has been written to hello_world.txt")
