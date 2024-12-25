import google.generativeai as genai

# Configure the Generative AI client
genai.configure(api_key="API_KEY")  # Replace with your actual API key
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud.   What is coding?")
print(response.text)
