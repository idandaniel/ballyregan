from typing import List

import pandas as pd
from loguru import logger

from ballyregan.backends.base import BaseBackend
from ballyregan.models import Proxy, Protocols, Anonymities


class DataframeBackend(BaseBackend):
    def __init__(self):
        self.df = pd.DataFrame(columns=['Protocol', 'IP', 'Port', 'Country', 'Anonymity'])
        self.df.set_index(['IP', 'Port'], inplace=True, verify_integrity=True)

    def create_proxy(self, proxy: Proxy) -> None:
        self.df = pd.concat(
            objs=[
                pd.DataFrame.from_records([{
                    'Protocol': proxy.protocol,
                    'IP': proxy.ip,
                    'Port': proxy.port,
                    'Country': proxy.country,
                    'Anonymity': proxy.anonymity
                }]),
                self.df
            ],
            axis=0,
            ignore_index=True
        )

    def read_proxies(self, protocols: List[Protocols] = [], anonymities: List[Anonymities] = [], limit: int = 0) -> List[Proxy]:
        proxies = []
        filtered_df = self.df.copy()

        if protocols:
            filtered_df[filtered_df['Protocol'].isin(protocols)]
            
        if anonymities:
           filtered_df[filtered_df['Anonymity'].isin(anonymities)]

        if limit:
            filtered_df = filtered_df.head(limit)

        for _, row in filtered_df.iterrows():
            proxies.append(Proxy(
                protocol=Protocols(row['Protocol']),
                ip=row['IP'],
                port=row['Port'],
                country=row['Country'],
                anonymity=row['Anonymity']
            ))
        
        return proxies

    def update_proxy(self, proxy_to_update: Proxy, new_proxy: Proxy, insert_if_not_exist: bool = True) -> None:
        mask = (
            (self.df['Protocol'] == proxy_to_update.protocol.value) &
            (self.df['IP'] == proxy_to_update.ip) &
            (self.df['Port'] == proxy_to_update.port) &
            (self.df['Country'] == (proxy_to_update.country or 'UNKNOWN')) &
            (self.df['Anonymity'] == (proxy_to_update.anonymity or 'UNKNOWN'))
        )

        if mask.any():
            self.df.loc[mask, 'Protocol'] = new_proxy.protocol.value
            self.df.loc[mask, 'IP'] = new_proxy.ip
            self.df.loc[mask, 'Port'] = new_proxy.port
            self.df.loc[mask, 'Country'] = new_proxy.country or 'UNKNOWN'
            self.df.loc[mask, 'Anonymity'] = new_proxy.anonymity or 'UNKNOWN'
        else:
            if insert_if_not_exist:
                self.create_proxy(new_proxy)

    def delete_proxy(self, proxy_to_delete: Proxy) -> None:
        mask = (
            (self.df['Protocol'] == proxy_to_delete.protocol.value) &
            (self.df['IP'] == proxy_to_delete.ip) &
            (self.df['Port'] == proxy_to_delete.port) &
            (self.df['Country'] == (proxy_to_delete.country or 'UNKNOWN')) &
            (self.df['Anonymity'] == (proxy_to_delete.anonymity or 'UNKNOWN'))
        )

        if mask.any():
            self.df.drop(self.df.index[mask], inplace=True)
            self.df.reset_index(drop=True, inplace=True)

    def export_to_csv(self, file_path: str) -> None:
        self.df.to_csv(file_path, index=False)

    def import_from_csv(self, file_path: str) -> None:
        self.df = pd.read_csv(file_path)
