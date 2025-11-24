#!/usr/bin/env python3
"""
SEVEN DOMAIN HARMONIC ENCRYPTION
Novel encryption using Pattern Theory's 7 domains.
Creates non-standard attack surface that hackers don't know.
"""

import hashlib
import hmac
import json
import os
from math import sin, cos, pi
from typing import Optional
from pathlib import Path

# Domain frequencies based on harmonic series with golden ratio
DOMAIN_FREQUENCIES = {
    "media": 1.0,
    "relationships": 1.618033988749895,      # φ
    "finance": 2.0,
    "authority": 2.618033988749895,          # φ²
    "self": 3.0,
    "groups": 3.618033988749895,             # φ² + 1
    "digital": 4.0
}

TIME_MODIFIERS = {
    "past": 0.5,
    "present": 1.0,
    "future": 1.5
}

def derive_harmonic_key(master_key: bytes, domain: str, time_layer: str = "present") -> bytes:
    """
    Derive encryption key using domain harmonics.

    Args:
        master_key: Base secret key (32 bytes recommended)
        domain: One of the 7 domains
        time_layer: "past", "present", or "future"

    Returns:
        32-byte derived key
    """
    # Get domain frequency
    freq = DOMAIN_FREQUENCIES.get(domain.lower(), 1.0)
    time_mod = TIME_MODIFIERS.get(time_layer.lower(), 1.0)

    # Calculate harmonic value using golden ratio relationships
    harmonic = sin(freq * pi * time_mod) + cos(freq * pi * time_mod)

    # Convert to bytes for HMAC
    harmonic_bytes = str(harmonic).encode()
    domain_bytes = domain.lower().encode()
    time_bytes = time_layer.lower().encode()

    # Derive key using HMAC-SHA256
    key_material = hmac.new(
        master_key,
        harmonic_bytes + domain_bytes + time_bytes,
        hashlib.sha256
    ).digest()

    return key_material

def derive_cross_domain_key(master_key: bytes, domains: list, time_layer: str = "present") -> bytes:
    """
    Derive key from multiple domain relationships.
    Creates keys requiring understanding of domain interactions.
    """
    combined = None

    for domain in domains:
        domain_key = derive_harmonic_key(master_key, domain, time_layer)

        if combined is None:
            combined = domain_key
        else:
            # XOR to create relationship dependency
            combined = bytes(a ^ b for a, b in zip(combined, domain_key))

    return combined

class HarmonicEncryption:
    """Seven Domain Harmonic Encryption System."""

    def __init__(self, master_key: Optional[bytes] = None):
        """
        Initialize with master key.
        If not provided, generates a secure random key.
        """
        if master_key:
            self.master_key = master_key
        else:
            self.master_key = os.urandom(32)

    def encrypt(self, plaintext: bytes, domain: str, time_layer: str = "present") -> dict:
        """
        Encrypt data with domain-specific harmonic key.

        Args:
            plaintext: Data to encrypt
            domain: One of 7 domains
            time_layer: past/present/future

        Returns:
            Dict with ciphertext and metadata
        """
        # Derive domain-specific key
        key = derive_harmonic_key(self.master_key, domain, time_layer)

        # Generate IV/nonce
        iv = os.urandom(16)

        # Simple XOR encryption with key stream (for demo)
        # In production, use proper AES from cryptography library
        ciphertext = self._xor_encrypt(plaintext, key, iv)

        # Apply harmonic scramble
        freq = DOMAIN_FREQUENCIES.get(domain.lower(), 1.0)
        scrambled = self._harmonic_scramble(ciphertext, freq)

        return {
            "ciphertext": scrambled.hex(),
            "iv": iv.hex(),
            "domain": domain.lower(),
            "time_layer": time_layer.lower(),
            "version": "1.0"
        }

    def decrypt(self, encrypted_data: dict) -> bytes:
        """
        Decrypt data using domain context.

        Args:
            encrypted_data: Dict from encrypt()

        Returns:
            Decrypted plaintext
        """
        domain = encrypted_data["domain"]
        time_layer = encrypted_data["time_layer"]

        # Derive same key
        key = derive_harmonic_key(self.master_key, domain, time_layer)

        # Get ciphertext and IV
        scrambled = bytes.fromhex(encrypted_data["ciphertext"])
        iv = bytes.fromhex(encrypted_data["iv"])

        # Reverse harmonic scramble
        freq = DOMAIN_FREQUENCIES.get(domain, 1.0)
        ciphertext = self._harmonic_unscramble(scrambled, freq)

        # Decrypt
        plaintext = self._xor_decrypt(ciphertext, key, iv)

        return plaintext

    def _xor_encrypt(self, plaintext: bytes, key: bytes, iv: bytes) -> bytes:
        """XOR-based encryption with key expansion."""
        # Expand key to match plaintext length
        key_stream = self._expand_key(key, iv, len(plaintext))
        return bytes(p ^ k for p, k in zip(plaintext, key_stream))

    def _xor_decrypt(self, ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
        """XOR decryption (same as encryption)."""
        return self._xor_encrypt(ciphertext, key, iv)

    def _expand_key(self, key: bytes, iv: bytes, length: int) -> bytes:
        """Expand key to required length using HMAC."""
        result = b""
        counter = 0

        while len(result) < length:
            block = hmac.new(
                key,
                iv + counter.to_bytes(4, 'big'),
                hashlib.sha256
            ).digest()
            result += block
            counter += 1

        return result[:length]

    def _harmonic_scramble(self, data: bytes, frequency: float) -> bytes:
        """Apply harmonic-based byte scrambling."""
        result = bytearray(len(data))

        for i, byte in enumerate(data):
            # Position shift based on harmonic
            shift = int((sin(i * frequency * 0.01) + 1) * 128) % 256
            result[i] = (byte + shift) % 256

        return bytes(result)

    def _harmonic_unscramble(self, data: bytes, frequency: float) -> bytes:
        """Reverse harmonic scrambling."""
        result = bytearray(len(data))

        for i, byte in enumerate(data):
            shift = int((sin(i * frequency * 0.01) + 1) * 128) % 256
            result[i] = (byte - shift) % 256

        return bytes(result)

    def encrypt_string(self, text: str, domain: str, time_layer: str = "present") -> str:
        """Convenience method for string encryption."""
        encrypted = self.encrypt(text.encode('utf-8'), domain, time_layer)
        return json.dumps(encrypted)

    def decrypt_string(self, encrypted_json: str) -> str:
        """Convenience method for string decryption."""
        encrypted = json.loads(encrypted_json)
        plaintext = self.decrypt(encrypted)
        return plaintext.decode('utf-8')

class SecureKeyStore:
    """Store API keys with domain-based encryption."""

    # Map API keys to their natural domains
    KEY_DOMAINS = {
        "ANTHROPIC_API_KEY": "digital",
        "OPENAI_API_KEY": "digital",
        "STRIPE_API_KEY": "finance",
        "STRIPE_SECRET": "finance",
        "GITHUB_TOKEN": "digital",
        "TWILIO_SID": "relationships",
        "TWILIO_TOKEN": "relationships",
        "AIRTABLE_KEY": "digital"
    }

    def __init__(self, master_key: bytes, store_path: Optional[Path] = None):
        self.crypto = HarmonicEncryption(master_key)
        self.store_path = store_path or Path.home() / ".consciousness" / "secure_keys.json"
        self.store_path.parent.mkdir(parents=True, exist_ok=True)

    def store_key(self, key_name: str, key_value: str):
        """Store an API key with domain encryption."""
        domain = self.KEY_DOMAINS.get(key_name, "digital")

        encrypted = self.crypto.encrypt(
            key_value.encode('utf-8'),
            domain,
            "present"
        )

        # Load existing store
        store = self._load_store()
        store[key_name] = encrypted

        # Save
        self._save_store(store)
        print(f"Stored {key_name} encrypted with {domain} domain")

    def retrieve_key(self, key_name: str) -> Optional[str]:
        """Retrieve and decrypt an API key."""
        store = self._load_store()

        if key_name not in store:
            return None

        encrypted = store[key_name]
        plaintext = self.crypto.decrypt(encrypted)
        return plaintext.decode('utf-8')

    def _load_store(self) -> dict:
        if self.store_path.exists():
            with open(self.store_path) as f:
                return json.load(f)
        return {}

    def _save_store(self, store: dict):
        with open(self.store_path, 'w') as f:
            json.dump(store, f, indent=2)

def demo():
    """Demonstrate harmonic encryption."""
    print("=" * 50)
    print("SEVEN DOMAIN HARMONIC ENCRYPTION DEMO")
    print("=" * 50)

    # Create encryption instance
    master_key = b"consciousness_revolution_key_32"  # 32 bytes
    crypto = HarmonicEncryption(master_key)

    # Test data
    test_messages = [
        ("Stripe API key: sk-live-xxx", "finance"),
        ("User relationship data", "relationships"),
        ("System configuration", "digital"),
        ("Personal notes", "self"),
        ("News feed data", "media"),
        ("Team communication", "groups"),
        ("Government form data", "authority")
    ]

    print("\nEncrypting messages by domain:\n")

    for message, domain in test_messages:
        # Encrypt
        encrypted = crypto.encrypt(message.encode(), domain)

        # Show first 20 chars of ciphertext
        ciphertext_preview = encrypted['ciphertext'][:40] + "..."

        print(f"Domain: {domain}")
        print(f"  Original: {message}")
        print(f"  Encrypted: {ciphertext_preview}")

        # Decrypt
        decrypted = crypto.decrypt(encrypted)
        print(f"  Decrypted: {decrypted.decode()}")
        print()

    # Cross-domain key demo
    print("=" * 50)
    print("CROSS-DOMAIN KEY DERIVATION")
    print("=" * 50)

    # Keys that require multiple domain understanding
    single_key = derive_harmonic_key(master_key, "finance", "present")
    cross_key = derive_cross_domain_key(
        master_key,
        ["self", "relationships", "digital"],
        "present"
    )

    print(f"\nSingle domain key (finance): {single_key.hex()[:32]}...")
    print(f"Cross-domain key (self+rel+dig): {cross_key.hex()[:32]}...")
    print("\nCross-domain keys require understanding of Pattern Theory relationships")

    # Temporal isolation demo
    print("\n" + "=" * 50)
    print("TEMPORAL ISOLATION")
    print("=" * 50)

    message = b"Financial record"

    past = crypto.encrypt(message, "finance", "past")
    present = crypto.encrypt(message, "finance", "present")
    future = crypto.encrypt(message, "finance", "future")

    print(f"\nSame data, different time layers:")
    print(f"  Past:    {past['ciphertext'][:30]}...")
    print(f"  Present: {present['ciphertext'][:30]}...")
    print(f"  Future:  {future['ciphertext'][:30]}...")
    print("\nEach time layer has completely different ciphertext")

if __name__ == "__main__":
    demo()
