"""
Aptos Blockchain Integration Service
Handles all interactions with Aptos smart contracts
"""

import os
from dotenv import load_dotenv
from typing import Optional, List, Dict, Any
from aptos_sdk.account import Account
from aptos_sdk.async_client import RestClient, FaucetClient
from aptos_sdk.transactions import EntryFunction, TransactionArgument, TransactionPayload
from aptos_sdk.bcs import Serializer

load_dotenv()

class AptosService:
    def __init__(self):
        # Initialize Aptos client
        self.node_url = os.getenv("APTOS_NODE_URL", "https://fullnode.testnet.aptoslabs.com/v1")
        self.faucet_url = os.getenv("APTOS_FAUCET_URL", "https://faucet.testnet.aptoslabs.com")
        self.client = RestClient(self.node_url)
        self.faucet_client = FaucetClient(self.faucet_url, self.client)
        self.contract_address = os.getenv("APTOS_CONTRACT_ADDRESS", "0x203e9bf58c965f98b788b20732faaf8dc135a827c2803935e623718226722964")
    
    def create_account(self) -> dict:
        """Create a new Aptos account"""
        account = Account.generate()
        return {
            "address": str(account.address()),
            "private_key": account.private_key.hex(),
            "public_key": str(account.public_key)
        }
    
    async def get_account_balance(self, address: str) -> int:
        """Get account balance in octas"""
        try:
            # First check if account exists
            try:
                await self.client.account(address)
            except Exception as acc_err:
                print(f"Account does not exist: {acc_err}")
                return 0
            
            # Get account resources
            resources = await self.client.account_resources(address)
            for resource in resources:
                if resource["type"] == "0x1::coin::CoinStore<0x1::aptos_coin::AptosCoin>":
                    return int(resource["data"]["coin"]["value"])
            
            # Account exists but no CoinStore means balance is 0
            # This is normal for accounts that haven't received any coins yet
            print(f"Account {address} exists but has no CoinStore registered")
            return 0
        except Exception as e:
            print(f"Error getting balance for {address}: {e}")
            return 0
    
    async def fund_account_from_faucet(self, address: str, amount: int = 100000000) -> dict:
        """Fund account from testnet faucet (100000000 = 1 APT)
        This will automatically register the CoinStore if it doesn't exist
        """
        try:
            # The faucet automatically registers the coin store when funding
            await self.faucet_client.fund_account(address, amount)
            
            # Wait a moment for the transaction to be processed
            import asyncio
            await asyncio.sleep(2)
            
            # Get the new balance
            balance = await self.get_account_balance(address)
            return {
                "success": True,
                "balance_octas": balance,
                "balance_apt": balance / 100000000,
                "message": "Account funded successfully"
            }
        except Exception as e:
            error_msg = str(e)
            print(f"Error funding account: {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "message": "Failed to fund account. Please try again."
            }
    
    async def mint_dataset_nft(
        self, 
        account: Account,
        dataset_id: int,
        hash_str: str,
        uri: str
    ) -> dict:
        """Mint a dataset NFT"""
        try:
            # Create transaction payload
            payload = EntryFunction.natural(
                f"{self.contract_address}::DatasetNFT",
                "mint_dataset",
                [],
                [
                    TransactionArgument(dataset_id, Serializer.u64),
                    TransactionArgument(hash_str, Serializer.str),
                    TransactionArgument(uri, Serializer.str),
                ]
            )
            
            # Simulate transaction (in production, submit with signature)
            import hashlib
            tx_hash = '0x' + hashlib.sha256(f"{account.address()}{dataset_id}{hash_str}".encode()).hexdigest()
            
            return {
                "success": True,
                "transaction_hash": tx_hash,
                "dataset_id": dataset_id,
                "note": "Transaction simulated - requires signature in production"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def grant_license(
        self,
        account: Account,
        dataset_id: int,
        user_address: str,
        duration_secs: int,
        license_type: str
    ) -> dict:
        """Grant a license to access a dataset"""
        try:
            # Map license type to integer
            license_type_map = {"standard": 0, "extended": 1, "enterprise": 2}
            license_int = license_type_map.get(license_type, 0)
            
            payload = EntryFunction.natural(
                f"{self.contract_address}::Licensing",
                "grant_license",
                [],
                [
                    TransactionArgument(dataset_id, Serializer.u64),
                    TransactionArgument(user_address, Serializer.address),
                    TransactionArgument(duration_secs, Serializer.u64),
                    TransactionArgument(license_int, Serializer.u64),
                ]
            )
            
            # Simulate transaction
            import hashlib
            tx_hash = '0x' + hashlib.sha256(f"{account.address()}{dataset_id}{user_address}".encode()).hexdigest()
            
            return {
                "success": True,
                "transaction_hash": tx_hash,
                "note": "Transaction simulated - requires owner signature in production"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def set_dataset_price(
        self,
        account: Account,
        dataset_id: int,
        base_price: float,
        per_query_price: float
    ) -> dict:
        """Set pricing for a dataset"""
        try:
            # Convert APT to octas (1 APT = 100000000 octas)
            base_price_octas = int(base_price * 100000000)
            per_query_price_octas = int(per_query_price * 100000000)
            
            payload = EntryFunction.natural(
                f"{self.contract_address}::PaymentRouter",
                "set_price",
                [],
                [
                    TransactionArgument(dataset_id, Serializer.u64),
                    TransactionArgument(base_price_octas, Serializer.u64),
                    TransactionArgument(per_query_price_octas, Serializer.u64),
                ]
            )
            
            # Simulate transaction
            import hashlib
            tx_hash = '0x' + hashlib.sha256(f"{account.address()}{dataset_id}{base_price}".encode()).hexdigest()
            
            return {
                "success": True,
                "transaction_hash": tx_hash,
                "note": "Transaction simulated - requires owner signature in production"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def pay_for_license(
        self,
        buyer_account: Account,
        seller_address: str,
        dataset_id: int
    ) -> dict:
        """Pay for a dataset license"""
        try:
            payload = EntryFunction.natural(
                f"{self.contract_address}::PaymentRouter",
                "pay_for_license",
                [],
                [
                    TransactionArgument(seller_address, Serializer.address),
                    TransactionArgument(dataset_id, Serializer.u64),
                ]
            )
            
            # Simulate transaction
            import hashlib
            tx_hash = '0x' + hashlib.sha256(f"{buyer_account.address()}{seller_address}{dataset_id}".encode()).hexdigest()
            
            return {
                "success": True,
                "transaction_hash": tx_hash,
                "note": "Transaction simulated - requires buyer signature in production"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def set_royalty_config(
        self,
        account: Account,
        dataset_id: int,
        contributors: List[str],
        share_percentage: int
    ) -> dict:
        """Set royalty configuration for a dataset"""
        try:
            payload = EntryFunction.natural(
                f"{self.contract_address}::Royalties",
                "set_royalty",
                [],
                [
                    TransactionArgument(dataset_id, Serializer.u64),
                    TransactionArgument(contributors, Serializer.sequence_serializer(Serializer.address)),
                    TransactionArgument(share_percentage, Serializer.u64),
                ]
            )
            
            # Simulate transaction
            import hashlib
            tx_hash = '0x' + hashlib.sha256(f"{account.address()}{dataset_id}".encode()).hexdigest()
            
            return {
                "success": True,
                "transaction_hash": tx_hash,
                "note": "Transaction simulated - requires owner signature in production"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_transaction_status(self, tx_hash: str) -> dict:
        """Get transaction status"""
        try:
            tx = await self.client.transaction_by_hash(tx_hash)
            return {
                "success": tx.get("success", False),
                "vm_status": tx.get("vm_status"),
                "hash": tx_hash,
                "version": tx.get("version"),
                "gas_used": tx.get("gas_used")
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "hash": tx_hash
            }
    
    async def get_account_info(self, address: str) -> dict:
        """Get account information"""
        try:
            account = await self.client.account(address)
            balance = await self.get_account_balance(address)
            return {
                "address": address,
                "sequence_number": account.get("sequence_number"),
                "authentication_key": account.get("authentication_key"),
                "balance_octas": balance,
                "balance_apt": balance / 100000000
            }
        except Exception as e:
            return {
                "error": str(e),
                "address": address
            }

# Singleton instance
aptos_service = AptosService()
