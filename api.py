from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import json
import os

app = Flask(__name__)
CORS(app)

# Set the full path to ark executable
# ARK_PATH = r"C:\Users\DhinazRangasamy\AppData\Roaming\npm\ark"

def extract_health_summary(ark_output):
    """
    Extract only the content after the last '◆ health-summary-agent'
    Handles cases with multiple agent outputs
    """
    try:
        lines = ark_output.split('\n')
        summary_start_idx = -1
        
        # Find the last occurrence of health-summary-agent
        for i, line in enumerate(lines):
            if 'health-summary-agent' in line:
                summary_start_idx = i
        
        if summary_start_idx == -1:
            return ark_output  # Marker not found
        
        # Get all lines after the marker
        summary_lines = lines[summary_start_idx + 1:]
        
        # Stop if we hit another agent marker
        result_lines = []
        for line in summary_lines:
            if line.strip().startswith('◆'):
                break
            result_lines.append(line)
        
        return '\n'.join(result_lines).strip()
    
    except Exception as e:
        return ark_output

@app.route('/health-advice', methods=['POST'])
def get_health_advice():
    try:
        data = request.get_json()
        
        if not data or 'prompt' not in data:
            return jsonify({"error": "No prompt provided"}), 400
        
        prompt = data['prompt']
        
        # Run ARK query command
        command = ['ark', 'query', 'team/team-v1', prompt]
        
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=60,
            shell=True
        )
        
        if result.returncode != 0:
            return jsonify({
                "error": "ARK query failed",
                "details": result.stderr,
                "command": ' '.join(command)
            }), 500
        
        # Extract only the health summary
        full_output = result.stdout
        summary_only = extract_health_summary(full_output)
        
        return jsonify({
            "success": True,
            "response": summary_only,
            "prompt": prompt,
            "full_output": full_output  # Optional: include for debugging
        }), 200
    
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Query timed out"}), 504
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/health-advice/full', methods=['POST'])
def get_health_advice_full():
    """Endpoint that returns the complete output including reasoning"""
    try:
        data = request.get_json()
        
        if not data or 'prompt' not in data:
            return jsonify({"error": "No prompt provided"}), 400
        
        prompt = data['prompt']
        command = [ARK_PATH, 'query', 'team/team-v1', prompt]
        
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=60,
            shell=True
        )
        
        if result.returncode != 0:
            return jsonify({
                "error": "ARK query failed",
                "details": result.stderr
            }), 500
        
        return jsonify({
            "success": True,
            "response": result.stdout,
            "prompt": prompt
        }), 200
    
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Query timed out"}), 504
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)