from transformers import pipeline, set_seed

# def hugging_face_test(length: int, outpath: str):
generator = pipeline('text-generation', model='gpt2')
set_seed(50)
text = generator("this is a test for hugging face", max_length=200, num_return_sequences=5)
print(text)