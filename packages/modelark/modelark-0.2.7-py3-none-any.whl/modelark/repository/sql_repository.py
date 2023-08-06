import time
import json
from uuid import uuid4
from typing import (
    List, Type, Tuple, Mapping, Generic, Callable, Union, overload)
from ..common import (
    T, R, L, Domain, Conditioner, DefaultConditioner,
    Locator, DefaultLocator, Editor, DefaultEditor)
from ..connector import Connector
from .repository import Repository


class SqlRepository(Repository, Generic[T]):
    def __init__(self,
                 table: str,
                 constructor: Callable,
                 connector: Connector,
                 conditioner: Conditioner = None,
                 locator: Locator = None,
                 editor: Editor = None) -> None:
        self.table = table
        self.constructor = constructor
        self.connector = connector
        self.conditioner = conditioner or DefaultConditioner()
        self.locator = locator or DefaultLocator('public')
        self.editor = editor or DefaultEditor()
        self.max_items = 10_000
        self.jsonb_field = 'data'

    async def add(self, item: Union[T, List[T]]) -> List[T]:
        records = []
        items = item if isinstance(item, list) else [item]
        for item in items:
            item.id = item.id or str(uuid4())
            item.updated_at = int(time.time())
            item.updated_by = self.editor.reference
            item.created_at = item.created_at or item.updated_at
            item.created_by = item.created_by or item.updated_by
            records.append((json.dumps(vars(item)),))

        namespace = f"{self.locator.location}.{self.table}"
        query = f"""
            INSERT INTO {namespace}({self.jsonb_field}) (
                SELECT *
                FROM unnest($1::{namespace}[]) AS d
            )
            ON CONFLICT (({self.jsonb_field}->>'id'))
            DO UPDATE
                SET {self.jsonb_field} = {namespace}.{self.jsonb_field} ||
                EXCLUDED.{self.jsonb_field} - 'created_at' - 'created_by'
            RETURNING *;
        """
        connection = await self.connector.get(self.locator.zone)
        rows = await connection.fetch(query, records)

        return [self.constructor(**json.loads(row[self.jsonb_field]))
                for row in rows if self.jsonb_field in row]

    @overload
    async def search(self, domain: Domain,
                     limit: int = None, offset: int = None) -> List[T]:
        """Standard search method"""

    @overload
    async def search(self, domain: Domain,
                     limit: int = None, offset: int = None,
                     *,
                     join: 'Repository[R]',
                     link: 'Repository[L]' = None,
                     source: str = None,
                     target: str = None) -> List[Tuple[T, List[R]]]:
        """Joining search method"""

    async def search(
            self, domain: Domain,
            limit: int = None,
            offset: int = None,
            *,
            join: 'Repository[R]' = None,
            link: 'Repository[L]' = None,
            source: str = None,
            target: str = None) -> Union[List[T], List[Tuple[T, List[R]]]]:

        condition, parameters = self.conditioner.parse(domain)

        select = f"SELECT {self.jsonb_field}"
        from_ = f"FROM {self.locator.location}.{self.table}"
        where = f"WHERE {condition}"
        group = ''
        order = f"{self._order_by()}"

        if join:
            reference = (link == self) and join or self
            join_table = link_table = getattr(join, 'table')
            join_jsonb_field = getattr(join, 'jsonb_field')
            source = source or f'{reference.model.__name__.lower()}_id'
            pivot = link not in (self, join) and link
            if pivot:
                link_table = getattr(pivot, 'table')

            select = (f"SELECT {self.table}.{self.jsonb_field}, "
                      f"array_agg({join_table}.{join_jsonb_field})")

            on = (f"ON {link_table}.{join_jsonb_field}->>'{source}' = "
                  f"{self.table}.{self.jsonb_field}->>'id'\n")
            if link == self:
                on = (f"ON {self.table}.{self.jsonb_field}->>'{source}' = "
                      f"{link_table}.{join_jsonb_field}->>'id'\n")
            elif pivot:
                target = target or f'{join.model.__name__.lower()}_id'
                link_jsonb_field = getattr(link, 'jsonb_field')
                on += (f"        JOIN {self.locator.location}.{join_table} "
                       f"ON {link_table}.{link_jsonb_field}->>'{target}' = "
                       f"{join_table}.{join_jsonb_field}->>'id'\n")

            from_ = (
                f"FROM {self.locator.location}.{self.table} "
                f"LEFT JOIN {self.locator.location}.{link_table}\n"
                f"        {on}")
            group = f"GROUP BY {self.table}.{self.jsonb_field}"

        query = f"""\
        {select}
        {from_}
        {where}
        {group}
        {order}
        {f'LIMIT {limit}' if limit is not None else ''}
        {f'OFFSET {offset}' if offset else ''}
        """

        connection = await self.connector.get(self.locator.zone)
        rows = await connection.fetch(query, *parameters)

        if join:
            records = []
            join_constructor = getattr(join, 'constructor')
            for row in rows:
                array = [join_constructor(**json.loads(item))
                         for item in row['array_agg']]
                records.append((self.constructor(
                    **json.loads(row[self.jsonb_field])), array))
            return records

        return [self.constructor(**json.loads(row[self.jsonb_field]))
                for row in rows if self.jsonb_field in row]

    async def remove(self, item: Union[T, List[T]]) -> bool:
        if not item:
            return False
        items = item if isinstance(item, list) else [item]
        ids = [item.id for item in items]
        placeholders = ", ".join(f'${i + 1}' for i in range(len(ids)))

        query = f"""
            DELETE FROM {self.locator.location}.{self.table}
            WHERE ({self.jsonb_field}->>'id') IN ({placeholders})
        """

        connection = await self.connector.get(self.locator.zone)
        result = await connection.execute(query, *ids)

        return bool(int(result.replace('DELETE', '') or 0))

    async def count(self, domain: Domain = None) -> int:
        condition, parameters = self.conditioner.parse(domain or [])

        query = f"""
            SELECT count(*) as count
            FROM {self.locator.location}.{self.table}
            WHERE {condition}
        """

        connection = await self.connector.get(self.locator.zone)
        result: Mapping[str, int] = next(
            iter(await connection.fetch(query, *parameters)), {})

        return result.get('count', 0)

    def _order_by(self) -> str:
        return f"ORDER BY {self.jsonb_field}->>'created_at' DESC NULLS LAST"
