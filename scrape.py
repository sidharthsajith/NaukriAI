from firecrawl import FirecrawlApp
from pydantic import BaseModel, Field


# Initialize the client with your API key
app = FirecrawlApp(api_key="fc-86571cce365c4b46bf438ad52d4afa49")

# Perform a basic search
search_result = app.search("AI Developer OR Machine Learning Engineer site:linkedin.com/in/ India", limit=100)

class ExtractSchema(BaseModel):
    name: str = Field(description="Name of the person")
    location: str = Field(description="Location of the person")
    experience: str = Field(description="Experience of the person")
    skills: list[str] = Field(description="Skills of the person")
    past_experience: list[str] = Field(description="Past experience of the person")
    
    
# Print the search results
for result in search_result.data:
    print(f"Title: {result['title']}")
    print(f"URL: {result['url']}")
    print(f"Description: {result['description']}")

for i in search_result.data:
    print(i['url'])
    data = app.extract((i['url']), prompt='Extract the name, location, experience, skills, and past experience of the person from the page.', schema=ExtractSchema.model_json_schema())
print(data)
