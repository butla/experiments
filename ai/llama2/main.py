from pathlib import Path
from pprint import pprint

from llama_cpp import Llama


def main():
    llm = Llama(model_path=str(Path("~/Downloads/codellama-13b.Q6_K.gguf").expanduser()))

    prompt = input('\n\n=== Prompt for LLAMA2:\n')
    query_result = llm(f'Q: {prompt} A: ', max_tokens=300, stop=["Q:", "\n"], echo=True)
    for index, choice in enumerate(query_result['choices']):
        print('CHOICE', index, ':')
        pprint(choice['text'])


if __name__ == "__main__":
    main()
