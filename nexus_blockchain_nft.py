#!/usr/bin/env python3
"""
NEXUS Blockchain/NFT Connector
- Web3 wallet integration
- Smart contract interaction stubs
- NFT minting/transfer
"""
import hashlib
import json
import logging
import time
from pathlib import Path
from typing import Dict, Optional

log_dir = Path("nexus_logs")
log_dir.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    handlers=[logging.FileHandler(log_dir / "blockchain.log", encoding="utf-8")],
)
logger = logging.getLogger("web3")


class Web3Wallet:
    """Simplified Web3 wallet."""

    def __init__(self, private_key: Optional[str] = None):
        self.private_key = (
            private_key or hashlib.sha256(str(time.time()).encode()).hexdigest()
        )
        self.address = "0x" + hashlib.sha256(self.private_key.encode()).hexdigest()[:40]
        logger.info(f"Wallet created: {self.address}")

    def sign_transaction(self, data: Dict) -> str:
        """Sign transaction with private key."""
        msg = json.dumps(data, sort_keys=True)
        signature = hashlib.sha256((msg + self.private_key).encode()).hexdigest()
        return signature


class NFTContract:
    """NFT smart contract stub."""

    def __init__(self, contract_address: str):
        self.contract_address = contract_address
        self.nfts = {}  # {token_id: {owner, metadata}}
        self.token_counter = 0
        logger.info(f"NFT Contract deployed: {contract_address}")

    def mint(self, owner: str, metadata: Dict) -> int:
        """Mint new NFT."""
        self.token_counter += 1
        token_id = self.token_counter
        self.nfts[token_id] = {
            "owner": owner,
            "metadata": metadata,
            "minted_at": time.time(),
        }
        logger.info(f"NFT minted: #{token_id} → {owner}")
        return token_id

    def transfer(self, token_id: int, from_addr: str, to_addr: str) -> bool:
        """Transfer NFT ownership."""
        if token_id not in self.nfts:
            return False
        if self.nfts[token_id]["owner"] != from_addr:
            return False

        self.nfts[token_id]["owner"] = to_addr
        logger.info(f"NFT #{token_id} transferred: {from_addr} → {to_addr}")
        return True

    def get_nft(self, token_id: int) -> Optional[Dict]:
        """Get NFT data."""
        return self.nfts.get(token_id)


class GameItemNFT:
    """Game item as NFT."""

    def __init__(self, contract: NFTContract):
        self.contract = contract

    def mint_weapon(
        self, owner: str, weapon_type: str, rarity: str, stats: Dict
    ) -> int:
        """Mint weapon NFT."""
        metadata = {
            "type": "weapon",
            "weapon_type": weapon_type,
            "rarity": rarity,
            "stats": stats,
            "image_uri": f"ipfs://weapon-{weapon_type}-{rarity}.png",
        }
        return self.contract.mint(owner, metadata)

    def mint_character(self, owner: str, character_class: str, level: int) -> int:
        """Mint character NFT."""
        metadata = {
            "type": "character",
            "class": character_class,
            "level": level,
            "image_uri": f"ipfs://char-{character_class}.png",
        }
        return self.contract.mint(owner, metadata)


class MarketplaceContract:
    """NFT marketplace smart contract."""

    def __init__(self):
        self.listings = {}  # {listing_id: {token_id, seller, price}}
        self.listing_counter = 0
        logger.info("Marketplace contract initialized")

    def create_listing(self, token_id: int, seller: str, price: float) -> int:
        """List NFT for sale."""
        self.listing_counter += 1
        listing_id = self.listing_counter
        self.listings[listing_id] = {
            "token_id": token_id,
            "seller": seller,
            "price": price,
            "status": "active",
        }
        logger.info(
            f"Listing created: #{listing_id} (token #{token_id}, price: {price})"
        )
        return listing_id

    def buy(self, listing_id: int, buyer: str) -> bool:
        """Purchase NFT."""
        if (
            listing_id not in self.listings
            or self.listings[listing_id]["status"] != "active"
        ):
            return False

        self.listings[listing_id]["status"] = "sold"
        self.listings[listing_id]["buyer"] = buyer
        logger.info(f"NFT sold: listing #{listing_id} → {buyer}")
        return True


if __name__ == "__main__":
    # Wallet test
    wallet = Web3Wallet()
    sig = wallet.sign_transaction({"to": "0xabc", "value": 100})
    logger.info(f"Signature: {sig[:16]}...")

    # NFT test
    nft_contract = NFTContract("0x123contract")
    game_items = GameItemNFT(nft_contract)

    token_id = game_items.mint_weapon(
        wallet.address, "sword", "legendary", {"attack": 150, "speed": 80}
    )
    logger.info(f"Minted weapon NFT: #{token_id}")

    # Marketplace test
    marketplace = MarketplaceContract()
    listing_id = marketplace.create_listing(token_id, wallet.address, 500.0)
    success = marketplace.buy(listing_id, "0xbuyer")
    logger.info(f"Purchase {'successful' if success else 'failed'}")
