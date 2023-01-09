import pandas as pd
import time
import cohere
co = cohere.Client('Rs6AKQKNDRaU8yMiBviX26d7SJZG71mzOVKAYpQT')
# response = co.generate(prompt='Once upon a time in a magical land called')

# print('Prediction: {}'.format(response.generations[0].text))


# prompt = '''
# "Killer whales have a diverse diet, although individual populations often specialize in particular types of prey"
# In summary:"'''


prompt = ''''''
data = open("terms.txt", "r")
for line in data:
    prompt += line
data.close()

userInput = input()
prompt += '"' + userInput  + '"'
inSummary = '\n In Summary: "'

prompt += inSummary



n_generations = 5

prediction = co.generate(
    model='large',
    prompt=prompt,
    return_likelihoods = 'GENERATION',
    stop_sequences=['"'],
    max_tokens=100,
    temperature=0.7,
    num_generations=n_generations,
    k=0,
    p=0.75)


# Get list of generations
gens = []
likelihoods = []
for gen in prediction.generations:
    gens.append(gen.text)

    sum_likelihood = 0
    for t in gen.token_likelihoods:
        sum_likelihood += t.likelihood
    # Get sum of likelihoods
    likelihoods.append(sum_likelihood)


pd.options.display.max_colwidth = 200
# Create a dataframe for the generated sentences and their likelihood scores
df = pd.DataFrame({'generation':gens, 'likelihood': likelihoods})
# Drop duplicates
df = df.drop_duplicates(subset=['generation'])
# Sort by highest sum likelihood
df = df.sort_values('likelihood', ascending=False, ignore_index=True)

#print('Candidate summaries for the sentence: \n"Killer whales have a diverse diet, although individual populations often specialize in particular types of prey."')

#print(df.values)
print(df.values[0][0])
