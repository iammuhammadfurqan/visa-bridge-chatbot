import json
import time
from datetime import datetime
from typing import Dict, List
import logging
from config import EVAL_CONFIG

class ChatbotEvaluator:
    def __init__(self):
        self.metrics = {
            'total_conversations': 0,
            'total_queries': 0,
            'response_times': [],
            'errors': [],
            'conversation_history': []
        }
        self.current_conversation = {
            'start_time': None,
            'queries': [],
            'responses': []
        }

    def start_conversation(self):
        """Start tracking a new conversation."""
        self.current_conversation = {
            'start_time': datetime.now(),
            'queries': [],
            'responses': []
        }
        self.metrics['total_conversations'] += 1

    def record_interaction(self, query: str, response: str, response_time: float, error: str = None):
        """Record a single interaction in the conversation."""
        self.metrics['total_queries'] += 1
        self.metrics['response_times'].append(response_time)
        
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'response': response,
            'response_time': response_time,
            'error': error
        }
        
        self.current_conversation['queries'].append(query)
        self.current_conversation['responses'].append(response)
        
        if error:
            self.metrics['errors'].append({
                'timestamp': datetime.now().isoformat(),
                'error': error,
                'query': query
            })

    def end_conversation(self):
        """End the current conversation and save metrics."""
        self.current_conversation['end_time'] = datetime.now()
        self.metrics['conversation_history'].append(self.current_conversation)
        self._save_metrics()

    def _save_metrics(self):
        """Save metrics to file."""
        try:
            with open(EVAL_CONFIG['metrics_file'], 'w') as f:
                json.dump(self.metrics, f, indent=2)
        except Exception as e:
            logging.error(f"Error saving metrics: {str(e)}")

    def generate_summary(self) -> Dict:
        """Generate a summary of the chatbot's performance."""
        if not self.metrics['response_times']:
            return {"error": "No data available for summary"}

        avg_response_time = sum(self.metrics['response_times']) / len(self.metrics['response_times'])
        error_rate = len(self.metrics['errors']) / self.metrics['total_queries'] if self.metrics['total_queries'] > 0 else 0

        summary = {
            'total_conversations': self.metrics['total_conversations'],
            'total_queries': self.metrics['total_queries'],
            'average_response_time': round(avg_response_time, 2),
            'error_rate': round(error_rate * 100, 2),
            'total_errors': len(self.metrics['errors']),
            'generated_at': datetime.now().isoformat()
        }

        return summary 