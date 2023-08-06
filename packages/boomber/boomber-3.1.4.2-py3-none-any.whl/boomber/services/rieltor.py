from boomber.services.service import Service


class Rieltor(Service):
    phone_codes = [380]

    async def run(self):
        await self.post(
            "https://rieltor.ua/api/users/register-sms/",
            json={"phone": self.formatted_phone, "retry": 0},
        )
