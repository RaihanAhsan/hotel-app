import requests
import json
from datetime import datetime, timedelta
from ..config import XENDIT_API_KEY, XENDIT_WEBHOOK_URL

class XenditService:
    def __init__(self):
        self.api_key = XENDIT_API_KEY
        self.base_url = "https://api.xendit.co"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self._encode_api_key()}"
        }

    def _encode_api_key(self):
        """Encode API key for Basic Auth"""
        import base64
        return base64.b64encode(f"{self.api_key}:".encode()).decode()

    def create_invoice(
        self,
        external_id: str,
        amount: float,
        payer_email: str,
        payer_name: str,
        description: str = "Hotel Booking Payment",
        items: list = None,
        success_redirect_url: str = "http://localhost:5173/payment/success",
        failure_redirect_url: str = "http://localhost:5173/payment/failure"
    ):
        """
        Create Xendit invoice using direct API call
        """
        # Prepare invoice items
        invoice_items = []
        if items:
            for item in items:
                invoice_items.append({
                    "name": item.get("name", "Room"),
                    "quantity": item.get("quantity", 1),
                    "price": item.get("price", amount),
                    "category": item.get("category", "Hotel")
                })
        else:
            invoice_items.append({
                "name": description,
                "quantity": 1,
                "price": amount,
                "category": "Hotel Booking"
            })

        # Prepare payload
        payload = {
            "external_id": external_id,
            "amount": amount,
            "payer_email": payer_email,
            "description": description,
            "invoice_items": invoice_items,
            "customer": {
                "given_names": payer_name,
                "email": payer_email
            },
            "currency": "IDR",
            "should_send_email": True,
            "success_redirect_url": success_redirect_url,
            "failure_redirect_url": failure_redirect_url,
            "payment_methods": ["BANK_TRANSFER", "CREDIT_CARD", "QR_CODE", "EWALLET"]
        }

        # Add webhook URL if configured
        if XENDIT_WEBHOOK_URL:
            payload["webhook_url"] = XENDIT_WEBHOOK_URL

        try:
            response = requests.post(
                f"{self.base_url}/v2/invoices",
                headers=self.headers,
                json=payload
            )

            if response.status_code in [200, 201]:
                data = response.json()
                return {
                    "success": True,
                    "invoice_id": data.get("id"),
                    "invoice_url": data.get("invoice_url"),
                    "status": data.get("status"),
                    "expiry_date": data.get("expiry_date"),
                    "external_id": data.get("external_id")
                }
            else:
                error_data = response.json() if response.text else {}
                return {
                    "success": False,
                    "error": error_data.get("message", f"HTTP {response.status_code}"),
                    "error_code": error_data.get("error_code"),
                    "status_code": response.status_code
                }

        except requests.RequestException as e:
            return {
                "success": False,
                "error": str(e)
            }

    def get_invoice_status(self, invoice_id: str):
        """
        Get invoice status from Xendit
        """
        try:
            response = requests.get(
                f"{self.base_url}/v2/invoices/{invoice_id}",
                headers=self.headers
            )

            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "id": data.get("id"),
                    "external_id": data.get("external_id"),
                    "status": data.get("status"),
                    "amount": data.get("amount"),
                    "paid_amount": data.get("paid_amount"),
                    "payer_email": data.get("payer_email"),
                    "expiry_date": data.get("expiry_date"),
                    "created": data.get("created")
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}",
                    "details": response.text
                }

        except requests.RequestException as e:
            return {
                "success": False,
                "error": str(e)
            }

    def expire_invoice(self, invoice_id: str):
        """
        Expire an invoice
        """
        try:
            response = requests.post(
                f"{self.base_url}/v2/invoices/{invoice_id}/expire",
                headers=self.headers
            )

            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "status": data.get("status"),
                    "id": data.get("id")
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}"
                }

        except requests.RequestException as e:
            return {
                "success": False,
                "error": str(e)
            }


# Singleton instance
xendit_service = XenditService()