#!/usr/bin/env python3
"""
Machine Learning Predictive Analytics Module
Analyzes historical data and predicts future trends for content performance,
SEO rankings, traffic patterns, and system optimization opportunities.
"""

import os
import sys
import json
import sqlite3
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor, GradientBoostingClassifier
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score
import pickle
import warnings
warnings.filterwarnings('ignore')

class MLPredictiveAnalytics:
    """
    Machine Learning system for predictive analytics
    """
    
    def __init__(self, base_dir="/opt/fueltheaura-ai"):
        self.base_dir = base_dir
        self.data_dir = f"{base_dir}/data"
        self.ml_dir = f"{self.data_dir}/ml_models"
        self.predictions_dir = f"{self.data_dir}/ml_predictions"
        self.reports_dir = f"{self.data_dir}/ml_reports"
        
        # Create directories
        os.makedirs(self.ml_dir, exist_ok=True)
        os.makedirs(self.predictions_dir, exist_ok=True)
        os.makedirs(self.reports_dir, exist_ok=True)
        
        # Initialize models
        self.models = {}
        self.scalers = {}
        
        # Initialize ML database
        self.init_ml_database()
    
    def init_ml_database(self):
        """Initialize ML predictions database"""
        db_path = f"{self.data_dir}/ml_predictions.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Predictions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                prediction_type TEXT,
                prediction_date TEXT,
                predicted_value REAL,
                confidence_score REAL,
                actual_value REAL,
                accuracy REAL,
                model_version TEXT,
                features_used TEXT
            )
        ''')
        
        # Model performance table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS model_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                model_name TEXT,
                model_type TEXT,
                accuracy REAL,
                rmse REAL,
                r2_score REAL,
                training_samples INTEGER,
                features TEXT
            )
        ''')
        
        # Insights table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ml_insights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                insight_type TEXT,
                insight_category TEXT,
                description TEXT,
                confidence REAL,
                recommended_action TEXT,
                priority TEXT,
                status TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def load_historical_data(self):
        """Load historical data from all databases"""
        print("📊 Loading historical data...")
        
        data = {
            'improvements': self.load_improvements_data(),
            'seo_metrics': self.load_seo_data(),
            'content_quality': self.load_content_data(),
            'audits': self.load_audit_data(),
            'system_metrics': self.load_system_data()
        }
        
        return data
    
    def load_improvements_data(self):
        """Load improvement history"""
        try:
            db_path = f"{self.data_dir}/supervisor_improvements.db"
            if not os.path.exists(db_path):
                return pd.DataFrame()
            
            conn = sqlite3.connect(db_path)
            query = """
                SELECT 
                    timestamp,
                    category,
                    improvement_type,
                    impact_score,
                    status
                FROM improvements
                ORDER BY timestamp
            """
            df = pd.read_sql_query(query, conn)
            conn.close()
            
            if not df.empty:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df['date'] = df['timestamp'].dt.date
            
            return df
        except Exception as e:
            print(f"  ⚠️ Error loading improvements: {e}")
            return pd.DataFrame()
    
    def load_seo_data(self):
        """Load SEO metrics history"""
        try:
            db_path = f"{self.data_dir}/supervisor_improvements.db"
            if not os.path.exists(db_path):
                return pd.DataFrame()
            
            conn = sqlite3.connect(db_path)
            query = """
                SELECT 
                    timestamp,
                    page_url,
                    word_count,
                    keyword_density,
                    page_speed_score,
                    mobile_friendly
                FROM seo_metrics
                ORDER BY timestamp
            """
            df = pd.read_sql_query(query, conn)
            conn.close()
            
            if not df.empty:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            return df
        except Exception as e:
            print(f"  ⚠️ Error loading SEO data: {e}")
            return pd.DataFrame()
    
    def load_content_data(self):
        """Load content quality data"""
        try:
            db_path = f"{self.data_dir}/content_intelligence.db"
            if not os.path.exists(db_path):
                return pd.DataFrame()
            
            conn = sqlite3.connect(db_path)
            query = """
                SELECT 
                    created_at as timestamp,
                    title,
                    quality_score,
                    word_count,
                    engagement_score
                FROM blog_posts
                ORDER BY created_at
            """
            df = pd.read_sql_query(query, conn)
            conn.close()
            
            if not df.empty:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            return df
        except Exception as e:
            print(f"  ⚠️ Error loading content data: {e}")
            return pd.DataFrame()
    
    def load_audit_data(self):
        """Load audit history from JSON files"""
        try:
            audit_dir = f"{self.data_dir}/audits"
            if not os.path.exists(audit_dir):
                return pd.DataFrame()
            
            audit_files = [f for f in os.listdir(audit_dir) if f.endswith('.json')]
            
            data = []
            for file in sorted(audit_files)[-100:]:  # Last 100 audits
                with open(f"{audit_dir}/{file}", 'r') as f:
                    audit = json.load(f)
                    data.append({
                        'timestamp': audit.get('timestamp'),
                        'website_status': audit.get('website_status', {}).get('status'),
                        'response_time': audit.get('website_status', {}).get('response_time', 0),
                        'issues_count': len(audit.get('blog_issues', [])) + len(audit.get('compliance_issues', []))
                    })
            
            df = pd.DataFrame(data)
            if not df.empty:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            return df
        except Exception as e:
            print(f"  ⚠️ Error loading audit data: {e}")
            return pd.DataFrame()
    
    def load_system_data(self):
        """Load system metrics from supervisor reports"""
        try:
            reports_dir = f"{self.data_dir}/supervisor_reports"
            if not os.path.exists(reports_dir):
                return pd.DataFrame()
            
            report_files = [f for f in os.listdir(reports_dir) if f.endswith('.json')]
            
            data = []
            for file in sorted(report_files)[-100:]:  # Last 100 reports
                with open(f"{reports_dir}/{file}", 'r') as f:
                    report = json.load(f)
                    data.append({
                        'timestamp': report.get('timestamp'),
                        'disk_free_gb': report.get('disk_space', {}).get('free_space_gb', 0),
                        'disk_used_percent': report.get('disk_space', {}).get('used_percent', 0),
                        'backups_created': len(report.get('backups', {}).get('backups_created', []))
                    })
            
            df = pd.DataFrame(data)
            if not df.empty:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            return df
        except Exception as e:
            print(f"  ⚠️ Error loading system data: {e}")
            return pd.DataFrame()
    
    def prepare_time_series_features(self, df, date_column='timestamp'):
        """Extract time-based features from timestamp"""
        if df.empty or date_column not in df.columns:
            return df
        
        df = df.copy()
        df['hour'] = df[date_column].dt.hour
        df['day_of_week'] = df[date_column].dt.dayofweek
        df['day_of_month'] = df[date_column].dt.day
        df['month'] = df[date_column].dt.month
        df['week_of_year'] = df[date_column].dt.isocalendar().week
        df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
        
        return df
    
    def train_improvement_impact_predictor(self, data):
        """Train model to predict improvement impact"""
        print("🤖 Training improvement impact predictor...")
        
        df = data['improvements']
        if df.empty or len(df) < 50:
            print("  ⚠️ Insufficient data for training (need 50+ samples)")
            return None
        
        # Prepare features
        df = self.prepare_time_series_features(df)
        
        # Encode categorical variables
        df['category_encoded'] = pd.Categorical(df['category']).codes
        df['type_encoded'] = pd.Categorical(df['improvement_type']).codes
        
        # Select features
        features = ['hour', 'day_of_week', 'month', 'category_encoded', 'type_encoded']
        X = df[features].fillna(0)
        y = df['impact_score'].fillna(0)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test_scaled)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        
        print(f"  ✅ Model trained - RMSE: {rmse:.4f}, R²: {r2:.4f}")
        
        # Save model
        self.models['improvement_impact'] = model
        self.scalers['improvement_impact'] = scaler
        
        # Save to disk
        with open(f"{self.ml_dir}/improvement_impact_model.pkl", 'wb') as f:
            pickle.dump(model, f)
        with open(f"{self.ml_dir}/improvement_impact_scaler.pkl", 'wb') as f:
            pickle.dump(scaler, f)
        
        # Log performance
        self.log_model_performance(
            model_name='improvement_impact',
            model_type='RandomForestRegressor',
            accuracy=r2,
            rmse=rmse,
            r2_score=r2,
            training_samples=len(X_train),
            features=features
        )
        
        return {
            'model': model,
            'scaler': scaler,
            'rmse': rmse,
            'r2': r2,
            'features': features
        }
    
    def train_content_quality_predictor(self, data):
        """Train model to predict content quality"""
        print("🤖 Training content quality predictor...")
        
        df = data['content_quality']
        if df.empty or len(df) < 30:
            print("  ⚠️ Insufficient data for training (need 30+ samples)")
            return None
        
        # Prepare features
        df = self.prepare_time_series_features(df)
        
        # Select features
        features = ['word_count', 'hour', 'day_of_week', 'month']
        X = df[features].fillna(0)
        y = df['quality_score'].fillna(0)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train model
        model = GradientBoostingClassifier(n_estimators=100, random_state=42)
        
        # Convert to binary classification (high quality > 0.7)
        y_train_binary = (y_train > 0.7).astype(int)
        y_test_binary = (y_test > 0.7).astype(int)
        
        model.fit(X_train_scaled, y_train_binary)
        
        # Evaluate
        y_pred = model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test_binary, y_pred)
        
        print(f"  ✅ Model trained - Accuracy: {accuracy:.4f}")
        
        # Save model
        self.models['content_quality'] = model
        self.scalers['content_quality'] = scaler
        
        # Save to disk
        with open(f"{self.ml_dir}/content_quality_model.pkl", 'wb') as f:
            pickle.dump(model, f)
        with open(f"{self.ml_dir}/content_quality_scaler.pkl", 'wb') as f:
            pickle.dump(scaler, f)
        
        # Log performance
        self.log_model_performance(
            model_name='content_quality',
            model_type='GradientBoostingClassifier',
            accuracy=accuracy,
            rmse=0,
            r2_score=0,
            training_samples=len(X_train),
            features=features
        )
        
        return {
            'model': model,
            'scaler': scaler,
            'accuracy': accuracy,
            'features': features
        }
    
    def train_traffic_trend_predictor(self, data):
        """Train model to predict traffic trends"""
        print("🤖 Training traffic trend predictor...")
        
        # Combine multiple data sources for traffic proxy
        improvements_df = data['improvements']
        content_df = data['content_quality']
        
        if improvements_df.empty or content_df.empty:
            print("  ⚠️ Insufficient data for training")
            return None
        
        # Create daily aggregates
        improvements_daily = improvements_df.groupby('date').agg({
            'impact_score': 'sum',
            'category': 'count'
        }).reset_index()
        improvements_daily.columns = ['date', 'daily_impact', 'daily_improvements']
        
        content_daily = content_df.groupby(content_df['timestamp'].dt.date).agg({
            'quality_score': 'mean',
            'word_count': 'sum'
        }).reset_index()
        content_daily.columns = ['date', 'avg_quality', 'total_words']
        
        # Merge data
        df = pd.merge(improvements_daily, content_daily, on='date', how='outer').fillna(0)
        
        if len(df) < 30:
            print("  ⚠️ Insufficient data for training (need 30+ days)")
            return None
        
        # Create target variable (traffic proxy)
        df['traffic_proxy'] = (
            df['daily_impact'] * 10 +
            df['avg_quality'] * 5 +
            df['total_words'] / 100
        )
        
        # Prepare time features
        df['date'] = pd.to_datetime(df['date'])
        df = self.prepare_time_series_features(df, 'date')
        
        # Select features
        features = ['daily_impact', 'daily_improvements', 'avg_quality', 
                   'total_words', 'day_of_week', 'month', 'is_weekend']
        X = df[features].fillna(0)
        y = df['traffic_proxy']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test_scaled)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        
        print(f"  ✅ Model trained - RMSE: {rmse:.4f}, R²: {r2:.4f}")
        
        # Save model
        self.models['traffic_trend'] = model
        self.scalers['traffic_trend'] = scaler
        
        # Save to disk
        with open(f"{self.ml_dir}/traffic_trend_model.pkl", 'wb') as f:
            pickle.dump(model, f)
        with open(f"{self.ml_dir}/traffic_trend_scaler.pkl", 'wb') as f:
            pickle.dump(scaler, f)
        
        # Log performance
        self.log_model_performance(
            model_name='traffic_trend',
            model_type='RandomForestRegressor',
            accuracy=r2,
            rmse=rmse,
            r2_score=r2,
            training_samples=len(X_train),
            features=features
        )
        
        return {
            'model': model,
            'scaler': scaler,
            'rmse': rmse,
            'r2': r2,
            'features': features
        }
    
    def predict_next_week_improvements(self):
        """Predict improvement opportunities for next week"""
        print("🔮 Predicting next week's improvement opportunities...")
        
        if 'improvement_impact' not in self.models:
            print("  ⚠️ Model not trained yet")
            return None
        
        model = self.models['improvement_impact']
        scaler = self.scalers['improvement_impact']
        
        # Generate predictions for next 7 days
        predictions = []
        today = datetime.now()
        
        for day in range(1, 8):
            future_date = today + timedelta(days=day)
            
            # Create feature vector for each improvement category
            categories = ['seo', 'performance', 'design', 'content']
            
            for cat_idx, category in enumerate(categories):
                features = np.array([[
                    future_date.hour,
                    future_date.weekday(),
                    future_date.month,
                    cat_idx,
                    0  # type_encoded placeholder
                ]])
                
                features_scaled = scaler.transform(features)
                predicted_impact = model.predict(features_scaled)[0]
                
                predictions.append({
                    'date': future_date.strftime('%Y-%m-%d'),
                    'category': category,
                    'predicted_impact': round(predicted_impact, 3),
                    'confidence': 0.75  # Placeholder confidence
                })
        
        # Save predictions
        self.save_predictions(predictions, 'improvement_opportunities')
        
        return predictions
    
    def predict_content_performance(self, word_count=2000):
        """Predict content performance based on features"""
        print(f"🔮 Predicting content performance for {word_count} word article...")
        
        if 'content_quality' not in self.models:
            print("  ⚠️ Model not trained yet")
            return None
        
        model = self.models['content_quality']
        scaler = self.scalers['content_quality']
        
        now = datetime.now()
        features = np.array([[
            word_count,
            now.hour,
            now.weekday(),
            now.month
        ]])
        
        features_scaled = scaler.transform(features)
        prediction = model.predict(features_scaled)[0]
        probability = model.predict_proba(features_scaled)[0]
        
        result = {
            'word_count': word_count,
            'predicted_high_quality': bool(prediction),
            'confidence': round(float(max(probability)), 3),
            'timestamp': now.isoformat()
        }
        
        print(f"  ✅ Prediction: {'High Quality' if prediction else 'Needs Improvement'} (confidence: {result['confidence']})")
        
        return result
    
    def predict_traffic_trend(self, days_ahead=30):
        """Predict traffic trend for next N days"""
        print(f"🔮 Predicting traffic trend for next {days_ahead} days...")
        
        if 'traffic_trend' not in self.models:
            print("  ⚠️ Model not trained yet")
            return None
        
        model = self.models['traffic_trend']
        scaler = self.scalers['traffic_trend']
        
        predictions = []
        today = datetime.now()
        
        for day in range(1, days_ahead + 1):
            future_date = today + timedelta(days=day)
            
            # Use average values for features
            features = np.array([[
                0.7,  # daily_impact (average)
                5,    # daily_improvements (average)
                0.75, # avg_quality (average)
                2000, # total_words (average)
                future_date.weekday(),
                future_date.month,
                1 if future_date.weekday() >= 5 else 0
            ]])
            
            features_scaled = scaler.transform(features)
            predicted_traffic = model.predict(features_scaled)[0]
            
            predictions.append({
                'date': future_date.strftime('%Y-%m-%d'),
                'predicted_traffic_index': round(predicted_traffic, 2),
                'day_of_week': future_date.strftime('%A')
            })
        
        # Save predictions
        self.save_predictions(predictions, 'traffic_trend')
        
        return predictions
    
    def generate_ml_insights(self, data):
        """Generate actionable insights from ML analysis"""
        print("💡 Generating ML insights...")
        
        insights = []
        
        # Analyze improvement patterns
        if not data['improvements'].empty:
            df = data['improvements']
            
            # Best performing categories
            category_impact = df.groupby('category')['impact_score'].mean().sort_values(ascending=False)
            
            if len(category_impact) > 0:
                best_category = category_impact.index[0]
                best_impact = category_impact.iloc[0]
                
                insights.append({
                    'type': 'improvement_pattern',
                    'category': 'optimization',
                    'description': f"'{best_category}' improvements have highest average impact ({best_impact:.2f})",
                    'confidence': 0.85,
                    'recommended_action': f"Prioritize {best_category} improvements for maximum impact",
                    'priority': 'high'
                })
            
            # Best time for improvements
            df = self.prepare_time_series_features(df)
            hour_impact = df.groupby('hour')['impact_score'].mean().sort_values(ascending=False)
            
            if len(hour_impact) > 0:
                best_hour = hour_impact.index[0]
                
                insights.append({
                    'type': 'timing_optimization',
                    'category': 'scheduling',
                    'description': f"Improvements made around {best_hour}:00 have higher impact",
                    'confidence': 0.75,
                    'recommended_action': f"Schedule critical improvements for {best_hour}:00",
                    'priority': 'medium'
                })
        
        # Analyze content patterns
        if not data['content_quality'].empty:
            df = data['content_quality']
            
            # Optimal word count
            high_quality = df[df['quality_score'] > 0.7]
            if len(high_quality) > 0:
                avg_words = high_quality['word_count'].mean()
                
                insights.append({
                    'type': 'content_optimization',
                    'category': 'content',
                    'description': f"High-quality content averages {avg_words:.0f} words",
                    'confidence': 0.80,
                    'recommended_action': f"Target {avg_words:.0f} words for new content",
                    'priority': 'high'
                })
        
        # Analyze system health trends
        if not data['system_metrics'].empty:
            df = data['system_metrics']
            
            # Disk usage trend
            if 'disk_used_percent' in df.columns:
                recent_usage = df.tail(10)['disk_used_percent'].mean()
                
                if recent_usage > 70:
                    insights.append({
                        'type': 'system_health',
                        'category': 'maintenance',
                        'description': f"Disk usage trending high ({recent_usage:.1f}%)",
                        'confidence': 0.90,
                        'recommended_action': "Schedule cleanup or increase storage",
                        'priority': 'high'
                    })
        
        # Save insights
        for insight in insights:
            self.save_insight(insight)
        
        return insights
    
    def save_predictions(self, predictions, prediction_type):
        """Save predictions to database"""
        try:
            db_path = f"{self.data_dir}/ml_predictions.db"
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            for pred in predictions:
                cursor.execute('''
                    INSERT INTO predictions 
                    (timestamp, prediction_type, prediction_date, predicted_value, confidence_score, model_version)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    datetime.now().isoformat(),
                    prediction_type,
                    pred.get('date', datetime.now().isoformat()),
                    pred.get('predicted_impact', pred.get('predicted_traffic_index', 0)),
                    pred.get('confidence', 0.75),
                    'v1.0'
                ))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"  ⚠️ Error saving predictions: {e}")
    
    def save_insight(self, insight):
        """Save insight to database"""
        try:
            db_path = f"{self.data_dir}/ml_predictions.db"
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO ml_insights 
                (timestamp, insight_type, insight_category, description, confidence, recommended_action, priority, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                insight['type'],
                insight['category'],
                insight['description'],
                insight['confidence'],
                insight['recommended_action'],
                insight['priority'],
                'active'
            ))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"  ⚠️ Error saving insight: {e}")
    
    def log_model_performance(self, model_name, model_type, accuracy, rmse, r2_score, training_samples, features):
        """Log model performance metrics"""
        try:
            db_path = f"{self.data_dir}/ml_predictions.db"
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO model_performance 
                (timestamp, model_name, model_type, accuracy, rmse, r2_score, training_samples, features)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                model_name,
                model_type,
                accuracy,
                rmse,
                r2_score,
                training_samples,
                json.dumps(features)
            ))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"  ⚠️ Error logging performance: {e}")
    
    def generate_ml_report(self):
        """Generate comprehensive ML analytics report"""
        print("📊 Generating ML analytics report...")
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'models_trained': len(self.models),
            'model_details': {},
            'recent_predictions': self.get_recent_predictions(),
            'active_insights': self.get_active_insights(),
            'model_performance': self.get_model_performance()
        }
        
        # Add model details
        for model_name in self.models.keys():
            report['model_details'][model_name] = {
                'status': 'trained',
                'last_updated': datetime.now().isoformat()
            }
        
        # Save report
        filename = f"{self.reports_dir}/ml_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"  ✅ Report saved: {filename}")
        
        return report
    
    def get_recent_predictions(self, limit=20):
        """Get recent predictions from database"""
        try:
            db_path = f"{self.data_dir}/ml_predictions.db"
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT prediction_type, prediction_date, predicted_value, confidence_score
                FROM predictions
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
            
            predictions = []
            for row in cursor.fetchall():
                predictions.append({
                    'type': row[0],
                    'date': row[1],
                    'value': row[2],
                    'confidence': row[3]
                })
            
            conn.close()
            return predictions
        except Exception as e:
            print(f"  ⚠️ Error getting predictions: {e}")
            return []
    
    def get_active_insights(self):
        """Get active insights from database"""
        try:
            db_path = f"{self.data_dir}/ml_predictions.db"
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT insight_type, description, confidence, recommended_action, priority
                FROM ml_insights
                WHERE status = 'active'
                ORDER BY confidence DESC, priority DESC
                LIMIT 10
            ''')
            
            insights = []
            for row in cursor.fetchall():
                insights.append({
                    'type': row[0],
                    'description': row[1],
                    'confidence': row[2],
                    'action': row[3],
                    'priority': row[4]
                })
            
            conn.close()
            return insights
        except Exception as e:
            print(f"  ⚠️ Error getting insights: {e}")
            return []
    
    def get_model_performance(self):
        """Get model performance metrics"""
        try:
            db_path = f"{self.data_dir}/ml_predictions.db"
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT model_name, model_type, accuracy, rmse, r2_score, training_samples
                FROM model_performance
                ORDER BY timestamp DESC
                LIMIT 10
            ''')
            
            performance = []
            for row in cursor.fetchall():
                performance.append({
                    'model': row[0],
                    'type': row[1],
                    'accuracy': row[2],
                    'rmse': row[3],
                    'r2': row[4],
                    'samples': row[5]
                })
            
            conn.close()
            return performance
        except Exception as e:
            print(f"  ⚠️ Error getting performance: {e}")
            return []
    
    def run_ml_analytics(self):
        """Run complete ML analytics cycle"""
        print(f"🤖 ML Predictive Analytics - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # Load data
        data = self.load_historical_data()
        
        # Train models
        print("\n📚 Training ML models...")
        self.train_improvement_impact_predictor(data)
        self.train_content_quality_predictor(data)
        self.train_traffic_trend_predictor(data)
        
        # Generate predictions
        print("\n🔮 Generating predictions...")
        improvement_predictions = self.predict_next_week_improvements()
        traffic_predictions = self.predict_traffic_trend(30)
        content_prediction = self.predict_content_performance(2000)
        
        # Generate insights
        print("\n💡 Analyzing patterns...")
        insights = self.generate_ml_insights(data)
        
        # Generate report
        print("\n📊 Creating report...")
        report = self.generate_ml_report()
        
        # Print summary
        print("\n" + "=" * 70)
        print("📊 ML Analytics Summary:")
        print(f"  Models trained: {len(self.models)}")
        print(f"  Predictions generated: {len(improvement_predictions or []) + len(traffic_predictions or [])}")
        print(f"  Insights discovered: {len(insights)}")
        print(f"  Report saved: {self.reports_dir}/")
        print("=" * 70)
        
        return report

def main():
    """Main ML analytics loop"""
    ml_system = MLPredictiveAnalytics()
    
    print("🤖 ML Predictive Analytics System Started")
    print("Running analytics every 24 hours...")
    print()
    
    while True:
        try:
            ml_system.run_ml_analytics()
            print("\n⏰ Next ML analytics in 24 hours...")
            print()
            time.sleep(24 * 60 * 60)  # 24 hours
        except KeyboardInterrupt:
            print("\n👋 ML Analytics stopped")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Retrying in 1 hour...")
            time.sleep(60 * 60)

if __name__ == "__main__":
    import time
    main()