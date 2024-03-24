from langchain_community.llms import Ollama


class OllamaLlm:
    def __init__(self):
        self.llm = Ollama(model="llama2")

    def __call__(self, text, *args, **kwargs):
        return self.llm(text)
