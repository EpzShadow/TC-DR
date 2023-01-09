import pandas as pd
import time
import cohere
co = cohere.Client('Rs6AKQKNDRaU8yMiBviX26d7SJZG71mzOVKAYpQT')

def splitParagraphs(text): #split text into paragraphs
    # print(text)
    result = []
    curr = ""
    for i in text:
        if i == "\n":
            # print("YEEEEEEEEE")
            result.append(curr)
            curr = ""
        else:
            # print(i)
            curr += i
    if curr != "":
        result.append(curr)
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

        if len(text) > 1000:
            continue

        curPrompt = prompt + '"' + text + '"'
        inSummary = '\n In summary: "'
        curPrompt += inSummary
        #thank you co:here documentation
        n_generations = 5

        prediction = co.generate(
            model='large',
            prompt=curPrompt,
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


        # Create a dataframe for the generated sentences and their likelihood scores
        df = pd.DataFrame({'generation':gens, 'likelihood': likelihoods})
        # Drop duplicates
        df = df.drop_duplicates(subset=['generation'])
        # Sort by highest sum likelihood
        df = df.sort_values('likelihood', ascending=False, ignore_index=True)

        output.append(df.values[0][0][:-1])
    if len(output) == 0:
        return ["TC;DR could not summarize this paragraph, please try again."]
    return output

def main(userInput, merge = False): #function that gets called when hitting submit
    if merge: #this is when we call main after the first time and we need to merge everything into 1
        userInput.replace("\n")
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
# print(main("Offering personalized opportunities to create, connect, communicate, discover, and share.\nPeople are different. We want to strengthen your relationships through shared experiences you actually care about. So we build systems that try to understand who and what you and others care about, and use that information to help you create, find, join, and share in experiences that matter to you. Part of that is highlighting content, features, offers, and accounts you might be interested in, and offering ways for you to experience Instagram, based on things you and others do on and off Instagram.\nFostering a positive, inclusive, and safe environment.\nWe develop and use tools and offer resources to our community members that help to make their experiences positive and inclusive, including when we think they might need help. We also have teams and systems that work to combat abuse and violations of our Terms and policies, as well as harmful and deceptive behavior. We use all the information we have-including your information-to try to keep our platform secure. We also may share information about misuse or harmful content with other Meta Companies or law enforcement. Learn more in the Data Policy."))
