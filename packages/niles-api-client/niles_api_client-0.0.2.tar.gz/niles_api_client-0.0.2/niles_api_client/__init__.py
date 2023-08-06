#  Copyright (c) 2019 Markus Ressel
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
import asyncio
import json
import logging
import uuid
from datetime import datetime
from types import coroutine
from typing import Dict, Any, List

import websockets as websockets

from niles_api_client.const import *
from niles_api_client.util import json_converter

LOGGER = logging.getLogger(__name__)

__version__ = "0.0.2"


class NilesException(Exception):
    pass


class NilesApiClient:

    def __init__(self, api_token: str, host: str = "localhost", port: int = 9465, ssl: bool = False):
        self.api_token = api_token
        self.host = host
        self.port = port
        self.ssl = ssl

        self.uri = f"{'wss' if ssl else 'ws'}://{self.host}:{self.port}"

        self.websocket_client = None
        self._incoming_message_task = None
        # initially a map of "uuid" -> "event",
        # when a response is ready "uuid" -> "response data"
        self._response_events = {}
        # map of "topic" -> "callback"
        self._topic_events = {}

    async def connect(self):
        if self.websocket_client is not None:
            return

        self.websocket_client = await websockets.connect(
            self.uri,
            extra_headers=[
                (X_Auth_Token, self.api_token)
            ],
        )
        if self._incoming_message_task is None:
            self._incoming_message_task = asyncio.create_task(self._incoming_message_task_loop())

    async def _incoming_message_task_loop(self):
        while True:
            try:
                message = await self.websocket_client.recv()
                message = json.loads(message)
                # LOGGER.debug(f"Received Message: {response}")

                message_uuid = message[KEY_UUID]
                message_type = message[KEY_TYPE]
                message_data = message[KEY_DATA]
                if message_type == "response":
                    event = self._response_events.get(message_uuid, None)
                    if event is None:
                        LOGGER.warning(f"No callback for incoming message: {message_uuid}")
                    else:
                        if message[KEY_STATUS] == STATUS_ERROR:
                            self._response_events[message_uuid] = NilesException(message[KEY_DATA])
                        else:
                            self._response_events[message_uuid] = message_data
                        event.set()
                elif message_type == "event":
                    topic = message[KEY_TOPIC]
                    callbacks = self._topic_events.get(topic, None)
                    for callback in callbacks:
                        asyncio.create_task(callback(topic, message_data))

            except Exception as ex:
                LOGGER.exception(ex)
                await asyncio.sleep(1)

    async def disconnect(self):
        if self.websocket_client is None:
            return
        if self._incoming_message_task is not None:
            self._incoming_message_task.cancel()
            self._incoming_message_task = None
        await self.websocket_client.close()
        self.websocket_client = None

    async def execute_command(self, name: str, data: Dict = None, timeout: int = 3) -> Any:
        """
        Send a command request to the server and return the response
        :param name: command name
        :param data: command data
        :param timeout: time to wait for a response in seconds
        :return: response data
        """
        if self.websocket_client is None:
            await self.connect()

        message_id = str(uuid.uuid4())
        command_message = json.dumps({
            KEY_UUID: message_id,
            KEY_NAME: name,
            KEY_DATA: data
        }, default=json_converter)
        response = asyncio.wait_for(self._wait_for_response(message_id), timeout)
        await self.websocket_client.send(command_message)
        try:
            return await response
        finally:
            self._response_events.pop(message_id, None)

    async def get_version(self) -> str:
        """
        :return: the server version
        """
        return await self.execute_command(COMMAND_VERSION)

    async def login(self, username: str, password: str):
        """
        Authenticate with the given credentials
        :param username: user name
        :param password: password
        """
        return await self.execute_command(COMMAND_LOGIN, {
            "username": username,
            "password": password
        })

    async def logout(self):
        """
        Logout the current user
        """
        return await self.execute_command(COMMAND_LOGOUT)

    async def get_users(self) -> List[Dict]:
        """
        Get a list of all users
        :return: list of users
        """
        return await self.execute_command(COMMAND_GET_USERS)

    async def add_user(self, username: str, password: str) -> Dict:
        """
        Create a new user with the given credentials
        :param username: user name
        :param password: password
        :return: user
        """
        return await self.execute_command(COMMAND_ADD_USER, {
            "username": username,
            "password": password
        })

    async def delete_user(self, username: str, password: str):
        """
        Deletes an existing user
        :param username: user name
        :param password: user password
        """
        return await self.execute_command(COMMAND_DELETE_USER, {
            "username": username,
            "password": password
        })

    async def get_products(self) -> List[Dict]:
        """
        Get a list of all products
        :return: list of products
        """
        return await self.execute_command(COMMAND_GET_PRODUCTS)

    async def get_product(self, product_id: int) -> Dict:
        """
        Get a product
        :param product_id: product id
        :return: product
        """
        return await self.execute_command(COMMAND_GET_PRODUCT, {
            "product_id": product_id
        })

    async def add_product(self, product: Dict) -> Dict:
        """
        Add a product to the catalog
        :param product: product parameters
        :return: product
        """
        return await self.execute_command(COMMAND_ADD_PRODUCT, product)

    async def find_product(self, query: str or None = None, barcode: str or None = None):
        """
        Find a product using a query string or a barcode
        :param query: search query
        :param barcode: product barcode
        :return: product
        """
        return await self.execute_command(COMMAND_FIND_PRODUCT, {
            "query": query,
            "barcode": barcode
        })

    async def get_stock_items(self, product_id: int = None) -> List[Dict]:
        """
        Get stock items
        :param product_id: (optional) product id
        """
        return await self.execute_command(COMMAND_GET_STOCK_ITEMS, {
            "product_id": product_id,
        })

    async def add_to_stock(self, product_id: int, amount: int, price: float = None, expiration_date: datetime = None):
        """
        Add a specific amount of an existing product to stock
        :param product_id: product id
        :param amount: amount
        :param price: price
        :param expiration_date: expiration_date
        """
        return await self.execute_command(COMMAND_ADD_TO_STOCK, {
            "product_id": product_id,
            "amount": amount,
            "price": price,
            "expiration_date": expiration_date,
        })

    async def remove_from_stock(self, stock_item_id: int):
        """
        Remove a specific stock item
        :param stock_item_id: stock item id
        """
        return await self.execute_command(COMMAND_REMOVE_FROM_STOCK, {
            "stock_item_id": stock_item_id
        })

    async def get_shopping_lists(self) -> List[Dict]:
        """
        Get a list of all shopping lists
        :return: list of shopping lists
        """
        return await self.execute_command(COMMAND_GET_SHOPPING_LISTS)

    async def get_shopping_list(self, shopping_list_id: int) -> Dict:
        """
        Get a shopping list
        :param shopping_list_id: shopping list id
        :return: shopping list
        """
        return await self.execute_command(COMMAND_GET_SHOPPING_LIST, {
            "id": shopping_list_id
        })

    async def add_to_shopping_list(self, product_id: int, amount: int, shopping_list_id: int) -> Dict:
        """
        Add a product to a shopping list
        :param product_id: product id
        :param amount: amount
        :param shopping_list_id: shopping list id
        :return: updated shopping list
        """
        return await self.execute_command(COMMAND_ADD_TO_SHOPPING_LIST, {
            "product_id": product_id,
            "amount": amount,
            "shopping_list_id": shopping_list_id
        })

    async def remove_from_shopping_list(self, product_id: int, amount: int, shopping_list_id: int) -> Dict:
        """
        Remove a product from a shopping list
        :param product_id: product id
        :param amount: amount
        :param shopping_list_id: shopping list id
        :return: updated shopping list
        """
        return await self.execute_command(COMMAND_REMOVE_FROM_SHOPPING_LIST, {
            "product_id": product_id,
            "amount": amount,
            "shopping_list_id": shopping_list_id
        })

    async def get_shopping_list_items(self, shopping_list_id: int) -> List[Dict]:
        """
        Get all items of a shopping list
        :param shopping_list_id: shopping list id
        :return: shopping list items
        """
        return await self.execute_command(COMMAND_GET_SHOPPING_LIST_ITEMS, {
            "shopping_list_id": shopping_list_id
        })

    async def get_persons(self) -> List[Dict]:
        """
        Get a list of all persons
        :return: list of persons
        """
        return await self.execute_command(COMMAND_GET_PERSONS)

    async def get_tasks(self) -> List[Dict]:
        """
        Get a list of all tasks
        :return: list of tasks
        """
        return await self.execute_command(COMMAND_GET_TASKS)

    async def add_task(self, task: Dict) -> Dict:
        """
        Add a task
        :param task: task parameters
        :return: task
        """
        return await self.execute_command(COMMAND_ADD_TASK, task)

    async def assign_task_to_person(self, task_id: int, person_id: int or None) -> Dict:
        """
        Add a task
        :param task_id: task id
        :param person_id: person id
        :return: task
        """
        return await self.execute_command(COMMAND_ASSIGN_TASK_TO_PERSON, {
            "task_id": task_id,
            "person_id": person_id,
        })

    async def delete_task(self, name: str):
        """
        Delete a task
        :param name: task name to delete
        """
        return await self.execute_command(COMMAND_DELETE_TASK, {
            "name": name
        })

    async def execute_task(self, task_id: int, person_id: int):
        """
        Execute a task
        :param task_id: task id
        :param person_id: person id of the executing person
        """
        return await self.execute_command(COMMAND_EXECUTE_TASK, {
            "task_id": task_id,
            "person_id": person_id
        })

    async def get_task_executions(self, task_id: int or None = None, person_id: int or None = None):
        """
        Get a list of task executions
        :param task_id: task id
        :param person_id: person id of the executing person
        """
        return await self.execute_command(COMMAND_GET_TASK_EXECUTIONS, {
            "task_id": task_id,
            "person_id": person_id
        })

    async def get_barcodes(self):
        """
        Get a list of all barcodes
        """
        return await self.execute_command(COMMAND_GET_BARCODES)

    async def get_barcode_scans(self):
        """
        Get a list of all barcode scans
        """
        return await self.execute_command(COMMAND_GET_BARCODE_SCANS)

    async def subscribe(self, topic: str, callback: coroutine):
        """
        Subscribe to a topic
        :param topic: the topic path
        :param callback: coroutine to call on events
        """
        response = await self.execute_command(COMMAND_SUBSCRIBE, {
            KEY_TOPIC: topic
        })
        await self._add_callback(topic, callback)
        return response

    async def unsubscribe(self, topic: str):
        """
        Unsubscribe from a topic
        :param topic: the topic path
        """
        return await self.execute_command(COMMAND_UNSUBSCRIBE, {
            KEY_TOPIC: topic
        })

    async def _add_callback(self, topic, callback):
        self._topic_events.setdefault(topic, set()).add(callback)

    async def _wait_for_response(self, message_id: str):
        event = asyncio.Event()
        self._response_events[message_id] = event
        await event.wait()
        response = self._response_events.pop(message_id)
        if isinstance(response, NilesException):
            raise response
        else:
            return response
