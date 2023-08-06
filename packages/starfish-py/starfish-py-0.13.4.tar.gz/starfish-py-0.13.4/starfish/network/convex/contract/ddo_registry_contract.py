"""
    starfish-ddo-registry contract

"""
import re

from starfish.network.convex.contract.contract_base import ContractBase
from starfish.network.convex.convex_account import ConvexAccount
from starfish.network.convex.convex_network import ConvexNetwork
from starfish.types import AccountAddress


class DDORegistryContract(ContractBase):

    def __init__(self, convex: ConvexNetwork):
        ContractBase.__init__(self, convex, 'starfish-ddo-registry')

    def register_did(self, did: str, ddo_text: str, account: ConvexAccount):
        encode_ddo_text = re.sub('"', '\\"', ddo_text)
        command = f'(call {self.address} (register {did} "{encode_ddo_text}"))'
        result = self._convex.send(command, account)
        if result and 'value' in result:
            return result['value']
        return result

    def resolve(self, did: str, account_address: AccountAddress):
        command = f'(call {self.address} (resolve {did}))'
        if isinstance(account_address, str):
            address = account_address
        else:
            address = account_address.address
        result = self._convex.query(command, address)
        if result and 'value' in result:
            return result['value']
        return result

    def owner(self, did: str,  account_address: AccountAddress):
        command = f'(call {self.address} (owner {did}))'
        if isinstance(account_address, str):
            address = account_address
        else:
            address = account_address.address
        result = self._convex.query(command, address)
        if result and 'value' in result:
            return result['value']
        return result
