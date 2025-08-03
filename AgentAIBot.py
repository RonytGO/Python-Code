# -*- coding: utf-8 -*-
"""
Created on Sun Aug  3 13:17:52 2025

@author: Ronyt
"""

from transformers import pipeline, set_seed

# Initialize the chatbot with proper parameters
chatbot = pipeline(
    "text-generation", 
    model="gpt2",
    truncation=True,  # Explicitly enable truncation
    pad_token_id=50256  # Explicitly set pad token
)

def chat():
    print("Bot: Hello! How can I help you today? (Type 'quit' to exit)")
    set_seed(42)  # For reproducibility
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['quit', 'exit']:
            break
            
        # Generate response with clearer parameters
        response = chatbot(
            user_input,
            max_new_tokens=50,  # Use max_new_tokens instead of max_length
            do_sample=True,
            top_k=50,
            temperature=0.7
        )[0]['generated_text']
        
        # Clean up the response by removing the input text if it's repeated
        bot_response = response.replace(user_input, "").strip()
        print(f"Bot: {bot_response}")

chat()