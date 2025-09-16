import shodan
import pandas as pd

API_KEY = "c1T4xSmOuUHuYfqcmgBY0wbuwR9sXwsd"
api = shodan.Shodan(API_KEY)

query = 'product:"IP Camera" geo:"36.6103,-88.3148" port:554'
results = api.search(query)

devices = []
for result in results['matches']:
    devices.append({
        'ip': result['ip_str'],
        'port': result['port'],
        'location': result.get('location', {}).get('city', 'Unknown'),
        'org': result.get('org', 'Unknown'),
        'data': result['data'][:200]
    })

df = pd.DataFrame(devices)
df.to_csv("data/shodan_results.csv", index=False)
print("Scan complete. Data saved.")
