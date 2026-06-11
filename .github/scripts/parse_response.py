import json, re, os, sys

response = json.load(open("/tmp/response.json"))
content = response["choices"][0]["message"]["content"]

# Strip markdown code fences if the model wrapped the response
content = re.sub(r"^```json\s*", "", content.strip())
content = re.sub(r"^```\s*", "", content.strip())
content = re.sub(r"\s*```$", "", content.strip())

try:
    data = json.loads(content)
except json.JSONDecodeError as e:
    print(f"Failed to parse JSON: {e}", file=sys.stderr)
    print(f"Raw content: {content[:500]}", file=sys.stderr)
    sys.exit(1)

slug = os.environ["SLUG"]
os.makedirs(slug, exist_ok=True)

with open(f"{slug}/index.html", "w") as f:
    f.write(data["index_html"])

with open("card.txt", "w") as f:
    f.write(data["homepage_card"])

print("Page written successfully")
