from http import HTTPStatus
from typing import Union, Set, List
import asyncio
import httpx
import logging

class Autoreg:
    def __init__(self, app, settings: object, log: object= None,exclude_list: Union[Set[str],List[str]] = None):
        """[Auto registration endpoints in DAC]
        Args:
            app: [Instance of Fastapi app]
            log: Optional: [Instance of Log]
            settings: [Instance of Settings]
        """
        self.app = app
        self.log = log or logging.getLogger(__name__)
        # endpoints in exclude_list is not registered in DAC
        self.exclude_list = {"/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc", "/metrics/"}
        self.dac_url = settings.DAC_URL
        self.service_name = settings.SERVICE_NAME
        self.prefixes = set()
        if exclude_list:
            self.exclude_list = self.exclude_list | exclude_list if isinstance(exclude_list,set) else set(exclude_list)

    async def autoreg(self):
        """
        [autoreg function creates service and endpoints]
        """

        # Gettings routes from app instance and creating prefixes set
        for route in self.app.routes:
            if route.path not in self.exclude_list:
                try:
                    self.prefixes.add(route.path)
                except Exception as err:
                    self.log.error(err, exc_info=True)
  

        # Creating service
        service_id = await self.create_service()

        # If service created successfully, creating endpoints with foreign key to this service: self.service_name
        if service_id:
            await self.create_endpoints(service_id)


    async def create_endpoints(self,service_id: str):
        """[summary]
        Args:
            service_id (str): [service_id of created service]
            [Creating endpoints pointing to service_id]
        """

        # Getting registered prefixes from database
        # We will use this prefixes list to check if endpoint is registered or not
        registered_prefixes = await self.registered_endpoints()

        for prefix in registered_prefixes:
            if prefix not in registered_prefixes:
                async with httpx.AsyncClient() as client:
                    await client.post(
                        f"{self.dac_url}/endpoints", 
                        json={"service_id": service_id, "prefix": prefix}
                        )
                    
                    self.log.info(f"{prefix} registered")
            else:
                log.warning(f"{prefix} is already registered")

    async def create_service(self):
        """[summary]

        Returns:
            [type]: [service id (str)]
        
        Flow:
            [get service_id] if exists return service_id
            [create service_id] if service not exists
        """
        # In one async with client we can not send 2 requests. 

        # Get service_name from database. Return id if exists
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.dac_url}/services/by-name/{self.service_name}")
                if response.status_code == HTTPStatus.OK:
                    self.log.info(f"{response.json().get('name')} exists")
                    return response.json().get("id")
            
            # Create service_name if not exists
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{self.dac_url}/services", json = {"name": self.service_name})
                self.log.info(f"{response.json().get('name')} created")
                if response:
                    return response.json().get("id")
        except Exception as err:
            self.log.error(err,exc_info=True)


    async def registered_endpoints(self):
        """Get registered endpoints from database

        Returns:
            [list]: [Getting prefixes from endpoints registered in database]
        """
        async with httpx.AsyncClient() as client:
                    endpoints = await client.get(
                        f"{self.dac_url}/endpoints"
                    )
        return [content.get("prefix") for content in endpoints.json()]