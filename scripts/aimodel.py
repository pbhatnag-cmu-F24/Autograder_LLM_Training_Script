import os
import json
import openai
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

class JavaCodeFormatter:
    """
    A class to format Java code for fine-tuning Llama models using the OpenAI API.
    
    This formatter:
    1. Takes Java code as input
    2. Uses OpenAI API to generate appropriately formatted examples 
    3. Creates JSONL files suitable for Llama fine-tuning
    """
    
    def __init__(self):
        """
        Initialize the formatter with your OpenAI API key.
        
        Args:
            api_key: Your OpenAI API key
        """


        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
            
        if not self.api_key:
            raise ValueError("No API key provided and OPENAI_API_KEY not found in environment variables")
                
        openai.api_key = self.api_key
        
    def format_single_example(self, java_code: str, 
                             model: str = "gpt-4-turbo",
                             max_tokens: int = 2048) -> Dict[str, Any]:
        """
        Format a single Java code example.
        
        Args:
            java_code: The Java code to format
            model: The OpenAI model to use
            max_tokens: Maximum tokens in response
            
        Returns:
            A dictionary with formatted data ready for Llama fine-tuning
        """
        # Create the system prompt to guide the formatting
        system_prompt = """
        You are a Java code formatting expert. Your task is to take the provided Java code and 
        format it for fine-tuning a Llama model. Follow these guidelines:
        
        1. Properly indent the code using 4 spaces
        2. Add appropriate comments for complex sections
        
        Return only the formatted code without any additional explanation.
        """
        
        try:
            # Call the OpenAI API
            response = openai.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": java_code}
                ],
                max_tokens=max_tokens,
                temperature=0.2  # Lower temperature for more consistent formatting
            )
            
            # Extract the formatted code
            formatted_code = response.choices[0].message.content
            
            # Create a training example in the format expected by Llama
            training_example = {
                "input": java_code,
                "output": formatted_code
            }
            
            return training_example
            
        except Exception as e:
            print(f"Error formatting code: {e}")
            return {"error": str(e)}
    
    def format_batch(self, java_code_list: List[str]) -> List[Dict[str, Any]]:
        """
        Format a batch of Java code examples.
        
        Args:
            java_code_list: List of Java code snippets to format
            
        Returns:
            List of formatted examples
        """
        formatted_examples = []
        
        for i, code in enumerate(java_code_list):
            print(f"Processing example {i+1}/{len(java_code_list)}...")
            example = self.format_single_example(code)
            if "error" not in example:
                formatted_examples.append(example)
            else:
                print(f"Skipping example {i+1} due to error")
                
        return formatted_examples
    
    def save_to_jsonl(self, examples: List[Dict[str, Any]], output_file: str) -> None:
        """
        Save formatted examples to a JSONL file for Llama fine-tuning.
        
        Args:
            examples: List of formatted examples
            output_file: Path to save the JSONL file
        """
        with open(output_file, 'w') as f:
            for example in examples:
                f.write(json.dumps(example) + '\n')
        
        print(f"Saved {len(examples)} examples to {output_file}")
    
    def process_from_directory(self, input_dir: str, output_file: str) -> None:
        """
        Process all Java files from a directory.
        
        Args:
            input_dir: Directory containing Java files
            output_file: Path to save the JSONL file
        """
        java_code_list = []
        
        # Collect Java files from the directory
        for root, dirs, files in os.walk(input_dir):
            for file in files:
                if file.endswith(".java"):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            java_code_list.append(f.read())
                    except Exception as e:
                        print(f"Error reading file {file_path}: {e}")
        
        print(f"Found {len(java_code_list)} Java files")
        
        # Format and save the examples
        formatted_examples = self.format_batch(java_code_list)
        self.save_to_jsonl(formatted_examples, output_file)


# Example usage
if __name__ == "__main__":
    # Replace with your OpenAI API key
    API_KEY = "your_openai_api_key_here"
    
    formatter = JavaCodeFormatter(API_KEY)
    
    # Example 1: Format a single Java code snippet
    java_code = """
    public class Example {
      public static void main(String[] args) {
        System.out.println("Hello World");
        int x=5;
        if(x>3) {
            System.out.println("x is greater than 3");
        }
      }
    }
    """
    
    example = formatter.format_single_example(java_code)
    print(json.dumps(example, indent=2))