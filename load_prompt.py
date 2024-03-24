from langchain.prompts import load_prompt, PromptTemplate, PipelinePromptTemplate
from collections import defaultdict
import os


dir_path = os.getcwd()+'/prompt'
sub_dirs = os.listdir(dir_path)
prompt_dict = defaultdict(PromptTemplate)

for sub_dir in sub_dirs:
    prompt = load_prompt(os.path.join(dir_path,sub_dir))
    prompt_dict[sub_dir[:-5]] = prompt


# print(prompt_dict['general_prompt'].invoke({'context':'123', 'question':'321'}))

input_prompts = [
    ("general", prompt_dict['general_prompt1']),
    ("answer_langauge", prompt_dict['answer_language']),
]
full_template = """{general}

{answer_langauge}

"""
full_prompt = PromptTemplate.from_template(full_template)
pipeline_prompt = PipelinePromptTemplate(
    final_prompt=full_prompt, pipeline_prompts=input_prompts
)
