from firecrawl import FirecrawlApp
from pydantic import BaseModel, Field

# Initialize the FirecrawlApp with your API key
app = FirecrawlApp(api_key='your_api_key')

class ExtractSchema(BaseModel):
    company_mission: str
    supports_sso: bool
    is_open_source: bool
    is_in_yc: bool

data = app.extract([
  'https://docs.firecrawl.dev/*', 
  'https://firecrawl.dev/', 
  'https://www.ycombinator.com/companies/'
], prompt='Extract the company mission, whether it supports SSO, whether it is open source, and whether it is in Y Combinator from the page.', schema=ExtractSchema.model_json_schema())
print(data)