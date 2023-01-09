import cohere
co = cohere.Client('Rs6AKQKNDRaU8yMiBviX26d7SJZG71mzOVKAYpQT')
response = co.generate(prompt='Once upon a time in a magical land called')

print('Prediction: {}'.format(response.generations[0].text))