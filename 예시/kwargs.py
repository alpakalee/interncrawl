def example_function(arg1, arg2, **kwargs):
    print(f"arg1: {arg1}")
    print(f"arg2: {arg2}")
    for key, value in kwargs.items():
        print(f"{key}: {value}")

example_function(1, 2, third=3, fourth=4, fifth=5)
