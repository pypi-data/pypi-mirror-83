from boomber.services.service import Service


class IQLab(Service):
    phone_codes = [380]

    async def run(self):
        await self.post(
            "https://iqlab.com.ua/session/ajaxregister",
            data={
                "cellphone": self.format(self.formatted_phone, "+** (***) *** ** **"),
            },
        )
