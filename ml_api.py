#!/usr/bin/env python3
"""
ML Analytics API
Provides REST API endpoints to access ML predictions and insights
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
ML_DB_PATH = "/opt/fueltheaura-ai/data/ml_predictions.db"
SUPERVISOR_DB_PATH = "/opt/fueltheaura-ai/data/supervisor_improvements.db"

def get_db_connection(db_path):
    """Get database connection"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/ml/stats', methods=['GET'])
def get_stats():
    """Get ML system statistics"""
    try:
        conn = get_db_connection(ML_DB_PATH)
        cursor = conn.cursor()
        
        # Get total predictions
        cursor.execute("SELECT COUNT(*) as count FROM predictions")
        total_predictions = cursor.fetchone()['count']
        
        # Get active insights
        cursor.execute("SELECT COUNT(*) as count FROM ml_insights WHERE status='active'")
        active_insights = cursor.fetchone()['count']
        
        # Get models trained
        cursor.execute("SELECT COUNT(DISTINCT model_name) as count FROM model_performance")
        models_trained = cursor.fetchone()['count']
        
        conn.close()
        
        # Get average impact from supervisor DB
        conn = get_db_connection(SUPERVISOR_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT AVG(impact_score) as avg_impact FROM improvements")
        result = cursor.fetchone()
        avg_impact = result['avg_impact'] if result['avg_impact'] else 0
        conn.close()
        
        return jsonify({
            'success': True,
            'data': {
                'totalPredictions': total_predictions,
                'activeInsights': active_insights,
                'modelsTrained': models_trained,
                'avgImpact': round(avg_impact, 2)
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/ml/insights', methods=['GET'])
def get_insights():
    """Get active ML insights"""
    try:
        conn = get_db_connection(ML_DB_PATH)
        cursor = conn.cursor()
        
        # Get active insights ordered by priority and confidence
        cursor.execute("""
            SELECT 
                insight_type,
                insight_category,
                description,
                confidence,
                recommended_action,
                priority,
                timestamp
            FROM ml_insights
            WHERE status='active'
            ORDER BY 
                CASE priority 
                    WHEN 'high' THEN 1 
                    WHEN 'medium' THEN 2 
                    ELSE 3 
                END,
                confidence DESC
            LIMIT 10
        """)
        
        insights = []
        for row in cursor.fetchall():
            insights.append({
                'type': row['insight_type'],
                'category': row['insight_category'],
                'description': row['description'],
                'confidence': row['confidence'],
                'action': row['recommended_action'],
                'priority': row['priority'],
                'timestamp': row['timestamp']
            })
        
        conn.close()
        
        return jsonify({
            'success': True,
            'data': insights
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/ml/predictions', methods=['GET'])
def get_predictions():
    """Get recent ML predictions"""
    try:
        limit = request.args.get('limit', 20, type=int)
        prediction_type = request.args.get('type', None)
        
        conn = get_db_connection(ML_DB_PATH)
        cursor = conn.cursor()
        
        query = """
            SELECT 
                prediction_type,
                prediction_date,
                predicted_value,
                confidence_score,
                timestamp
            FROM predictions
        """
        
        params = []
        if prediction_type:
            query += " WHERE prediction_type = ?"
            params.append(prediction_type)
        
        query += " ORDER BY prediction_date DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        
        predictions = []
        for row in cursor.fetchall():
            predictions.append({
                'type': row['prediction_type'],
                'date': row['prediction_date'],
                'value': row['predicted_value'],
                'confidence': row['confidence_score'],
                'timestamp': row['timestamp']
            })
        
        conn.close()
        
        return jsonify({
            'success': True,
            'data': predictions
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/ml/models', methods=['GET'])
def get_models():
    """Get model performance information"""
    try:
        conn = get_db_connection(ML_DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                model_name,
                model_type,
                accuracy,
                rmse,
                r2_score,
                training_samples,
                timestamp
            FROM model_performance
            ORDER BY timestamp DESC
        """)
        
        models = []
        seen_models = set()
        
        for row in cursor.fetchall():
            model_name = row['model_name']
            if model_name not in seen_models:
                models.append({
                    'name': model_name,
                    'type': row['model_type'],
                    'accuracy': row['accuracy'],
                    'rmse': row['rmse'],
                    'r2_score': row['r2_score'],
                    'trainingSamples': row['training_samples'],
                    'lastUpdated': row['timestamp']
                })
                seen_models.add(model_name)
        
        conn.close()
        
        return jsonify({
            'success': True,
            'data': models
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/ml/dashboard', methods=['GET'])
def get_dashboard_data():
    """Get complete dashboard data in one request"""
    try:
        # Get stats
        stats_response = get_stats()
        stats_data = json.loads(stats_response.get_data())
        
        # Get insights
        insights_response = get_insights()
        insights_data = json.loads(insights_response.get_data())
        
        # Get predictions
        predictions_response = get_predictions()
        predictions_data = json.loads(predictions_response.get_data())
        
        # Get models
        models_response = get_models()
        models_data = json.loads(models_response.get_data())
        
        return jsonify({
            'success': True,
            'data': {
                'stats': stats_data['data'],
                'insights': insights_data['data'],
                'predictions': predictions_data['data'],
                'models': models_data['data'],
                'lastUpdated': datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)