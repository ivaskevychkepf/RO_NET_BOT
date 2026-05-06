import aiohttp
import uuid

MONO_API_URL = "https://api.monobank.ua/api/merchant/invoice/create"

class MonoService:
    def __init__(self, token: str):
        self.token = token

    async def create_invoice(self, amount_uah: int, desc: str, redirect_url: str | None = None):
        """
        Створює рахунок Monobank (invoice)
        """

        headers = {
            "X-Token": self.token,
            "Content-Type": "application/json"
        }

        payload = {
            "amount": amount_uah * 100,
            "ccy": 980,
            "merchantPaymInfo": {
                "reference": str(uuid.uuid4()),
                "destination": desc
            },
            "redirectUrl": redirect_url,
            "webHookUrl": None
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(MONO_API_URL, json=payload, headers=headers) as resp:
                data = await resp.json()

        return data


    async def get_invoice_status(self, invoice_id: str):
        """
        Перевірка статусу платежу
        """

        url = f"https://api.monobank.ua/api/merchant/invoice/status?invoiceId={invoice_id}"

        headers = {
            "X-Token": self.token
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                return await resp.json()