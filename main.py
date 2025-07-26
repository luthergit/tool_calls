
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()


client = OpenAI(
base_url="https://openrouter.ai/api/v1",
api_key=os.getenv("OPENROUTER_API_KEY"),
)
history = []

system_prompt = """
You are a helpful assistant that can calculate the BMI of a person.
In order to calculate the BMI.
When the user provides the weight and height, call the bmi_calculator function with the weight and height.

For example, my weight is 60kg and my height 170m. Respond with bmi_caluator 60 170
If the user says lbs, inches and another metrics, covert it to kg and meters.
ONLY return the format given, NO EXTRA WORDS.
"""

comment_on_bmi_prompt = """
You are a sassy comedian, be as cruel as you can on commenting if the bmi is good or not. Spare no feelings.
"""

stylist_prompt = """
    You are a sassy fashion stylist from a world renowned fashion company, from the Devil Wears Prada, you are given a bmi and you need to give the user a style advice. Be as cruel as you can on commenting
and spare no feelings.
"""

history.append({"role": "system", "content": system_prompt})



def ask_llm(prompt):
    history.append({"role": "user", "content": prompt})

    completion = client.chat.completions.create(
    model = "moonshotai/kimi-k2",
    messages=history
    )

    llm_response = completion.choices[0].message.content

    history.append({"role": "assistant", "content": llm_response})

    return llm_response

def bmi_calculator(weight, height):
    return weight / (height**2)


function_lookup = {
    "bmi_calculator": bmi_calculator
}

def comment_on_bmi(bmi):

    completion = client.chat.completions.create(
        model="openai/gpt-4o",
        messages=[
            {"role": "system", "content": comment_on_bmi_prompt},
            {"role": "user", "content": f"The BMI is {bmi}. Comment on the BMI."}
        ]
        )
    
    llm_response = completion.choices[0].message.content

    return llm_response

def stylist(bmi):
    completion = client.chat.completions.create(
        model="openai/gpt-4o",
        messages=[
            {"role": "system", "content": stylist_prompt},
            {"role": "user", "content": f"The BMI is {bmi}. Comment on the BMI."}
        ]
    )

    llm_response = completion.choices[0].message.content
    return llm_response

def main():
    user_input = input("Give me your weight and height: ")
    response = ask_llm(user_input)
    print("response:" ,response)
    func_name, weight, height = response.split(" ")
    result = function_lookup[func_name](float(weight), float(height))
    print(result, end="\n\n")
    comment = comment_on_bmi(result)
    print(comment, end="\n\n")
    style = stylist(result)
    print(style, end="\n\n")
    
if __name__ == "__main__":
    main()
