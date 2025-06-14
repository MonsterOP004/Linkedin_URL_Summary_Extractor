import requests
import time

# Record start time
start_time = time.time()

# Make the API request
response = requests.post(
    "http://localhost:8111/url_content_summarizer",
    json={"url": "https://medium.com/@vipra_singh/ai-agents-building-multi-agent-system-part-8-be15da64b7eb"}
)

# Calculate elapsed time
elapsed_time = time.time() - start_time

# Print the response and timing information
print(f"API Response Time: {elapsed_time:.2f} seconds")
print(response.json())