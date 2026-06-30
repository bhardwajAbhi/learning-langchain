from langchain_ollama.chat_models import ChatOllama

llm = ChatOllama(model="gemma:2b")

query = "Which operating system is the most popular in mobile devices?"
print("Query:", query)

response = llm.invoke(query)

print("Response:", response.content)

"""
Query: Which operating system is the most popular in mobile devices?
Response: content='Android is the most popular operating system in mobile devices, with a market share of over 80%.' 
additional_kwargs={} response_metadata={'model': 'gemma:2b', 'created_at': '2026-06-30T09:55:51.581108758Z', 'done': True, 
'done_reason': 'stop', 'total_duration': 814374719, 'load_duration': 93605697, 'prompt_eval_count': 33, 'prompt_eval_duration': 99404120, 
'eval_count': 22, 'eval_duration': 610037131, 'logprobs': None, 'model_name': 'gemma:2b', 'model_provider': 'ollama'} 
id='lc_run--019f17f4-db6c-77f3-b348-559b6c6ec57f-0' tool_calls=[] invalid_tool_calls=[] usage_metadata={'input_tokens': 33, 'output_tokens': 22, 'total_tokens': 55}
"""