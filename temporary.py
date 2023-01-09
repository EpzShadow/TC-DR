import pandas as pd
import time
import cohere
co = cohere.Client('Rs6AKQKNDRaU8yMiBviX26d7SJZG71mzOVKAYpQT')

def splitParagraphs(text): #split text into paragraphs
    result = []
    curr = ""
    for i in text:
        if i == "\n":
            result.append(curr)
            curr = ""
        else:
            curr += i
    return result

def algo(paragraph, prompt): #run the algorithm on the paragraph
    maxChar = 650   
    allText = [""] #each part of the text (may need to split up if too big)

    for i in paragraph:
        allText[-1] += i
        if i == "." and len(allText[-1]) >= maxChar:
            allText.append("")

    if allText[-1] == "":
        allText.pop() 

    output = []

    for text in allText:

        prompt += '"' + text  + '"'
        inSummary = '\n In Summary: "'
        prompt += inSummary

        #thank you co:here documentation
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

        output.append(df.values[0][0])

    return output

def main(userInput): #function that gets called when hitting submit
    formatted = splitParagraphs(userInput)
    result = ""
    prompt = ''''''
    data = open("terms.txt", "r")
    for line in data:
        prompt += line
    data.close()
    for paragraph in formatted:
        summary = algo(paragraph, prompt)
        for line in summary:
            result += line + "\n"
        result += "\n"
    return result
    
print(main("For all content you submit to the Services, you grant Snap and our affiliates a worldwide, royalty-free, sublicensable, and transferable license to host, store, cache, use, display, reproduce, modify, adapt, edit, publish, analyze, transmit, and distribute that content. This license is for the purpose of operating, developing, providing, promoting, and improving the Services and researching and developing new ones. This license includes a right for us to make your content available to, and pass these rights along to, service providers with whom we have contractual relationships related to the provision of the Services, solely for the purpose of providing such Services."))