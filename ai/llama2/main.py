from pprint import pprint

from llama_cpp import Llama


def main():
    llm = Llama(model_path="./models/7B/llama-model.gguf")
    pprint(llm("Q: Name the planets in the solar system? A: ", max_tokens=32, stop=["Q:", "\n"], echo=True))


if __name__ == "__main__":
    main()
