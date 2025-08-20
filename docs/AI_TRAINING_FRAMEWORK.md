# AI Pre-Training Framework Documentation
## Smith & Williams Trucking TMS - Intelligent Assistant Training Guide

---

## Table of Contents
1. [Overview](#overview)
2. [Training Data Structure](#training-data-structure)
3. [Business Context Training](#business-context-training)
4. [Command Recognition Patterns](#command-recognition-patterns)
5. [Response Templates](#response-templates)
6. [Learning Mechanisms](#learning-mechanisms)
7. [Integration Points](#integration-points)
8. [Performance Optimization](#performance-optimization)

---

## Overview

The AI Assistant in the Smith & Williams Trucking TMS is designed to understand and execute natural language commands related to trucking operations, business management, and personal finance tracking. This framework documents how the AI is trained and how it continues to learn from interactions.

### Core Capabilities
- Natural language understanding for trucking industry terminology
- Context-aware command execution
- Self-learning from user interactions
- Pattern recognition for predictive assistance
- Multi-domain knowledge (business operations, personal management)

---

## Training Data Structure

### 1. Domain Knowledge Base

```python
DOMAIN_KNOWLEDGE = {
    "trucking_operations": {
        "entities": ["load", "shipment", "dispatch", "delivery", "pickup"],
        "actions": ["create", "update", "track", "assign", "complete"],
        "attributes": ["rate", "miles", "weight", "commodity", "equipment"]
    },
    
    "financial_management": {
        "entities": ["invoice", "payment", "expense", "revenue"],
        "actions": ["record", "reconcile", "calculate", "report"],
        "attributes": ["amount", "date", "category", "source"]
    },
    
    "fleet_management": {
        "entities": ["truck", "trailer", "driver", "maintenance"],
        "actions": ["assign", "schedule", "track", "service"],
        "attributes": ["status", "location", "capacity", "availability"]
    },
    
    "personal_management": {
        "entities": ["property", "vehicle", "investment", "goal"],
        "actions": ["add", "track", "analyze", "plan"],
        "attributes": ["value", "type", "location", "performance"]
    }
}
```

### 2. Industry-Specific Vocabulary

```python
TRUCKING_VOCABULARY = {
    "abbreviations": {
        "BOL": "Bill of Lading",
        "POD": "Proof of Delivery",
        "HOS": "Hours of Service",
        "ELD": "Electronic Logging Device",
        "CDL": "Commercial Driver's License",
        "DOT": "Department of Transportation",
        "MC": "Motor Carrier",
        "IFTA": "International Fuel Tax Agreement",
        "LTL": "Less Than Truckload",
        "FTL": "Full Truckload"
    },
    
    "equipment_types": [
        "Dry Van", "Reefer", "Flatbed", "Step Deck",
        "RGN", "Tanker", "Box Truck", "Hotshot"
    ],
    
    "status_terms": [
        "Dispatched", "In Transit", "At Pickup", "Loading",
        "At Delivery", "Unloading", "Delivered", "Detained"
    ]
}
```

---

## Business Context Training

### 1. Company-Specific Information

```python
COMPANY_CONTEXT = {
    "business_name": "Smith & Williams Trucking LLC",
    "owner": "Brandon Smith",
    "role": "CEO/Owner-Operator",
    "primary_operations": ["Regional Freight", "Dedicated Routes"],
    
    "key_partners": {
        "factoring": "Treadstone Capital",
        "carrier_service": "CanAmex",
        "gps_eld": "Motive",
        "load_boards": ["Truckstop.com", "DAT"]
    },
    
    "operational_patterns": {
        "typical_routes": ["CA-TX", "CA-AZ", "CA-NV"],
        "average_rate_per_mile": 2.50,
        "preferred_equipment": "53' Dry Van",
        "payment_terms": "Net 30 with factoring"
    }
}
```

### 2. User Preferences Learning

```python
USER_PREFERENCES = {
    "Brandon": {
        "communication_style": "direct",
        "priority_metrics": ["revenue", "profit_margin", "utilization"],
        "report_frequency": "daily",
        "preferred_views": ["executive_dashboard", "driver_portal"],
        "common_tasks": [
            "check_daily_revenue",
            "review_active_loads",
            "track_expenses",
            "monitor_hos_status"
        ]
    }
}
```

---

## Command Recognition Patterns

### 1. Intent Classification

```python
INTENT_PATTERNS = {
    "create_shipment": [
        r"(create|add|new).*(load|shipment)",
        r"(load|shipment).*(from|pickup).*(to|deliver)",
        r"\$\d+.*(from|pickup).*(to|deliver)"
    ],
    
    "track_load": [
        r"(where|status|location).*(load|shipment|truck)",
        r"(track|find|locate).*(load|shipment)",
        r"load\s*#?\s*\d+"
    ],
    
    "financial_query": [
        r"(revenue|profit|income).*(today|week|month)",
        r"how much.*(made|earned|spent)",
        r"(show|display).*(expenses|costs)"
    ],
    
    "hos_status": [
        r"(hos|hours|drive time|duty)",
        r"(break|rest).*(required|needed)",
        r"(compliance|violation)"
    ]
}
```

### 2. Entity Extraction

```python
ENTITY_EXTRACTORS = {
    "location": {
        "pattern": r"(from|at|in|to)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*,?\s*[A-Z]{2})",
        "type": "city_state"
    },
    
    "money": {
        "pattern": r"\$?\d+(?:,\d{3})*(?:\.\d{2})?",
        "type": "currency"
    },
    
    "date": {
        "pattern": r"(today|tomorrow|yesterday|\d{1,2}/\d{1,2}(?:/\d{2,4})?)",
        "type": "date"
    },
    
    "load_number": {
        "pattern": r"(?:load\s*#?|SWT)?\s*(\d{5,})",
        "type": "identifier"
    }
}
```

---

## Response Templates

### 1. Confirmation Responses

```python
CONFIRMATION_TEMPLATES = {
    "shipment_created": """
    ✅ Load created successfully!
    - Load #: {load_number}
    - Route: {origin} to {destination}
    - Rate: ${rate:,.2f} ({rpm:.2f}/mile)
    - Pickup: {pickup_date}
    
    Would you like to assign a driver?
    """,
    
    "expense_recorded": """
    ✅ Expense recorded:
    - Category: {category}
    - Amount: ${amount:,.2f}
    - Date: {date}
    - Notes: {notes}
    
    Year-to-date {category}: ${ytd_total:,.2f}
    """,
    
    "status_update": """
    ✅ Status updated to: {new_status}
    - Load #: {load_number}
    - Location: {current_location}
    - ETA: {estimated_arrival}
    """
}
```

### 2. Information Responses

```python
INFORMATION_TEMPLATES = {
    "daily_summary": """
    📊 Daily Summary for {date}:
    
    **Operations:**
    - Active Loads: {active_loads}
    - Completed: {completed_loads}
    - Miles Driven: {total_miles:,}
    
    **Financial:**
    - Revenue: ${revenue:,.2f}
    - Expenses: ${expenses:,.2f}
    - Net: ${net_profit:,.2f}
    
    **HOS Status:**
    - Drive Time Remaining: {drive_hours:.1f} hrs
    - Status: {duty_status}
    """,
    
    "load_tracking": """
    📍 Load #{load_number} Status:
    - Current Location: {location}
    - Speed: {speed} mph
    - Distance Remaining: {remaining_miles} miles
    - ETA: {eta}
    - Status: {status}
    """
}
```

---

## Learning Mechanisms

### 1. Pattern Recognition

```python
class PatternLearning:
    def learn_from_interaction(self, user_input, action_taken, outcome):
        """Learn patterns from user interactions"""
        
        # Extract patterns
        patterns = {
            'time_of_day': self.extract_time_pattern(user_input),
            'command_structure': self.extract_command_pattern(user_input),
            'entity_references': self.extract_entities(user_input),
            'success_rate': 1.0 if outcome == 'success' else 0.0
        }
        
        # Update pattern database
        self.update_pattern_confidence(patterns)
        
        # Adjust future predictions
        self.refine_predictions(patterns)
    
    def predict_user_intent(self, context):
        """Predict what user might need based on patterns"""
        
        predictions = []
        current_time = context['time']
        current_day = context['day']
        
        # Time-based predictions
        if current_time.hour == 6:  # Morning
            predictions.append("Review today's scheduled loads")
        
        if current_day == 'Friday':  # End of week
            predictions.append("Generate weekly revenue report")
        
        if context['fuel_level'] < 25:  # Low fuel
            predictions.append("Find nearest fuel stop")
        
        return predictions
```

### 2. Feedback Integration

```python
class FeedbackLearning:
    def process_correction(self, original_intent, corrected_intent, context):
        """Learn from user corrections"""
        
        # Record the correction
        self.corrections_db.add({
            'original': original_intent,
            'corrected': corrected_intent,
            'context': context,
            'timestamp': datetime.now()
        })
        
        # Adjust confidence scores
        self.decrease_confidence(original_intent, context)
        self.increase_confidence(corrected_intent, context)
        
        # Retrain intent classifier if needed
        if self.correction_count(original_intent) > threshold:
            self.retrain_classifier(original_intent)
```

---

## Integration Points

### 1. Database Integration

```python
AI_DATABASE_MAPPINGS = {
    "natural_language": {
        "add new load": "INSERT INTO shipments",
        "show revenue": "SELECT SUM(rate) FROM shipments",
        "list active drivers": "SELECT * FROM drivers WHERE status = 'Active'",
        "track expenses": "SELECT * FROM expenses"
    },
    
    "entity_to_table": {
        "load": "shipments",
        "driver": "drivers",
        "truck": "trucks",
        "customer": "customers",
        "invoice": "invoices"
    }
}
```

### 2. API Integration

```python
AI_API_MAPPINGS = {
    "gps_commands": {
        "where is my truck": "motive.get_vehicle_location()",
        "current speed": "motive.get_current_speed()",
        "fuel level": "motive.get_fuel_level()"
    },
    
    "payment_commands": {
        "reconcile payments": "quickbooks.auto_match_payments()",
        "sync invoices": "quickbooks.sync_invoices()",
        "export to quickbooks": "quickbooks.export_data()"
    }
}
```

---

## Performance Optimization

### 1. Response Time Optimization

```python
OPTIMIZATION_STRATEGIES = {
    "caching": {
        "frequently_accessed": ["active_loads", "today_revenue", "hos_status"],
        "cache_duration": 300,  # 5 minutes
        "invalidation_triggers": ["new_load", "status_update", "payment_received"]
    },
    
    "query_optimization": {
        "use_indexes": True,
        "batch_operations": True,
        "lazy_loading": True
    },
    
    "prediction_preloading": {
        "preload_at_login": ["user_preferences", "common_tasks"],
        "background_refresh": ["gps_data", "hos_status"],
        "predictive_caching": ["likely_next_actions"]
    }
}
```

### 2. Accuracy Improvements

```python
ACCURACY_MEASURES = {
    "confidence_thresholds": {
        "high_confidence": 0.9,  # Execute immediately
        "medium_confidence": 0.7,  # Ask for confirmation
        "low_confidence": 0.5  # Show options
    },
    
    "context_weighting": {
        "current_view": 0.3,  # Weight based on current screen
        "recent_actions": 0.2,  # Weight based on recent activity
        "user_patterns": 0.3,  # Weight based on historical patterns
        "time_context": 0.2  # Weight based on time of day/week
    },
    
    "continuous_learning": {
        "min_interactions": 10,  # Minimum before pattern recognition
        "confidence_decay": 0.95,  # Daily confidence decay
        "retraining_threshold": 100  # Interactions before retraining
    }
}
```

---

## Training Implementation

### 1. Initial Training

```python
def train_ai_assistant():
    """Initial training of AI assistant"""
    
    ai = IntelligentAssistant()
    
    # Load domain knowledge
    ai.load_knowledge_base(DOMAIN_KNOWLEDGE)
    ai.load_vocabulary(TRUCKING_VOCABULARY)
    
    # Train intent classifier
    ai.train_intent_classifier(INTENT_PATTERNS)
    
    # Configure entity extractors
    ai.configure_extractors(ENTITY_EXTRACTORS)
    
    # Load response templates
    ai.load_templates(CONFIRMATION_TEMPLATES, INFORMATION_TEMPLATES)
    
    # Initialize learning mechanisms
    ai.enable_pattern_learning()
    ai.enable_feedback_learning()
    
    # Set optimization parameters
    ai.configure_optimization(OPTIMIZATION_STRATEGIES)
    
    return ai
```

### 2. Continuous Training

```python
def continuous_training_loop(ai):
    """Continuous training from user interactions"""
    
    while True:
        # Get user interaction
        interaction = ai.get_next_interaction()
        
        if interaction:
            # Process and learn
            result = ai.process_interaction(interaction)
            
            # Learn from outcome
            ai.learn_from_outcome(
                interaction.input,
                result.action,
                result.success
            )
            
            # Update patterns
            ai.update_user_patterns(interaction.user_id)
            
            # Check for retraining need
            if ai.needs_retraining():
                ai.retrain_models()
        
        # Sleep briefly
        time.sleep(0.1)
```

---

## Usage Examples

### Example 1: Load Creation
```
User: "Create a load from LA to Phoenix for $3500 picking up tomorrow"

AI Processing:
1. Intent: create_shipment (confidence: 0.95)
2. Entities extracted:
   - Origin: Los Angeles, CA
   - Destination: Phoenix, AZ
   - Rate: $3500
   - Pickup: tomorrow (computed date)
3. Action: Create shipment record
4. Response: Confirmation with load details
```

### Example 2: Financial Query
```
User: "How much did I make this week?"

AI Processing:
1. Intent: financial_query (confidence: 0.92)
2. Time period: current week
3. Metric: revenue
4. Query: SELECT SUM(rate) FROM shipments WHERE week = current
5. Response: Weekly revenue summary with comparison
```

### Example 3: Predictive Assistance
```
Context: Friday, 4:00 PM

AI Prediction:
"It's Friday afternoon. Would you like me to:
1. Generate weekly revenue report
2. Review next week's scheduled loads
3. Calculate driver settlements"
```

---

## Best Practices

1. **Regular Knowledge Updates**
   - Update industry terminology quarterly
   - Refresh company-specific patterns monthly
   - Review correction patterns weekly

2. **Performance Monitoring**
   - Track response accuracy daily
   - Monitor response times hourly
   - Review user satisfaction weekly

3. **Privacy and Security**
   - Never store sensitive payment information
   - Encrypt personal management data
   - Audit access logs regularly

4. **User Experience**
   - Keep responses concise and actionable
   - Always provide override options
   - Learn from user preferences

---

## Future Enhancements

1. **Voice Integration**
   - Natural speech recognition
   - Voice command execution
   - Audio confirmations

2. **Predictive Analytics**
   - Load recommendation engine
   - Route optimization suggestions
   - Maintenance predictions

3. **Multi-Language Support**
   - Spanish language commands
   - Regional dialect recognition
   - Industry-specific translations

4. **Advanced Learning**
   - Deep learning models for complex patterns
   - Reinforcement learning for optimization
   - Transfer learning from industry data

---

## Conclusion

This AI training framework provides a comprehensive foundation for the intelligent assistant in the Smith & Williams Trucking TMS. By combining domain-specific knowledge, continuous learning, and user pattern recognition, the system delivers an intuitive and powerful natural language interface for managing all aspects of the trucking business and personal management needs.

The framework is designed to evolve with usage, becoming more accurate and helpful over time while maintaining the flexibility to adapt to changing business needs and user preferences.