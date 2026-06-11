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
    print(f"Raw content:\n{content[:500]}", file=sys.stderr)
    sys.exit(1)

slug = os.environ["SLUG"]
os.makedirs(slug, exist_ok=True)

# Write the event page
with open(f"{slug}/index.html", "w") as f:
    f.write(data["index_html"])

# Update the homepage — remove empty placeholder, insert new card before </ul>
with open("index.html", "r") as f:
    homepage = f.read()

# Remove the "no events" placeholder if present
homepage = re.sub(r'\s*<li class="empty">.*?</li>', '', homepage)

# Insert the new card before the closing </ul>
card = data["homepage_card"]
homepage = homepage.replace("</ul>", f"    {card}\n  </ul>", 1)

with open("index.html", "w") as f:
    f.write(homepage)

print(f"Event page written to {slug}/index.html")
print("Homepage updated")
