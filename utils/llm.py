import os
from groq import Groq
from dotenv import load_dotenv
import json
load_dotenv()
import re

class LLM:
    def __init__(self):
        """
        Initialize the LLM class with the Groq client.
        The API key is fetched from the environment variable.
        """
        self.client = Groq(api_key = os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.3-70b-versatile"

    def parse_user_input(self, message: str) -> str:
        """
        Parse raw user input using the Llama model.

        Args:
            message (str): The raw input message from the user.

        Returns:
            str: Parsed content or response from the LLM.
        """
        try:
            # Create a chat completion request
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": message,
                    }
                ],
                model=self.model,
            )

            # Extract and return the LLM's response
            return chat_completion.choices[0].message.content

        except Exception as e:
            # Handle any exceptions from the API
            return f"Error: Unable to process the request. Details: {e}"

    # def parse_user_details(self, raw_input: str) -> dict:
    #     """
    #     Extract key details like name, medicine names, address, and others from raw user input.
    #
    #     Args:
    #         raw_input (str): Raw message from the user.
    #
    #     Returns:
    #         dict: Extracted details such as name, medicines, address, etc.
    #     """
    #     # Generic prompt to extract all key details
    #     prompt = (
    #         f"Extract all relevant details from the following user input: '{raw_input}'. "
    #         f"Identify and return the user's name, medicine names, address, and any other "
    #         f"relevant details in a JSON format with keys: 'name', 'medicines', 'address', "
    #         f"and 'others' (if applicable). Ensure medicines are returned as a list. "
    #         f"Return only the JSON object without any additional text or explanations."
    #     )
    #
    #     try:
    #         # Call the LLM with the specific prompt
    #         chat_completion = self.client.chat.completions.create(
    #             messages=[
    #                 {
    #                     "role": "user",
    #                     "content": prompt,
    #                 }
    #             ],
    #             model=self.model,
    #         )
    #
    #         # Extract the LLM's response
    #         response = chat_completion.choices[0].message.content
    #
    #         # Use regex to extract the JSON part from the response
    #         json_match = re.search(r'```(?:json)?\n({.*?})\n```', response, re.DOTALL)
    #         if json_match:
    #             json_str = json_match.group(1)
    #             try:
    #                 # Parse the JSON string into a dictionary
    #                 parsed_response = json.loads(json_str)
    #                 return parsed_response
    #             except json.JSONDecodeError:
    #                 # Return raw response if JSON parsing fails
    #                 return {"error": "Failed to parse JSON", "raw_response": response}
    #         else:
    #             # Return raw response if no JSON is found
    #             return {"error": "No JSON found in response", "raw_response": response}
    #
    #     except Exception as e:
    #         # Handle exceptions gracefully
    #         return {"error": f"Unable to process the request. Details: {e}"}


    def parse_user_details(self, raw_input: str) -> dict:
        """
        Extract structured details like user_id, name, medicines, address, latitude, longitude, and contact details.

        Args:
            raw_input (str): Raw message from the user.

        Returns:
            dict: Extracted details formatted for database storage.
        """
        prompt = (
            f"Extract relevant details from the following user input: '{raw_input}'. "
            f"Ensure the output is formatted as a JSON object with the following structure:\n"
            f"1. 'user_id' (string) - **Always set to the value of 'phone' ($MobileNumber), the WhatsApp number of the order placer.**\n"
            f"2. 'name' (string) - Name of the person **placing the order**.\n"
            f"3. 'medicines' (list) - List of medicine names ordered.\n"
            f"4. 'address' (string) - Complete delivery address.\n"
            f"5. 'latitude' (float) - Latitude coordinate of the delivery location **(from 'lat_location' / $Latitudes_Latitude).**\n"
            f"6. 'longitude' (float) - Longitude coordinate of the delivery location **(from 'long_location' / $Longitudes_Longitude).**\n"
            f"7. 'contact_person' (string) - Name of the person **who will receive the delivery**.\n"
            f"8. 'contact_phone' (string) - Phone number of the **delivery recipient** (could be different from 'user_id').\n"
            f"\nEnsure:\n"
            f"- 'user_id' is **always** taken from 'phone'.\n"
            f"- 'medicines' is a list.\n"
            f"- 'latitude' and 'longitude' are floats.\n"
            f"- All other fields are strings.\n"
            f"Return only the JSON object without any extra text or explanations."
        )

        try:
            # Call the LLM with the specific prompt
            chat_completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
            )

            # Extract the LLM's response
            response = chat_completion.choices[0].message.content

            # Use regex to extract the JSON part from the response
            json_match = re.search(r'```(?:json)?\n({.*?})\n```', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
                try:
                    # Parse the JSON string into a dictionary
                    parsed_response = json.loads(json_str)
                    return parsed_response
                except json.JSONDecodeError:
                    return {"error": "Failed to parse JSON", "raw_response": response}
            else:
                return {"error": "No JSON found in response", "raw_response": response}

        except Exception as e:
            return {"error": f"Unable to process the request. Details: {e}"}
