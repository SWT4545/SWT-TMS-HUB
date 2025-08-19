"""
API Integrations Module for Smith & Williams Trucking TMS
Includes Motive, Vector, Google Maps, and placeholder for future APIs
"""
import os
import requests
import json
from datetime import datetime
import googlemaps
from geopy.distance import geodesic
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MotiveAPI:
    """Integration with Motive (formerly KeepTruckin) for GPS and ELD data"""
    
    def __init__(self):
        self.api_key = os.getenv('MOTIVE_API_KEY', '')
        self.base_url = "https://api.gomotive.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def get_vehicle_location(self, vehicle_id):
        """Get current GPS location of a vehicle"""
        if not self.api_key:
            return {"error": "Motive API key not configured"}
        
        try:
            response = requests.get(
                f"{self.base_url}/vehicles/{vehicle_id}/location",
                headers=self.headers
            )
            if response.status_code == 200:
                data = response.json()
                return {
                    "lat": data.get("latitude"),
                    "lng": data.get("longitude"),
                    "speed": data.get("speed"),
                    "heading": data.get("heading"),
                    "timestamp": data.get("located_at"),
                    "address": data.get("address")
                }
            else:
                return {"error": f"API error: {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}
    
    def get_driver_hos(self, driver_id):
        """Get driver's Hours of Service status"""
        if not self.api_key:
            return {"error": "Motive API key not configured"}
        
        try:
            response = requests.get(
                f"{self.base_url}/drivers/{driver_id}/hos_status",
                headers=self.headers
            )
            if response.status_code == 200:
                data = response.json()
                return {
                    "duty_status": data.get("duty_status"),
                    "drive_time_remaining": data.get("drive_time_remaining"),
                    "shift_time_remaining": data.get("shift_time_remaining"),
                    "cycle_time_remaining": data.get("cycle_time_remaining"),
                    "break_time_remaining": data.get("break_time_remaining")
                }
            else:
                return {"error": f"API error: {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}
    
    def create_trip(self, load_data):
        """Create a new trip in Motive"""
        if not self.api_key:
            return {"error": "Motive API key not configured"}
        
        payload = {
            "trip": {
                "destination_address": load_data.get("delivery_address"),
                "origin_address": load_data.get("pickup_address"),
                "scheduled_at": load_data.get("pickup_date"),
                "load_id": load_data.get("load_id"),
                "driver_id": load_data.get("driver_id"),
                "vehicle_id": load_data.get("truck_id")
            }
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/trips",
                headers=self.headers,
                json=payload
            )
            if response.status_code == 201:
                return response.json()
            else:
                return {"error": f"API error: {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}


class VectorAPI:
    """Integration with Vector for document management"""
    
    def __init__(self):
        self.api_key = os.getenv('VECTOR_API_KEY', '')
        self.base_url = "https://api.vectorapp.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def upload_document(self, file_data, load_id, doc_type="BOL"):
        """Upload a document to Vector"""
        if not self.api_key:
            return {"error": "Vector API key not configured"}
        
        try:
            files = {'file': file_data}
            data = {
                'load_id': load_id,
                'document_type': doc_type,
                'uploaded_at': datetime.now().isoformat()
            }
            
            response = requests.post(
                f"{self.base_url}/documents/upload",
                headers={"Authorization": f"Bearer {self.api_key}"},
                files=files,
                data=data
            )
            
            if response.status_code == 201:
                return response.json()
            else:
                return {"error": f"API error: {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}
    
    def get_document(self, document_id):
        """Retrieve a document from Vector"""
        if not self.api_key:
            return {"error": "Vector API key not configured"}
        
        try:
            response = requests.get(
                f"{self.base_url}/documents/{document_id}",
                headers=self.headers
            )
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"API error: {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}


class GoogleMapsAPI:
    """Integration with Google Maps for distance and routing"""
    
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_MAPS_API_KEY', '')
        if self.api_key:
            self.client = googlemaps.Client(key=self.api_key)
        else:
            self.client = None
    
    def calculate_distance(self, origin, destination):
        """Calculate distance between two addresses"""
        if not self.client:
            # Fallback to estimated calculation
            return self.estimate_distance(origin, destination)
        
        try:
            result = self.client.distance_matrix(
                origins=[origin],
                destinations=[destination],
                mode="driving",
                units="imperial"
            )
            
            if result['status'] == 'OK':
                element = result['rows'][0]['elements'][0]
                if element['status'] == 'OK':
                    return {
                        "distance_miles": element['distance']['value'] / 1609.34,  # Convert meters to miles
                        "distance_text": element['distance']['text'],
                        "duration_seconds": element['duration']['value'],
                        "duration_text": element['duration']['text']
                    }
            return {"error": "Could not calculate distance"}
        except Exception as e:
            return {"error": str(e)}
    
    def estimate_distance(self, origin, destination):
        """Estimate distance when API is not available"""
        # Simple estimation based on state-to-state average distances
        # This is a fallback method
        state_distances = {
            ("CA", "TX"): 1400,
            ("CA", "FL"): 2700,
            ("NY", "CA"): 2900,
            ("TX", "FL"): 1100,
            ("IL", "CA"): 2000,
            # Add more as needed
        }
        
        # Extract states from addresses if possible
        # For now, return a default estimate
        return {
            "distance_miles": 500,  # Default estimate
            "distance_text": "~500 miles (estimated)",
            "duration_seconds": 28800,  # 8 hours
            "duration_text": "~8 hours (estimated)",
            "is_estimate": True
        }
    
    def geocode_address(self, address):
        """Get latitude and longitude for an address"""
        if not self.client:
            return {"error": "Google Maps API key not configured"}
        
        try:
            result = self.client.geocode(address)
            if result:
                location = result[0]['geometry']['location']
                return {
                    "lat": location['lat'],
                    "lng": location['lng'],
                    "formatted_address": result[0]['formatted_address']
                }
            return {"error": "Address not found"}
        except Exception as e:
            return {"error": str(e)}


class GeofenceManager:
    """Manage geofences for automated check-ins"""
    
    @staticmethod
    def check_geofence(current_lat, current_lng, geofence_lat, geofence_lng, radius_meters=500):
        """Check if current location is within a geofence"""
        current_point = (current_lat, current_lng)
        geofence_point = (geofence_lat, geofence_lng)
        
        distance = geodesic(current_point, geofence_point).meters
        
        return {
            "within_geofence": distance <= radius_meters,
            "distance_meters": distance,
            "distance_feet": distance * 3.28084
        }
    
    @staticmethod
    def auto_checkin(load_id, location_type, timestamp=None):
        """Automatically check in at a location"""
        from modules.database_enhanced import execute_query
        
        if timestamp is None:
            timestamp = datetime.now()
        
        if location_type == "pickup_arrival":
            field = "pickup_arrival_time"
        elif location_type == "pickup_departure":
            field = "pickup_departure_time"
        elif location_type == "delivery_arrival":
            field = "delivery_arrival_time"
        elif location_type == "delivery_departure":
            field = "delivery_departure_time"
        else:
            return False
        
        query = f"UPDATE loads SET {field} = ?, updated_at = ? WHERE id = ?"
        execute_query(query, (timestamp, datetime.now(), load_id))
        
        return True


class TruckstopAPI:
    """Placeholder for Truckstop.com Load Board API"""
    
    def __init__(self):
        self.api_key = os.getenv('TRUCKSTOP_API_KEY', '')
        self.base_url = "https://api.truckstop.com/v2"
        # Placeholder for future implementation
    
    def search_loads(self, origin_state, destination_state, equipment_type):
        """Search for available loads - TO BE IMPLEMENTED"""
        return {
            "status": "pending_implementation",
            "message": "Truckstop.com API integration will be available soon"
        }


class QuickBooksAPI:
    """Placeholder for QuickBooks Online API"""
    
    def __init__(self):
        self.client_id = os.getenv('QUICKBOOKS_CLIENT_ID', '')
        self.client_secret = os.getenv('QUICKBOOKS_CLIENT_SECRET', '')
        # Placeholder for future implementation
    
    def create_invoice(self, load_data):
        """Create invoice in QuickBooks - TO BE IMPLEMENTED"""
        return {
            "status": "pending_implementation",
            "message": "QuickBooks integration will be available soon"
        }
    
    def sync_payments(self):
        """Sync payments with QuickBooks - TO BE IMPLEMENTED"""
        return {
            "status": "pending_implementation",
            "message": "QuickBooks integration will be available soon"
        }