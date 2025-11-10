from flask import Flask, render_template, request, jsonify
import shodan
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import io
import base64
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt

app = Flask(__name__)

# Shodan API Key - Replace with your own key
DEFAULT_API_KEY = "c1T4xSmOuUHuYfqcmgBY0wbuwR9sXwsd"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    try:
        data = request.json
        query = data.get('query') or ''
        use_demo = data.get('use_demo', False)
        
        # Strip whitespace if query is a string
        query = query.strip() if query else ''
        
        if not query and not use_demo:
            return jsonify({'error': 'Query is required'}), 400
        
        # Demo mode - use sample data
        if use_demo:
            return handle_demo_mode()
        
        # Use the API key defined in the code
        api = shodan.Shodan(DEFAULT_API_KEY)
        
        # Perform Shodan search
        try:
            results = api.search(query)
        except shodan.APIError as e:
            error_message = str(e)
            if '401' in error_message or 'Invalid API key' in error_message:
                return jsonify({
                    'error': 'Invalid API key. Try Demo Mode instead.',
                    'suggest_demo': True
                }), 401
            elif '403' in error_message or 'no query credits' in error_message.lower():
                return jsonify({
                    'error': 'No query credits available. Try Demo Mode to see how the app works with sample data.',
                    'suggest_demo': True
                }), 403
            else:
                return jsonify({'error': f'Shodan API Error: {error_message}'}), 400
        
        # Format results for DataFrame
        devices_list = []
        for result in results['matches']:
            devices_list.append({
                'ip': result['ip_str'],
                'port': result['port'],
                'location': result.get('location', {}).get('city', 'Unknown'),
                'country': result.get('location', {}).get('country_name', 'Unknown'),
                'org': result.get('org', 'Unknown'),
                'product': result.get('product', 'Unknown'),
                'data': result['data'][:500]  # Keep more data for ML
            })
        
        if not devices_list:
            return jsonify({
                'success': True,
                'total': 0,
                'devices': [],
                'ml_results': None
            })
        
        # Run AI Classification
        ml_results = run_ai_classifier(devices_list)
        
        # Format devices with ML predictions
        devices_with_ml = []
        for i, device in enumerate(devices_list):
            device_copy = device.copy()
            device_copy['ml_prediction'] = ml_results['predictions'][i]
            device_copy['risk_level'] = 'Exposed' if ml_results['predictions'][i] == 1 else 'Benign'
            devices_with_ml.append(device_copy)
        
        return jsonify({
            'success': True,
            'total': results['total'],
            'devices': devices_with_ml,
            'ml_results': {
                'accuracy': ml_results['accuracy'],
                'total_devices': len(devices_list),
                'exposed_count': sum(ml_results['predictions']),
                'benign_count': len(ml_results['predictions']) - sum(ml_results['predictions']),
                'visualization': ml_results['visualization']
            }
        })
    
    except shodan.APIError as e:
        error_message = str(e)
        if '401' in error_message or 'Invalid API key' in error_message:
            return jsonify({'error': 'Invalid API key. Please check your Shodan API key.'}), 401
        elif '403' in error_message or 'no query credits' in error_message.lower():
            return jsonify({'error': 'No query credits available. Please enter a valid Shodan API key with credits, or upgrade your account at https://account.shodan.io/'}), 403
        else:
            return jsonify({'error': f'Shodan API Error: {error_message}'}), 400
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500

def handle_demo_mode():
    """
    Use sample CSV data for demo purposes when API credits aren't available.
    """
    try:
        # Load sample data
        df = pd.read_csv("data/shodan_results.csv")
        
        # Convert to device list format
        devices_list = []
        for _, row in df.iterrows():
            devices_list.append({
                'ip': row['ip'],
                'port': row['port'],
                'location': row['location'],
                'country': 'US',  # Sample data location
                'org': row['org'],
                'product': 'IP Camera',
                'data': row['data']
            })
        
        # Run AI Classification on demo data
        ml_results = run_ai_classifier(devices_list)
        
        # Format devices with ML predictions
        devices_with_ml = []
        for i, device in enumerate(devices_list):
            device_copy = device.copy()
            device_copy['ml_prediction'] = ml_results['predictions'][i]
            device_copy['risk_level'] = 'Exposed' if ml_results['predictions'][i] == 1 else 'Benign'
            devices_with_ml.append(device_copy)
        
        return jsonify({
            'success': True,
            'total': len(devices_list),
            'devices': devices_with_ml,
            'demo_mode': True,
            'ml_results': {
                'accuracy': ml_results['accuracy'],
                'total_devices': len(devices_list),
                'exposed_count': sum(ml_results['predictions']),
                'benign_count': len(ml_results['predictions']) - sum(ml_results['predictions']),
                'visualization': ml_results['visualization']
            }
        })
    except Exception as e:
        return jsonify({'error': f'Demo mode error: {str(e)}'}), 500

def run_ai_classifier(devices_list):
    """
    Runs the AI classifier on device data to identify exposed vs benign devices.
    """
    # Create DataFrame
    df = pd.DataFrame(devices_list)
    
    # Label data (1 = exposed camera, 0 = benign)
    # Look for keywords that indicate exposed/vulnerable devices
    keywords = ['webcam', 'surveillance', 'camera', 'rtsp', 'unauthorized', 'default', 'admin']
    df['label'] = df['data'].apply(
        lambda x: 1 if any(keyword in x.lower() for keyword in keywords) else 0
    )
    
    # Vectorize banner data
    vectorizer = CountVectorizer(max_features=100)
    X = vectorizer.fit_transform(df['data'])
    y = df['label']
    
    # Train model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)
    
    # Calculate accuracy
    accuracy = model.score(X_test, y_test)
    
    # Predict on all devices
    predictions = model.predict(X).tolist()
    
    # Create visualization
    visualization_base64 = create_visualization(predictions)
    
    return {
        'accuracy': round(accuracy * 100, 2),
        'predictions': predictions,
        'visualization': visualization_base64
    }

def create_visualization(predictions):
    """
    Creates a bar chart showing exposed vs benign devices.
    """
    plt.figure(figsize=(8, 6))
    
    exposed_count = sum(predictions)
    benign_count = len(predictions) - exposed_count
    
    categories = ['Benign', 'Exposed']
    counts = [benign_count, exposed_count]
    colors = ['#4CAF50', '#F44336']
    
    plt.bar(categories, counts, color=colors, edgecolor='black', linewidth=1.5)
    plt.title('AI Classification Results', fontsize=16, fontweight='bold')
    plt.xlabel('Device Type', fontsize=12)
    plt.ylabel('Count', fontsize=12)
    plt.grid(axis='y', alpha=0.3)
    
    # Add count labels on bars
    for i, (cat, count) in enumerate(zip(categories, counts)):
        plt.text(i, count + 0.5, str(count), ha='center', va='bottom', fontweight='bold')
    
    # Convert plot to base64 string
    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()
    
    return image_base64

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
