import traceback


def main():
    try:
        with open("diary.txt", "a", encoding="utf-8") as diary_file:
            first_prompt = True

            while True:
                prompt = "What happened today? " if first_prompt else "What else? "
                line = input(prompt)
                diary_file.write(line + "\n")

                if line == "done for now":
                    break

                first_prompt = False

    except Exception as e:
        print(f"An exception occurred. {type(e).__name__}")
        trace_back = traceback.extract_tb(e.__traceback__)
        stack_trace = []

        for trace in trace_back:
            stack_trace.append(
                f"File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}"
            )

        print(f"Exception type: {type(e).__name__}")
        message = str(e)
        if message:
            print(f"Exception message: {message}")
        print(f"Stack trace: {stack_trace}")


if __name__ == "__main__":
    main()