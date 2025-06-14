from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()

# Initialize the Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.environ["GEMINI_API_KEY"],
    temperature=0.3,
)

# Function to parse the structured LLM output
def parse_llm_output(text):
    parsed = {
        "main_topic": "",
        "key_points": [],
        "summary": ""
    }

    lines = text.strip().split("\n")

    for line in lines:
        if line.startswith("MAIN_TOPIC:"):
            parsed["main_topic"] = line.replace("MAIN_TOPIC:", "").strip()
        elif line.startswith("KEY_POINT:"):
            parsed["key_points"].append(line.replace("KEY_POINT:", "").strip())
        elif line.startswith("SUMMARY:"):
            parsed["summary"] = line.replace("SUMMARY:", "").strip()

    return parsed

# Function to get structured response from LLM
def get_response(yaml_content):
    try:
        system_message = """
        You are an advanced AI assistant specialized in deep analytical processing of web content. Your goal is to extract not just information, but profound insights, underlying arguments, and nuanced implications from the provided URL content.

        Your task is to meticulously analyze the YAML representation of a webpage fetched from a URL and extract the following with maximum depth and inference:
        1.  **Main Topic/Core Purpose**: Provide a concise yet exhaustive explanation of the primary subject, overarching theme, or fundamental purpose of the URL content. Include any implicit goals or key takeaways.
        2.  **Key Points/Inferences**: Identify and articulate all significant details, facts, arguments, and critical inferences. For each point, consider its importance, context, and any subtle implications. Dig deep to uncover connections between ideas and non-obvious conclusions. Aim for a comprehensive capture of all valuable insights.
        3.  **Comprehensive Analytical Summary**: Compose a detailed and insightful summary (7-10 sentences) that synthesizes all major findings. This summary should not merely reiterate but offer an analytical overview, connecting key elements, highlighting significant patterns, and discussing the overall significance or impact of the URL's content.

        Format your output using a single newline `\\n` between every field and entry, in this exact order:

        MAIN_TOPIC: <Detailed and insightful main topic/core purpose, including implicit goals>
        KEY_POINT: <First highly significant key point with its inferred context/implication>
        KEY_POINT: <Second highly significant key point with its inferred context/implication>
        ... (Provide a robust list of all crucial key points and their deeper insights/inferences)
        SUMMARY: <An extensive, analytical, and synthesising 7-10 sentence summary of the URL content>

        Use the exact keywords 'MAIN_TOPIC:', 'KEY_POINT:', and 'SUMMARY:' to denote fields.
        Ensure every piece of information provided is rich in detail and reflects a deep understanding of the content.
        Do not include any headers, bullet points, or extra line breaks beyond the specified format.

        This flat structure ensures that the output can be parsed line-by-line using newline as a delimiter.
        """

        # Combine system message with YAML content
        full_prompt = f"{system_message}\n\nAnalyze this YAML representation of a webpage:\n{yaml_content}"

        # Get response from LLM
        response = llm.invoke(full_prompt)

        # Convert to structured JSON
        if isinstance(response.content, str):
            return parse_llm_output(response.content)
        else:
            return {"error": "Unexpected response format", "raw": response}

    except Exception as e:
        return {
            "error": f"Error processing with LLM: {str(e)}",
            "main_topic": "Could not determine",
            "key_points": [],
            "summary": "Analysis failed due to an error."
        }