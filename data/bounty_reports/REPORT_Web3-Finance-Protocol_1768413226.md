# BUG BOUNTY REPORT: Web3-Finance-Protocol
## Summary
Detected **1** vulnerabilities in https://github.com/example/web3-finance.

### [WEB3_CRITICAL] Reentrancy
- **File:** contracts/Vault.sol
- **Line:** 42
- **Description:** External call before state update in withdraw() function.
- **Est. Reward:** $100000+
- **POC Script:** `c:\Users\selam\NEXUS-ONE\data\bounty_reports\poc_Web3-Finance-Protocol_reentrancy.py`

